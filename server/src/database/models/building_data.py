from . import Base
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import Interval
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class BuildingData(Base):

    __tablename__ = 'building_data'

    id: Mapped[Integer] = mapped_column(Integer(), primary_key=True)
    building_id: Mapped[ForeignKey] = mapped_column(ForeignKey('building.id'))
    building_level: Mapped[Integer] = mapped_column(Integer())
    culture_points: Mapped[Integer] = mapped_column(Integer())
    required_wood: Mapped[Integer] = mapped_column(Integer())
    required_clay: Mapped[Integer] = mapped_column(Integer())
    required_crop: Mapped[Integer] = mapped_column(Integer())
    required_free_crop: Mapped[Integer] = mapped_column(Integer())
