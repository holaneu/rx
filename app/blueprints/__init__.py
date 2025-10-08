"""
Blueprints package - Flask application modularization

This package contains all Flask blueprints for the application:
- api: All REST API endpoints (/api/*)
- ui: Main user-facing pages (/, /workflows)  
- files: File system management (/files/*)

Blueprints provide clean separation of concerns and make the application
more maintainable and scalable.

Usage:
    from app.blueprints import register_blueprints
    register_blueprints(app)
"""

from flask import Flask
from .api import api_blueprint
from .ui import ui_blueprint  
from .files import files_blueprint


def register_blueprints(app: Flask) -> None:
    """
    Register all application blueprints with the Flask app.
    
    Args:
        app (Flask): Flask application instance
    """
    # Register API blueprint with /api prefix
    app.register_blueprint(api_blueprint)
    
    # Register UI blueprint (no prefix - main pages)
    app.register_blueprint(ui_blueprint)
    
    # Register files blueprint with /files prefix  
    app.register_blueprint(files_blueprint)
    
    print("Blueprints registered successfully:")
    print(f"  - API routes: /api/*")
    print(f"  - UI routes: /, /workflows")
    print(f"  - Files routes: /files/*")


# Export registration function and blueprints
__all__ = [
    'register_blueprints',
    'api_blueprint', 
    'ui_blueprint',
    'files_blueprint'
]