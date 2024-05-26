from app.models.account_model import Account
from app.models.user_model import User
from app.models.transaction_model import DepositForm, withdrawForm
from werkzeug.security import generate_password_hash, check_password_hash

def get_current_user_account_details(user_id):
    user = User.get_user_by_user_id(user_id)
    account_number = user.account_num if user else None
    return Account.get_account_by_number(account_number)

def get_deposit_requests(user_id):
    deposit_requests = DepositForm.get_deposit_requests_by_user(user_id)
    withdraw_requests = withdrawForm.get_withdraw_requests_by_user(user_id)
    return deposit_requests + withdraw_requests if withdraw_requests else deposit_requests

def check_upi_id(account, upi_id):
    if account and 'upi_id' in account and check_password_hash(account['upi_id'], upi_id):
        Account.increment_balance_checks(account['account_number'])
        return account['balance']
    return None

def is_upi_id_taken(upi_id):
    return Account.is_upi_id_taken(upi_id)

def update_account_upi_id(user_id, upi_id):
    hashed_upi_id = generate_password_hash(upi_id)
    Account.update_account_upi_id(user_id, hashed_upi_id)
