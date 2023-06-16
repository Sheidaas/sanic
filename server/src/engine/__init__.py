from sanic import Sanic

from ..database.models.users import User

from .selenium_session import SeleniumSession


class Engine:

    def __init__(self):
        self.run = True
        self.is_running = False
        self.selenium_sessions: list[SeleniumSession] = []

    def create_new_game_session(self, username: str, password: str, server, user: User, client) -> None:
        app = Sanic.get_app()
        database = app.ctx.get('DATABASE')

        server = database.travian_server_manager.get_travian_server_by_url(server)
        game_session = None
        game_session.server_id = server.id
        game_session.user_name = user.name
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
