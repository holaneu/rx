"""
Workflows API Blueprint - Workflow management endpoints

This blueprint handles workflow-related API routes:
- Start task (/api/start_task)
- Continue task (/api/continue_task) 
- Get workflows registry (/api/get_workflows_registry)

Separated for focused workflow API functionality.
"""

import uuid
import time
import inspect
from flask import Blueprint, request, jsonify
from app.core import WORKFLOWS_REGISTRY
from app.utils.response_types import response_output_error, ResponseKey, ResponseStatus
from app.blueprints.shared.helpers import get_workflows_catalog, generators

# Create workflows API blueprint
workflows_api_blueprint = Blueprint('workflows_api', __name__, url_prefix='/api')


@workflows_api_blueprint.route("/start_task", methods=["POST"])
def start_task():
    """Start a new workflow task."""
    try:
        task_id = str(uuid.uuid4())
        data = request.json
        if not data or 'workflow_id' not in data:
            return jsonify(response_output_error({
                ResponseKey.ERROR.value: "[start_task()]: workflow_id is required. Probably you forgot to select workflow.",
                ResponseKey.TASK_ID.value: task_id
                })), 400
        workflow_id = data.get('workflow_id')
        workflow = WORKFLOWS_REGISTRY.get(workflow_id)
        if not workflow:
            return jsonify(response_output_error({
                ResponseKey.ERROR.value: "[start_task()]: Invalid workflow. Workflow not found in workflows registry.",
                ResponseKey.TASK_ID.value: task_id
                })), 400
        workflow_func_params = inspect.signature(workflow['function']).parameters
        # Build kwargs based on required parameters
        kwargs = {}
        if 'input' in workflow_func_params:
            user_input = data.get('user_input')
            if user_input is None or user_input.strip() == "":
                return jsonify(response_output_error({
                    ResponseKey.ERROR.value: "[start_task()]: Missing required input. Selected workflow requires 'input' to be provided.",
                    ResponseKey.TASK_ID.value: task_id
                    })), 400
            kwargs['input'] = user_input
        
        if 'model' in data and 'model' in workflow_func_params:
            kwargs['model'] = data.get('model')
        # Always include task_id
        kwargs['task_id'] = task_id
                
        generator_func = workflow['function'](**kwargs)
        generators[task_id] = generator_func
        
        # Check if the result is a generator
        if hasattr(generator_func, '__iter__') and hasattr(generator_func, '__next__'):
            # Kick off the generator until first yield
            response_from_generator = next(generator_func)
        else:
            # If it's not a generator, use the return value directly
            response_from_generator = generator_func
        return jsonify({"task_id": task_id, "timestamp": time.time(), **response_from_generator})        
    except Exception as e:
        return jsonify(response_output_error({ResponseKey.ERROR.value: str(e)})), 500


@workflows_api_blueprint.route("/continue_task", methods=["POST"])
def continue_task():
    """Continue an existing workflow task."""
    data = request.json
    task_id = data.get("task_id")
    generator_func = generators.get(task_id)
    if not generator_func:
        return jsonify(response_output_error({ResponseKey.ERROR.value: "[continue_task()]: unknown task_id. Probably the workflow func incorrectly works with task_id"})), 400
    try:
        continue_generator = generator_func.send(data.get("user_input")) # .send() will resume the generator
        return jsonify(continue_generator)
    except StopIteration as e:
        # Signal SSE stream to close
        generators.pop(task_id, None)        
        return jsonify(getattr(e, "value", None) or {})


@workflows_api_blueprint.get("/get_workflows_registry")
def get_workflows_registry():
    """Return current workflow registry without function objects."""    
    try:
        workflows = get_workflows_catalog()
        return jsonify({
            ResponseKey.STATUS.value: ResponseStatus.SUCCESS.value,
            ResponseKey.DATA.value: workflows,
            ResponseKey.MESSAGE.value: "Workflows registry retrieved successfully.",
        })
    except Exception as e:
        return jsonify({
            ResponseKey.STATUS.value: ResponseStatus.ERROR.value,
            ResponseKey.ERROR.value: f"[get_workflows_registry]: {str(e)}.",
            ResponseKey.MESSAGE.value: f"[get_workflows_registry]: {str(e)}.",
        }), 500


# Export blueprint
__all__ = ['workflows_api_blueprint']