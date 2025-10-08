"""
API Blueprint - All REST API endpoints

This blueprint handles all API routes with /api prefix:
- Task management (/api/start_task, /api/continue_task)
- Tools testing (/api/tools/test)
- System diagnostics (/api/diagnostic)
- Plugin management (/api/reload_plugins)
- Workflow registry access (/api/get_workflows_registry)

Separated from UI routes to provide:
- Clean API organization
- Consistent JSON responses
- Dedicated error handling for API endpoints
- CORS configuration isolated to API routes
"""

import uuid
import time
import inspect
from flask import Blueprint, request, jsonify
from app.core import WORKFLOWS_REGISTRY, PROMPTS_REGISTRY, TOOLS_REGISTRY
from app.utils.response_types import response_output_error, ResponseKey, ResponseStatus


# Create API blueprint with '/api' prefix
api_blueprint = Blueprint('api', __name__, url_prefix='/api')

# In‐memory store for generator functions (shared with main app)
generators: dict[str, any] = {}


def get_workflows_catalog():
    """Return workflows registry without function objects for API responses."""
    try:
        if not WORKFLOWS_REGISTRY:
            print("Warning: WORKFLOWS_REGISTRY is empty, attempting to reload plugins...")
            # Try to reload plugins if registry is empty
            from app.core import PluginsManager
            manager = PluginsManager()
            manager.load_all_plugins()
            
        # Sort workflows alphabetically by title
        sorted_workflows = sorted(
            WORKFLOWS_REGISTRY.items(),
            key=lambda item: item[1].get('title', item[0])  # Sort by title, fallback to workflow_id
        )
        
        return {
            workflow_id: {key: value for key, value in workflow_data.items() if key != "function"}
            for workflow_id, workflow_data in sorted_workflows
        }
    except Exception as e:
        print(f"Error in get_workflows_catalog: {e}")
        # Return empty dict to prevent 500 error
        return {}


@api_blueprint.route("/start_task", methods=["POST"])
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


@api_blueprint.route("/continue_task", methods=["POST"])
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


@api_blueprint.route('/tools/test', methods=['POST'])
def test_tools():
    """Test endpoint for tool functionality."""
    try:
        data = request.json
        input_message = data.get("message", "")
        if not input_message:
            return jsonify({
                ResponseKey.STATUS.value: ResponseStatus.ERROR.value, 
                ResponseKey.ERROR.value: "No input",
                ResponseKey.DATA.value: "No input",
                ResponseKey.MESSAGE.value: {
                    ResponseKey.TITLE.value: ResponseStatus.ERROR.value,
                    ResponseKey.BODY.value: f"No input"
                } 
            }), 400
        return jsonify({
            ResponseKey.STATUS.value: ResponseStatus.SUCCESS.value, 
            ResponseKey.DATA.value: input_message + " - from test endpoint",
            ResponseKey.MESSAGE.value: {
                ResponseKey.TITLE.value: ResponseStatus.SUCCESS.value,
                ResponseKey.BODY.value: f"Message processed"
            } 
        }), 200
    except Exception as e:
        return jsonify({
            ResponseKey.STATUS.value: ResponseStatus.ERROR.value, 
            ResponseKey.ERROR.value: str(e),
            ResponseKey.MESSAGE.value: {
                ResponseKey.TITLE.value: ResponseStatus.ERROR.value,
                ResponseKey.BODY.value: f"Error: {str(e)}"
            } 
        }), 500


@api_blueprint.get("/get_workflows_registry")
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


@api_blueprint.route('/diagnostic', methods=['GET'])
def diagnostic():
    """Comprehensive diagnostic endpoint to debug plugin loading issues."""
    import os
    import sys
    from pathlib import Path
    
    try:
        # Basic environment info
        cwd = os.getcwd()
        python_path = sys.path[:5]  # First 5 entries
        
        # Check plugins directory using actual PluginsConfig
        from app.core import PluginsConfig
        config = PluginsConfig()
        plugins_dir_abs = config.PLUGINS_ROOT
        plugins_dir = plugins_dir_abs.name  # Just the directory name for display
        
        # Check individual plugin type directories
        workflows_dir = config.get_plugin_directory("workflows")
        prompts_dir = config.get_plugin_directory("prompts")  
        tools_dir = config.get_plugin_directory("tools")
        
        # Count plugin files
        workflow_files = []
        if workflows_dir.exists():
            workflow_files = [f.name for f in workflows_dir.glob("*.py") 
                            if f.name not in {"__init__.py", "_core.py", "core.py"}]
        
        # Check registries - already imported at top level
        
        # Test plugin manager
        plugin_manager_error = None
        try:
            from app.core import PluginsManager
            manager = PluginsManager()
            manager.load_plugins_for_type("workflows")
        except Exception as e:
            plugin_manager_error = str(e)
        
        return jsonify({
            "status": "success",
            "environment": {
                "cwd": cwd,
                "python_path": python_path,
                "plugins_dir": str(plugins_dir),
                "plugins_dir_abs": str(plugins_dir_abs),
                "plugins_dir_exists": plugins_dir_abs.exists()
            },
            "plugin_directories": {
                "workflows_dir_exists": workflows_dir.exists(),
                "prompts_dir_exists": prompts_dir.exists(), 
                "tools_dir_exists": tools_dir.exists(),
                "workflow_files_found": len(workflow_files),
                "workflow_files": workflow_files[:10]  # Show first 10
            },
            "registries": {
                "workflows_loaded": len(WORKFLOWS_REGISTRY),
                "prompts_loaded": len(PROMPTS_REGISTRY),
                "tools_loaded": len(TOOLS_REGISTRY),
                "workflow_keys": list(WORKFLOWS_REGISTRY.keys())[:5]  # First 5
            },
            "plugin_manager": {
                "error": plugin_manager_error,
                "can_import": plugin_manager_error is None
            }
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e),
            "message": f"Diagnostic failed: {str(e)}"
        })


@api_blueprint.route('/reload_plugins', methods=['GET', 'POST'])
def reload_plugins():
    """Reload plugins using the new simplified plugins system."""
    try:
        from app.core import PluginsManager
        
        # Clear existing registries
        WORKFLOWS_REGISTRY.clear()
        PROMPTS_REGISTRY.clear() 
        TOOLS_REGISTRY.clear()
        
        # Reload all plugins
        manager = PluginsManager()
        manager.load_all_plugins()
        
        return jsonify({
            "status": "success",
            "message": "Plugins reloaded successfully",
            "counts": {
                "workflows": len(WORKFLOWS_REGISTRY),
                "prompts": len(PROMPTS_REGISTRY),
                "tools": len(TOOLS_REGISTRY)
            },
            "workflows": list(WORKFLOWS_REGISTRY.keys())[:10]  # Show first 10
        })
        
    except Exception as e:
        return jsonify({
            "status": "error", 
            "error": str(e),
            "message": f"Plugin reload failed: {str(e)}"
        })


# Export blueprint for registration
__all__ = ['api_blueprint', 'generators']