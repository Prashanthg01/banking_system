class User:
    def __init__(self, account_num, user_id, password):
        self.account_num = account_num
        self.user_id = user_id
        self.password = password

    def to_dict(self):
        return {
            "account_num": self.account_num,
            "user_id": self.user_id,
            "password": self.password
        }
