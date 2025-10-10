"""Test plugins loading directly."""

import sys
from pathlib import Path

def test_plugin_loading():
    # Add project root to path
    project_root = Path(__file__).parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
        print(f"Added to path: {project_root}")
    
    print("Testing direct plugin import...")
    
    try:
        # Import a plugin module directly  
        import plugins.prompts.m_analyze_situation
        print("✓ Successfully imported m_analyze_situation")
    except Exception as e:
        print(f"✗ Failed to import m_analyze_situation: {e}")
        return False
    
    # Check if it registered in the registry
    from app.utils.registries import PROMPTS_REGISTRY
    print(f"Prompts in registry after import: {len(PROMPTS_REGISTRY)}")
    
    if PROMPTS_REGISTRY:
        print(f"Sample keys: {list(PROMPTS_REGISTRY.keys())[:3]}")
        return True
    else:
        print("No prompts registered")
        return False

if __name__ == "__main__":
    success = test_plugin_loading()
    print(f"Test {'PASSED' if success else 'FAILED'}")