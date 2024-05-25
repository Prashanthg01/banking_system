from app import mongo

class Account:
    @staticmethod
    def create_account(data):
        accounts_collection = mongo.db.accounts
        accounts_collection.insert_one(data)
        return True
