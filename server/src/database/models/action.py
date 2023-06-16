from . import Base
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Action(Base):

    __tablename__ = 'action'

    id: Mapped[Integer] = mapped_column(Integer(), primary_key=True)
    name: Mapped[String] = mapped_column(String())
    execution_time: Mapped[DateTime] = mapped_column(DateTime())
    execution_function: Mapped[String] = mapped_column(String())
    execution_args: Mapped[String] = mapped_column(String())
    game_session_id: Mapped[ForeignKey] = mapped_column(ForeignKey('game_session.uuid'))