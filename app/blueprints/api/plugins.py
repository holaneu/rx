"""
Plugins API Blueprint - Plugin management endpoints

This blueprint handles plugin-related API routes:
- Reload plugins (/api/reload_plugins)

Separated for focused plugin management API functionality.
"""

from flask import Blueprint, jsonify
from app.core import WORKFLOWS_REGISTRY, PROMPTS_REGISTRY, TOOLS_REGISTRY

# Create plugins API blueprint
plugins_api_blueprint = Blueprint('plugins_api', __name__, url_prefix='/api')


@plugins_api_blueprint.route('/reload_plugins', methods=['GET', 'POST'])
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


# Export blueprint
__all__ = ['plugins_api_blueprint']