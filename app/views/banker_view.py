from flask import Blueprint, request, render_template, redirect, url_for
from app.controllers.banker_controller import register_account
from flask_jwt_extended import jwt_required

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
