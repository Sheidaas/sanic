import jwt
import hashlib
from ...utils import ERRORS
from sanic import Sanic
from sanic.views import HTTPMethodView
from sanic.request import Request
from sanic.response import json, HTTPResponse


class Login(HTTPMethodView):

    def __init__(self) -> None:
        super().__init__()
        app = Sanic.get_app()
        self.config = app.ctx.get('CONFIG')
        self.database = app.ctx.get('DATABASE')

    async def get(self, request: Request):
        if not request.token:
            return HTTPResponse(body=[
                ERRORS['AUTH-000']
            ], status=400)
        is_valid = self.validate_token(request.token)
        if not is_valid:
            return HTTPResponse(body=[
                ERRORS['AUTH-001']
                ], status=401)
        return json({'token': request.token})

    async def post(self, request: Request):
        if not request.json:
            return HTTPResponse(body=[
                ERRORS['AUTH-000']
                ], status=400)

        is_valid = self.validate_credentials(request.json)
        if not is_valid:
            return HTTPResponse(body=[
                ERRORS['AUTH-001']
                ], status=401)
        return json({'token': is_valid})

    def validate_token(self, token: str):
        secret_key = self.config.get('KEYS', 'SECRET_KEY')
        try:
            user_data = jwt.decode(token, secret_key, algorithms=['HS256'])
        except jwt.InvalidTokenError:
            return False

        username = user_data.get('username')
        if not username:
            return False

        cleaned_instance = self.database.user_manager.get_by_username(username)
        if not cleaned_instance:
            return False

        if cleaned_instance.get_token() != token:
            return False

        return True

    def validate_credentials(self, json_dict: dict):
        username = json_dict.get('username')
        password = json_dict.get('password')

        if not username or not password:
            return False
        
        database_user = self.database.user_manager.get_by_username(username)
        if not database_user:
            return False

        if hashlib.md5(password.encode()).hexdigest() != database_user.password:
            return False

        return database_user.get_token()

