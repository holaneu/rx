#!/usr/bin/env python3
"""
Test module loading with the fixes to see what errors occur during workflow loading.
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
_app_root = Path(__file__).parent.parent
if str(_app_root) not in sys.path:
    sys.path.insert(0, str(_app_root))

# Add user folder to Python path for imports
_user_path = _app_root / "user"
if _user_path.exists() and str(_user_path) not in sys.path:
    sys.path.insert(0, str(_user_path))

def test_workflow_loading():
    """Test the fixed workflow loading mechanism."""
    print("=== TESTING FIXED WORKFLOW LOADING ===")
    
    try:
        from app.utils.registries import WORKFLOWS_REGISTRY
        print("✓ Successfully imported WORKFLOWS_REGISTRY")
        print(f"  Initial registry count: {len(WORKFLOWS_REGISTRY)}")
        
        from app.utils.module_manager import ModuleManager
        print("✓ Successfully imported ModuleManager")
        
        # Clear the registry first
        WORKFLOWS_REGISTRY.clear()
        print(f"  Cleared registry, count: {len(WORKFLOWS_REGISTRY)}")
        
        # Test the module loading
        manager = ModuleManager()
        print("Starting module loading...")
        manager.full_reload()
        
        print(f"  Final registry count: {len(WORKFLOWS_REGISTRY)}")
        print(f"  Workflows loaded: {list(WORKFLOWS_REGISTRY.keys())}")
        
        if len(WORKFLOWS_REGISTRY) > 0:
            print("✓ Workflows successfully loaded!")
            return True
        else:
            print("✗ No workflows were loaded")
            return False
            
    except Exception as e:
        print(f"✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_workflow_loading()
    print(f"\nTest {'PASSED' if success else 'FAILED'}")