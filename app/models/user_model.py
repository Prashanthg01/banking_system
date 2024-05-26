from app import mongo

class User:
    def __init__(self, account_num, user_id, password, role="customer"):
        self.account_num = account_num
        self.user_id = user_id
        self.password = password
        self.role = role

    def to_dict(self):
        return {
            "account_num": self.account_num,
            "user_id": self.user_id,
            "password": self.password,
            "role": self.role
        }
        
    @staticmethod
    def get_user_by_user_id(user_id):
        user_data = mongo.db.users.find_one({"user_id": user_id})
        if user_data:
            return User(user_data['account_num'], user_data['user_id'], user_data['password'], user_data['role'])
        return None
