from . import Base
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Interval
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Construction(Base):

    __tablename__ = 'construction'

    id: Mapped[Integer] = mapped_column(Integer(), primary_key=True)
    field_id: Mapped[Integer] = mapped_column(Integer())
    field_type: Mapped[String] = mapped_column(String())
    from_level: Mapped[Integer] = mapped_column(Integer())
    to_level: Mapped[Integer] = mapped_column(Integer())
    building_time: Mapped[Interval] = mapped_column(Interval())
    started_time: Mapped[DateTime] = mapped_column(DateTime())
    finish_time: Mapped[DateTime] = mapped_column(DateTime())
    village_id: Mapped[ForeignKey] = mapped_column(ForeignKey('village.id'))
