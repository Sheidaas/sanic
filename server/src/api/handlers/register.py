import datetime
import hashlib
from ..forms.user_form import UserForm
from sanic import Sanic
from sanic.views import HTTPMethodView
from sanic.request import Request
from sanic.response import json, HTTPResponse
from ...database.models.users import User
from ...utils import ERRORS


class Register(HTTPMethodView):

    def __init__(self) -> None:
        super().__init__()
        app = Sanic.get_app()
        self.config = app.ctx.get('CONFIG')
        self.database = app.ctx.get('DATABASE')

    async def post(self, request: Request):
        if not request.json:
            return HTTPResponse(body=[
                ERRORS['AUTH-000']
            ], status=400)
        user_form = UserForm()
        if not user_form.is_valid(request.json):
            return HTTPResponse(body=user_form.errors, status=401)
        new_user = self.register(request.json)
        return json({'token': new_user.get_token()})

    def register(self, credentials: dict):
        new_user = User()
        new_user.name = credentials.get('username')
        new_user.password = hashlib.md5(credentials.get('password').encode()).hexdigest()
        new_user.email = credentials.get('email')
        new_user.is_admin = False
        new_user.premium_end_date = datetime.datetime.now()
        self.database.user_manager.insert(new_user)
        return new_user



