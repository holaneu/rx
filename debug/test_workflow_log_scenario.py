#!/usr/bin/env python3
"""
Test the workflow log saving that was causing the original issue
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

def test_workflow_log_scenario():
    """Test the specific workflow log saving scenario that was failing"""
    print("TESTING WORKFLOW LOG SAVING SCENARIO")
    print("=" * 50)
    
    try:
        from user.tools.m_included import save_to_file, formatted_datetime, user_data_files_path
        
        # Simulate the workflow log saving scenario
        formatted_time = formatted_datetime("%Y%m%d_%H%M%S")
        log_filepath = user_data_files_path(f"logs/workflow_{formatted_time}.json")
        
        print(f"Generated log filepath: {log_filepath}")
        print(f"Filepath type: {type(log_filepath)}")
        print(f"Is absolute path: {os.path.isabs(log_filepath)}")
        
        log_content = '''{
  "name": "test_workflow",
  "task_id": "test-123",
  "timestamp": "2025-09-22T12:00:00",
  "log": [
    {
      "title": "Test log entry",
      "body": "This is a test"
    }
  ]
}'''
        
        # This should now work without throwing "Path traversal not allowed" error
        result = save_to_file(content=log_content, filepath=log_filepath)
        print(f"✓ Workflow log save succeeded: {result}")
        
        # Verify the file was actually created
        if os.path.exists(result['message']['body'].replace('File path: ', '')):
            print("✓ Log file was actually created on disk")
        else:
            print("✗ Log file was not found on disk")
        
    except Exception as e:
        print(f"✗ Workflow log save failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_workflow_log_scenario()