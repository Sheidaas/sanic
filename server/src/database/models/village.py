from . import Base

from .construction import Construction
from .activities_times import ActivitiesTimes

from typing import List
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Village(Base):

    __tablename__ = 'village'

    id: Mapped[Integer] = mapped_column(Integer(), primary_key=True)
    name: Mapped[String] = mapped_column(String())
    coordinate_x: Mapped[Integer] = mapped_column(Integer())
    coordinate_y: Mapped[Integer] = mapped_column(Integer())
    stored_wood: Mapped[Integer] = mapped_column(Integer())
    stored_clay: Mapped[Integer] = mapped_column(Integer())
    stored_iron: Mapped[Integer] = mapped_column(Integer())
    stored_crop: Mapped[Integer] = mapped_column(Integer())
    production_wood: Mapped[Integer] = mapped_column(Integer())
    production_clay: Mapped[Integer] = mapped_column(Integer())
    production_iron: Mapped[Integer] = mapped_column(Integer())
    production_crop: Mapped[Integer] = mapped_column(Integer())
    magazine_size: Mapped[Integer] = mapped_column(Integer())
    granary_size: Mapped[Integer] = mapped_column(Integer())
    free_crop: Mapped[Integer] = mapped_column(Integer())
    game_session_id: Mapped[ForeignKey] = mapped_column(ForeignKey('game_session.uuid'))
    constructions: Mapped[List[Construction]] = relationship(
        cascade='all, delete',
        passive_deletes=True
    )
    activities_times: Mapped[ActivitiesTimes] = relationship(
        cascade='all, delete',
        passive_deletes=True
    )