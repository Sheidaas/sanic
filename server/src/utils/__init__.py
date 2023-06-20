import os
import datetime
from sanic import Sanic
from jwt import decode
from jwt import InvalidTokenError
from configparser import ConfigParser


def read_config_file(root_path: str):
    config_parser = ConfigParser()
    config_parser.read(os.path.join(root_path, 'resources', 'config.ini'))
    return config_parser


def get_database():
    app = Sanic.get_app()
    return app.ctx.get('DATABASE')


def get_config() -> ConfigParser:
    app = Sanic.get_app()
    return app.ctx.get('CONFIG')


def suppose_time_when_enough_resources(required_resources, current_resources, production, magazine_size, granary_size):
    if required_resources['free_crop'] > current_resources['free_crop']:
        return False
    if required_resources['Wood'] > magazine_size or \
            required_resources['Clay'] > magazine_size or \
            required_resources['Iron'] > magazine_size or \
            required_resources['Crop'] > granary_size:
        return False

    needed_wood = required_resources['Wood'] - current_resources['Wood']
    needed_clay = required_resources['Clay'] - current_resources['Clay']
    needed_iron = required_resources['Iron'] - current_resources['Iron']
    needed_crop = required_resources['Crop'] - current_resources['Crop']

    return max([
        needed_wood / (production['Wood'] / 3600),
        needed_clay / (production['Clay'] / 3600),
        needed_iron / (production['Iron'] / 3600),
        needed_crop / (production['Crop'] / 3600),
    ])


def shift_resources(session):
    current_time = datetime.datetime.now()
    shift_time = current_time - session.last_refresh_time
    s_shift_time = shift_time.seconds
    if not s_shift_time or 5 > s_shift_time:
        return False

    for village in session.villages:
        for key, value in village.resources.items():
            new_amount = (value['production'] / 3600) * s_shift_time
            if key == 'Crop':
                value['amount'] = village.granary_size if value['amount'] + new_amount >= village.granary_size else \
                    value['amount'] + new_amount
            else:
                value['amount'] = village.magazine_size if value['amount'] + new_amount >= village.magazine_size else \
                    value['amount'] + new_amount

    session.last_refresh_time = current_time
    return True


def decode_jwt(token: str) -> dict | None:
    config = get_config()
    secret_key = config.get('JWT', 'SECRET_KEY')
    algorithms = config.get('JWT', 'ALGORITHMS').split(',')
    
    try:
        return decode(token, secret_key, algorithms=algorithms)
    except InvalidTokenError:
        return None
