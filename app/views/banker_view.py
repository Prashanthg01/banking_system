from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from app.controllers.banker_controller import register_account
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.account_model import DepositForm, Account, withdrawForm
from app import mongo

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
    account = Account.get_account_by_number(account_number)
    if not account:
        return jsonify({"msg": "Account not found"}), 404

    if request.method == 'POST':
        # Update account details
        account['name'] = request.form['name']
        account['phone_number'] = request.form['phone_number']
        account['address'] = request.form['address']
        account['ifsc_code'] = request.form['ifsc_code']
        account['balance'] = float(request.form['balance'])  # Ensure balance is a float

        Account.update_account(account)
        return redirect(url_for('banker.banker_dashboard'))

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
    
    if access_token_cookie:
        all_accounts = Account.get_all_accounts()
        deposit_requests = DepositForm.get_all_deposit_requests()
        withdraw_requests = withdrawForm.get_all_withdraw_requests()
        return render_template('banker/dashboard.html', user_id=current_user, deposit_requests=deposit_requests, all_accounts=all_accounts, withdraw_requests=withdraw_requests)
    else:
        return jsonify({"msg": "Missing access token cookie"}), 401
    
@banker_bp.route('/update_deposit_status/<form_id>/<request_amount>', methods=['POST'])
@jwt_required()
def update_deposit_status(form_id, request_amount):
    # Get the new status from the form data
    new_status = request.form.get('status')
    
    # Update the status of the deposit request in the database
    result = mongo.db.deposit_forms.update_one(
        {"form_id": form_id},
        {"$set": {"status": new_status}}
    )

    if result.matched_count > 0 and result.modified_count > 0:
        # If the status is accepted, update the account balance
        if new_status == "accepted":
            account_num = DepositForm.get_account_number_form_id(form_id)
            account = Account.get_account_by_number(account_num)
            if account:
                new_balance = account.get('balance', 0) + float(request_amount)
                Account.update_account({"account_number": account_num, "balance": new_balance})
                return jsonify({"msg": "Status updated and balance adjusted successfully"}), 200
            else:
                return jsonify({"msg": "Account not found"}), 404
        else:
            return jsonify({"msg": "Status updated successfully"}), 200
    else:
        return jsonify({"msg": "Deposit request not found"}), 404
    
@banker_bp.route('/update_withdraw_status/<form_id>/<request_amount>', methods=['POST'])
@jwt_required()
def update_withdraw_status(form_id, request_amount):
    # Get the new status from the form data
    new_status = request.form.get('status')
    print(form_id)
    print(request_amount)
    
    # Update the status of the deposit request in the database
    result = mongo.db.withdraw_forms.update_one(
        {"form_id": form_id},
        {"$set": {"status": new_status}}
    )

    if result.matched_count > 0 and result.modified_count > 0:
        # If the status is accepted, update the account balance
        if new_status == "success":
            account_num = withdrawForm.get_account_number_form_id(form_id)
            print(account_num)
            account = Account.get_account_by_number(account_num)
            current_balance = account.get('balance', 0)
            print(current_balance)
            if float(request_amount) < float(current_balance):
                if account:
                    new_balance = current_balance - float(request_amount)
                    print(new_balance)
                    Account.update_account({"account_number": account_num, "balance": new_balance})
                    return jsonify({"msg": "Status updated and balance adjusted successfully"}), 200
                else:
                    return jsonify({"msg": "Account not found"}), 404
            else:
                return jsonify({"msg": "Withdraw Amount is greater than current balance"}), 404
        else:
            return jsonify({"msg": "Status updated successfully"}), 200
    else:
        return jsonify({"msg": "Deposit request not found"}), 404