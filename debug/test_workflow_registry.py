#!/usr/bin/env python3
"""
Debug Script 4: Complete Workflow Registration Test
This script tests the complete workflow registration process from discovery to registry.
Usage: python debug/test_workflow_registry.py
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path so we can import modules
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_registry_before_loading():
    """Check registry state before any loading"""
    print("=" * 60)
    print("REGISTRY STATE BEFORE LOADING")
    print("=" * 60)
    
    try:
        from app.utils.registries import WORKFLOWS_REGISTRY
        print(f"Initial registry size: {len(WORKFLOWS_REGISTRY)}")
        
        if WORKFLOWS_REGISTRY:
            print("Pre-existing workflows:")
            for name, data in WORKFLOWS_REGISTRY.items():
                print(f"  - {name}: {data.get('title', 'No title')}")
        else:
            print("Registry is initially empty")
            
    except Exception as e:
        print(f"Error accessing registry: {e}")

def test_module_manager_full_reload():
    """Test the complete module manager reload process"""
    print("\n" + "=" * 60)
    print("TESTING MODULE MANAGER FULL RELOAD")
    print("=" * 60)
    
    try:
        from app.utils.module_manager import ModuleManager
        from app.utils.registries import WORKFLOWS_REGISTRY
        
        print("Creating ModuleManager instance...")
        manager = ModuleManager()
        
        print("Registry size before reload:", len(WORKFLOWS_REGISTRY))
        
        print("Executing full_reload()...")
        manager.full_reload()
        
        print("Registry size after reload:", len(WORKFLOWS_REGISTRY))
        
        if WORKFLOWS_REGISTRY:
            print("Workflows registered after reload:")
            for name, data in WORKFLOWS_REGISTRY.items():
                print(f"  - {name}:")
                print(f"    title: {data.get('title', 'N/A')}")
                print(f"    module: {data.get('module', 'N/A')}")
                print(f"    category: {data.get('category', 'N/A')}")
                print(f"    type: {data.get('type', 'N/A')}")
        else:
            print("✗ Registry is still empty after full reload!")
            
        return len(WORKFLOWS_REGISTRY) > 0
        
    except Exception as e:
        print(f"Error during module manager test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_manual_workflow_loading():
    """Manually test loading a single workflow file and registering it"""
    print("\n" + "=" * 60)
    print("TESTING MANUAL WORKFLOW LOADING")
    print("=" * 60)
    
    # Find a workflow file to test
    user_workflows_dir = project_root / "user" / "workflows"
    
    if not user_workflows_dir.exists():
        print(f"✗ User workflows directory doesn't exist: {user_workflows_dir}")
        return False
    
    workflow_files = list(user_workflows_dir.glob("m_*.py"))
    
    if not workflow_files:
        print(f"✗ No workflow files found in {user_workflows_dir}")
        return False
    
    # Test the first workflow file
    test_file = workflow_files[0]
    print(f"Testing file: {test_file.name}")
    
    try:
        from app.utils.registries import WORKFLOWS_REGISTRY
        
        # Clear registry first
        initial_count = len(WORKFLOWS_REGISTRY)
        
        # Import the module manually
        import importlib.util
        
        module_name = test_file.stem
        spec = importlib.util.spec_from_file_location(module_name, str(test_file))
        
        if not spec or not spec.loader:
            print(f"✗ Could not create spec for {module_name}")
            return False
        
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module  # Register in sys.modules
        spec.loader.exec_module(module)
        
        print(f"✓ Loaded module {module_name}")
        
        # Check if anything was registered
        new_count = len(WORKFLOWS_REGISTRY)
        added_workflows = new_count - initial_count
        
        print(f"Workflows added to registry: {added_workflows}")
        
        if added_workflows > 0:
            print("Newly registered workflows:")
            # Find the new entries (this is simplified, assumes they're the last ones)
            for name, data in list(WORKFLOWS_REGISTRY.items())[-added_workflows:]:
                print(f"  - {name}: {data.get('title', 'No title')}")
        
        return added_workflows > 0
        
    except Exception as e:
        print(f"✗ Error during manual loading: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_workflow_decorator_functionality():
    """Test if the workflow decorator is working correctly"""
    print("\n" + "=" * 60)
    print("TESTING WORKFLOW DECORATOR")
    print("=" * 60)
    
    try:
        from app.workflows._core import workflow
        from app.utils.registries import WORKFLOWS_REGISTRY
        
        # Clear any existing test entries
        test_workflow_name = "test_workflow_debug"
        if test_workflow_name in WORKFLOWS_REGISTRY:
            del WORKFLOWS_REGISTRY[test_workflow_name]
        
        initial_count = len(WORKFLOWS_REGISTRY)
        
        # Create a test workflow function
        @workflow(name="Test Debug Workflow", description="A test workflow for debugging", category="debug")
        def test_workflow_debug(input_text=""):
            """Test workflow function"""
            return f"Processed: {input_text}"
        
        new_count = len(WORKFLOWS_REGISTRY)
        added = new_count - initial_count
        
        print(f"Registry entries added: {added}")
        
        if test_workflow_name in WORKFLOWS_REGISTRY:
            print(f"✓ Test workflow successfully registered")
            workflow_data = WORKFLOWS_REGISTRY[test_workflow_name]
            print(f"  Name: {workflow_data.get('name')}")
            print(f"  Title: {workflow_data.get('title')}")
            print(f"  Description: {workflow_data.get('description')}")
            print(f"  Category: {workflow_data.get('category')}")
            print(f"  Type: {workflow_data.get('type')}")
            
            # Clean up
            del WORKFLOWS_REGISTRY[test_workflow_name]
            return True
        else:
            print(f"✗ Test workflow was not registered")
            return False
            
    except Exception as e:
        print(f"✗ Error testing workflow decorator: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_config_and_paths():
    """Test the module configuration and paths"""
    print("\n" + "=" * 60)
    print("TESTING MODULE CONFIGURATION")
    print("=" * 60)
    
    try:
        from app.utils.module_manager import ModuleManager
        
        manager = ModuleManager()
        config = manager.config
        
        print("Getting all module paths...")
        all_paths = config.get_all_module_paths()
        
        for category, paths in all_paths.items():
            print(f"\nCategory: {category}")
            for package_type, path in paths.items():
                if package_type == "workflows":  # Focus on workflows
                    path_obj = Path(path) if path else None
                    exists = path_obj.exists() if path_obj else False
                    status = "✓" if exists else "✗"
                    print(f"  {status} {package_type}: {path}")
                    
                    if exists and path_obj.is_dir():
                        workflow_files = list(path_obj.glob("m_*.py"))
                        print(f"    Workflow files found: {len(workflow_files)}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error testing configuration: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_complete_workflow():
    """Run a complete workflow registration test"""
    print("\n" + "=" * 60)
    print("COMPLETE WORKFLOW REGISTRATION TEST")
    print("=" * 60)
    
    tests = [
        ("Registry before loading", test_registry_before_loading),
        ("Workflow decorator", test_workflow_decorator_functionality),
        ("Module configuration", test_config_and_paths),
        ("Manual workflow loading", test_manual_workflow_loading),
        ("Module manager full reload", test_module_manager_full_reload),
    ]
    
    results = {}
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            results[test_name] = False
    
    print(f"\n{'='*60}")
    print("FINAL TEST RESULTS")
    print(f"{'='*60}")
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {test_name}")
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    print(f"\nOverall: {passed}/{total} tests passed")

if __name__ == "__main__":
    print("WORKFLOW REGISTRY DEBUG SCRIPT")
    print(f"Project root: {project_root}")
    print(f"Current working directory: {os.getcwd()}")
    
    test_complete_workflow()
    
    print(f"\n{'='*60}")
    print("WORKFLOW REGISTRY DEBUG SCRIPT COMPLETED")
    print(f"{'='*60}")