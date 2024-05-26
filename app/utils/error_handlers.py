from flask import jsonify
from werkzeug.exceptions import HTTPException
from flask import Blueprint, jsonify

error_handlers_bp = Blueprint('error_handlers', __name__)

@error_handlers_bp.app_errorhandler(400)
def bad_request(error):
    response = jsonify({"error": "Bad Request", "message": str(error)})
    response.status_code = 400
    return response

@error_handlers_bp.app_errorhandler(401)
def unauthorized(error):
    response = jsonify({"error": "Unauthorized", "message": str(error)})
    response.status_code = 401
    return response

@error_handlers_bp.app_errorhandler(403)
def forbidden(error):
    response = jsonify({"error": "Forbidden", "message": str(error)})
    response.status_code = 403
    return response

@error_handlers_bp.app_errorhandler(404)
def not_found(error):
    response = jsonify({"error": "Not Found", "message": str(error)})
    response.status_code = 404
    return response

@error_handlers_bp.app_errorhandler(500)
def internal_server_error(error):
    response = jsonify({"error": "Internal Server Error", "message": str(error)})
    response.status_code = 500
    return response
