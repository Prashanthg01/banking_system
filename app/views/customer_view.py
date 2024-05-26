from flask import request, jsonify, render_template, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.customer_controller import deposit_amount, withdraw_amount
from app.models.account_model import DepositForm, Account, withdrawForm
from app.models.user_model import User

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/dashboard')
@jwt_required()
def customer_dashboard():
    current_user = get_jwt_identity()
    current_user_object = User.get_user_by_user_id(current_user)
    current_user_account_number = current_user_object.account_num if current_user_object else None
    current_user_account_details = Account.get_account_by_number(current_user_account_number)
    access_token_cookie = request.cookies.get('access_token_cookie')
    
    deposit_requests = DepositForm.get_deposit_requests_by_user(current_user)
    withdraw_requests = withdrawForm.get_withdraw_requests_by_user(current_user)
    deposit_requests.append(withdraw_requests[0]) if withdraw_requests else deposit_requests
    if access_token_cookie:
        if deposit_requests:
            return render_template('customer/dashboard.html', user_id=current_user, current_user_account_details=current_user_account_details, deposit_requests=deposit_requests)
        else:
            return render_template('customer/dashboard.html', user_id=current_user, current_user_account_details=current_user_account_details)
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
        return render_template('customer/deposit.html', deposit_requests=deposit_requests, form_type="deposit")
    else:
        return render_template('customer/deposit.html', msg="No deposit requests found", form_type="deposit")
    
@customer_bp.route('/withdraw', methods=['GET', 'POST'])
@jwt_required()
def withdraw():
    if request.method == 'POST':
        data = request.form.to_dict()
        response, status = withdraw_amount(data)
        if status == 200:
            return jsonify({"msg": "withdraw successful"}), 200
        else:
            return jsonify({"msg": response.json['msg']}), status
        
    current_user = get_jwt_identity()
    withdraw_requests = withdrawForm.get_withdraw_requests_by_user(current_user)
    if withdraw_requests:
        return render_template('customer/deposit.html', withdraw_requests=withdraw_requests, form_type="withdraw")
    else:
        return render_template('customer/deposit.html', msg="No withdraw requests found", form_type="withdraw")