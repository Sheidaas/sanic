import pytest
from configparser import ConfigParser

from src.utils import read_config_file


class TestReadConfigFile:

    @pytest.mark.usefixtures('root_path')
    @pytest.mark.asyncio
    async def test_is_config_correct(self, root_path):
        config = read_config_file(root_path)
        assert config
        assert isinstance(config, ConfigParser)

    @pytest.mark.usefixtures('root_path')
    @pytest.mark.asyncio
    async def test_read_config_file(self, root_path):
        config = read_config_file(root_path)
        config_dict = {
            'JWT': {
                'SECRET_KEY': str,
                'ALGORITHMS': str,
                'DAYS_TO_TOKEN_EXPIRE': int,
            },
            'SERVER': {
                'HOST': str,
                'PORT': str,
                'DEBUG': bool,
            },
            'DATABASE': {
                'DEBUG': bool,
                'POSTGRES_DATABASE': str,
                'POSTGRES_HOST': str,
                'POSTGRES_USERNAME': str,
                'POSTGRES_PASSWORD': str,
            }
        }

        for section_key in config_dict.keys():
            for item_key, item in config_dict[section_key].items():
                config_value = config.get(section_key, item_key)

                assert config_value
                if item == bool:
                    assert True if config_value == 'True' or config_value == 'False' else False
                else:
                    assert item(config_value)

