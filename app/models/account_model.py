from app import mongo

class Account:
    @staticmethod
    def create_account(data):
        data['balance'] = 0
        accounts_collection = mongo.db.accounts
        accounts_collection.insert_one(data)
        return True

    @staticmethod
    def get_account_by_number(account_number):
        accounts_collection = mongo.db.accounts
        return accounts_collection.find_one({"account_number": account_number})

    @staticmethod
    def update_account(account):
        accounts_collection = mongo.db.accounts
        accounts_collection.update_one({"account_number": account['account_number']}, {"$set": account})

class DepositForm:
    @staticmethod
    def create_deposit_request(data):
        deposit_forms_collection = mongo.db.deposit_forms
        deposit_forms_collection.insert_one(data)
        return True
    
    @staticmethod
    def get_deposit_requests_by_user(user_id):
        return list(mongo.db.deposit_forms.find({"name": user_id}))
    
    @staticmethod
    def get_deposit_request_status_by_account_number(account_num):
        deposit_request = mongo.db.deposit_forms.find_one({"account_number": account_num})
        if deposit_request:
            return deposit_request.get('status')
        else:
            return None

    @staticmethod
    def get_all_deposit_requests():
        return list(mongo.db.deposit_forms.find())