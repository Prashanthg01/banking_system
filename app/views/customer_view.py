from flask import request, jsonify, render_template, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/dashboard')
@jwt_required()
def customer_dashboard():
    current_user = get_jwt_identity()
    access_token_cookie = request.cookies.get('access_token_cookie')
    if access_token_cookie:
        return render_template('customer/dashboard.html', user_id=current_user)
    else:
        return jsonify({"msg": "Missing access token cookie"}), 401