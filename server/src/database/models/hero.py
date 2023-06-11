from . import Base
from.adventure import Adventure

from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import Boolean
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Hero(Base):

    __tablename__ = 'hero'

    id: Mapped[Integer] = mapped_column(Integer(), primary_key=True)
    health: Mapped[Integer] = mapped_column(Integer())
    experience: Mapped[Integer] = mapped_column(Integer())
    level: Mapped[Integer] = mapped_column(Integer())
    current_production: Mapped[String] = mapped_column(String())
    strength: Mapped[Integer] = mapped_column(Integer())
    off_bonus: Mapped[Integer] = mapped_column(Integer())
    deff_bonus: Mapped[Integer] = mapped_column(Integer())
    resources: Mapped[Integer] = mapped_column(Integer())
    available_points: Mapped[Integer] = mapped_column(Integer())
    speed: Mapped[Integer] = mapped_column(Integer())
    is_hid: Mapped[Boolean] = mapped_column(Boolean())
    is_dead: Mapped[Boolean] = mapped_column(Boolean())
    adventures: Mapped[List[Adventure]] = relationship()
    game_session_id: Mapped[ForeignKey] = mapped_column(ForeignKey('game_session.id'))
