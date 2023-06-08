from .models import Base
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from .managers.user_manager import UserManager


class Database:

    def __init__(self):
        self.engine = None
        self.user_manager: UserManager = UserManager(self.get_session)
        self.buildings_manager = None

        self.initialize_database()

    def initialize_database(self):
        url = URL
        Base.metadata.create_all(self.engine)
        