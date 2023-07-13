import pytest
from sanic import Sanic
from src.database import Database
from src.utils import get_database


class TestGetDatabase:

    @pytest.mark.usefixtures('app')
    @pytest.mark.asyncio
    async def test_is_database_correct(self, app: Sanic) -> None:
        """
        Sanic needs to be running because get_database gets database from SanicApp.ctx.get("DATABASE")
        """
        database: Database = get_database()

        assert database
        assert isinstance(database, Database)
