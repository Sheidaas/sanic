from sanic import Sanic
from ..database.models.users import User
from ..database import Database
from .selenium_session import SeleniumSession


class Engine:

    def __init__(self, database: Database) -> None:
        """
        database: connection to db
        run: should engine run sessions
        is_running: is engine running sessions, if run = false is_running will try to close sessions
        selenium_sessions: list of selenium client sessions
        """
        self.database: Database = database
        self.run: bool = True
        self.is_running: bool = False
        self.selenium_sessions: list[SeleniumSession] = []

    def create_session(self, service, service_user: ServiceUser) -> None:
        app = Sanic.get_app()
        database = app.ctx.get('DATABASE')

        server = database.travian_server_manager.get_travian_server_by_url(server)
        game_session = None
        game_session.server_id = server.id
        game_session.user_name = internal_user.name
        game_session.username = username
        game_session.password = password
        game_session = database.insert(game_session)
        self.selenium_sessions.append(SeleniumSession(game_session, None, client))

    def load_game_session_by_id(self, game_session_id: int) -> None:
        app = Sanic.get_app()
        database = app.ctx.get('DATABASE')

        game_session = database.game_sessions_manager.get_by_id(game_session_id)
        self.selenium_sessions.append(SeleniumSession(game_session, None, None))

    def on_update(self):
        while self.run:
            self.is_running = True


        self.is_running = False
