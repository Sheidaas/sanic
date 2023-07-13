


class SeleniumSession:

    def __init__(self, game_session, proxy, client):
        self.client = client
        self.game_session = game_session
        self.current_village_id: int = 0
        self.proxy = proxy


        self.current_village_name = ''

        self.get_driver()
        self.navigator.login_to_game()

    def get_driver(self):


