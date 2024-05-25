from flask import Blueprint, request, jsonify, render_template, redirect, url_for, make_response
from app.controllers.auth_controller import register_user, login_user
from flask_jwt_extended import jwt_required, unset_jwt_cookies, get_jwt_identity, create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form.to_dict()
        response, status = register_user(data)
        if status == 201:
            return redirect(url_for('auth.login'))
        else:
            return render_template('register.html', error=response.json['msg'])
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form.to_dict()
        response, status = login_user(data)
        if status == 200:
            access_token = response.json['access_token']
            refresh_token = response.json['refresh_token']
            role = response.json['role']
            
            resp = make_response(redirect(url_for('customer.customer_dashboard') if role == 'customer' else url_for('banker.banker_dashboard')))
            resp.set_cookie('access_token_cookie', access_token, httponly=True)
            resp.set_cookie('refresh_token_cookie', refresh_token, httponly=True)
            return resp
        else:
            return render_template('login.html', error=response.json['msg'])
    return render_template('login.html')

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = jsonify({"msg": "Logout successful"})
    unset_jwt_cookies(response)
    return response, 200

@auth_bp.route('/token/refresh', methods=['POST'])
def refresh():
    refresh_token = request.cookies.get('refresh_token')
    if refresh_token:
        new_access_token = create_access_token(identity=get_jwt_identity())
        resp = make_response(jsonify({'access_token': new_access_token}), 200)
        resp.set_cookie('access_token', new_access_token, httponly=True)
        return resp
    else:
        return jsonify({"msg": "Missing refresh token"}), 401
