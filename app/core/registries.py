"""
Registry module to break circular dependencies.
This module acts as a central store for all application registries.

Moved to app/core/ as part of the application structure redesign.
All registries remain functionally identical to preserve compatibility.
"""

# Define global registries for different plugin types
WORKFLOWS_REGISTRY = {}
ASSISTANTS_REGISTRY = {}  # Reserved for future use
PROMPTS_REGISTRY = {}
TOOLS_REGISTRY = {}

# Export all registries for easy importing
__all__ = [
    'WORKFLOWS_REGISTRY',
    'ASSISTANTS_REGISTRY', 
    'PROMPTS_REGISTRY',
    'TOOLS_REGISTRY'
]