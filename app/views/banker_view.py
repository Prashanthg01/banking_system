from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from app.controllers.banker_controller import register_account
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.account_model import DepositForm 
from app import mongo

banker_bp = Blueprint('banker', __name__)

@banker_bp.route('/register_account', methods=['GET', 'POST'])
@jwt_required()
def register_account_view():
    if request.method == 'POST':
        data = request.form.to_dict()
        response, status = register_account(data)
        if status == 201:
            return redirect(url_for('banker.register_account_view'))
        else:
            return render_template('register_account.html', error=response.json['msg'])
    return render_template('register_account.html')

@banker_bp.route('/dashboard')
@jwt_required()
def banker_dashboard():
    current_user = get_jwt_identity()
    access_token_cookie = request.cookies.get('access_token_cookie')
    
    if access_token_cookie:
        deposit_requests = DepositForm.get_all_deposit_requests()
        return render_template('banker/dashboard.html', user_id=current_user, deposit_requests=deposit_requests)
    else:
        return jsonify({"msg": "Missing access token cookie"}), 401
    
@banker_bp.route('/update_status/<request_account_num>', methods=['POST'])
@jwt_required()
def update_status(request_account_num):
    # Get the new status from the form data
    new_status = request.form.get('status')
    print("request_id", request_account_num)
    print("new_status", new_status)

    # Update the status of the deposit request in the database
    result = mongo.db.deposit_forms.update_one(
        {"account_number": request_account_num},
        {"$set": {"status": new_status}}
    )

    if result.modified_count > 0:
        return jsonify({"msg": "Status updated successfully"}), 200
    else:
        return jsonify({"msg": "Deposit request not found"}), 404