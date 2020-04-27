from flask_jwt_extended import create_access_token, create_refresh_token
from flask_pymongo import ObjectId

from app import mongo, bcrypt, jwt


class PasswordNotSetError(Exception):
    pass


class UserNotSavedError(Exception):
    pass


class ValidationError(Exception):
    pass


class User:

    def __init__(self, email, login, is_active=True):
        self.id = None

        self.email = email
        self.login = login

        self.hashed_password = None

        self.is_active = is_active

    def set_password(self, password, hashed=False):
        if not hashed:
            User.validate_password(password)
            self.hashed_password = bcrypt.generate_password_hash(password).decode()
        else:
            self.hashed_password = password

    def check_password(self, password):
        if not self.hashed_password:
            raise PasswordNotSetError('You should set password with set_password() before calling check_password().')

        return bcrypt.check_password_hash(self.hashed_password, password)

    def save(self):
        if not self.hashed_password:
            raise PasswordNotSetError('You should set password with set_password() before calling save().')

        User.validate_email(self.email)
        User.validate_login(self.login)

        result = mongo.db.users.insert_one({
            'email': self.email,
            'login': self.login,
            'hashed_password': self.hashed_password,
            'is_active': self.is_active,
        })

        self.id = str(result.inserted_id)

    def generate_tokens(self):
        if not self.id:
            raise UserNotSavedError('You should save() user before generating tokens.')

        access_token = create_access_token(identity=self.id, fresh=True)
        refresh_token = create_refresh_token(self.id)

        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
        }

    @classmethod
    def get_user_by_login(cls, login):
        result = mongo.db.users.find_one({'login': login})
        if result:
            user = cls(result['email'], result['login'])
            user.id = str(result['_id'])
            user.set_password(result['hashed_password'], hashed=True)

            return user

        return None

    @classmethod
    def get_user_by_id(cls, id):
        result = mongo.db.users.find_one(ObjectId(id))
        if result:
            user = cls(result['email'], result['login'])
            user.id = str(result['_id'])
            user.set_password(result['hashed_password'], hashed=True)

            return user

        return None

    @staticmethod
    def validate_email(email):
        if mongo.db.users.find_one({'email': email}):
            raise ValidationError('Email already exists.')

    @staticmethod
    def validate_login(login):
        if mongo.db.users.find_one({'login': login}):
            raise ValidationError('Login already exists.')

    @staticmethod
    def validate_password(password):
        pass


@jwt.user_loader_callback_loader
def retrieve_user(identity):
    return User.get_user_by_id(identity)
