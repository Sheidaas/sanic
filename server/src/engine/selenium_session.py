from Modules.game_manager.navigator import Navigator
from .scrappers.village_scrapper import VillageScrapper

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

    #def __get_info__(self):
    #    self.___get_profile_info___()
    #    self.___scan_hero___()
    #    self.___scan_current_village___()

    #def ___get_profile_info___(self):
    #    self.tribe, self.alliance = scrap_profile(self.navigator)

    def ___scan_current_village___(self):
        village_scrapper = VillageScrapper(self.game_session.server.url, self.driver, self.current_village_name,
                                           self.game_session.tribe, self.navigator)
        scrapped_village = village_scrapper.scrap_village(self.client)
        self.game_session.villages.append(scrapped_village)
