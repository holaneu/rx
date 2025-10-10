"""
API Blueprints - Backend API route handlers

This package contains all Flask blueprints for API endpoints:
- workflows: Workflow management API (/api/workflows/*)
- tools: Tools testing API (/api/tools/*)
- plugins: Plugin management API (/api/reload_plugins)
- system: System diagnostics API (/api/diagnostic)
- files: Files CRUD API (/api/files/*) - for future implementation

Each blueprint handles specific API functionality with consistent
JSON responses and error handling.
"""

from .workflows import workflows_api_blueprint
from .tools import tools_api_blueprint
from .plugins import plugins_api_blueprint
from .system import system_api_blueprint
from .files import files_api_blueprint

# Export all API blueprints
__all__ = [
    'workflows_api_blueprint',
    'tools_api_blueprint',
    'plugins_api_blueprint', 
    'system_api_blueprint',
    'files_api_blueprint'
]