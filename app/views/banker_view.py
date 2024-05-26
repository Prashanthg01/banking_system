from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from app.controllers.banker_controller import register_account
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.transaction_model import DepositForm, withdrawForm
from app.models.account_model import Account
from app import mongo
from app.controllers import banker_controller

banker_bp = Blueprint('banker', __name__)

@banker_bp.route('/register_account', methods=['GET', 'POST'])
# @jwt_required()
def register_account_view():
    if request.method == 'POST':
        data = request.form.to_dict()
        response, status = register_account(data)
        if status == 201:
            return redirect(url_for('banker.register_account_view'))
        else:
            return render_template('register_account.html', error=response.json['msg'])
    return render_template('register_account.html')

@banker_bp.route('/edit_account/<account_number>', methods=['GET', 'POST'])
@jwt_required()
def edit_account(account_number):
    if request.method == 'POST':
        data = request.form.to_dict()
        response, status = banker_controller.update_account_details(account_number, data)
        if status == 200:
            return redirect(url_for('banker.banker_dashboard'))
        else:
            return jsonify(response), status

    account = banker_controller.get_account_by_number(account_number)
    if not account:
        return jsonify({"msg": "Account not found"}), 404

    return render_template('banker/edit_account.html', account=account)

@banker_bp.route('/delete_account/<account_number>', methods=['POST'])
@jwt_required()
def delete_account(account_number):
    account = Account.get_account_by_number(account_number)
    if account:
        mongo.db.accounts.delete_one({"account_number": account_number})
        return redirect(url_for('banker.banker_dashboard'))
    else:
        return jsonify({"msg": "Account not found"}), 404

@banker_bp.route('/dashboard')
@jwt_required()
def banker_dashboard():
    current_user = get_jwt_identity()
    access_token_cookie = request.cookies.get('access_token_cookie')
    
    deposit_requests = DepositForm.get_all_deposit_requests()
    withdraw_requests = withdrawForm.get_all_withdraw_requests()
    deposit_and_withdraw_history = deposit_requests + withdraw_requests if withdraw_requests else deposit_requests
    deposit_and_withdraw_history.sort(key=lambda x: (x['date'], x['time']))
    
    if access_token_cookie:
        all_accounts = Account.get_all_accounts()
        deposit_requests = DepositForm.get_all_deposit_requests()
        withdraw_requests = withdrawForm.get_all_withdraw_requests()
        return render_template('banker/dashboard.html', user_id=current_user, deposit_requests=deposit_requests, all_accounts=all_accounts, withdraw_requests=withdraw_requests, deposit_and_withdraw_history=deposit_and_withdraw_history)
    else:
        return jsonify({"msg": "Missing access token cookie"}), 401