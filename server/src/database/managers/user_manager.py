from . import Manager

from sqlalchemy import select
from sqlalchemy.orm import Session

from Modules.database.models import User


class UserManager(Manager):

    def insert(self, user: User) -> User:
        session: Session = self.get_session()
        session.add(user)
        session.commit()
        return user

    def get_by_username(self, username: str) -> User | None:
        session: Session = self.get_session()
        return session.execute(select(User).where(User.name.is_(username))).scalar_one_or_none()

