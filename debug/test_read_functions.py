#!/usr/bin/env python3
"""
Test both open_file and json_db_load functions
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

def test_read_functions():
    """Test both read functions with various path scenarios"""
    print("TESTING READ FUNCTIONS (open_file & json_db_load)")
    print("=" * 55)
    
    try:
        from user.tools.m_included import open_file, json_db_load, user_data_files_path
        from app.configs.app_config import APP_SETTINGS
        
        print(f"USER_DATA_FILES_PATH: {APP_SETTINGS.USER_DATA_FILES_PATH}")
        
        # Test 1: open_file with relative path
        print("\n1. Testing open_file with relative path:")
        try:
            content = open_file("ai_news.md")
            print(f"✓ Successfully opened 'ai_news.md' (content length: {len(content)} chars)")
        except Exception as e:
            print(f"✗ Failed: {e}")
        
        # Test 2: json_db_load with relative path
        print("\n2. Testing json_db_load with relative path:")
        try:
            # First create a test database file
            from user.tools.m_included import json_db_save
            test_db = {
                "db_info": {"id": "test123", "title": "Test Database"},
                "collections": {"test_collection": [{"id": "entry1", "data": "test"}]}
            }
            save_result = json_db_save("databases/test_read_db.json", test_db)
            print(f"  Created test database: {save_result['message']}")
            
            # Now try to load it with relative path
            loaded_db = json_db_load("databases/test_read_db.json")
            if loaded_db and "db_info" in loaded_db:
                print(f"✓ Successfully loaded database with relative path")
                print(f"  Database title: {loaded_db['db_info']['title']}")
            else:
                print(f"✗ Failed to load database or got empty result: {loaded_db}")
        except Exception as e:
            print(f"✗ Failed: {e}")
        
        # Test 3: json_db_load with absolute path
        print("\n3. Testing json_db_load with absolute path:")
        try:
            abs_path = user_data_files_path("databases/test_read_db.json")
            loaded_db = json_db_load(abs_path)
            if loaded_db and "db_info" in loaded_db:
                print(f"✓ Successfully loaded database with absolute path")
            else:
                print(f"✗ Failed to load database with absolute path: {loaded_db}")
        except Exception as e:
            print(f"✗ Failed: {e}")
        
        # Test 4: Test non-existent file with json_db_load
        print("\n4. Testing json_db_load with non-existent file:")
        try:
            result = json_db_load("nonexistent_database.json")
            if result == {}:
                print("✓ Correctly returned empty dict for non-existent file")
            else:
                print(f"? Unexpected result: {result}")
        except Exception as e:
            print(f"✗ Failed: {e}")
        
        # Test 5: Test the original problematic case
        print("\n5. Testing original problematic case scenarios:")
        
        # This is what was likely failing before
        problematic_paths = [
            "user/files/ai_news.md",  # This was the original error
            "files/ai_news.md",       # Another likely wrong path
        ]
        
        for path in problematic_paths:
            try:
                content = open_file(path)
                print(f"✗ Path '{path}' should have failed but succeeded: {len(content)} chars")
            except Exception as e:
                print(f"✓ Path '{path}' correctly failed: File not found (path was wrong)")
        
        print("\n" + "=" * 55)
        print("Read functions testing completed!")
        
    except ImportError as e:
        print(f"Import error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    test_read_functions()