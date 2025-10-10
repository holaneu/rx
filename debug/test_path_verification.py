#!/usr/bin/env python3
"""
Debug Script 3: Path Verification
This script verifies all paths exist and are accessible on the server.
Usage: python debug/test_path_verification.py
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path so we can import modules
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def check_path_detailed(path, description=""):
    """Check a path and provide detailed information"""
    path = Path(path)
    print(f"\nChecking: {description if description else str(path)}")
    print(f"Path: {path}")
    print(f"Absolute path: {path.resolve()}")
    
    # Basic existence
    exists = path.exists()
    print(f"Exists: {'✓ YES' if exists else '✗ NO'}")
    
    if not exists:
        return False
    
    # Type of path
    if path.is_file():
        print("Type: File")
        print(f"Size: {path.stat().st_size} bytes")
    elif path.is_dir():
        print("Type: Directory")
        try:
            contents = list(path.iterdir())
            print(f"Contents: {len(contents)} items")
        except PermissionError:
            print("Contents: Permission denied")
    
    # Permissions
    try:
        readable = os.access(path, os.R_OK)
        writable = os.access(path, os.W_OK)
        executable = os.access(path, os.X_OK)
        
        print(f"Readable: {'✓' if readable else '✗'}")
        print(f"Writable: {'✓' if writable else '✗'}")
        print(f"Executable: {'✓' if executable else '✗'}")
    except Exception as e:
        print(f"Permission check failed: {e}")
    
    return True

def test_environment_info():
    """Display environment information"""
    print("=" * 60)
    print("ENVIRONMENT INFORMATION")
    print("=" * 60)
    
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Script location: {Path(__file__).resolve()}")
    print(f"Project root: {project_root.resolve()}")
    print(f"Platform: {sys.platform}")
    
    # Environment variables
    env_vars_to_check = ['PATH', 'PYTHONPATH', 'HOME', 'USER', 'USERNAME']
    print(f"\nEnvironment variables:")
    for var in env_vars_to_check:
        value = os.environ.get(var, 'NOT SET')
        print(f"  {var}: {value}")

def test_critical_paths():
    """Test all critical paths for the application"""
    print("\n" + "=" * 60)
    print("CRITICAL PATHS VERIFICATION")
    print("=" * 60)
    
    critical_paths = [
        (project_root, "Project root"),
        (project_root / "app", "App directory"),
        (project_root / "user", "User directory"),
        (project_root / "app" / "workflows", "App workflows directory"),
        (project_root / "user" / "workflows", "User workflows directory"),
        (project_root / "app" / "utils", "App utils directory"),
        (project_root / "app" / "utils" / "module_manager.py", "Module manager file"),
        (project_root / "app" / "utils" / "registries.py", "Registries file"),
        (project_root / "app" / "workflows" / "_core.py", "Workflow core file"),
        (project_root / "main.py", "Main application file"),
        (project_root / "requirements.txt", "Requirements file"),
    ]
    
    all_good = True
    for path, description in critical_paths:
        if not check_path_detailed(path, description):
            all_good = False
        print("-" * 40)
    
    print(f"\nAll critical paths OK: {'✓ YES' if all_good else '✗ NO'}")
    return all_good

def test_workflow_files_access():
    """Test access to specific workflow files"""
    print("\n" + "=" * 60)
    print("WORKFLOW FILES ACCESS TEST")
    print("=" * 60)
    
    workflow_dirs = [
        project_root / "app" / "workflows",
        project_root / "user" / "workflows"
    ]
    
    for workflow_dir in workflow_dirs:
        print(f"\nScanning workflow directory: {workflow_dir}")
        
        if not workflow_dir.exists():
            print("✗ Directory does not exist")
            continue
        
        try:
            # List all files
            all_files = list(workflow_dir.iterdir())
            py_files = [f for f in all_files if f.suffix == '.py']
            workflow_files = [f for f in py_files if f.name.startswith('m_')]
            
            print(f"Total files: {len(all_files)}")
            print(f"Python files: {len(py_files)}")
            print(f"Workflow files (m_*.py): {len(workflow_files)}")
            
            # Test reading a few workflow files
            for i, wf in enumerate(workflow_files[:3]):  # Test first 3 files
                print(f"\nTesting file access: {wf.name}")
                try:
                    with open(wf, 'r', encoding='utf-8') as f:
                        content = f.read(100)  # Read first 100 chars
                    print(f"  ✓ Can read file (first 100 chars)")
                    print(f"  Content preview: {repr(content[:50])}")
                except Exception as e:
                    print(f"  ✗ Cannot read file: {e}")
                    
        except Exception as e:
            print(f"✗ Error scanning directory: {e}")

def test_python_import_paths():
    """Test Python import paths"""
    print("\n" + "=" * 60)
    print("PYTHON IMPORT PATHS")
    print("=" * 60)
    
    print("sys.path entries:")
    for i, path in enumerate(sys.path):
        exists = Path(path).exists() if path else False
        status = "✓" if exists else "✗"
        print(f"  {i}: {status} {path}")
    
    # Test importing key modules
    print(f"\nTesting key imports:")
    modules_to_test = [
        'app',
        'app.utils',
        'app.utils.registries',
        'app.workflows',
        'user',
        'user.workflows'
    ]
    
    for module_name in modules_to_test:
        try:
            __import__(module_name)
            print(f"  ✓ {module_name}")
        except ImportError as e:
            print(f"  ✗ {module_name}: {e}")
        except Exception as e:
            print(f"  ? {module_name}: {e}")

if __name__ == "__main__":
    print("PATH VERIFICATION DEBUG SCRIPT")
    
    # Run all tests
    test_environment_info()
    test_critical_paths()
    test_workflow_files_access()
    test_python_import_paths()
    
    print("\n" + "=" * 60)
    print("PATH VERIFICATION COMPLETED")
    print("=" * 60)