import pytest
from src.utils.dictionaries import FIELD_NAMES
from src.utils.auth import decode_jwt


TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IlNoZWlkYSIsImVtYWlsIjoibWFjaWVqd3J6ZXN6Y3oxQHdwLnBsI' \
        'iwicHJlbWl1bV9leHBpcmF0aW9uX2RhdGUiOiIyMDIzLTA2LTIzIDE3OjA3OjU4LjA1NTE5OCIsImlzX2FkbWluIjpmYWxzZSwidG9rZW5f' \
        'ZXhwaXJhdGlvbl9kYXRlIjoiMjAyMy0wNi0zMCJ9.5eUZXQ495ujTYtINhptg3vjRM87WureEwm8Ibpzsoio'


USER_DATA = {
    FIELD_NAMES['USERNAME']: 'Sheida',
    FIELD_NAMES['PASSWORD']: 'admin',
    FIELD_NAMES['EMAIL']: 'maciejwrzeszcz1@wp.pl',
}


class TestAuthDecodeJWT:

    @pytest.mark.asyncio
    async def test_valid_token(self):
        is_valid = decode_jwt(TOKEN)
        assert isinstance(is_valid, dict)
        required_fields = FIELD_NAMES.values()
        response_fields = is_valid.keys()
        for response_field in response_fields:
            assert response_field in required_fields

    @pytest.mark.asyncio
    async def test_invalid_token(self):
        invalid_token = 'asdf'
        is_valid = decode_jwt(invalid_token)
        assert isinstance(is_valid, dict)















