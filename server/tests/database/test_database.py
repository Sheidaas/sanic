import pytest
from configparser import ConfigParser
from src.database import Database
from src.database.models import Base
from src.database.managers.building_manager import BuildingManager
from src.database.managers.game_session_manager import GameSessionManager
from src.database.managers.user_manager import UserManager
from src.utils import read_config_file
from sqlalchemy.engine import Engine
from sanic import Sanic


TABLES_NAMES = [
    'action',
    'activities_times',
    'adventure',
    'building',
    'building_data',
    'building_data_additional',
    'building_data_times',
    'building_requirements_data',
    'construction',
    'construction_site',
    'hero',
    'proxy',
    'travian_server',
    'user',
    'village',
    'game_session',
]


class TestDatabase:

    @pytest.mark.usefixtures('root_path')
    @pytest.mark.asyncio
    async def test_can_database_initialize(self, root_path):
        config = read_config_file(root_path)
        database = Database(config)

        assert isinstance(database, Database)
        assert isinstance(database.config, ConfigParser)
        assert isinstance(database.user_manager, UserManager)
        assert isinstance(database.building_manager, BuildingManager)
        assert isinstance(database.game_session_manager, GameSessionManager)
        assert isinstance(database.engine, Engine)

    @pytest.mark.usefixtures('app')
    @pytest.mark.asyncio
    async def test_are_database_in_sanic_initialized_properly(self, app: Sanic):
        database = app.ctx.get('DATABASE')
        assert isinstance(database, Database)
        assert isinstance(database.engine, Engine)

    @pytest.mark.usefixtures('app')
    @pytest.mark.asyncio
    async def test_are_good_tables(self, app: Sanic):
        tables_names = Base.metadata.tables.keys()
        for table_name in tables_names:
            assert table_name in TABLES_NAMES
        for table_name in TABLES_NAMES:
            assert table_name in tables_names
