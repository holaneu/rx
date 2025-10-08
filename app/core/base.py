"""
Base classes and common functionality shared across domains.

This module provides foundational functionality that is used across 
multiple parts of the application including:
- Project root resolution
- Path management utilities  
- Common configuration patterns
- Base classes for managers and configurations

All functionality follows Python instructions for path handling and 
PythonAnywhere compatibility.
"""

from pathlib import Path
from typing import Optional


class BaseManager:
    """Base class providing common functionality for all managers."""
    
    @staticmethod
    def get_project_root() -> Path:
        """
        Get the project root directory using robust path resolution.
        
        This method follows Python instructions for absolute path resolution
        and ensures compatibility with PythonAnywhere hosting environment.
        
        Returns:
            Path: Absolute path to the project root directory
            
        Raises:
            Exception: If project root cannot be determined
        """
        # Start from this file's location and walk up directory tree
        current_file_path = Path(__file__).resolve()
        
        # Look for directory that contains both 'app' and 'plugins' folders
        for parent_path in current_file_path.parents:
            if (parent_path / "app").exists() and (parent_path / "plugins").exists():
                return parent_path
        
        # Fallback: if we can't find project root, raise clear error
        raise Exception(
            f"Could not determine project root. "
            f"Starting from: {current_file_path}. "
            f"Expected to find directory containing both 'app' and 'plugins' folders."
        )
    
    @classmethod
    def resolve_absolute_path(cls, relative_path: str) -> Path:
        """
        Resolve a relative path to an absolute path based on project root.
        
        This method ensures all paths are absolute and work correctly
        regardless of the current working directory.
        
        Args:
            relative_path (str): Path relative to project root
            
        Returns:
            Path: Absolute path resolved from project root
            
        Example:
            resolve_absolute_path("plugins") -> /full/path/to/project/plugins
        """
        project_root = cls.get_project_root()
        return project_root / relative_path


class BaseConfig:
    """Base class providing common configuration patterns."""
    
    @classmethod  
    def resolve_absolute_path(cls, relative_path: str) -> Path:
        """
        Convenience method for path resolution in configuration classes.
        
        Args:
            relative_path (str): Path relative to project root
            
        Returns:
            Path: Absolute path resolved from project root
        """
        return BaseManager.resolve_absolute_path(relative_path)
        
    @classmethod
    def validate_directory_exists(cls, directory_path: Path) -> bool:
        """
        Validate that a directory exists and is accessible.
        
        Args:
            directory_path (Path): Path to directory to check
            
        Returns:
            bool: True if directory exists and is accessible
        """
        try:
            return directory_path.exists() and directory_path.is_dir()
        except (OSError, PermissionError):
            return False


# Export commonly used classes
__all__ = [
    'BaseManager',
    'BaseConfig'
]