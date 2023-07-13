from . import Base
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Building(Base):

    __tablename__ = 'building'

    id: Mapped[Integer] = mapped_column(Integer(), primary_key=True)
    name: Mapped[String] = mapped_column(String())
