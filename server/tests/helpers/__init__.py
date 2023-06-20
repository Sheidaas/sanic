from sanic import Sanic
from src.utils.dictionaries import URLS


async def create_user(app: Sanic, user_data: dict):
    return await app.asgi_client.post(URLS['USER'], json=user_data)


async def get_user(app: Sanic, token: str):
    headers = get_authorization_header(token)
    return await app.asgi_client.get(URLS['USER'], headers=headers)


async def login_with_token(app: Sanic, token: str):
    headers = get_authorization_header(token)
    return await app.asgi_client.get(URLS['LOGIN'], headers=headers)


def get_authorization_header(token: str) -> dict:
    return {
        'Authorization': f'Bearer {token}'
    }
