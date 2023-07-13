import logging
import os.path

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session
from configparser import ConfigParser
from ..utils.dictionaries import LOGGERS_NAMES
from .models import Base
from .managers.user_manager import UserManager
from .managers.game_session_manager import GameSessionManager
from .managers.building_manager import BuildingManager


class Database:

    def __init__(self, config: ConfigParser, root_path=''):
        self.config = config
        self.database_type = config.get('DATABASE', 'DATABASE_TYPE')
        self.root_path = root_path
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
        error_logger = logging.getLogger(LOGGERS_NAMES['ERROR'])

        if self.database_type == 'SQLITE':
            filename = self.config.get('DATABASE', 'DATABASE_FILENAME')
            if not filename:
                error_logger.error('DATABASE_FILENAME IS NOT SET')
                raise ValueError

            if filename == ':memory:':
                self.engine: Engine = create_engine(f'sqlite:///{filename}')
            else:
                _filename = os.path.join(self.root_path, 'resources', filename)
                self.engine: Engine = create_engine(f'sqlite:///{_filename}')

        elif self.database_type == 'POSTGRES':
            postgres_username: str = self.config.get('DATABASE', 'POSTGRES_USERNAME')
            postgres_password: str = self.config.get('DATABASE', 'POSTGRES_PASSWORD')
            postgres_host: str = self.config.get('DATABASE', 'POSTGRES_HOST')
            postgres_database: str = self.config.get('DATABASE', 'POSTGRES_DATABASE')

            if not postgres_username:
                error_logger.error('POSTGRES_USERNAME IS NOT SET')
                raise ValueError

            if not postgres_password:
                error_logger.error('POSTGRES_PASSWORD IS NOT SET')
                raise ValueError

            if not postgres_host:
                error_logger.error('POSTGRES_HOST IS NOT SET')
                raise ValueError

            if not postgres_database:
                error_logger.error('POSTGRES_DATABASE IS NOT SET')
                raise ValueError

            url = f'postgresql+psycopg2://{postgres_username}:{postgres_password}@{postgres_host}/{postgres_database}'
            self.engine = create_engine(url)

        elif not self.database_type:
            error_logger.error('DATABASE_TYPE IS NOT SET')
            raise ValueError

        else:
            error_logger.error(f'NO SUPPORT FOR: {self.database_type}')
            raise ValueError

        # In this point self.engine should be Engine instance
        Base.metadata.create_all(self.engine)

    def insert(self, model_to_save):
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

    async def async_insert(self, model_to_save):
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
