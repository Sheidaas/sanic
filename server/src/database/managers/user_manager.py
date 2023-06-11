from . import Manager

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models.users import User


class UserManager(Manager):

    def insert(self, user: User) -> User:
        session: Session = self.get_session()
        session.add(user)
        try:
            session.commit()
        except Exception as exc:
            raise exc
        finally:
            session.refresh(user)
        return user

    def get_by_username(self, username: str) -> User | None:
        session: Session = self.get_session()
        stmt = select(User).where(User.name == username)
        return session.execute(stmt).scalar_one_or_none()

