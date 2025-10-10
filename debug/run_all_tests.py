#!/usr/bin/env python3
"""
Debug Script: Run All Tests
This script runs all debugging tests in sequence.
Usage: python debug/run_all_tests.py
"""

import sys
import os
import subprocess
from pathlib import Path

# Add the project root to Python path so we can import modules
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def run_debug_script(script_name):
    """Run a debug script and capture its output"""
    script_path = project_root / "debug" / script_name
    
    if not script_path.exists():
        print(f"✗ Script not found: {script_path}")
        return False
    
    print(f"\n{'='*80}")
    print(f"RUNNING: {script_name}")
    print(f"{'='*80}")
    
    try:
        # Run the script
        result = subprocess.run([sys.executable, str(script_path)], 
                              capture_output=True, text=True, cwd=str(project_root))
        
        # Print the output
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        if result.returncode == 0:
            print(f"✓ {script_name} completed successfully")
            return True
        else:
            print(f"✗ {script_name} failed with return code {result.returncode}")
            return False
            
    except Exception as e:
        print(f"✗ Error running {script_name}: {e}")
        return False

def main():
    """Run all debug tests"""
    print("RUNNING ALL DEBUG TESTS")
    print(f"Project root: {project_root}")
    print(f"Current working directory: {os.getcwd()}")
    
    # List of debug scripts to run
    debug_scripts = [
        "test_path_verification.py",
        "test_workflow_discovery.py", 
        "test_module_loading.py",
        "test_workflow_registry.py"
    ]
    
    results = {}
    
    for script in debug_scripts:
        results[script] = run_debug_script(script)
    
    # Summary
    print(f"\n{'='*80}")
    print("FINAL SUMMARY")
    print(f"{'='*80}")
    
    for script, success in results.items():
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status} - {script}")
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    print(f"\nOverall: {passed}/{total} scripts completed successfully")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    main()