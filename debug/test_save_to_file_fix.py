#!/usr/bin/env python3
"""
Debug Script: Test save_to_file path validation fix
This script tests the improved path validation logic for save_to_file function.
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path so we can import modules
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
user_path = project_root / "user"
if str(user_path) not in sys.path:
    sys.path.insert(0, str(user_path))

def test_save_to_file_path_validation():
    """Test the save_to_file function with various path scenarios"""
    print("TESTING save_to_file PATH VALIDATION")
    print("=" * 50)
    
    try:
        from user.tools.m_included import save_to_file, user_data_files_path
        from app.configs.app_config import APP_SETTINGS
        
        print(f"USER_DATA_FILES_PATH: {APP_SETTINGS.USER_DATA_FILES_PATH}")
        print(f"USER_DATA_FILES_PATH resolved: {Path(APP_SETTINGS.USER_DATA_FILES_PATH).resolve()}")
        
        # Test case 1: Relative path (should work)
        print("\n1. Testing relative path:")
        try:
            result = save_to_file("test_relative.txt", "Test content")
            print(f"✓ Relative path succeeded: {result}")
        except Exception as e:
            print(f"✗ Relative path failed: {e}")
        
        # Test case 2: Absolute path within allowed directory (should work)
        print("\n2. Testing absolute path via user_data_files_path:")
        try:
            abs_path = user_data_files_path("test_absolute.txt")
            print(f"Generated path: {abs_path}")
            result = save_to_file(abs_path, "Test absolute content")
            print(f"✓ Absolute path via helper succeeded: {result}")
        except Exception as e:
            print(f"✗ Absolute path via helper failed: {e}")
        
        # Test case 3: Direct absolute path construction (should work if within bounds)
        print("\n3. Testing direct absolute path construction:")
        try:
            direct_abs_path = str(Path(APP_SETTINGS.USER_DATA_FILES_PATH) / "test_direct_absolute.txt")
            print(f"Direct absolute path: {direct_abs_path}")
            result = save_to_file(direct_abs_path, "Test direct absolute content")
            print(f"✓ Direct absolute path succeeded: {result}")
        except Exception as e:
            print(f"✗ Direct absolute path failed: {e}")
        
        # Test case 4: Path with .. (should fail)
        print("\n4. Testing path traversal attack:")
        try:
            result = save_to_file("../../../etc/passwd", "Bad content")
            print(f"✗ Path traversal unexpectedly succeeded: {result}")
        except ValueError as e:
            if "Path traversal not allowed" in str(e):
                print(f"✓ Path traversal correctly blocked: {e}")
            else:
                print(f"? Path traversal blocked with different message: {e}")
        except Exception as e:
            print(f"? Path traversal blocked with unexpected error: {e}")
        
        # Test case 5: Absolute path outside allowed directory (should fail)
        print("\n5. Testing absolute path outside allowed directory:")
        try:
            if os.name == 'nt':  # Windows
                bad_path = "C:\\Windows\\System32\\malicious.txt"
            else:  # Unix/Linux
                bad_path = "/etc/malicious.txt"
            result = save_to_file(bad_path, "Malicious content")
            print(f"✗ Outside path unexpectedly succeeded: {result}")
        except ValueError as e:
            if "Path traversal not allowed" in str(e):
                print(f"✓ Outside path correctly blocked: {e}")
            else:
                print(f"? Outside path blocked with different message: {e}")
        except Exception as e:
            print(f"? Outside path blocked with unexpected error: {e}")
        
        print("\n" + "=" * 50)
        print("save_to_file path validation test completed!")
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure you're running this from the project root")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    test_save_to_file_path_validation()