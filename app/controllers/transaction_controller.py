from flask import jsonify
from app.models.transaction_model import DepositForm, withdrawForm
from datetime import datetime
from app.utils.customer_utils import generate_unique_id

def deposit_amount(data):
    unique_id = generate_unique_id()
    required_fields = ['name', 'account_number', 'amount', 'ifsc_code']
    for field in required_fields:
        if field not in data:
            return jsonify({"msg": f"Missing {field}"}), 400

    # Get the current date and time
    current_date = datetime.now().strftime('%Y-%m-%d')
    current_time = datetime.now().strftime('%H:%M:%S')

    # Create a deposit request with status "pending"
    deposit_request = {
        "name": data['name'],
        "account_number": data['account_number'],
        "amount": int(data['amount']),
        "ifsc_code": data['ifsc_code'],
        "status": "pending",
        "date": current_date,
        "time": current_time,
        "form_type": "deposit",
        'form_id': unique_id
    }

    DepositForm.create_deposit_request(deposit_request)
    return jsonify({"msg": "Deposit request submitted successfully"}), 201

def withdraw_amount(data):
    unique_id = generate_unique_id()
    required_fields = ['name', 'account_number', 'amount', 'ifsc_code']
    for field in required_fields:
        if field not in data:
            return jsonify({"msg": f"Missing {field}"}), 400

    # Get the current date and time
    current_date = datetime.now().strftime('%Y-%m-%d')
    current_time = datetime.now().strftime('%H:%M:%S')

    # Create a withdraw request with status "pending"
    withdraw_request = {
        "name": data['name'],
        "account_number": data['account_number'],
        "amount": int(data['amount']),
        "ifsc_code": data['ifsc_code'],
        "status": "pending",
        "date": current_date,
        "time": current_time,
        "form_type": "withdraw",
        'form_id': unique_id
    }

    withdrawForm.create_withdraw_request(withdraw_request)
    return jsonify({"msg": "withdraw request submitted successfully"}), 201
