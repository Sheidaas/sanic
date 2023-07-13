import pytest
from sanic import Sanic
from configparser import ConfigParser
from src.utils import get_config


NEED_SECTIONS = [
    'LOGGER',
    'JWT',
    'SERVER',
    'DATABASE'
]


class TestGetConfig:

    @pytest.mark.usefixtures('app')
    @pytest.mark.asyncio
    async def test_is_config_correct(self, app: Sanic) -> None:
        """
        Sanic needs to be running because get_config gets config from SanicApp.ctx.get("CONFIG")
        """
        config: ConfigParser = get_config()

        assert config
        assert isinstance(config, ConfigParser)

    @pytest.mark.usefixtures('app')
    @pytest.mark.asyncio
    async def test_are_good_sections(self, app: Sanic) -> None:
        config: ConfigParser = get_config()

        real_sections = config.sections()
        for need_section in NEED_SECTIONS:
            assert need_section in real_sections

        for real_section in real_sections:
            assert real_section in NEED_SECTIONS
