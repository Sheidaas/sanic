class Engine:

    def __init__(self):
        self.selenium_sessions: List[SeleniumSession] = []

    def create_new_game_session(self, username: str, password: str, server: TravianServer, user: User, client) -> None:
        server = database.travian_server_manager.get_travian_server_by_url(server)
        game_session = GameSession()
        game_session.server_id = server.id
        game_session.user_name = user.name
        game_session.username = username
        game_session.password = password
        game_session = database.game_sessions_manager.insert_model(game_session)
        self.selenium_sessions.append(SeleniumSession(game_session, None, client))

    def load_game_session_by_id(self, game_session_id: int) -> None:
        game_session = database.game_sessions_manager.get_by_id(game_session_id)
        self.selenium_sessions.append(SeleniumSession(game_session, None, None))

    def on_update(self):
        for session in self.selenium_sessions:
            session.___scan_current_village___()