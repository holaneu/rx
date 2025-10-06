#!/usr/bin/env python3
"""
Test script to verify that workflows are sorted alphabetically.
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

# Import the function we want to test
from main import get_workflows_catalog

def test_workflow_sorting():
    """Test that workflows are returned in alphabetical order by title."""
    print("Testing workflow sorting...")
    
    try:
        workflows = get_workflows_catalog()
        
        if not workflows:
            print("Warning: No workflows found in registry")
            return
            
        # Extract titles from workflows
        titles = [workflow['title'] for workflow in workflows.values()]
        
        print(f"Found {len(titles)} workflows:")
        for i, title in enumerate(titles, 1):
            print(f"  {i}. {title}")
        
        # Check if they are sorted
        sorted_titles = sorted(titles)
        
        if titles == sorted_titles:
            print("✅ SUCCESS: Workflows are sorted alphabetically!")
        else:
            print("❌ FAILED: Workflows are NOT sorted alphabetically!")
            print("Expected order:")
            for i, title in enumerate(sorted_titles, 1):
                print(f"  {i}. {title}")
                
    except Exception as e:
        print(f"Error during test: {e}")

if __name__ == "__main__":
    test_workflow_sorting()