from . import Base
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class BuildingRequirementsData(Base):

    __tablename__ = 'building_requirements_data'

    id: Mapped[Integer] = mapped_column(Integer(), primary_key=True)
    building_id: Mapped[ForeignKey] = mapped_column(ForeignKey('building.id'))
    required_building_id: Mapped[ForeignKey] = mapped_column(ForeignKey('building.id'))
    required_building_level: Mapped[Integer] = mapped_column(Integer())
