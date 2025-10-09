"""
UI Blueprint - Main application pages (non-API routes)

This blueprint handles the main user-facing pages of the application:
- Homepage (/)
- Workflows page (/workflows)  
- Other UI-related routes

Separated from API routes to provide clean organization and 
potential for different error handling strategies.
"""

from flask import Blueprint, render_template
from app.core import WORKFLOWS_REGISTRY
from app.configs.llm_config import llm_models


# Create UI blueprint
ui_blueprint = Blueprint('ui', __name__)


def get_workflows_catalog():
    """Return workflows registry without function objects for template rendering."""
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


@ui_blueprint.route('/')
def page_index():
    """Homepage with workflows catalog."""
    try:
        return render_template('index.html', workflows=get_workflows_catalog())
    except Exception as e:
        print(f"Error in page_index: {e}")
        return f"Application starting up, please refresh in a moment. Error: {e}", 503


@ui_blueprint.route('/workflows')
def page_workflows():
    """Workflows management page."""
    try:
        return render_template('workflows.html', workflows=get_workflows_catalog(), llm_models=llm_models)
    except Exception as e:
        print(f"Error in page_workflows: {e}")
        return f"Application starting up, please refresh in a moment. Error: {e}", 503


# Export blueprint for registration
__all__ = ['ui_blueprint']