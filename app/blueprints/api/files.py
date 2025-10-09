"""
Files API Blueprint - File CRUD endpoints (placeholder)

This blueprint handles file-related API routes:
- Future file CRUD operations (/api/files/*)

Currently placeholder - to be implemented in future.
"""

from flask import Blueprint, jsonify

# Create files API blueprint
files_api_blueprint = Blueprint('files_api', __name__, url_prefix='/api/files')


@files_api_blueprint.route('/', methods=['GET'])
def placeholder():
    """Placeholder endpoint for future file CRUD API."""
    return jsonify({
        "status": "not_implemented",
        "message": "File CRUD API endpoints will be implemented in the future"
    }), 501


# Export blueprint
__all__ = ['files_api_blueprint']