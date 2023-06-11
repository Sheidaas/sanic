import unittest
import requests


URLS = {
    'LOGIN': 'http://localhost/login',
    'REGISTER': 'http://localhost/register'
}


class TestLoginApi(unittest.TestCase):

    def test_login_token(self):
        token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InNoZWlkYSIsImlzX2FkbWluIjp0cnVlfQ.touEKLGPGyQoGlyRKZWQ0i24igXV3_OXZ7MC9FmKlKY'
        response = requests.post(URLS['LOGIN'], json={'username': 'sheida', 'password': 'sheida'})
        response_data = response.json()
        assert token == response_data['token']
        assert response.status_code == 200


class TestRegisterApi(unittest.TestCase):

    def test_register(self):
        data = {
            'username': 'sheida1',
            'password': 'sheida',
            'email': 'sheida'
        }
        response = requests.post(URLS['REGISTER'], json=data)
        assert response.json().get('token')
        assert response.status_code == 200

