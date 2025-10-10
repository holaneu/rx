"""
Tools API Blueprint - Tools testing endpoints

This blueprint handles tool-related API routes:
- Test tools (/api/tools/test)

Separated for focused tools API functionality.
"""

from flask import Blueprint, request, jsonify
from app.utils.response_types import ResponseKey, ResponseStatus

# Create tools API blueprint
tools_api_blueprint = Blueprint('tools_api', __name__, url_prefix='/api')


@tools_api_blueprint.route('/tools/test', methods=['POST'])
def test_tools():
    """Test endpoint for tool functionality."""
    try:
        data = request.json
        input_message = data.get("message", "")
        if not input_message:
            return jsonify({
                ResponseKey.STATUS.value: ResponseStatus.ERROR.value, 
                ResponseKey.ERROR.value: "No input",
                ResponseKey.DATA.value: "No input",
                ResponseKey.MESSAGE.value: {
                    ResponseKey.TITLE.value: ResponseStatus.ERROR.value,
                    ResponseKey.BODY.value: f"No input"
                } 
            }), 400
        return jsonify({
            ResponseKey.STATUS.value: ResponseStatus.SUCCESS.value, 
            ResponseKey.DATA.value: input_message + " - from test endpoint",
            ResponseKey.MESSAGE.value: {
                ResponseKey.TITLE.value: ResponseStatus.SUCCESS.value,
                ResponseKey.BODY.value: f"Message processed"
            } 
        }), 200
    except Exception as e:
        return jsonify({
            ResponseKey.STATUS.value: ResponseStatus.ERROR.value, 
            ResponseKey.ERROR.value: str(e),
            ResponseKey.MESSAGE.value: {
                ResponseKey.TITLE.value: ResponseStatus.ERROR.value,
                ResponseKey.BODY.value: f"Error: {str(e)}"
            } 
        }), 500


# Export blueprint
__all__ = ['tools_api_blueprint']