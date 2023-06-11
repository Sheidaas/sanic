from . import Base
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Proxy(Base):

    __tablename__ = 'proxy'

    id: Mapped[Integer] = mapped_column(Integer(), primary_key=True)
    server: Mapped[String] = mapped_column(String())
    port: Mapped[String] = mapped_column(String())