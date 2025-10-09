"""
UI Blueprints - Frontend/UI route handlers

This package contains all Flask blueprints for user-facing pages:
- base: Homepage and basic pages (/)
- workflows: Workflow management (/workflows)
- files: File browser (/files/*)

Each blueprint handles specific UI functionality for better organization
and maintainability.
"""

from .base import base_blueprint
from .workflows import workflows_blueprint  
from .files import files_blueprint

# Export all UI blueprints
__all__ = [
    'base_blueprint',
    'workflows_blueprint', 
    'files_blueprint'
]