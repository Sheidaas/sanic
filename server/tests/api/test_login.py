import pytest
from sanic import Sanic
from src.utils.dictionaries import FIELD_NAMES, ERROR_CODES
from helpers import login_with_token, create_user


USER_DATA = {
    FIELD_NAMES['USERNAME']: 'Sheida',
    FIELD_NAMES['PASSWORD']: 'admin',
    FIELD_NAMES['EMAIL']: 'maciejwrzeszcz1@wp.pl',
}


class TestLoginGet:

    @pytest.mark.usefixtures('app')
    @pytest.mark.asyncio
    async def test_can_login_with_token(self, app: Sanic):
        request, response = await create_user(app, USER_DATA)
        token = response.json.get(FIELD_NAMES['TOKEN'])
        assert response.status_code == 201
        assert token

        login_request, login_response = await login_with_token(app, token)
        login_token = login_response.json.get(FIELD_NAMES['TOKEN'])
        assert login_response.status_code == 200
        assert login_token
        assert token == login_token

    @pytest.mark.usefixtures('app')
    @pytest.mark.asyncio
    async def test_can_login_with_no_token(self, app: Sanic):
        request, response = await create_user(app, USER_DATA)
        token = response.json.get(FIELD_NAMES['TOKEN'])
        assert response.status_code == 201
        assert token

        empty_token = ''
        login_request, login_response = await login_with_token(app, empty_token)
        login_token = login_response.json.get(FIELD_NAMES['TOKEN'])
        errors_list = login_response.json.get('errors')
        assert login_response.status_code == 401
        assert not login_token
        assert len(errors_list) == 1
        assert errors_list[0]['error'] == ERROR_CODES['AUTH-001']['error']  # Empty credentials








