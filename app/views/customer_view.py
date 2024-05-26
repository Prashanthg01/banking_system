from flask import request, jsonify, render_template, Blueprint, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.account_model import Account
from app.models.transaction_model import withdrawForm, DepositForm
from app.models.user_model import User
from werkzeug.security import generate_password_hash, check_password_hash

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

    deposit_requests = deposit_requests + withdraw_requests if withdraw_requests else deposit_requests
    if access_token_cookie:
        if deposit_requests:
            return render_template('customer/dashboard.html', user_id=current_user, current_user_account_details=current_user_account_details, deposit_requests=deposit_requests)
        else:
            return render_template('customer/dashboard.html', user_id=current_user, current_user_account_details=current_user_account_details)
    else:
        return jsonify({"msg": "Missing access token cookie"}), 401

@customer_bp.route('/check_balance', methods=['GET', 'POST'])
@jwt_required()
def check_balance():
    current_user = get_jwt_identity()
    account = Account.get_account_by_user(current_user)
    
    if request.method == 'POST':
        if 'upi_id' in request.form:
            upi_id = request.form['upi_id']
            if account and 'upi_id' in account:
                if check_password_hash(account['upi_id'], upi_id):
                    # Increment the balance_checks field
                    Account.increment_balance_checks(current_user)
                    return jsonify({"balance": account['balance']}), 200
                else:
                    return jsonify({"msg": "UPI ID does not match"}), 400
            else:
                return redirect(url_for('customer.check_balance', action="create"))

        elif 'new_upi_id' in request.form and 'reenter_upi_id' in request.form:
            upi_id = request.form['new_upi_id']
            reenter_upi_id = request.form['reenter_upi_id']
            if upi_id == reenter_upi_id and len(upi_id) == 6 and upi_id.isdigit():
                if Account.is_upi_id_taken(upi_id):
                    return jsonify({"msg": "UPI ID is already registered"}), 400
                hashed_upi_id = generate_password_hash(upi_id)
                Account.update_account_upi_id(current_user, hashed_upi_id)
                return jsonify({"msg": "UPI ID created successfully"}), 201
            else:
                return jsonify({"msg": "UPI ID does not match or is not valid"}), 400

    
    action = "check" if 'upi_id' in account else "create"
    return render_template('customer/check_balance.html', action=action)