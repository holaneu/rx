"""
Base UI Blueprint - Homepage and basic pages

This blueprint handles the homepage and other basic UI routes:
- Homepage (/)

Separated from other UI routes for clear organization.
"""

from flask import Blueprint, render_template
from app.blueprints.shared.helpers import get_workflows_catalog

# Create base UI blueprint
base_blueprint = Blueprint('base', __name__)


@base_blueprint.route('/')
def page_index():
    """Homepage with workflows catalog."""
    try:
        return render_template('index.html', workflows=get_workflows_catalog())
    except Exception as e:
        print(f"Error in page_index: {e}")
        return f"Application starting up, please refresh in a moment. Error: {e}", 503


# Export blueprint
__all__ = ['base_blueprint']