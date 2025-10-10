"""Simplified plugins manager for loading plugin modules with robust path handling."""

import sys
import importlib
from pathlib import Path
from typing import Dict, Set
from .base import BaseManager
from .plugins_config import PluginsConfig


class PluginsManager(BaseManager):
    """
    Simplified manager for loading plugins from plugins/ directory.
    
    Inherits from BaseManager for robust path resolution and follows
    Python instructions for cross-platform compatibility.
    """
    
    def __init__(self):
        self.config = PluginsConfig()
        self.loaded_plugins: Set[str] = set()
    
    def load_all_plugins(self) -> None:
        """Load all plugins from all plugin types."""
        for plugin_type in self.config.PLUGIN_TYPES.keys():
            self.load_plugins_for_type(plugin_type)
    
    def load_plugins_for_type(self, plugin_type: str) -> None:
        """
        Load all plugins for a specific type (workflows, prompts, tools).
        
        Args:
            plugin_type (str): The type of plugins to load (workflows/prompts/tools)
        """
        # Get the plugin directory and registry using new config
        plugin_dir = self.config.get_plugin_directory(plugin_type)
        registry = self.config.get_registry_for_plugin_type(plugin_type)
        
        if not plugin_dir.exists():
            print(f"Warning: Plugin directory does not exist: {plugin_dir}")
            return
        if registry is None:
            print(f"Warning: No registry found for plugin type: {plugin_type}")
            return
        
        # Clear existing plugin modules from registry
        self._clear_plugins_from_registry(registry, plugin_type)
        
        # Add project root to Python path using BaseManager method
        try:
            project_root = self.get_project_root()
            if str(project_root) not in sys.path:
                sys.path.insert(0, str(project_root))
        except Exception as e:
            print(f"Warning: Could not determine project root: {e}")
            return
        
        # Load all Python modules from the plugin directory
        for py_file in plugin_dir.glob("*.py"):
            if py_file.name not in {"__init__.py", "_core.py", "core.py"}:
                try:
                    module_name = f"plugins.{plugin_type}.{py_file.stem}"
                    
                    # Remove from sys.modules to force fresh import
                    if module_name in sys.modules:
                        del sys.modules[module_name]
                    
                    # Import the module using importlib - this will trigger decorators to register functions
                    module = importlib.import_module(module_name)
                    self.loaded_plugins.add(module_name)
                    
                except Exception as e:
                    # Log error but continue with other modules
                    print(f"Warning: Failed to load plugin {py_file.name}: {e}")
                    continue
    
    def _clear_plugins_from_registry(self, registry: Dict[str, dict], plugin_type: str) -> None:
        """Clear existing plugin entries from registry."""
        # Remove entries that come from plugins directory
        keys_to_remove = [
            key for key, value in registry.items()
            if isinstance(value, dict) and value.get("module", "").startswith(f"plugins.{plugin_type}")
        ]
        for key in keys_to_remove:
            del registry[key]
        
        # Remove from sys.modules 
        for module_name in list(sys.modules.keys()):
            if module_name.startswith(f"plugins.{plugin_type}"):
                del sys.modules[module_name]
    
    def reload_plugins(self) -> None:
        """Reload all plugins - useful for development."""
        # Clear all loaded plugins
        self.loaded_plugins.clear()
        
        # Reload all plugins
        self.load_all_plugins()
        
        # Invalidate Python import cache
        importlib.invalidate_caches()
    
    def get_loaded_plugins_count(self) -> int:
        """Get the number of loaded plugins."""
        return len(self.loaded_plugins)
    
    def get_diagnostic_info(self) -> dict:
        """
        Get comprehensive diagnostic information about plugin loading.
        
        Returns:
            dict: Diagnostic information including config validation and loaded plugins
        """
        diagnostics = {
            "manager_info": {
                "loaded_plugins_count": self.get_loaded_plugins_count(),
                "loaded_plugins": list(self.loaded_plugins)
            },
            "config_validation": self.config.validate_plugin_structure()
        }
        
        return diagnostics


# Export the main manager class
__all__ = ['PluginsManager']