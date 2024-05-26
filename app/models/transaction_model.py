from app import mongo

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
    def get_account_number_form_id(form_id):
        deposit_request = mongo.db.deposit_forms.find_one({"form_id": form_id})
        if deposit_request:
            return deposit_request.get('account_number')
        else:
            return None
        
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
    
class withdrawForm:
    @staticmethod
    def create_withdraw_request(data):
        withdraw_forms_collection = mongo.db.withdraw_forms
        withdraw_forms_collection.insert_one(data)
        return True
    
    @staticmethod
    def get_withdraw_requests_by_user(user_id):
        return list(mongo.db.withdraw_forms.find({"name": user_id}))
    
    @staticmethod
    def get_withdraw_request_status_by_account_number(account_num):
        withdraw_request = mongo.db.withdraw_forms.find_one({"account_number": account_num})
        if withdraw_request:
            return withdraw_request.get('status')
        else:
            return None

    @staticmethod
    def get_account_number_form_id(form_id):
        deposit_request = mongo.db.withdraw_forms.find_one({"form_id": form_id})
        if deposit_request:
            return deposit_request.get('account_number')
        else:
            return None

    @staticmethod
    def get_all_withdraw_requests():
        return list(mongo.db.withdraw_forms.find())