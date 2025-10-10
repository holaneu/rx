"""
Blueprints package - Flask application modularization

This package contains all Flask blueprints for the application organized
in a structured hierarchy:
- ui/: Frontend/UI blueprints (base, workflows, files)
- api/: Backend API blueprints (workflows, tools, plugins, system, files)
- shared/: Common utilities and helpers

New structure provides:
- Better organization by functional area
- Separation of UI vs API concerns
- Shared code reuse through helpers
- Cleaner maintainability and scalability

Usage:
    from app.blueprints import register_blueprints
    register_blueprints(app)
"""

from flask import Flask

# Import UI blueprints
from .ui import base_blueprint, workflows_blueprint, files_blueprint

# Import API blueprints  
from .api import (
    workflows_api_blueprint, 
    tools_api_blueprint,
    plugins_api_blueprint,
    system_api_blueprint,
    files_api_blueprint
)

# Import shared utilities for backward compatibility
from .shared import generators


def register_blueprints(app: Flask) -> None:
    """
    Register all application blueprints with the Flask app.
    
    Args:
        app (Flask): Flask application instance
    """
    # Register UI blueprints (no prefix - main pages)
    app.register_blueprint(base_blueprint)
    app.register_blueprint(workflows_blueprint)
    app.register_blueprint(files_blueprint)
    
    # Register API blueprints (all have /api prefix)
    app.register_blueprint(workflows_api_blueprint)
    app.register_blueprint(tools_api_blueprint)
    app.register_blueprint(plugins_api_blueprint)
    app.register_blueprint(system_api_blueprint)
    app.register_blueprint(files_api_blueprint)
    
    print("Blueprints registered successfully:")
    print(f"  - UI routes: /, /workflows, /files/*")
    print(f"  - API routes: /api/* (workflows, tools, plugins, system, files)")


# Export registration function and shared utilities for backward compatibility
__all__ = [
    'register_blueprints',
    'generators'  # Export for main.py compatibility
]