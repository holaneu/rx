#!/usr/bin/env python3
"""
Test all fixed file operation functions for path validation
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

def test_all_file_functions():
    """Test all file operation functions that were fixed"""
    print("TESTING ALL FIXED FILE OPERATION FUNCTIONS")
    print("=" * 60)
    
    try:
        from user.tools.m_included import (
            save_to_file, save_to_external_file, save_to_external_file2, 
            save_to_json_file, json_db_save, user_data_files_path
        )
        from app.configs.app_config import APP_SETTINGS
        
        # Test 1: save_to_file
        print("\n1. Testing save_to_file with absolute path:")
        try:
            abs_path = user_data_files_path("test_save_to_file.txt")
            result = save_to_file(abs_path, "Test content for save_to_file")
            print(f"✓ save_to_file succeeded: {result['message']['body']}")
        except Exception as e:
            print(f"✗ save_to_file failed: {e}")
        
        # Test 2: save_to_json_file
        print("\n2. Testing save_to_json_file with absolute path:")
        try:
            abs_path = user_data_files_path("test_save_to_json_file.json")
            test_data = {"test": "data", "number": 42}
            result = save_to_json_file(test_data, abs_path)
            print(f"✓ save_to_json_file succeeded: {result['message']['body']}")
        except Exception as e:
            print(f"✗ save_to_json_file failed: {e}")
        
        # Test 3: json_db_save
        print("\n3. Testing json_db_save with absolute path:")
        try:
            abs_path = user_data_files_path("databases/test_json_db.json")
            test_db = {
                "db_info": {"id": "test123", "title": "Test Database"},
                "collections": {"test_collection": [{"id": "entry1", "data": "test"}]}
            }
            result = json_db_save(abs_path, test_db)
            print(f"✓ json_db_save succeeded: {result['message']}")
        except Exception as e:
            print(f"✗ json_db_save failed: {e}")
        
        # Test 4: save_to_external_file (if external path is configured)
        print("\n4. Testing save_to_external_file:")
        try:
            external_path = os.getenv('EXTERNAL_STORAGE_1_LOCAL_PATH')
            if external_path:
                result = save_to_external_file("test_external.txt", "Test external content")
                print(f"✓ save_to_external_file succeeded: {result['message']['body']}")
            else:
                print("⚠ save_to_external_file skipped (no EXTERNAL_STORAGE_1_LOCAL_PATH configured)")
        except Exception as e:
            print(f"✗ save_to_external_file failed: {e}")
        
        # Test 5: save_to_external_file2 (if external path is configured)
        print("\n5. Testing save_to_external_file2:")
        try:
            external_path = os.getenv('EXTERNAL_STORAGE_1_LOCAL_PATH')
            if external_path:
                result = save_to_external_file2("test_external2.txt", "Test external content 2", external_root_path=external_path)
                print(f"✓ save_to_external_file2 succeeded: {result['message']['body']}")
            else:
                print("⚠ save_to_external_file2 skipped (no EXTERNAL_STORAGE_1_LOCAL_PATH configured)")
        except Exception as e:
            print(f"✗ save_to_external_file2 failed: {e}")
        
        # Test security: Path traversal attacks should be blocked
        print("\n6. Testing security - path traversal attacks:")
        
        functions_to_test = [
            ("save_to_file", lambda: save_to_file("../../../malicious.txt", "bad content")),
            ("save_to_json_file", lambda: save_to_json_file({"bad": "data"}, "../../../malicious.json")),
        ]
        
        for func_name, func_call in functions_to_test:
            try:
                result = func_call()
                print(f"✗ {func_name} should have blocked path traversal but didn't: {result}")
            except ValueError as e:
                if "Path traversal not allowed" in str(e):
                    print(f"✓ {func_name} correctly blocked path traversal")
                else:
                    print(f"? {func_name} blocked with different message: {e}")
            except Exception as e:
                if "Path traversal not allowed" in str(e):
                    print(f"✓ {func_name} correctly blocked path traversal")
                else:
                    print(f"? {func_name} failed with: {e}")
        
        # Special test for json_db_save (returns error response instead of raising exception)
        try:
            result = json_db_save("../../../malicious.json", {"bad": "db"})
            if result.get("success") == False and "Path traversal not allowed" in result.get("message", ""):
                print("✓ json_db_save correctly blocked path traversal")
            else:
                print(f"✗ json_db_save should have blocked path traversal but didn't: {result}")
        except Exception as e:
            print(f"? json_db_save failed with: {e}")
        
        print("\n" + "=" * 60)
        print("All file operation functions testing completed!")
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure you're running this from the project root")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    test_all_file_functions()