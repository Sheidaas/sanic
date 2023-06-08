from sanic import Sanic
from src.engine import Engine
from src.api.handlers.login import Login
from src.utils import read_config_file


def get_app(root_path: str):
    app = Sanic(
        name='travian_bot',
        ctx={
            'DATABASE': None,
            'ENGINE': Engine(),
            'CONFIG': read_config_file(root_path)
            })

    app.add_route(Login.as_view(), '/login')
    return app
