"""Debug version of plugins manager with verbose output."""

import sys
import importlib
from pathlib import Path

# Add project root to sys.path first
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from app.configs.plugins_config import PluginsConfig


def debug_load_plugins():
    """Debug function to test plugin loading step by step."""
    config = PluginsConfig()
    
    print("=== Starting plugin loading debug ===")
    
    # Add project root to path
    current_file = Path(__file__).resolve()
    project_root = None
    
    for parent in current_file.parents:
        if (parent / "app").exists() and (parent / "plugins").exists():
            project_root = parent
            break
    
    print(f"Found project root: {project_root}")
    
    if project_root and str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
        print(f"Added to sys.path: {project_root}")
    
    # Test one plugin type
    plugin_type = "prompts"
    plugin_dir = config.get_plugin_directory(plugin_type)
    
    print(f"Plugin directory: {plugin_dir}")
    print(f"Resolved path: {plugin_dir.resolve()}")
    print(f"Exists: {plugin_dir.exists()}")
    
    if not plugin_dir.exists():
        print("ERROR: Plugin directory doesn't exist!")
        return
    
    # List Python files
    py_files = [f for f in plugin_dir.glob("*.py") 
                if f.name not in {"__init__.py", "_core.py", "core.py"}]
    
    print(f"Found {len(py_files)} Python files to load")
    
    loaded_count = 0
    for py_file in py_files[:2]:  # Test first 2 files only
        print(f"\n--- Loading {py_file.name} ---")
        
        try:
            module_name = f"plugins.{plugin_type}.{py_file.stem}"
            print(f"Module name: {module_name}")
            
            # Remove from sys.modules to force fresh import
            if module_name in sys.modules:
                del sys.modules[module_name]
                print("Removed from sys.modules")
            
            # Import the module
            module = importlib.import_module(module_name)
            loaded_count += 1
            print(f"✓ Successfully loaded: {py_file.stem}")
            
        except Exception as e:
            print(f"✗ Failed to load {py_file.name}: {e}")
    
    print(f"\n=== Summary ===")
    print(f"Loaded {loaded_count} plugins")
    
    # Check registry
    from app.utils.registries import PROMPTS_REGISTRY
    print(f"Items in PROMPTS_REGISTRY: {len(PROMPTS_REGISTRY)}")
    
    if PROMPTS_REGISTRY:
        print(f"Sample keys: {list(PROMPTS_REGISTRY.keys())[:3]}")

if __name__ == "__main__":
    debug_load_plugins()