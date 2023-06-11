from . import Base
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import Interval
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class BuildingAdditionalData(Base):

    __tablename__ = 'building_data_additional'

    id: Mapped[Integer] = mapped_column(Integer(), primary_key=True)
    building_id: Mapped[ForeignKey] = mapped_column(ForeignKey('building.id'))
    building_level: Mapped[Integer] = mapped_column(Integer())
    bonus_name: Mapped[String] = mapped_column(String())
    bonus_value: Mapped[Interval] = mapped_column(Interval())
