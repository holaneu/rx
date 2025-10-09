"""
Workflows UI Blueprint - Workflow management pages

This blueprint handles workflow-related UI routes:
- Workflows management page (/workflows)

Separated for focused workflow UI functionality.
"""

from flask import Blueprint, render_template
from app.blueprints.shared.helpers import get_workflows_catalog
from app.configs.llm_config import llm_models

# Create workflows UI blueprint
workflows_blueprint = Blueprint('workflows', __name__)


@workflows_blueprint.route('/workflows')
def page_workflows():
    """Workflows management page."""
    try:
        return render_template('workflows.html', workflows=get_workflows_catalog(), llm_models=llm_models)
    except Exception as e:
        print(f"Error in page_workflows: {e}")
        return f"Application starting up, please refresh in a moment. Error: {e}", 503


# Export blueprint
__all__ = ['workflows_blueprint']