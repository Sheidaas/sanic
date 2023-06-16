from .navigator import Navigator


from selenium import webdriver
import undetected_chromedriver as uc


class SeleniumSession:

    def __init__(self, game_session, proxy, client):
        self.client = client
        self.game_session = game_session
        self.current_village_id: int = 0
        self.proxy = proxy
        self.driver = None
        self.navigator: Navigator | None = None

        self.current_village_name = ''

        self.get_driver()
        self.navigator.login_to_game()

    def get_driver(self):

        options = uc.ChromeOptions()
        options.headless = False
        options.add_argument("--window-size=1920x1080")
        options.add_argument("--disable-blink-features=AutomationControlled")

        self.driver = uc.Chrome(options=options)
        self.driver.implicitly_wait(5)

        self.navigator = Navigator(self.driver, self.game_session)
