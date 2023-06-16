from . import Base
from typing import List
from .proxy import Proxy
from .travian_server import TravianServer
from .hero import Hero
from .action import Action
from .village import Village
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from uuid import uuid4


class GameSession(Base):

    __tablename__ = 'game_session'

    uuid: Mapped[Integer] = mapped_column(String, primary_key=True, default=uuid4)
    # User_name is for relationship with User table
    user = mapped_column(ForeignKey('user.name'))
    # Username is for travian session
    username: Mapped[String] = mapped_column(String())
    password: Mapped[String] = mapped_column(String())
    tribe: Mapped[String] = mapped_column(String(), nullable=True)
    proxy_id = mapped_column(ForeignKey('proxy.id'), nullable=True)
    proxy: Mapped[Proxy] = relationship()
    server_id = mapped_column(ForeignKey('travian_server.id'))
    server: Mapped[TravianServer] = relationship()
    hero: Mapped[Hero] = relationship()
    actions: Mapped[List[Action]] = relationship(
        cascade='all, delete',
        passive_deletes=True
    )
    villages: Mapped[List[Village]] = relationship(
        cascade='all, delete',
        passive_deletes=True
    )
