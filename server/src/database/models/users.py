import datetime
import jwt

from . import Base

from ...utils import get_config

from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class User(Base):

    __tablename__ = 'user'

    name: Mapped[str] = mapped_column(primary_key=True)
    password: Mapped[str] = mapped_column(String())
    email: Mapped[str] = mapped_column(String())
    premium_end_date: Mapped[DateTime] = mapped_column(DateTime())
    is_admin: Mapped[Boolean] = mapped_column(Boolean())

    def is_premium(self):
        if datetime.datetime.now() >= self.premium_end_date:
            return False
        return True

    def get_token(self):
        secret_key = get_config().get('KEYS', 'SECRET_KEY')
        return jwt.encode({'username': self.name, 'is_admin': self.is_admin, 'due': 0}, secret_key)

    def to_dict(self):
        return {
            'username': self.name,
            'email': self.email,
            'premium_end_date': str(self.premium_end_date),
            'is_admin': self.is_admin
        }