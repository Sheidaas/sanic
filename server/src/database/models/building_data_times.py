from . import Base
from sqlalchemy import ForeignKey
from sqlalchemy import Interval
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class BuildingDataTimes(Base):

    __tablename__ = 'building_data_times'

    id: Mapped[Integer] = mapped_column(Integer(), primary_key=True)
    building_id: Mapped[ForeignKey] = mapped_column(ForeignKey('building.id'))
    building_level: Mapped[Integer] = mapped_column(Integer())
    main_building_level: Mapped[Integer] = mapped_column(Integer())
    time: Mapped[Interval] = mapped_column(Interval())
