"""
Files UI Blueprint - File browser and management

This blueprint handles file-related UI routes:
- File browser (/files, /files/folder/<id>)
- File detail view (/files/file/<id>)

Moved from the original files.py blueprint for better organization.
"""

from flask import Blueprint, render_template, redirect, url_for, abort
from pathlib import Path
from app.storage.manager import FileStorageManager
from app.configs.app_config import APP_SETTINGS

# Create files UI blueprint with '/files' prefix
files_blueprint = Blueprint('files', __name__, url_prefix='/files')

# Initialize file manager
FILES_FOLDER = APP_SETTINGS.USER_DATA_PATH
file_manager = FileStorageManager(base_path=FILES_FOLDER, skip_folders=["__pycache__"])


# Redirect to handle the trailing slash issue
@files_blueprint.route('/')
def files_with_slash():
    """Redirect /files/ to /files"""
    return redirect(url_for('files.files'))


@files_blueprint.route('')
@files_blueprint.route('/folder/<item_id>')
def files(item_id=None):
    """
    File browser - show files and folders.
    
    Args:
        item_id: Optional folder ID to browse into
    """
    structure = file_manager.get_structure()
    items_list = structure['items']
    
    # Get current folder and build breadcrumb path
    current_folder = None
    breadcrumbs = []
    
    if item_id:
        current_folder = next((item for item in items_list if item.id == item_id), None)
        if not current_folder or current_folder.type != 'folder':
            abort(404)
            
        # Build breadcrumbs
        temp_folder = current_folder
        while hasattr(temp_folder, 'parent'):
            parent = next((item for item in items_list if item.id == temp_folder.parent), None)
            if parent:
                breadcrumbs.insert(0, parent)
                temp_folder = parent
            else:
                break
        breadcrumbs.append(current_folder)
    
    # Filter items for current folder
    filtered_items = [
        item for item in items_list 
        if (not item_id and not hasattr(item, 'parent')) or
           (hasattr(item, 'parent') and item.parent == item_id)
    ]
    
    return render_template('files.html', 
                         items=filtered_items, 
                         current_folder=current_folder,
                         breadcrumbs=breadcrumbs)


@files_blueprint.route('/file/<item_id>')
def file_detail(item_id):
    """
    File detail view - show file contents.
    
    Args:
        item_id: File ID to display
    """
    structure = file_manager.get_structure()
    item = next((item for item in structure['items'] if item.id == item_id), None)
    
    if not item or item.type != 'file':
        abort(404)
    
    # Generate breadcrumbs by traversing up through parent folders
    breadcrumbs = []
    if not hasattr(item, 'parent'):
        # If item has no parent, it's in the root folder
        breadcrumbs = [{'id': None, 'name': 'root', 'type': 'folder'}]
    else:
        current = next((i for i in structure['items'] if i.id == item.parent), None)
        while current:
            breadcrumbs.insert(0, current)
            current = next((i for i in structure['items'] if i.id == current.parent), None) if hasattr(current, 'parent') and current.parent else None

    try:
        full_path = Path(FILES_FOLDER) / item.file_path
        print(f"DEBUG: Reading file from {full_path}")
        print(f"DEBUG: File exists: {full_path.exists()}")
        with full_path.open('r', encoding='utf-8') as f:
            content = f.read()
        print(f"DEBUG: Content length: {len(content)}")
        print(f"DEBUG: First 50 chars: {content[:50]}")
        return render_template('files_file_detail.html', item=item, content=content, breadcrumbs=breadcrumbs)
    except Exception as e:
        print(f"Error reading file {item.file_path}: {e}")
        abort(500)


# Export blueprint
__all__ = ['files_blueprint']