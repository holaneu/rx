"""
Test script for Phase 1: Core directory creation
Tests that the new core functionality works correctly without breaking existing code.
"""

import sys
from pathlib import Path

# Add project root to Python path for imports
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

def test_phase_1():
    """Test Phase 1 implementation - core directory and base functionality."""
    
    print("=== PHASE 1 TESTING ===")
    
    try:
        # Test 1: Import new core module
        print("1. Testing core module import...")
        import app.core
        print(f"   ✅ Core module imported: {app.core.__version__}")
        
        # Test 2: Test base functionality  
        print("2. Testing base functionality...")
        from app.core.base import BaseManager, BaseConfig
        
        project_root = BaseManager.get_project_root()
        print(f"   ✅ Project root detected: {project_root}")
        
        plugins_path = BaseManager.resolve_absolute_path("plugins")
        print(f"   ✅ Plugins path resolved: {plugins_path}")
        
        # Test 3: Verify existing plugin system still works
        print("3. Testing existing plugin system...")
        from app.utils.plugins_manager import PluginsManager
        from app.utils.registries import WORKFLOWS_REGISTRY, PROMPTS_REGISTRY, TOOLS_REGISTRY
        
        pm = PluginsManager()
        pm.load_all_plugins()
        
        workflows_count = len(WORKFLOWS_REGISTRY)
        prompts_count = len(PROMPTS_REGISTRY) 
        tools_count = len(TOOLS_REGISTRY)
        
        print(f"   ✅ Plugins loaded: {pm.get_loaded_plugins_count()}")
        print(f"   ✅ Workflows: {workflows_count}, Prompts: {prompts_count}, Tools: {tools_count}")
        
        # Test 4: Verify Flask app still loads
        print("4. Testing Flask app compatibility...")
        from main import app
        print(f"   ✅ Flask app loaded: {app.name}")
        
        print("\n=== PHASE 1 COMPLETED SUCCESSFULLY ===")
        print("✅ Core directory created")
        print("✅ Base functionality implemented") 
        print("✅ Existing functionality preserved")
        print("✅ Ready for Phase 2")
        
        return True
        
    except Exception as e:
        print(f"\n❌ PHASE 1 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_phase_1()
    sys.exit(0 if success else 1)