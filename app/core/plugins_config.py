"""Simplified plugins configuration with robust path resolution."""

from pathlib import Path
from .base import BaseConfig

# During migration, use existing registries to maintain compatibility
from app.utils.registries import (
    WORKFLOWS_REGISTRY,
    PROMPTS_REGISTRY,
    TOOLS_REGISTRY,
)


class PluginsConfig(BaseConfig):
    """
    Simplified configuration for plugin management.
    
    Uses BaseConfig for robust path resolution that works correctly
    across different hosting environments including PythonAnywhere.
    """
    
    # Root plugins directory - using robust path resolution from BaseConfig
    PLUGINS_ROOT = BaseConfig.resolve_absolute_path("plugins")
    
    # Supported plugin types and their registries
    PLUGIN_TYPES = {
        "workflows": WORKFLOWS_REGISTRY,
        "prompts": PROMPTS_REGISTRY, 
        "tools": TOOLS_REGISTRY,
    }
    
    @classmethod
    def get_plugin_directory(cls, plugin_type: str) -> Path:
        """Get the directory path for a specific plugin type."""
        return cls.PLUGINS_ROOT / plugin_type
    
    @classmethod
    def get_registry_for_plugin_type(cls, plugin_type: str) -> dict:
        """Get the registry for a specific plugin type."""
        return cls.PLUGIN_TYPES.get(plugin_type, {})
    
    @classmethod
    def get_all_plugin_directories(cls) -> list:
        """Get all plugin directories that exist."""
        directories = []
        for plugin_type in cls.PLUGIN_TYPES.keys():
            plugin_dir = cls.get_plugin_directory(plugin_type)
            if cls.validate_directory_exists(plugin_dir):
                directories.append(plugin_dir)
        return directories
    
    @classmethod
    def validate_plugin_structure(cls) -> dict:
        """
        Validate the plugin directory structure and return diagnostic info.
        
        Returns:
            dict: Diagnostic information about plugin directories
        """
        diagnostics = {
            "plugins_root_exists": cls.validate_directory_exists(cls.PLUGINS_ROOT),
            "plugins_root_path": str(cls.PLUGINS_ROOT),
            "plugin_types": {}
        }
        
        for plugin_type in cls.PLUGIN_TYPES.keys():
            plugin_dir = cls.get_plugin_directory(plugin_type)
            diagnostics["plugin_types"][plugin_type] = {
                "exists": cls.validate_directory_exists(plugin_dir),
                "path": str(plugin_dir),
                "file_count": len(list(plugin_dir.glob("*.py"))) if plugin_dir.exists() else 0
            }
        
        return diagnostics


# Export the main configuration class
__all__ = ['PluginsConfig']