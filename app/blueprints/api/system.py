"""
System API Blueprint - System diagnostics and debug endpoints

This blueprint handles system-related API routes:
- System diagnostics (/api/diagnostic)

Separated for focused system/debug API functionality.
"""

import os
import sys
from pathlib import Path
from flask import Blueprint, jsonify
from app.core import WORKFLOWS_REGISTRY, PROMPTS_REGISTRY, TOOLS_REGISTRY

# Create system API blueprint
system_api_blueprint = Blueprint('system_api', __name__, url_prefix='/api')


@system_api_blueprint.route('/diagnostic', methods=['GET'])
def diagnostic():
    """Comprehensive diagnostic endpoint to debug plugin loading issues."""
    try:
        # Basic environment info
        cwd = os.getcwd()
        python_path = sys.path[:5]  # First 5 entries
        
        # Check plugins directory using actual PluginsConfig
        from app.core import PluginsConfig
        config = PluginsConfig()
        plugins_dir_abs = config.PLUGINS_ROOT
        plugins_dir = plugins_dir_abs.name  # Just the directory name for display
        
        # Check individual plugin type directories
        workflows_dir = config.get_plugin_directory("workflows")
        prompts_dir = config.get_plugin_directory("prompts")  
        tools_dir = config.get_plugin_directory("tools")
        
        # Count plugin files
        workflow_files = []
        if workflows_dir.exists():
            workflow_files = [f.name for f in workflows_dir.glob("*.py") 
                            if f.name not in {"__init__.py", "_core.py", "core.py"}]
        
        # Check registries - already imported at top level
        
        # Test plugin manager
        plugin_manager_error = None
        try:
            from app.core import PluginsManager
            manager = PluginsManager()
            manager.load_plugins_for_type("workflows")
        except Exception as e:
            plugin_manager_error = str(e)
        
        return jsonify({
            "status": "success",
            "environment": {
                "cwd": cwd,
                "python_path": python_path,
                "plugins_dir": str(plugins_dir),
                "plugins_dir_abs": str(plugins_dir_abs),
                "plugins_dir_exists": plugins_dir_abs.exists()
            },
            "plugin_directories": {
                "workflows_dir_exists": workflows_dir.exists(),
                "prompts_dir_exists": prompts_dir.exists(), 
                "tools_dir_exists": tools_dir.exists(),
                "workflow_files_found": len(workflow_files),
                "workflow_files": workflow_files[:10]  # Show first 10
            },
            "registries": {
                "workflows_loaded": len(WORKFLOWS_REGISTRY),
                "prompts_loaded": len(PROMPTS_REGISTRY),
                "tools_loaded": len(TOOLS_REGISTRY),
                "workflow_keys": list(WORKFLOWS_REGISTRY.keys())[:5]  # First 5
            },
            "plugin_manager": {
                "error": plugin_manager_error,
                "can_import": plugin_manager_error is None
            }
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e),
            "message": f"Diagnostic failed: {str(e)}"
        })


# Export blueprint
__all__ = ['system_api_blueprint']