from sanic import Sanic
from .engine import Engine
from .api.login import Login
from .api.user import User
from .utils import read_config_file
from .database import Database
from .utils.dictionaries import URLS


def get_app(root_path: str):
    config = read_config_file(root_path)
    app = Sanic(
        name='travian_bot',
        ctx={
            'DATABASE': Database(config),
            'ENGINE': Engine(),
            'CONFIG': config
            })

    app.add_route(Login.as_view(), URLS['LOGIN'])
    app.add_route(User.as_view(), URLS['USER'])
    return app
