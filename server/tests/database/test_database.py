import pytest
from src.database import Database
from src.database.models import Base
from src.utils import read_config_file
from sqlalchemy.engine import Engine


class TestDatabase:

    @pytest.mark.usefixtures('root_path')
    @pytest.mark.asyncio
    async def test_can_database_initialize(self, root_path):
        config = read_config_file(root_path)
        database = Database(config)

        assert isinstance(database, Database)
        assert isinstance(database.engine, Engine)

    @pytest.mark.usefixtures('root_path')
    @pytest.mark.asyncio
    async def test_are_good_tables(self, root_path):
        config = read_config_file(root_path)
        database = Database(config)

        print(Base.metadata.tables.keys())
        assert False
