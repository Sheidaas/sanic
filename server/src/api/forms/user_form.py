from . import Form
from ...database.models.users import User
from ...utils import get_database, get_config
from ...utils.exceptions import ERROR_CODES
from jwt import decode, InvalidTokenError
from hashlib import md5
from datetime import datetime


class UserTokenLoginForm(Form):

    async def is_valid(self):
        token = self.raw_data.get('token')
        if not token:
            self.errors.append(ERROR_CODES['AUTH-001'])
            return False

        secret_key = get_config().get('KEYS', 'SECRET_KEY')
        try:
            user_data: dict = decode(token, secret_key, algorithms=['HS256'])
        except InvalidTokenError:
            self.errors.append(ERROR_CODES['AUTH-002'])
            return False

        username = user_data.get('username')
        if not username:
            self.errors.append(ERROR_CODES['AUTH-002'])

        due_to = user_data.get('due_to')
        if not due_to:
            self.errors.append(ERROR_CODES['AUTH-002'])
        else:
            try:
                due_to = datetime.fromisoformat(due_to)
            except ValueError:
                self.errors.append(ERROR_CODES['AUTH-002'])
                return False

            if datetime.now() > due_to:
                self.errors.append(ERROR_CODES['AUTH-003'])

        if self.errors:
            return False

        self.cleaned_instance = await get_database().user_manager.get_by_username(username)
        if not self.cleaned_instance:
            raise Exception

        return True


class UserCredentialLoginForm(Form):

    async def is_valid(self):
        username = self.raw_data.get('username')
        password = self.raw_data.get('password')

        if not username or not password:
            self.errors.append(ERROR_CODES['AUTH-001'])
            return False

        self.cleaned_instance = await get_database().user_manager.get_by_username(username)
        if not self.cleaned_instance:
            self.errors.append(ERROR_CODES['AUTH-002'])
            return False

        if md5(password.encode()).hexdigest() != self.cleaned_instance.password:
            self.errors.append(ERROR_CODES['AUTH-002'])
            return False

        return True


class UserRegisterForm(Form):

    async def is_valid(self):
        username: str = self.raw_data.get('username')
        password: str = self.raw_data.get('password')
        email: str = self.raw_data.get('email')

        if not username:
            self.errors.append(ERROR_CODES['REGISTER-000'])
        else:
            if await get_database().user_manager.get_by_username(username):
                self.errors.append(ERROR_CODES['REGISTER-003'])

        if not password:
            self.errors.append(ERROR_CODES['REGISTER-001'])

        if not email:
            self.errors.append(ERROR_CODES['REGISTER-002'])
        else:
            # TODO sprawdzać tutaj stringa pod względem bycia emailem lub nie
            # Aktualnie sprawdzane jest jedynie czy email nie jest pusty - docelowo napis ma być sprawdzony regexem
            pass

        if self.errors:
            return False

        self.cleaned_instance = User()
        self.cleaned_instance.name = username
        self.cleaned_instance.password = md5(password.encode()).hexdigest()
        self.cleaned_instance.email = email
        self.cleaned_instance.is_admin = False
        self.cleaned_instance.premium_end_date = datetime.now()
        return True
