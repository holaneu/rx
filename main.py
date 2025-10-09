"""
Main Flask Application Entry Point

This is the refactored main application file that uses the new blueprint-based
architecture. All routes have been moved to appropriate blueprints for better
organization and maintainability.

Structure:
- Flask app configuration and setup
- Blueprint registration  
- Plugin initialization
- Application entry point

All routes are now handled by blueprints:
- UI routes: app/blueprints/ui.py
- API routes: app/blueprints/api.py  
- Files routes: app/blueprints/files.py
"""

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
from pathlib import Path

# Import configuration
from app.configs.app_config import APP_SETTINGS

# Import blueprint registration system
from app.blueprints import register_blueprints

# Import generators from blueprints to maintain shared state
from app.blueprints import generators


# ----------------------
# Flask App Configuration
# ----------------------

def create_app():
    """
    Application factory pattern for creating Flask app with proper configuration.
    
    Returns:
        Flask: Configured Flask application instance
    """
    # Create Flask app with proper static and template folders
    app = Flask(
        __name__, 
        static_folder='app/ui/static', 
        template_folder='app/ui/templates'
    )

    # Enable CORS for API routes only (maintains existing security model)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Load environment variables and setup secret key
    dotenv_path = Path(__file__).parent / '.env'
    load_dotenv(dotenv_path)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    
    # Register template filters
    @app.template_filter('active_page')
    def active_page(current_page, page_name):
        """Template filter for highlighting active navigation items."""
        return 'active' if current_page == page_name else ''
    
    # Register template context processor for backward-compatible URL generation
    @app.context_processor
    def inject_url_helpers():
        """Inject URL helper functions for backward compatibility with templates."""
        from flask import url_for
        return {
            # Map old endpoint names to new blueprint endpoints
            'page_index': lambda: url_for('base.page_index'),
            'page_workflows': lambda: url_for('workflows.page_workflows'),
            'files': lambda item_id=None: url_for('files.files', item_id=item_id) if item_id else url_for('files.files'),
            'files_file_detail': lambda item_id: url_for('files.file_detail', item_id=item_id)
        }

    # Register all application blueprints
    register_blueprints(app)
    
    return app


# ----------------------
# Plugin Initialization
# ----------------------

def load_plugins_at_startup():
    """Load all plugins using the new core system at application startup."""
    try:
        from app.core import PluginsManager
        
        manager = PluginsManager()
        manager.load_all_plugins()
        
        print(f"✅ Loaded plugins at startup: {manager.get_loaded_plugins_count()} total")
        
        # Display plugin counts for verification
        from app.core import WORKFLOWS_REGISTRY, PROMPTS_REGISTRY, TOOLS_REGISTRY
        print(f"   - Workflows: {len(WORKFLOWS_REGISTRY)}")
        print(f"   - Prompts: {len(PROMPTS_REGISTRY)}")  
        print(f"   - Tools: {len(TOOLS_REGISTRY)}")
        
    except Exception as e:
        print(f"❌ Error loading plugins at startup: {e}")


# ----------------------
# Application Instance
# ----------------------

# Create the Flask application
app = create_app()

# Load plugins at module level (executed when main.py is imported)
load_plugins_at_startup()


# ----------------------
# Development Server Entry Point
# ----------------------

if __name__ == '__main__':
    """
    Development server entry point.
    
    For production, use a proper WSGI server like Gunicorn:
    gunicorn -w 4 -b 0.0.0.0:5000 main:app
    """
    # Ensure user data directory exists
    os.makedirs(str(APP_SETTINGS.USER_DATA_PATH), exist_ok=True)
    
    # Run development server
    app.run(
        host='0.0.0.0',  # Allow external connections
        port=5005,       # Use same port as before
        debug=True       # Enable debug mode for development
    )