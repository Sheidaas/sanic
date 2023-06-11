from . import Base
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import Interval
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Adventure(Base):

    __tablename__ = 'adventure'

    id: Mapped[Integer] = mapped_column(Integer(), primary_key=True)
    place: Mapped[String] = mapped_column(String())
    coordinate_x: Mapped[Integer] = mapped_column(Integer())
    coordinate_y: Mapped[Integer] = mapped_column(Integer())
    duration: Mapped[Interval] = mapped_column(Interval())
    danger_level: Mapped[Integer] = mapped_column(Integer())
    started_time: Mapped[DateTime] = mapped_column(Integer())
    hero_id: Mapped[ForeignKey] = mapped_column(ForeignKey('hero.id'))
