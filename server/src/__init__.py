import logging
from sanic import Sanic
from .database import Database
from .engine import Engine
from .utils import read_config_file
from .utils.logger import set_logger
from .utils.dictionaries import URLS, LOGGERS_NAMES
from .api.login import Login
from .api.user import User
from .api import middlewares
from .api.listeners import after_server_start


def get_app(root_path: str):
    _config = read_config_file(root_path)
    set_logger(root_path, _config)

    _database = Database(_config, root_path=root_path)
    _engine = Engine(_database)

    # Setting loggers
    app = Sanic(
        name='travian_bot',
        ctx={
            'DATABASE': _database,
            'ENGINE': _engine,
            'CONFIG': _config,
            'ROOT_PATH': root_path
            },
    )

    # Setting routing
    app.add_route(Login.as_view(), URLS['LOGIN'])
    app.add_route(User.as_view(), URLS['USER'])

    # Setting requests middlewares
    app.register_middleware(middlewares.log_request)

    # Register listeners
    app.register_listener(after_server_start, 'main_process_start')

    if bool(_config.get('DATABASE', 'USE_FIXTURES')):
        pass
        #from .database.fixtures import TravianServerFixture
        #app.add_task(TravianServerFixture(_database).some())

    return app
