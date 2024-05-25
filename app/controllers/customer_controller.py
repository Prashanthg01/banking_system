from flask import jsonify
from app.models.account_model import DepositForm

def deposit_amount(data):
    required_fields = ['name', 'account_number', 'amount', 'ifsc_code']
    for field in required_fields:
        if field not in data:
            return jsonify({"msg": f"Missing {field}"}), 400

    # Create a deposit request with status "pending"
    deposit_request = {
        "name": data['name'],
        "account_number": data['account_number'],
        "amount": int(data['amount']),
        "ifsc_code": data['ifsc_code'],
        "status": "pending"
    }

    DepositForm.create_deposit_request(deposit_request)
    return jsonify({"msg": "Deposit request submitted successfully"}), 201
