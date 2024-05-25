from flask import jsonify, request
from app.models.account_model import Account

def register_account(data):
    required_fields = ['name', 'phone_number', 'address', 'gender', 'account_number', 'ifsc_code']
    for field in required_fields:
        if field not in data:
            return jsonify({"msg": f"Missing {field}"}), 400
    
    Account.create_account(data)
    return jsonify({"msg": "Account successfully registered"}), 201
