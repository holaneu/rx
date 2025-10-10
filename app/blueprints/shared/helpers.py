"""
Shared Helper Functions

This module contains utility functions and shared data structures
used across multiple blueprints to avoid code duplication.
"""

# In‐memory store for generator functions (shared across application)
# This needs to be accessible from main.py for backward compatibility
generators: dict[str, any] = {}


def get_workflows_catalog():
    """
    Return workflows registry without function objects for API/template use.
    
    This function is shared between UI and API blueprints to ensure
    consistent workflow data formatting.
    
    Returns:
        dict: Workflows registry with function objects removed and sorted by title
    """
    try:
        from app.core import WORKFLOWS_REGISTRY
        
        if not WORKFLOWS_REGISTRY:
            print("Warning: WORKFLOWS_REGISTRY is empty, attempting to reload plugins...")
            # Try to reload plugins if registry is empty
            from app.core import PluginsManager
            manager = PluginsManager()
            manager.load_all_plugins()
            
        # Sort workflows alphabetically by title
        sorted_workflows = sorted(
            WORKFLOWS_REGISTRY.items(),
            key=lambda item: item[1].get('title', item[0])  # Sort by title, fallback to workflow_id
        )
        
        return {
            workflow_id: {key: value for key, value in workflow_data.items() if key != "function"}
            for workflow_id, workflow_data in sorted_workflows
        }
    except Exception as e:
        print(f"Error in get_workflows_catalog: {e}")
        # Return empty dict to prevent 500 error
        return {}


# Export all shared utilities
__all__ = [
    'get_workflows_catalog',
    'generators'
]