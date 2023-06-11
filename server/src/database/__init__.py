from sqlalchemy.orm import Session

from .models import Base
from sqlalchemy import create_engine
from .managers.user_manager import UserManager


class Database:

    def __init__(self):
        self.engine = None
        self.user_manager: UserManager = UserManager(self.get_session)
        self.buildings_manager = None

        self.initialize_database()

    def get_session(self):
        return Session(self.engine)

    def initialize_database(self):
        url = 'postgresql+psycopg2://postgres:postgres@database/postgres'
        self.engine = create_engine(url)
        Base.metadata.create_all(self.engine)
        