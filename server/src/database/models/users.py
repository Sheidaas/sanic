from . import Base

from ...utils.dictionaries import FIELD_NAMES

from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from datetime import datetime


class User(Base):

    __tablename__ = 'user'

    name: Mapped[str] = mapped_column(primary_key=True)
    password: Mapped[str] = mapped_column(String())
    email: Mapped[str] = mapped_column(String())
    premium_end_date: Mapped[DateTime] = mapped_column(DateTime())
    is_admin: Mapped[Boolean] = mapped_column(Boolean())

    def is_premium(self):
        if datetime.now() >= self.premium_end_date:
            return False
        return True

    def to_dict(self):
        return {
            FIELD_NAMES['USERNAME']: self.name,
            FIELD_NAMES['EMAIL']: self.email,
            FIELD_NAMES['PREMIUM_EXPIRATION_DATE']: str(self.premium_end_date),
            FIELD_NAMES['IS_ADMIN']: self.is_admin
        }
