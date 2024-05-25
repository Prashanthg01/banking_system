from flask import jsonify
from app import mongo, bcrypt
from flask_jwt_extended import create_access_token, set_access_cookies, create_refresh_token
from app.models.user_model import User
from pymongo.errors import DuplicateKeyError

def register_user(data):
    if not data.get('account_num') or not data.get('user_id') or not data.get('password'):
        return jsonify({"msg": "Missing required fields"}), 400

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    user = User(
        account_num=data['account_num'],
        user_id=data['user_id'],
        password=hashed_password
    )

    try:
        mongo.db.users.insert_one(user.to_dict())
    except DuplicateKeyError:
        return jsonify({"msg": "User ID already exists"}), 400

    return jsonify({"msg": "User registered successfully"}), 201

def login_user(data):
    if not data.get('user_id') or not data.get('password'):
        return jsonify({"msg": "Missing required fields"}), 400

    user = mongo.db.users.find_one({"user_id": data['user_id']})

    if user and bcrypt.check_password_hash(user['password'], data['password']):
        access_token = create_access_token(identity=data['user_id'])
        refresh_token = create_refresh_token(identity=user['user_id'])
        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200
    else:
        return jsonify({"msg": "Invalid user ID or password"}), 401
