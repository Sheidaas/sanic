ERROR_CODES = {
    'AUTH-000': {
        'error': 'auth-000',
        'message': 'Not authenticated'
    },
    'AUTH-001': {
        'error': 'auth-001',
        'message': 'Credentials are empty'
    },
    'AUTH-002': {
        'error': 'auth-002',
        'message': 'Invalid credentials'
    },
    'AUTH-003': {
        'error': 'auth-003',
        'message': 'Token expired'
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
    },
    'GAME-SESSION-000': {
        'error': 'game-session-000',
        'message': 'Game session with this UUID does not exist'
    },
    'GAME-SESSION-001': {
        'error': 'game-session-001',
        'message': 'UUID is invalid'
    },
    'GAME-SESSION-002': {
        'error': 'game-session-002',
        'message': 'Empty UUID'
    },
    'GAME-SESSION-003': {
        'error': 'game-session-003',
        'message': 'User is not game session owner'
    },
}


class InternalSeleniumException(Exception):

    def __init__(self, error: dict[str, str]):
        self.error = error