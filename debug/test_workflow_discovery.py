#!/usr/bin/env python3
"""
Debug Script 1: Test Workflow Discovery
This script tests if workflows are being discovered correctly in both app and user directories.
Usage: python debug/test_workflow_discovery.py
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path so we can import modules
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_paths_exist():
    """Test if all expected workflow directories exist"""
    print("=" * 60)
    print("TESTING PATH EXISTENCE")
    print("=" * 60)
    
    # Expected workflow paths
    paths_to_check = [
        project_root / "app" / "workflows",
        project_root / "user" / "workflows",
        project_root / "app" / "utils" / "module_manager.py",
        project_root / "app" / "utils" / "registries.py",
        project_root / "app" / "workflows" / "_core.py"
    ]
    
    all_exist = True
    for path in paths_to_check:
        exists = path.exists()
        status = "✓ OK" if exists else "✗ MISSING"
        print(f"{status} - {path}")
        if not exists:
            all_exist = False
    
    print(f"\nAll paths exist: {'YES' if all_exist else 'NO'}")
    return all_exist

def test_workflow_files():
    """Check what workflow files are found in directories"""
    print("\n" + "=" * 60)
    print("TESTING WORKFLOW FILE DISCOVERY")
    print("=" * 60)
    
    directories = [
        project_root / "app" / "workflows",
        project_root / "user" / "workflows"
    ]
    
    for directory in directories:
        print(f"\nScanning directory: {directory}")
        if not directory.exists():
            print("  ✗ Directory does not exist!")
            continue
        
        # Look for Python files that start with 'm_'
        python_files = list(directory.glob("*.py"))
        workflow_files = [f for f in python_files if f.name.startswith("m_")]
        
        print(f"  Total Python files: {len(python_files)}")
        print(f"  Workflow files (m_*.py): {len(workflow_files)}")
        
        if workflow_files:
            print("  Workflow files found:")
            for file in workflow_files:
                print(f"    - {file.name}")
        else:
            print("  No workflow files found!")
            if python_files:
                print("  Other Python files found:")
                for file in python_files:
                    print(f"    - {file.name}")

def test_module_manager():
    """Test the module manager's ability to discover workflows"""
    print("\n" + "=" * 60)
    print("TESTING MODULE MANAGER")
    print("=" * 60)
    
    try:
        from app.utils.module_manager import ModuleManager
        print("✓ Successfully imported ModuleManager")
        
        # Create instance
        manager = ModuleManager()
        print("✓ Successfully created ModuleManager instance")
        
        # Try to get configuration
        config = manager.config
        print(f"✓ Got configuration: {type(config)}")
        
        # Try to get workflow paths
        all_paths = config.get_all_module_paths()
        print(f"✓ Got all module paths: {len(all_paths)} categories")
        
        for category, paths in all_paths.items():
            print(f"  Category '{category}':")
            for package_type, path in paths.items():
                exists = Path(path).exists() if path else False
                status = "✓" if exists else "✗"
                print(f"    {status} {package_type}: {path}")
        
    except Exception as e:
        print(f"✗ Error testing ModuleManager: {e}")
        import traceback
        traceback.print_exc()

def test_registries():
    """Test the workflow registries"""
    print("\n" + "=" * 60)
    print("TESTING WORKFLOW REGISTRIES")
    print("=" * 60)
    
    try:
        from app.utils.registries import WORKFLOWS_REGISTRY
        print("✓ Successfully imported WORKFLOWS_REGISTRY")
        print(f"  Current registry size: {len(WORKFLOWS_REGISTRY)}")
        
        if WORKFLOWS_REGISTRY:
            print("  Registered workflows:")
            for name, workflow_data in WORKFLOWS_REGISTRY.items():
                print(f"    - {name}: {workflow_data.get('title', 'No title')}")
        else:
            print("  ✗ Registry is empty!")
            
    except Exception as e:
        print(f"✗ Error testing registries: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("WORKFLOW DISCOVERY DEBUG SCRIPT")
    print(f"Project root: {project_root}")
    print(f"Current working directory: {os.getcwd()}")
    
    # Run all tests
    test_paths_exist()
    test_workflow_files()
    test_module_manager()
    test_registries()
    
    print("\n" + "=" * 60)
    print("DEBUG SCRIPT COMPLETED")
    print("=" * 60)