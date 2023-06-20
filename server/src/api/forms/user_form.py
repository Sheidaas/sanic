from . import Form
from ...database.models.users import User
from ...utils import get_database, decode_jwt
from ...utils.dictionaries import ERROR_CODES, FIELD_NAMES
from hashlib import md5
from datetime import datetime


class UserTokenLoginForm(Form):

    async def is_valid(self):
        token = self.raw_data.get(FIELD_NAMES['TOKEN'])
        if not token:
            self.errors.append(ERROR_CODES['AUTH-001'])
            return False

        user_data = decode_jwt(token)
        if not user_data:
            self.errors.append(ERROR_CODES['AUTH-002'])
            return False

        username = user_data.get(FIELD_NAMES['USERNAME'])
        if not username:
            self.errors.append(ERROR_CODES['AUTH-002'])

        due_to = user_data.get(FIELD_NAMES['TOKEN_EXPIRATION_DATE'])
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
        username = self.raw_data.get(FIELD_NAMES['USERNAME'])
        password = self.raw_data.get(FIELD_NAMES['PASSWORD'])

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
        username: str = self.raw_data.get(FIELD_NAMES['USERNAME'])
        password: str = self.raw_data.get(FIELD_NAMES['PASSWORD'])
        email: str = self.raw_data.get(FIELD_NAMES['EMAIL'])

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
            # TODO: sprawdzać tutaj stringa pod względem bycia emailem lub nie
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
