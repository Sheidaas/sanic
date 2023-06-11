from . import Form
from ...utils import ERRORS
from sanic import Sanic


class UserForm(Form):

    def is_valid(self, credentials):
        username = credentials.get('username')
        password = credentials.get('password')
        email = credentials.get('email')

        if not username:
            self.errors.append(ERRORS['REGISTER-000'])
        else:
            app = Sanic.get_app()
            if app.ctx.get('DATABASE').user_manager.get_by_username(username):
                self.errors.append(ERRORS['REGISTER-003'])

        if not password:
            self.errors.append(ERRORS['REGISTER-001'])

        if not email:
            self.errors.append(ERRORS['REGISTER-002'])

        if self.errors:
            return False
        return True
