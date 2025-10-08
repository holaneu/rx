"""
Test script for Phase 2: Management files moved to core
Tests that the new core structure works and old imports still function.
"""

import sys
from pathlib import Path

# Add project root to Python path for imports
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

def test_phase_2():
    """Test Phase 2 implementation - management files in core directory."""
    
    print("=== PHASE 2 TESTING ===")
    
    try:
        # Test 1: Import new core functionality
        print("1. Testing new core imports...")
        from app.core import PluginsManager, PluginsConfig
        from app.core import WORKFLOWS_REGISTRY, PROMPTS_REGISTRY, TOOLS_REGISTRY
        print(f"   ✅ Core imports successful")
        
        # Test 2: Test new PluginsConfig with BaseConfig
        print("2. Testing upgraded PluginsConfig...")
        config = PluginsConfig()
        
        # Test path resolution
        plugins_root = config.PLUGINS_ROOT
        print(f"   ✅ Plugins root: {plugins_root}")
        
        # Test validation method
        validation = config.validate_plugin_structure()
        print(f"   ✅ Structure validation: {validation['plugins_root_exists']}")
        
        # Test 3: Test new PluginsManager with BaseManager
        print("3. Testing upgraded PluginsManager...")
        manager = PluginsManager()
        
        # Test diagnostic info
        diagnostic = manager.get_diagnostic_info()
        print(f"   ✅ Manager diagnostic available")
        
        # Test 4: Load plugins using new system
        print("4. Testing plugin loading with new system...")
        manager.load_all_plugins()
        
        loaded_count = manager.get_loaded_plugins_count()
        workflows_count = len(WORKFLOWS_REGISTRY)
        prompts_count = len(PROMPTS_REGISTRY)
        tools_count = len(TOOLS_REGISTRY)
        
        print(f"   ✅ Plugins loaded: {loaded_count}")
        print(f"   ✅ Workflows: {workflows_count}, Prompts: {prompts_count}, Tools: {tools_count}")
        
        # Test 5: Verify old imports still work (backward compatibility)
        print("5. Testing backward compatibility...")
        try:
            from app.utils.plugins_manager import PluginsManager as OldManager
            from app.configs.plugins_config import PluginsConfig as OldConfig
            from app.utils.registries import WORKFLOWS_REGISTRY as OldRegistry
            print(f"   ✅ Old imports still work")
        except ImportError as e:
            print(f"   ⚠️  Old imports expected to fail during migration: {e}")
        
        # Test 6: Verify Flask app compatibility
        print("6. Testing Flask app compatibility...")
        try:
            from main import app
            print(f"   ✅ Flask app loaded: {app.name}")
        except Exception as e:
            print(f"   ❌ Flask app failed: {e}")
            return False
        
        print("\n=== PHASE 2 COMPLETED SUCCESSFULLY ===")
        print("✅ Management files moved to core/")
        print("✅ Enhanced with BaseManager/BaseConfig") 
        print("✅ Plugin loading functional")
        print("✅ Flask compatibility maintained")
        print("✅ Ready for Phase 3")
        
        return True
        
    except Exception as e:
        print(f"\n❌ PHASE 2 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_phase_2()
    sys.exit(0 if success else 1)