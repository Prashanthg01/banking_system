from flask import request, jsonify, render_template, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers import customer_controller

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/dashboard')
@jwt_required()
def customer_dashboard():
    current_user = get_jwt_identity()
    current_user_account_details = customer_controller.get_current_user_account_details(current_user)
    access_token_cookie = request.cookies.get('access_token_cookie')
    
    deposit_requests = customer_controller.get_deposit_requests(current_user)

    if access_token_cookie:
        return render_template(
            'customer/dashboard.html',
            user_id=current_user,
            current_user_account_details=current_user_account_details,
            deposit_requests=deposit_requests
        )
    else:
        return jsonify({"msg": "Missing access token cookie"}), 401

@customer_bp.route('/check_balance', methods=['GET', 'POST'])
@jwt_required()
def check_balance():
    current_user = get_jwt_identity()
    account = customer_controller.get_current_user_account_details(current_user)
    
    if request.method == 'POST':
        if 'upi_id' in request.form:
            upi_id = request.form['upi_id']
            balance = customer_controller.check_upi_id(account, upi_id)
            if balance is not None:
                return jsonify({"balance": balance}), 200
            else:
                return jsonify({"msg": "UPI ID does not match"}), 400
        elif 'new_upi_id' in request.form and 'reenter_upi_id' in request.form:
            upi_id = request.form['new_upi_id']
            reenter_upi_id = request.form['reenter_upi_id']
            if upi_id == reenter_upi_id and len(upi_id) == 6 and upi_id.isdigit():
                if customer_controller.is_upi_id_taken(upi_id):
                    return jsonify({"msg": "UPI ID is already registered"}), 400
                customer_controller.update_account_upi_id(current_user, upi_id)
                return jsonify({"msg": "UPI ID created successfully"}), 201
            else:
                return jsonify({"msg": "UPI ID does not match or is not valid"}), 400
    
    action = "check" if 'upi_id' in account else "create"
    return render_template('customer/check_balance.html', action=action)