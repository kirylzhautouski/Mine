from app import mongo, bcrypt


class ValidationError(Exception):
    pass


class User:

    def __init__(self, email, login, password, is_active=True):
        User.validate_email(email)
        User.validate_login(login)
        User.validate_password(password)

        self.id = None

        self.email = email
        self.login = login

        self.hashed_password = bcrypt.generate_password_hash(password).decode()

        self.is_active = is_active

    def save(self):
        result = mongo.db.users.insert_one({
            'email': self.email,
            'login': self.login,
            'hashed_password': self.hashed_password,
            'is_active': self.is_active,
        })

        self.id = str(result.inserted_id)

    @staticmethod
    def validate_email(email):
        if not email:
            raise ValidationError('Email should not be empty.')

        if mongo.db.users.find_one({'email': email}):
            raise ValidationError('Email already exists.')

    @staticmethod
    def validate_login(login):
        if not login:
            raise ValidationError('Login should not be empty.')

        if mongo.db.users.find_one({'login': login}):
            raise ValidationError('Login already exists.')

    @staticmethod
    def validate_password(password):
        if not password:
            raise ValidationError('Password should not be empty.')
