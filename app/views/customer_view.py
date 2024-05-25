from flask import request, jsonify, render_template, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.customer_controller import deposit_amount
from app.models.account_model import DepositForm 

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

@customer_bp.route('/deposit', methods=['GET', 'POST'])
@jwt_required()
def deposit():
    if request.method == 'POST':
        data = request.form.to_dict()
        response, status = deposit_amount(data)
        if status == 200:
            return jsonify({"msg": "Deposit successful"}), 200
        else:
            return jsonify({"msg": response.json['msg']}), status
        
    current_user = get_jwt_identity()
    deposit_requests = DepositForm.get_deposit_requests_by_user(current_user)
    if deposit_requests:
        return render_template('customer/deposit.html', deposit_requests=deposit_requests)
    else:
        return render_template('customer/deposit.html', msg="No deposit requests found")