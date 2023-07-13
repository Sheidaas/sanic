import pytest
from src.utils.dictionaries import TRAVIAN_URLS
from src.utils.dictionaries import URLS
from src.utils.dictionaries import FIELD_NAMES
from src.utils.dictionaries import ERROR_CODES


"""
This tests are checking that are the following keys in dictionaries, its not checking values of keys
"""


TRAVIAN_URLS_KEYS = [
    'LOGIN',
    'RESOURCES',
    'INSIDE_VILLAGE',
    'HERO',
    'ADVENTURES',
    'PROFILE',
    'BUILD',
]
URLS_KEYS = [
    'USER',
    'LOGIN',
    'GAME_SESSION',
]
FIELD_NAMES_KEYS = [
    'TOKEN',
    'USERNAME',
    'PASSWORD',
    'EMAIL',
    'TOKEN_EXPIRATION_DATE',
    'IS_ADMIN',
    'PREMIUM_EXPIRATION_DATE',
]
ERROR_CODES_KEYS = [
    'AUTH-000',
    'AUTH-001',
    'AUTH-002',
    'AUTH-003',
    'REGISTER-000',
    'REGISTER-001',
    'REGISTER-002',
    'REGISTER-003',
    'GAME-SESSION-000',
    'GAME-SESSION-001',
    'GAME-SESSION-002',
    'GAME-SESSION-003',
    'SERVER-ERROR-000',
    'SERVER-ERROR-001'
]


class TestDictionaries:

    @pytest.mark.asyncio
    async def test_are_travian_urls_good_keys(self) -> None:
        list_travian_urls_keys = TRAVIAN_URLS.keys()
        for key in list_travian_urls_keys:
            assert key in TRAVIAN_URLS_KEYS
        for key in TRAVIAN_URLS_KEYS:
            assert key in list_travian_urls_keys


    @pytest.mark.asyncio
    async def test_are_urls_good_keys(self) -> None:
        list_urls_keys = URLS.keys()
        for key in list_urls_keys:
            assert key in URLS_KEYS
        for key in URLS_KEYS:
            assert key in list_urls_keys

    @pytest.mark.asyncio
    async def test_are_field_names_good_keys(self) -> None:
        field_names_keys = FIELD_NAMES.keys()
        for key in field_names_keys:
            assert key in FIELD_NAMES_KEYS
        for key in FIELD_NAMES_KEYS:
            assert key in field_names_keys

    @pytest.mark.asyncio
    async def test_are_errors_codes_good_keys(self) -> None:
        list_error_codes_keys = ERROR_CODES.keys()
        for key in list_error_codes_keys:
            assert key in ERROR_CODES_KEYS
        for key in ERROR_CODES_KEYS:
            assert key in list_error_codes_keys
