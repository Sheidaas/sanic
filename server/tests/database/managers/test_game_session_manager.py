import pytest
from typing import Callable
from src.database import Database
from src.utils import read_config_file
from src.database.models.users import User
from src.database.managers.game_session_manager import GameSessionManager


class TestGameSessionManager:

    @pytest.mark.usefixtures('root_path')
    @pytest.mark.asyncio
    async def test_object_has_correct_assumptions(self, root_path):
        config = read_config_file(root_path)
        database = Database(config)

        assert isinstance(database.game_session_manager, GameSessionManager)
        assert isinstance(database.game_session_manager.get_session, Callable)

    @pytest.mark.usefixtures('root_path')
    @pytest.mark.asyncio
    async def test_get_game_session_by_uuid(self, root_path):
        config = read_config_file(root_path)
        database = Database(config)

        user = User()
        user.name = 'Sheida'
        user.password = 'a'


