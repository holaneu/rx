#!/usr/bin/env python3
"""
Test the fixed open_file function
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

def test_open_file():
    """Test the open_file function with the problematic path"""
    print("TESTING open_file FUNCTION")
    print("=" * 40)
    
    try:
        from user.tools.m_included import open_file, user_data_files_path
        from app.configs.app_config import APP_SETTINGS
        
        print(f"USER_DATA_FILES_PATH: {APP_SETTINGS.USER_DATA_FILES_PATH}")
        
        # Test 1: The problematic relative path that was failing
        print("\n1. Testing problematic relative path:")
        try:
            content = open_file("ai_news.md")
            print(f"✓ Successfully opened 'ai_news.md' (content length: {len(content)} chars)")
            print(f"First 100 chars: {content[:100]}...")
        except Exception as e:
            print(f"✗ Failed to open 'ai_news.md': {e}")
        
        # Test 2: Test with files/ prefix (what was actually being tried)
        print("\n2. Testing with 'files/' prefix that was failing:")
        try:
            content = open_file("files/ai_news.md")
            print(f"✗ This should have failed but succeeded: {len(content)} chars")
        except Exception as e:
            print(f"✓ Correctly failed (file path was wrong): {e}")
        
        # Test 3: Test with user/files/ prefix (the original failing path)
        print("\n3. Testing original failing path 'user/files/ai_news.md':")
        try:
            content = open_file("user/files/ai_news.md")
            print(f"✗ This should have failed but succeeded: {len(content)} chars")
        except Exception as e:
            print(f"✓ Correctly failed (invalid relative path): {e}")
        
        # Test 4: Test absolute path
        print("\n4. Testing absolute path:")
        try:
            abs_path = user_data_files_path("ai_news.md")
            content = open_file(abs_path)
            print(f"✓ Successfully opened with absolute path (content length: {len(content)} chars)")
        except Exception as e:
            print(f"✗ Failed with absolute path: {e}")
        
        # Test 5: Test another existing file
        print("\n5. Testing another file 'quick_notes.md':")
        try:
            content = open_file("quick_notes.md")
            print(f"✓ Successfully opened 'quick_notes.md' (content length: {len(content)} chars)")
        except Exception as e:
            print(f"✗ Failed to open 'quick_notes.md': {e}")
        
        # Test 6: Test non-existent file
        print("\n6. Testing non-existent file:")
        try:
            content = open_file("nonexistent.txt")
            print(f"✗ Should have failed but got: {len(content)} chars")
        except FileNotFoundError as e:
            print(f"✓ Correctly failed for non-existent file: {e}")
        except Exception as e:
            print(f"? Failed with different error: {e}")
        
        print("\n" + "=" * 40)
        print("open_file testing completed!")
        
    except ImportError as e:
        print(f"Import error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    test_open_file()