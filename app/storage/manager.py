import os
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Set, Union
from .models import FileSystemItem

class FileStorageManager:
    def __init__(self, base_path: Union[str, Path], skip_folders: Optional[List[str]] = None):
        self.base_path = Path(base_path).resolve()
        # Store skip_folders as a set of lowercase names for fast lookup
        self.skip_folders: Set[str] = set(f.lower() for f in (skip_folders or []))

    def _generate_id(self, path: Union[str, Path]) -> str:
        """Generate a unique ID for a file/folder based on its path"""
        return hashlib.md5(str(path).encode()).hexdigest()[:12]

    def scan_directory(self) -> Dict[str, FileSystemItem]:
        items: Dict[str, FileSystemItem] = {}
        folders: List[tuple] = []
        files: List[tuple] = []
        
        for root_path in self.base_path.rglob('*'):
            root = str(root_path)
            
            # Skip if this is a skipped folder or inside one
            if any(part.lower() in self.skip_folders for part in root_path.parts):
                continue

            if root_path.is_dir():
                # Process directory
                if root_path != self.base_path:  # Skip base directory itself
                    dir_id = self._generate_id(root_path)
                    parent_dir = root_path.parent
                    parent_id = self._generate_id(parent_dir) if parent_dir != self.base_path else None
                    folder_item = FileSystemItem.from_path(
                        str(self.base_path), str(root_path), dir_id, parent_id
                    )
                    # Use folder name for sorting instead of full path
                    folder_name = root_path.name.lower()
                    folders.append((folder_name, dir_id, folder_item))
            
            elif root_path.is_file():
                # Process file
                file_id = self._generate_id(root_path)
                parent_dir = root_path.parent
                parent_id = None if parent_dir == self.base_path else self._generate_id(parent_dir)
                file_item = FileSystemItem.from_path(
                    str(self.base_path), str(root_path), file_id, parent_id
                )
                # Use filename for sorting instead of full path
                files.append((root_path.name.lower(), file_id, file_item))

        # Sort folders and files by their names
        folders.sort(key=lambda x: x[0])
        files.sort(key=lambda x: x[0])
        
        # Add folders first
        for _, dir_id, folder_item in folders:
            items[dir_id] = folder_item
            
        # Then add files
        for _, file_id, file_item in files:
            items[file_id] = file_item

        return items

    def get_structure(self) -> Dict:
        """Returns a JSON-serializable structure of the file system"""
        items = self.scan_directory()
        return {
            'items': list(items.values()),
            'total': len(items)
        }
