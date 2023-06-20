import pytest
import os
from src import get_app
from src.utils import read_config_file
from functools import partial
from sanic.worker.loader import AppLoader


@pytest.fixture
def app():
    path = os.path.join(os.getcwd(), 'tests')
    loader = AppLoader(factory=partial(get_app, path))
    app = loader.load()
    config = read_config_file(path)

    host = config.get('SERVER', 'HOST')
    port = int(config.get('SERVER', 'PORT'))
    debug = True if config.get('SERVER', 'DEBUG') == 'True' else False

    app.prepare(host=host, port=port, debug=debug)
    return app

@pytest.fixture
def root_path():
    return os.path.join(os.getcwd(), 'tests')