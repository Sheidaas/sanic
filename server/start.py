import os
from src import get_app
from functools import partial
from sanic import Sanic
from sanic.worker.loader import AppLoader
from src.utils import read_config_file

if __name__ == '__main__':
    root_path = os.getcwd()
    loader = AppLoader(factory=partial(get_app, root_path))
    app = loader.load()

    config = read_config_file(root_path)

    host = config.get('SERVER', 'HOST')
    port = int(config.get('SERVER', 'PORT'))
    debug = True if config.get('SERVER', 'DEBUG') == 'True' else False

    app.prepare(host=host, port=port, debug=debug)
    Sanic.serve(primary=app, app_loader=loader)
