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
    def get_account_by_user(user):
        accounts_collection = mongo.db.accounts
        return accounts_collection.find_one({"name": user})

    @staticmethod
    def get_account_by_form_id(form_id):
        accounts_collection = mongo.db.accounts
        return accounts_collection.find_one({"form_id": form_id})
    
    @staticmethod
    def update_account(account):
        accounts_collection = mongo.db.accounts
        accounts_collection.update_one({"account_number": account['account_number']}, {"$set": account})
    
    @staticmethod
    def update_account_upi_id(user, hashed_upi_id):
        accounts_collection = mongo.db.accounts
        accounts_collection.update_one({"name": user}, {"$set": {"upi_id": hashed_upi_id}})
    
    @staticmethod
    def is_upi_id_taken(upi_id):
        accounts_collection = mongo.db.accounts
        return accounts_collection.find_one({"upi_id": upi_id}) is not None
    
    @staticmethod
    def get_all_accounts():
        return list(mongo.db.accounts.find())

    @staticmethod
    def increment_balance_checks(user):
        accounts_collection = mongo.db.accounts
        account = accounts_collection.find_one({"name": user})
        if account:
            new_balance_checks = account.get("balance_checks", 0) + 1
            accounts_collection.update_one({"name": user}, {"$set": {"balance_checks": new_balance_checks}})
            return True
        return False