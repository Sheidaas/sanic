import jwt
import logging
from jwt import decode
from jwt import InvalidTokenError
from datetime import timedelta, date
from . import get_config
from .dictionaries import ERROR_CODES, FIELD_NAMES


def decode_jwt(token: str) -> dict | None:
    config = get_config()
    secret_key = config.get('JWT', 'SECRET_KEY')
    algorithms = config.get('JWT', 'ALGORITHMS').split(',')

    try:
        return decode(token, secret_key, algorithms=algorithms)
    except InvalidTokenError as exception:
        logging.error(exception)
        return ERROR_CODES['SERVER-ERROR-000']


def encode_jwt(data: dict) -> str | dict:
    config = get_config()
    secret_key = config.get('JWT', 'SECRET_KEY')
    algorithms = config.get('JWT', 'ALGORITHMS')
    expiration_date = date.today() + timedelta(days=int(config.get('JWT', 'DAYS_TO_TOKEN_EXPIRE')))
    data[FIELD_NAMES['TOKEN_EXPIRATION_DATE']] = str(expiration_date)
    logging.error(algorithms)
    try:
        jwt_code = jwt.encode(data, secret_key, algorithm=algorithms)
        logging.info(jwt_code)
    except Exception as exception:
        logging.error(exception)
        return ERROR_CODES['SERVER-ERROR-000']
    return jwt_code
