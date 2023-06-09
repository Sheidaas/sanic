from . import Manager

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models.users import User


class UserManager(Manager):

    async def get_by_username(self, username: str) -> User | None:
        session: Session = self.get_session()
        stmt = select(User).where(User.name == username)
        return session.execute(stmt).scalar_one_or_none()
