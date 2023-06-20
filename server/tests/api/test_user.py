import pytest
from sanic import Sanic
from src.utils.dictionaries import FIELD_NAMES, ERROR_CODES
from helpers import create_user, get_user


USER_DATA = {
    FIELD_NAMES['USERNAME']: 'Sheida',
    FIELD_NAMES['PASSWORD']: 'admin',
    FIELD_NAMES['EMAIL']: 'maciejwrzeszcz1@wp.pl',
}


class TestUserPost:

    @pytest.mark.usefixtures('app')
    @pytest.mark.asyncio
    async def test_can_create_user(self, app: Sanic):
        request, response = await create_user(app, USER_DATA)
        assert response.status_code == 201
        assert response.json.get(FIELD_NAMES['TOKEN'])

    @pytest.mark.usefixtures('app')
    @pytest.mark.asyncio
    async def test_can_create_user_with_the_same_name(self, app: Sanic):
        request, response = await create_user(app, USER_DATA)
        assert response.status_code == 201
        assert response.json.get(FIELD_NAMES['TOKEN'])

        request, response = await create_user(app, USER_DATA)
        errors_list = response.json.get('errors')

        assert response.status_code == 400
        assert len(errors_list) == 1
        assert errors_list[0]['error'] == ERROR_CODES['REGISTER-003']['error']  # Username is already taken error

    @pytest.mark.usefixtures('app')
    @pytest.mark.asyncio
    async def test_can_create_user_without_credentials(self, app: Sanic):
        empty_user_data = {}
        request, response = await create_user(app, empty_user_data)
        errors_list = response.json.get('errors')
        errors_codes_keys = [
            ERROR_CODES['REGISTER-000']['error'],  # Empty username error
            ERROR_CODES['REGISTER-001']['error'],  # Empty password error
            ERROR_CODES['REGISTER-002']['error']   # Empty email error
        ]

        assert response.status_code == 400
        assert len(errors_list) == 3
        for error in errors_list:
            assert error['error'] in errors_codes_keys
        assert FIELD_NAMES['TOKEN'] not in response.json.keys()


    # TODO: Napisać test, który sprawdzi endpointa pod względem poprawności adresu email


class TestUserGet:

    @pytest.mark.usefixtures('app')
    @pytest.mark.asyncio
    async def test_can_get_user_data(self, app: Sanic):
        request_create_user, response_create_user = await create_user(app, USER_DATA)
        token = response_create_user.json.get(FIELD_NAMES['TOKEN'])
        assert token

        request_get_user, response_get_user = await get_user(app, token)
        response_get_user_json_keys = response_get_user.json.keys()
        assert response_get_user.status_code == 200
        for key, value in USER_DATA.items():
            if key == FIELD_NAMES['PASSWORD']:
                continue

            assert key in response_get_user_json_keys
            assert response_get_user.json[key] == USER_DATA[key]

    @pytest.mark.usefixtures('app')
    @pytest.mark.asyncio
    async def test_can_get_error_no_token(self, app: Sanic):
        request_create_user, response_create_user = await create_user(app, USER_DATA)
        token = ''
        request_get_user, response_get_user = await get_user(app, token)
        errors_list = response_get_user.json.get('errors')

        assert response_get_user.status_code == 401
        assert len(errors_list) == 1
        assert errors_list[0]['error'] == ERROR_CODES['AUTH-001']['error']  # Empty credentials

    @pytest.mark.usefixtures('app')
    @pytest.mark.asyncio
    async def test_can_get_error_invalid_token(self, app: Sanic):
        request_create_user, response_create_user = await create_user(app, USER_DATA)
        token = 'invalid_token'
        request_get_user, response_get_user = await get_user(app, token)
        errors_list = response_get_user.json.get('errors')

        assert response_get_user.status_code == 401
        assert len(errors_list) == 1
        assert errors_list[0]['error'] == ERROR_CODES['AUTH-002']['error']  # Invalid credentials


