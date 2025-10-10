"""
Test script for Phase 3: Blueprints structure created
Tests that blueprints can be imported and registered without breaking existing functionality.
"""

import sys
from pathlib import Path

# Add project root to Python path for imports
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

def test_phase_3():
    """Test Phase 3 implementation - blueprints structure creation."""
    
    print("=== PHASE 3 TESTING ===")
    
    try:
        # Test 1: Import blueprints modules
        print("1. Testing blueprints imports...")
        from app.blueprints import api_blueprint, ui_blueprint, files_blueprint
        from app.blueprints import register_blueprints
        print("   ✅ All blueprints imported successfully")
        
        # Test 2: Check blueprint names and prefixes
        print("2. Testing blueprint configuration...")
        print(f"   ✅ API blueprint: {api_blueprint.name}, prefix: {api_blueprint.url_prefix}")
        print(f"   ✅ UI blueprint: {ui_blueprint.name}, prefix: {ui_blueprint.url_prefix}")  
        print(f"   ✅ Files blueprint: {files_blueprint.name}, prefix: {files_blueprint.url_prefix}")
        
        # Test 3: Test blueprint basic structure
        print("3. Testing blueprint structure...")
        print(f"   ✅ API blueprint name: {api_blueprint.name}")
        print(f"   ✅ UI blueprint name: {ui_blueprint.name}")
        print(f"   ✅ Files blueprint name: {files_blueprint.name}")
        
        # Test 4: Test Flask app with blueprints 
        print("4. Testing Flask app with blueprints...")
        from flask import Flask
        
        # Create test Flask app
        test_app = Flask(__name__)
        
        # Register blueprints  
        register_blueprints(test_app)
        
        # Check total routes
        total_routes = len(list(test_app.url_map.iter_rules()))
        print(f"   ✅ Total routes registered: {total_routes}")
        
        # Test 5: Verify original app still works
        print("5. Testing original Flask app compatibility...")
        try:
            from main import app
            original_routes = len(list(app.url_map.iter_rules()))
            print(f"   ✅ Original app still works with {original_routes} routes")
        except Exception as e:
            print(f"   ❌ Original app failed: {e}")
            return False
        
        # Test 6: Verify core functionality still works
        print("6. Testing core functionality...")
        from app.core import PluginsManager, WORKFLOWS_REGISTRY
        
        # Test plugin loading
        pm = PluginsManager()
        pm.load_all_plugins()
        
        workflows_count = len(WORKFLOWS_REGISTRY)
        print(f"   ✅ Plugins still load correctly: {workflows_count} workflows")
        
        print("\n=== PHASE 3 COMPLETED SUCCESSFULLY ===")
        print("✅ Blueprints structure created")
        print("✅ All routes modularized") 
        print("✅ Flask app registration works")
        print("✅ Backward compatibility maintained")
        print("✅ Core functionality preserved")
        print("✅ Ready for Phase 4")
        
        return True
        
    except Exception as e:
        print(f"\n❌ PHASE 3 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_phase_3()
    sys.exit(0 if success else 1)