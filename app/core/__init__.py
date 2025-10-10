"""
Core functionality and management for the application.

This module provides centralized access to core application functionality:
- Plugin management system
- Configuration management  
- Global registries
- Shared base classes and utilities

The core module acts as a single import point for commonly used functionality
across the application, improving maintainability and reducing import complexity.
"""

# Import core functionality for easy access
from .plugins_manager import PluginsManager
from .plugins_config import PluginsConfig
from .base import BaseManager, BaseConfig

# During migration, import existing registries for compatibility
from app.utils.registries import (
    WORKFLOWS_REGISTRY,
    PROMPTS_REGISTRY,
    TOOLS_REGISTRY,
    ASSISTANTS_REGISTRY
)

# Export all commonly used items
__all__ = [
    'PluginsManager',
    'PluginsConfig',
    'WORKFLOWS_REGISTRY',
    'PROMPTS_REGISTRY', 
    'TOOLS_REGISTRY',
    'ASSISTANTS_REGISTRY',
    'BaseManager',
    'BaseConfig'
]

# Version info for tracking migration progress
__version__ = "1.0.0-phase2"
__migration_phase__ = "Phase 2: Management files moved to core"