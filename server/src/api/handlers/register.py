import datetime
import hashlib
from sanic import Sanic
from sanic.views import HTTPMethodView
from sanic.request import Request
from sanic.response import json, HTTPResponse
from ...database.models.users import User


class Register(HTTPMethodView):

    def __init__(self) -> None:
        super().__init__()
        app = Sanic.get_app()
        self.config = app.ctx.get('CONFIG')
        self.database = app.ctx.get('DATABASE')

    async def post(self, request: Request):
        if not request.json:
            return HTTPResponse(status=400)

        new_user = self.can_register(request.json)
        if not new_user:
            return HTTPResponse(status=400)
        return json({'token': new_user.get_token()})

    def can_register(self, credentials: dict):
        username = credentials.get('username')
        password = credentials.get('password')
        email = credentials.get('email')

        if not username or not password or not email:
            return False

        if self.database.user_manager.get_by_username(username):
            return False

        new_user = User()
        new_user.name = username
        new_user.password = hashlib.md5(password.encode()).hexdigest()
        new_user.email = email
        new_user.is_admin = False
        new_user.premium_end_date = datetime.datetime.now()

        self.database.user_manager.insert(new_user)

        return new_user



