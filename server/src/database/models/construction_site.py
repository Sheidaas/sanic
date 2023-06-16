from . import Base
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class ConstructionSite(Base):

    __tablename__ = 'construction_site'

    id: Mapped[Integer] = mapped_column(Integer(), primary_key=True)
    field_id: Mapped[Integer] = mapped_column(Integer())
    level: Mapped[Integer] = mapped_column(Integer())
    building_id: Mapped[ForeignKey] = mapped_column(ForeignKey('building.id'))
    village_id: Mapped[ForeignKey] = mapped_column(ForeignKey('village.id'))
