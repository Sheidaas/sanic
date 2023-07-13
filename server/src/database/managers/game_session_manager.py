from . import Manager

from ..models.game_session import GameSession

from sqlalchemy import select
from sqlalchemy.orm import Session


class GameSessionManager(Manager):

    async def get_game_session_by_uuid(self, uuid: str):
        session: Session = self.get_session()
        stmt = select(GameSession).where(GameSession.uuid == uuid)
        return session.execute(stmt).scalar_one_or_none()
