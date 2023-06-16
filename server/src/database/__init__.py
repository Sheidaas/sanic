from ..utils import get_config

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from configparser import ConfigParser
from .models import Base
from .managers.user_manager import UserManager
from .managers.game_session_manager import GameSessionManager
from .managers.building_manager import BuildingManager


class Database:

    def __init__(self, config: ConfigParser):
        self.config = config
        self.engine: Engine | None = None

        self.game_session_manager: GameSessionManager = GameSessionManager(self.get_session)
        self.user_manager: UserManager = UserManager(self.get_session)
        self.building_manager: BuildingManager = BuildingManager(self.get_session)

        self.initialize_database()

    def get_session(self):
        if not self.engine:
            raise ValueError
        return Session(self.engine)

    def initialize_database(self):
        debug = bool(self.config.get('DATABASE', 'DEBUG'))
        if debug:
            self.engine = create_engine('sqlite:///:memory:')
        else:
            postgres_username = self.config.get('DATABASE', 'POSTGRES_USERNAME')
            postgres_password = self.config.get('DATABASE', 'POSTGRES_PASSWORD')
            postgres_host = self.config.get('DATABASE', 'POSTGRES_HOST')
            postgres_database = self.config.get('DATABASE', 'POSTGRES_DATABASE')

            url = f'postgresql+psycopg2://{postgres_username}:{postgres_password}@{postgres_host}/{postgres_database}'
            self.engine = create_engine(url)

        Base.metadata.create_all(self.engine)

    async def insert(self, model_to_save):
        session: Session = self.get_session()
        try:
            session.add(model_to_save)
        except Exception as exc:
            session.rollback()
            raise exc
        finally:
            session.commit()
            session.refresh(model_to_save)
        return model_to_save

