import pytest

from src.database import Database
from src.utils import read_config_file

class TestBuildingManager:

    @pytest.mark.usefixtures('root_path')
    @pytest.mark.asyncio
    async def test_(self, root_path):
        config = read_config_file(root_path)
        database = Database(config)
