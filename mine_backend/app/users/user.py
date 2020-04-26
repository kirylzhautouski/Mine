from app import mongo


class User:

    def __init__(self, email, login, is_active=True):
        self.email = email
        self.login = login

        self.is_active = is_active

    def set_password(password):
        pass

    def check_password(password):
        pass

    @staticmethod
    def validate_email(email):
        pass

    @staticmethod
    def validate_login(login):
        pass
