#!/usr/bin/env python3
"""
Debug Script 2: Test Module Loading
This script tests if individual workflow modules can be loaded and their metadata extracted.
Usage: python debug/test_module_loading.py
"""

import sys
import os
import importlib.util
from pathlib import Path

# Add the project root to Python path so we can import modules
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_load_single_workflow(file_path):
    """Test loading a single workflow file"""
    print(f"\nTesting file: {file_path.name}")
    print("-" * 40)
    
    try:
        # Create module spec
        module_name = file_path.stem  # filename without extension
        spec = importlib.util.spec_from_file_location(module_name, str(file_path))
        
        if not spec:
            print(f"  ✗ Could not create spec for {module_name}")
            return False
            
        if not spec.loader:
            print(f"  ✗ No loader available for {module_name}")
            return False
            
        print(f"  ✓ Created spec for {module_name}")
        
        # Create module from spec
        module = importlib.util.module_from_spec(spec)
        print(f"  ✓ Created module object")
        
        # Execute the module
        spec.loader.exec_module(module)
        print(f"  ✓ Executed module successfully")
        
        # Check what's in the module
        module_contents = dir(module)
        functions = [name for name in module_contents if not name.startswith('_') and callable(getattr(module, name, None))]
        
        print(f"  Found {len(functions)} functions: {', '.join(functions)}")
        
        # Check for workflow decorator usage
        workflow_functions = []
        for func_name in functions:
            func = getattr(module, func_name)
            if hasattr(func, 'is_workflow'):
                workflow_functions.append(func_name)
                print(f"    - {func_name}: is_workflow={func.is_workflow}")
                if hasattr(func, 'title'):
                    print(f"      title: {func.title}")
                if hasattr(func, 'description'):
                    print(f"      description: {func.description}")
        
        if workflow_functions:
            print(f"  ✓ Found {len(workflow_functions)} decorated workflow functions")
        else:
            print(f"  ✗ No workflow-decorated functions found")
            
        return True
        
    except Exception as e:
        print(f"  ✗ Error loading module: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_workflows_in_directory(directory):
    """Test loading all workflow files in a directory"""
    print(f"\n{'='*60}")
    print(f"TESTING DIRECTORY: {directory}")
    print(f"{'='*60}")
    
    if not directory.exists():
        print(f"✗ Directory does not exist: {directory}")
        return
    
    # Find workflow files
    workflow_files = list(directory.glob("m_*.py"))
    
    if not workflow_files:
        print(f"✗ No workflow files (m_*.py) found in {directory}")
        return
    
    print(f"Found {len(workflow_files)} workflow files")
    
    successful_loads = 0
    for file_path in workflow_files:
        if test_load_single_workflow(file_path):
            successful_loads += 1
    
    print(f"\nSUMMARY: {successful_loads}/{len(workflow_files)} files loaded successfully")

def test_registry_after_loading():
    """Test the registry after attempting to load modules"""
    print(f"\n{'='*60}")
    print("TESTING REGISTRY AFTER MODULE LOADING")
    print(f"{'='*60}")
    
    try:
        from app.utils.registries import WORKFLOWS_REGISTRY
        print(f"Registry size: {len(WORKFLOWS_REGISTRY)}")
        
        if WORKFLOWS_REGISTRY:
            print("Registered workflows:")
            for name, data in WORKFLOWS_REGISTRY.items():
                print(f"  - {name}:")
                print(f"    title: {data.get('title', 'N/A')}")
                print(f"    module: {data.get('module', 'N/A')}")
                print(f"    type: {data.get('type', 'N/A')}")
        else:
            print("✗ Registry is still empty after loading attempts")
            
    except Exception as e:
        print(f"✗ Error checking registry: {e}")

def test_specific_workflow_file(filename):
    """Test a specific workflow file by name"""
    print(f"\n{'='*60}")
    print(f"TESTING SPECIFIC FILE: {filename}")
    print(f"{'='*60}")
    
    # Look in both directories
    directories = [
        project_root / "app" / "workflows",
        project_root / "user" / "workflows"
    ]
    
    for directory in directories:
        file_path = directory / filename
        if file_path.exists():
            print(f"Found file in: {directory}")
            test_load_single_workflow(file_path)
            return
    
    print(f"✗ File '{filename}' not found in any workflow directory")

if __name__ == "__main__":
    print("MODULE LOADING DEBUG SCRIPT")
    print(f"Project root: {project_root}")
    print(f"Current working directory: {os.getcwd()}")
    
    # Test both workflow directories
    workflow_directories = [
        project_root / "app" / "workflows",
        project_root / "user" / "workflows"
    ]
    
    for directory in workflow_directories:
        test_workflows_in_directory(directory)
    
    # Check registry state
    test_registry_after_loading()
    
    # Test a specific file if it exists (you can modify this)
    # Uncomment and modify the line below to test a specific file
    # test_specific_workflow_file("m_ask_llm_basic.py")
    
    print(f"\n{'='*60}")
    print("MODULE LOADING DEBUG SCRIPT COMPLETED")
    print(f"{'='*60}")