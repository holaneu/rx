"""Simplified plugins manager for loading plugin modules."""

import sys
import importlib
from pathlib import Path
from typing import Dict
from app.configs.plugins_config import PluginsConfig


class PluginsManager:
    """Simplified manager for loading plugins from plugins/ directory."""
    
    def __init__(self):
        self.config = PluginsConfig()
        self.loaded_plugins = set()
    
    def load_all_plugins(self):
        """Load all plugins from all plugin types."""
        for plugin_type in self.config.PLUGIN_TYPES.keys():
            self.load_plugins_for_type(plugin_type)
    
    def load_plugins_for_type(self, plugin_type: str):
        """
        Load all plugins for a specific type (workflows, prompts, tools).
        
        Args:
            plugin_type (str): The type of plugins to load (workflows/prompts/tools)
        """
        # Get the plugin directory and registry
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
        
        # Add project root to Python path if not already there
        # Find project root by looking for the directory containing both 'app' and 'plugins'
        current_path = Path(__file__).resolve()
        project_root = None
        
        # Walk up the directory tree to find project root
        for parent in current_path.parents:
            if (parent / "app").exists() and (parent / "plugins").exists():
                project_root = parent
                break
        
        if project_root and str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))
        
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
    
    def _clear_plugins_from_registry(self, registry: Dict[str, dict], plugin_type: str):
        """Clear existing plugin entries from registry."""
        # Remove entries that come from plugins directory
        keys_to_remove = [
            key for key, value in registry.items()
            if isinstance(value, dict) and value.get("module", "").startswith(f"plugins.{plugin_type}")
        ]
        for key in keys_to_remove:
            del registry[key]
        
        # Remove from sys.modules 
        for module_name in list(sys.modules):
            if module_name.startswith(f"plugins.{plugin_type}"):
                del sys.modules[module_name]
    
    def reload_plugins(self):
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