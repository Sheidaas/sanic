import os
from src.app import get_app
from functools import partial
from sanic import Sanic
from sanic.worker.loader import AppLoader
from src.utils import read_config_file

if __name__ == '__main__':
    root_path = os.getcwd()
    loader = AppLoader(factory=partial(get_app, root_path))
    app = loader.load()

    config = read_config_file(root_path)
    print(config)
    host = config.get('SERVER', 'HOST')
    port = int(config.get('SERVER', 'PORT'))

    app.prepare(host=host, port=port, debug=True)
    Sanic.serve(primary=app, app_loader=loader)
