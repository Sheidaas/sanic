from . import Base
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class ActivitiesTimes(Base):

    __tablename__ = 'activities_times'

    id: Mapped[Integer] = mapped_column(Integer(), primary_key=True)
    last_time_resources_refreshed: Mapped[DateTime] = mapped_column(DateTime())
    last_time_constructions_refreshed: Mapped[DateTime] = mapped_column(DateTime())
    last_time_buildings_refreshed: Mapped[DateTime] = mapped_column(DateTime())
    last_time_army_refreshed: Mapped[DateTime] = mapped_column(DateTime())
    last_time_hero_status_refreshed: Mapped[DateTime] = mapped_column(DateTime())
    last_time_hero_adventures_refreshed: Mapped[DateTime] = mapped_column(DateTime())
    last_time_celebration_refreshed: Mapped[DateTime] = mapped_column(DateTime())
    last_time_smithy_refreshed: Mapped[DateTime] = mapped_column(DateTime())
    last_time_academy_refreshed: Mapped[DateTime] = mapped_column(DateTime())
    last_time_merchants_refreshed: Mapped[DateTime] = mapped_column(DateTime())
    last_time_barracks_refreshed: Mapped[DateTime] = mapped_column(DateTime())
    last_time_stable_refreshed: Mapped[DateTime] = mapped_column(DateTime())
    last_time_workshop_refreshed: Mapped[DateTime] = mapped_column(DateTime())
    last_time_culture_points_refreshed: Mapped[DateTime] = mapped_column(DateTime())
    last_time_residence_refreshed: Mapped[DateTime] = mapped_column(DateTime())
    last_time_palace_refreshed: Mapped[DateTime] = mapped_column(DateTime())
    next_time_resources_refreshed: Mapped[DateTime] = mapped_column(DateTime())
    next_time_constructions_refreshed: Mapped[DateTime] = mapped_column(DateTime())
    next_time_buildings_refreshed: Mapped[DateTime] = mapped_column(DateTime())
    next_time_army_refreshed: Mapped[DateTime] = mapped_column(DateTime())
    next_time_hero_status_refreshed: Mapped[DateTime] = mapped_column(DateTime())
    next_time_hero_adventures_refreshed: Mapped[DateTime] = mapped_column(DateTime())
    next_time_celebration_refreshed: Mapped[DateTime] = mapped_column(DateTime())
    next_time_smithy_refreshed: Mapped[DateTime] = mapped_column(DateTime())
    next_time_academy_refreshed: Mapped[DateTime] = mapped_column(DateTime())
    next_time_merchants_refreshed: Mapped[DateTime] = mapped_column(DateTime())
    next_time_barracks_refreshed: Mapped[DateTime] = mapped_column(DateTime())
    next_time_stable_refreshed: Mapped[DateTime] = mapped_column(DateTime())
    next_time_workshop_refreshed: Mapped[DateTime] = mapped_column(DateTime())
    next_time_culture_points_refreshed: Mapped[DateTime] = mapped_column(DateTime())
    next_time_residence_refreshed: Mapped[DateTime] = mapped_column(DateTime())
    next_time_palace_refreshed: Mapped[DateTime] = mapped_column(DateTime())
    village_id: Mapped[ForeignKey] = mapped_column(ForeignKey('village.id'))
