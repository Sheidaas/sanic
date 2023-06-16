import pytest
from sanic import Sanic
from src.utils import FIELD_NAMES
from src.utils.exceptions import ERROR_CODES


class TestUserPost:

    @pytest.mark.usefixtures('app')
    @pytest.mark.asyncio
    async def test_can_create_user(self, app: Sanic):
        # First try to register new user, it should pass because user
        # db is empty and there is no other user with username Sheida
        user_data = {
            FIELD_NAMES['USERNAME']: 'Sheida',
            FIELD_NAMES['PASSWORD']: 'admin',
            FIELD_NAMES['EMAIL']: 'maciejwrzeszcz1@wp.pl',
        }
        request, response = await app.asgi_client.post('/user', json=user_data)
        assert response.status_code == 201
        assert response.json.get('token')

        # But next request should be discarded and should tell us about no unique username
        request, response = await app.asgi_client.post('/user', json=user_data)
        assert response.status_code == 400

        # In that way we know that, there is only one error REGISTER-003
        for error in response.json.get('errors'):
            assert error['error'] == ERROR_CODES['REGISTER-003']['error']

        assert 1 == len(response.json.get('errors'))




