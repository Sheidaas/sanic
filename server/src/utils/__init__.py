import os
from configparser import ConfigParser


ERRORS = {
    'AUTH-000': {
        'error': 'auth-000',
        'message': 'Credentials are empty'
    },
    'AUTH-001': {
        'error': 'auth-001',
        'message': 'Invalid credentials'
    },
    'REGISTER-000': {
        'error': 'register-000',
        'message': 'Empty username'
    },
    'REGISTER-001': {
        'error': 'register-001',
        'message': 'Empty password'
    },
    'REGISTER-002': {
        'error': 'register-002',
        'message': 'Empty email'
    },
    'REGISTER-003': {
        'error': 'register-003',
        'message': 'Username is already taken'
    }
}


def read_config_file(root_path: str):
    config_parser = ConfigParser()
    config_parser.read(os.path.join(root_path, 'resources', 'config.ini'))
    return config_parser



