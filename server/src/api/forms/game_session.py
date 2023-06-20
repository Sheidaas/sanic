from uuid import UUID
from . import Form
from ...utils.dictionaries import ERROR_CODES
from ...utils import get_database


class GameSessionForm(Form):

    async def is_valid(self):
        uuid = self.raw_data.get('game_session_uuid')
        if not uuid:
            self.errors.append(ERROR_CODES['GAME-SESSION-002'])
            return False

        try:
            UUID(uuid)
        except ValueError:
            self.errors.append(ERROR_CODES['GAME-SESSION-001'])
            return False

        self.cleaned_instance = await get_database().game_session_manager.get_by_uuid(uuid)
        if not self.cleaned_instance:
            self.errors.append(ERROR_CODES['GAME-SESSION-000'])
            return False

        return True


class NewGameSessionForm(Form):
    pass

