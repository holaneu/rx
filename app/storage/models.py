from dataclasses import dataclass, field
from typing import Optional, Union
from pathlib import Path

@dataclass
class FileSystemItem:
    id: str
    type: str  # 'file' or 'folder'
    title: str
    file_path: str

    @classmethod
    def from_path(cls, base_path: Union[str, Path], full_path: Union[str, Path], item_id: str, parent_id: Optional[str] = None) -> 'FileSystemItem':
        base_path = Path(base_path)
        full_path = Path(full_path)
        
        rel_path = full_path.relative_to(base_path)
        item = cls(
            id=item_id,
            type='folder' if full_path.is_dir() else 'file',
            title=full_path.name,
            file_path=str(rel_path).replace('\\', '/')
        )
        
        if parent_id:
            setattr(item, 'parent', parent_id)
            
        if full_path.name.startswith('.'):
            setattr(item, 'is_hidden', True)
            
        return item
