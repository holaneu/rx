"""Simplified plugins configuration."""

from pathlib import Path
from app.utils.registries import (
    WORKFLOWS_REGISTRY,
    PROMPTS_REGISTRY,
    TOOLS_REGISTRY,
)

class PluginsConfig:
    """Simplified configuration for plugin management."""
    
    # Root plugins directory - single source of truth
    PLUGINS_ROOT = Path("plugins")
    
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
            if plugin_dir.exists():
                directories.append(plugin_dir)
        return directories