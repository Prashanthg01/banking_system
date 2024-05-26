from flask import jsonify, request
from app.models.account_model import Account

def register_account(data):
    required_fields = ['name', 'phone_number', 'address', 'gender', 'account_number', 'ifsc_code']
    for field in required_fields:
        if field not in data:
            return jsonify({"msg": f"Missing {field}"}), 400

    if 'balance' not in data:
        data['balance'] = 0
        
    Account.create_account(data)
    return jsonify({"msg": "Account successfully registered"}), 201

def get_account_by_number(account_number):
    return Account.get_account_by_number(account_number)

def update_account_details(account_number, data):
    account = Account.get_account_by_number(account_number)
    if not account:
        return {"msg": "Account not found"}, 404

    # Update account details
    account['name'] = data.get('name', account['name'])
    account['phone_number'] = data.get('phone_number', account['phone_number'])
    account['address'] = data.get('address', account['address'])
    account['ifsc_code'] = data.get('ifsc_code', account['ifsc_code'])
    account['balance'] = float(data.get('balance', account['balance']))  # Ensure balance is a float

    Account.update_account(account)
    return {"msg": "Account updated successfully"}, 200