from flask import Flask, render_template, request, jsonify, Response, abort, redirect, url_for
from flask_cors import CORS

import uuid
import json
from dotenv import load_dotenv
import os
import sys
from pathlib import Path
import time
import threading

# Add user folder to Python path for imports
_app_root = Path(__file__).parent
_user_path = _app_root / "user"
if _user_path.exists() and str(_user_path) not in sys.path:
    sys.path.insert(0, str(_user_path))

# Import workflows registry from the centralized location
from app.utils.registries import WORKFLOWS_REGISTRY
from app.utils.response_types import response_output_error, ResponseKey, ResponseStatus
from app.storage.manager import FileStorageManager
from app.configs.app_config import APP_SETTINGS
from app.configs.llm_config import llm_models


# ----------------------
# Flask app setup

app = Flask(__name__, static_folder='app/ui/static', template_folder='app/ui/templates')

# Enable CORS for API routes only
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Setup Secret Keys
dotenv_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# In‐memory stores for this example
generators: dict[str, any] = {}

# File storage manager
FILES_FOLDER = APP_SETTINGS.USER_DATA_PATH
# File storage manager setup
file_manager = FileStorageManager(base_path=FILES_FOLDER, skip_folders=["__pycache__"])

# Note: Removed threading lock for PythonAnywhere compatibility
# If concurrent access becomes an issue, consider using file-based locking instead


@app.template_filter('active_page')
def active_page(current_page, page_name):
    return 'active' if current_page == page_name else ''

# Helper function to serialize workflows for templates (removes function objects)
def get_workflows_catalog():
    """Return workflows registry without function objects for template rendering."""
    return {
        workflow_id: {key: value for key, value in workflow_data.items() if key != "function"}
        for workflow_id, workflow_data in WORKFLOWS_REGISTRY.items()
    }


# Routes
@app.route('/')
def page_index():
    return render_template('index.html', workflows=get_workflows_catalog())

@app.route('/workflows')
def page_workflows():
    return render_template('workflows.html', workflows=get_workflows_catalog(), llm_models=llm_models)

@app.route('/test')
def page_test():
    return render_template('test.html')

# redirect to handle the trailing slash issue
@app.route('/files/')
def files_with_slash():
    return redirect(url_for('files'))

@app.route('/files')
@app.route('/files/folder/<item_id>')
def files(item_id=None):
    structure = file_manager.get_structure()
    items_list = structure['items']
    
    # Get current folder and build breadcrumb path
    current_folder = None
    breadcrumbs = []
    
    if item_id:
        current_folder = next((item for item in items_list if item.id == item_id), None)
        if not current_folder or current_folder.type != 'folder':
            abort(404)
            
        # Build breadcrumbs
        temp_folder = current_folder
        while hasattr(temp_folder, 'parent'):
            parent = next((item for item in items_list if item.id == temp_folder.parent), None)
            if parent:
                breadcrumbs.insert(0, parent)
                temp_folder = parent
            else:
                break
        breadcrumbs.append(current_folder)
    
    # Filter items for current folder
    filtered_items = [
        item for item in items_list 
        if (not item_id and not hasattr(item, 'parent')) or
           (hasattr(item, 'parent') and item.parent == item_id)
    ]
    
    return render_template('files.html', 
                         items=filtered_items, 
                         current_folder=current_folder,
                         breadcrumbs=breadcrumbs)


@app.route('/files/file/<item_id>')
def files_file_detail(item_id):
    structure = file_manager.get_structure()
    item = next((item for item in structure['items'] if item.id == item_id), None)
    
    if not item or item.type != 'file':
        abort(404)
    
    # Generate breadcrumbs by traversing up through parent folders
    breadcrumbs = []
    if not hasattr(item, 'parent'):
        # If item has no parent, it's in the root folder
        breadcrumbs = [{'id': None, 'name': 'root', 'type': 'folder'}]
    else:
        current = next((i for i in structure['items'] if i.id == item.parent), None)
        while current:
            breadcrumbs.insert(0, current)
            current = next((i for i in structure['items'] if i.id == current.parent), None) if hasattr(current, 'parent') else None

    try:
        full_path = Path(FILES_FOLDER) / item.file_path
        with full_path.open('r', encoding='utf-8') as f:
            content = f.read()
        return render_template('files_file_detail.html', item=item, content=content, breadcrumbs=breadcrumbs)
    except Exception as e:
        abort(500)


# -------------------------------
# --- API routes ---
# -------------------------------

@app.route("/api/start_task", methods=["POST"])
def start_task():
    try:
        import inspect
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
        
        #response_from_generator = next(generator_func)

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


@app.route("/api/continue_task", methods=["POST"])
def continue_task():
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


@app.route('/api/tools/test', methods=['POST'])
def test():
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

# RENAME TO get_workflows_registry
@app.get("/api/get_workflows_registry")
def api_get_workflows_registry():
    """Return current workflow registry without function objects."""    
    try:
        workflows = get_workflows_catalog()
        return jsonify({
            ResponseKey.STATUS.value: ResponseStatus.SUCCESS.value,
            ResponseKey.DATA.value: workflows,
            ResponseKey.MESSAGE.value: "Workflows registry retrieved successfully.",
        })
    except Exception as e:
        return {
            ResponseKey.STATUS.value: ResponseStatus.ERROR.value,
            ResponseKey.ERROR.value: f"[{__name__}]: {str(e)}.",
            ResponseKey.MESSAGE.value: f"[{__name__}]: {str(e)}.",
        }

    
@app.route('/api/reload_modules', methods=['POST'])
def reload_modules():
    """Hot-reload all modules using the simple method that works on PythonAnywhere."""
    try:
        # Use the simple loading method instead of module manager
        load_user_workflows_simple()
        
        return {
            ResponseKey.STATUS.value: ResponseStatus.SUCCESS.value,
            ResponseKey.MESSAGE.value: f"Modules reloaded successfully. Loaded {len(WORKFLOWS_REGISTRY)} workflows.",
        }
    except Exception as e:
        return {
            ResponseKey.STATUS.value: ResponseStatus.ERROR.value,
            ResponseKey.ERROR.value: f"Error: {str(e)}",
            ResponseKey.MESSAGE.value: f"Error: {str(e)}",
        }

@app.route('/debug/workflows')
def debug_workflows():
    """Debug route to check workflows registry state."""
    import sys
    debug_info = {
        "workflows_registry_count": len(WORKFLOWS_REGISTRY),
        "workflows_registry_keys": list(WORKFLOWS_REGISTRY.keys()),
        "user_data_path": str(APP_SETTINGS.USER_DATA_PATH),
        "user_data_path_exists": APP_SETTINGS.USER_DATA_PATH.exists(),
        "python_path_has_user": str(APP_SETTINGS.USER_DATA_PATH) in sys.path,
    }
    
    # Try to check user workflows folder
    try:
        user_workflows_path = APP_SETTINGS.USER_DATA_PATH / "workflows"
        debug_info["user_workflows_path"] = str(user_workflows_path)
        debug_info["user_workflows_exists"] = user_workflows_path.exists()
        if user_workflows_path.exists():
            debug_info["user_workflows_files"] = [f.name for f in user_workflows_path.iterdir() if f.suffix == '.py']
    except Exception as e:
        debug_info["user_workflows_error"] = str(e)
    
    return jsonify(debug_info)

@app.route('/debug/simple_test')
def debug_simple_test():
    """Test the most basic workflow import without module manager."""
    import sys
    import traceback
    
    try:
        # Ensure paths are set up
        app_root = Path(__file__).parent
        user_path = app_root / "user"
        
        if str(app_root) not in sys.path:
            sys.path.insert(0, str(app_root))
        if str(user_path) not in sys.path:
            sys.path.insert(0, str(user_path))
        
        # Clear any existing registry entries
        WORKFLOWS_REGISTRY.clear()
        
        # Try to import workflow dependencies
        from app.workflows import workflow, Workflow
        
        # Import ALL workflow modules directly (this bypasses the module manager)
        workflows_path = user_path / "workflows"
        if workflows_path.exists():
            for py_file in workflows_path.glob("*.py"):
                if py_file.name not in {"__init__.py", "_core.py", "core.py"}:
                    try:
                        module_name = f"user.workflows.{py_file.stem}"
                        # Remove from sys.modules if already imported
                        if module_name in sys.modules:
                            del sys.modules[module_name]
                        # Import the module directly
                        exec(f"from user.workflows import {py_file.stem}")
                    except Exception as e:
                        print(f"Failed to import {py_file.name}: {e}")
        
        return jsonify({
            "status": "success",
            "message": "Simple import test successful",
            "workflows_count": len(WORKFLOWS_REGISTRY),
            "workflows": list(WORKFLOWS_REGISTRY.keys()),
            "sys_path_first_3": sys.path[:3]
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc(),
            "workflows_count": len(WORKFLOWS_REGISTRY),
            "sys_path_first_3": sys.path[:3] if 'sys' in locals() else []
        })

@app.route('/debug/reload_simple')
def debug_reload_simple():
    """Trigger the simple loading mechanism for all workflows."""
    try:
        # Use the same mechanism as simple_test but without clearing registry first
        app_root = Path(__file__).parent
        user_path = app_root / "user"
        
        if str(app_root) not in sys.path:
            sys.path.insert(0, str(app_root))
        if str(user_path) not in sys.path:
            sys.path.insert(0, str(user_path))
        
        # Import workflow dependencies
        from app.workflows import workflow, Workflow
        
        # Import ALL workflow modules directly
        workflows_path = user_path / "workflows"
        imported_count = 0
        errors = []
        
        if workflows_path.exists():
            for py_file in workflows_path.glob("*.py"):
                if py_file.name not in {"__init__.py", "_core.py", "core.py"}:
                    try:
                        module_name = f"user.workflows.{py_file.stem}"
                        # Remove from sys.modules if already imported
                        if module_name in sys.modules:
                            del sys.modules[module_name]
                        # Import the module directly
                        exec(f"from user.workflows import {py_file.stem}")
                        imported_count += 1
                    except Exception as e:
                        errors.append(f"{py_file.name}: {str(e)}")
        
        return jsonify({
            "status": "success",
            "message": "Simple reload completed",
            "workflows_count": len(WORKFLOWS_REGISTRY),
            "workflows": list(WORKFLOWS_REGISTRY.keys()),
            "imported_files": imported_count,
            "errors": errors
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e),
            "workflows_count": len(WORKFLOWS_REGISTRY)
        })

# --- Main entry point ---

# Initialize module loading at startup
def load_user_workflows_simple():
    """Simple workflow loading that works reliably on all platforms."""
    try:
        import sys
        # Ensure paths are set up
        app_root = Path(__file__).parent
        user_path = app_root / "user"
        
        if str(app_root) not in sys.path:
            sys.path.insert(0, str(app_root))
        if str(user_path) not in sys.path:
            sys.path.insert(0, str(user_path))
        
        # Import workflow dependencies first
        from app.workflows import workflow, Workflow
        
        # Import ALL workflow modules directly
        workflows_path = user_path / "workflows"
        if workflows_path.exists():
            for py_file in workflows_path.glob("*.py"):
                if py_file.name not in {"__init__.py", "_core.py", "core.py"}:
                    try:
                        module_name = f"user.workflows.{py_file.stem}"
                        # Remove from sys.modules if already imported
                        if module_name in sys.modules:
                            del sys.modules[module_name]
                        # Import the module directly
                        exec(f"from user.workflows import {py_file.stem}")
                    except Exception:
                        # Continue with other modules if one fails
                        pass
                        
    except Exception as e:
        print(f"Error loading workflows at startup: {e}")

# Load workflows at startup using the simple method
load_user_workflows_simple()

if __name__ == '__main__':
    os.makedirs(str(APP_SETTINGS.USER_DATA_PATH), exist_ok=True)
    app.run(port=5005, debug=True)
