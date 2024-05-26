from flask import request, jsonify, render_template, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.transaction_controller import deposit_amount, withdraw_amount
from app.models.transaction_model import DepositForm, withdrawForm
from app import mongo
from app.models.account_model import Account

transaction_bp = Blueprint('transactions', __name__)

@transaction_bp.route('/deposit', methods=['GET', 'POST'])
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
    
@transaction_bp.route('/withdraw', methods=['GET', 'POST'])
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


@transaction_bp.route('/update_deposit_status/<form_id>/<request_amount>', methods=['POST'])
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
    
@transaction_bp.route('/update_withdraw_status/<form_id>/<request_amount>', methods=['POST'])
@jwt_required()
def update_withdraw_status(form_id, request_amount):
    new_status = request.form.get('status')
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