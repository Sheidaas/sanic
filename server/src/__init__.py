from sanic import Sanic
from .engine import Engine
from .api.handlers.login import Login
from .api.handlers.register import Register
from .utils import read_config_file
from .database import Database


def get_app(root_path: str):
    app = Sanic(
        name='travian_bot',
        ctx={
            'DATABASE': Database(),
            'ENGINE': Engine(),
            'CONFIG': read_config_file(root_path)
            })

    app.add_route(Login.as_view(), '/login')
    app.add_route(Register.as_view(), '/register')
    return app
