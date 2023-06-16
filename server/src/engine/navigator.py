import random
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.common.exceptions import InvalidArgumentException, WebDriverException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

from ..utils.exceptions import InternalSeleniumException
from ..utils import URLS
from .custom_conditions import ExpectedUrl


class Navigator:

    def __init__(self, driver: Firefox, game_session):
        self.driver = driver
        self.username = game_session.username
        self.password = game_session.password
        self.server = game_session.server.url
        self.paths = {
            URLS['LOGIN']: {
                URLS['RESOURCES']: self.login_to_game,
            },
            URLS['RESOURCES']: {
                URLS['PROFILE']: self.go_to_profile,
                URLS['HERO']: self.go_to_hero_profile,
                URLS['INSIDE_VILLAGE']: self.go_to_village_center,
            }
        }

    @property
    def current_url(self) -> str:
        return self.driver.current_url

    @staticmethod
    def get_random_time() -> int:
        return random.randint(1, 10)

    def login_to_game(self):
        action_chain = ActionChains(self.driver)
        try:
            self.driver.get(self.server + URLS['LOGIN'])
        except (InvalidArgumentException, WebDriverException):
            raise InternalSeleniumException('invalid server url or server is not reachable')

        try:
            username_input = self.driver.find_element(By.NAME, 'name')
            password_input = self.driver.find_element(By.NAME, 'password')
            login_button = self.driver.find_element(By.ID, 'loginForm').find_element(By.TAG_NAME, 'button')
        except NoSuchElementException:
            raise InternalSeleniumException('login form isn\'t found')

        action_chain.click(username_input)
        action_chain.pause(self.get_random_time())
        action_chain.send_keys(self.username)
        action_chain.pause(self.get_random_time())
        action_chain.click(password_input)
        action_chain.pause(self.get_random_time())
        action_chain.send_keys(self.password)
        action_chain.pause(self.get_random_time())
        action_chain.click(login_button)
        action_chain.perform()

        try:
            WebDriverWait(self.driver, 5).until(ExpectedUrl(self.server + URLS['RESOURCES']))
        except Exception:
            raise InternalSeleniumException('invalid credentials')

    def go_to_profile(self):
        if self.server not in self.current_url:
            raise InternalSeleniumException('not even in travian')

        if self.current_url == self.server + URLS['PROFILE']:
            return

        try:
            self.driver.get(self.server + URLS['PROFILE'])
        except (InvalidArgumentException, WebDriverException):
            raise InternalSeleniumException('invalid server url or server is not reachable')

        try:
            WebDriverWait(self.driver, 5).until(ExpectedUrl(self.server + URLS['PROFILE']))
        except Exception:
            raise InternalSeleniumException('after click at profile button session isn\'t in profile url')

        action_chains = ActionChains(self.driver)
        action_chains.pause(2)
        action_chains.perform()

    def go_to_hero_profile(self):
        if self.server not in self.current_url:
            raise InternalSeleniumException('not even in travian')

        if self.current_url == self.server + URLS['HERO']:
            return

        try:
            hero_image_button = self.driver.find_element(By.ID, 'heroImageButton')
        except NoSuchElementException:
            raise InternalSeleniumException('login form isn\'t found')

        action_chains = ActionChains(self.driver)
        action_chains.click(hero_image_button)
        action_chains.pause(2)
        action_chains.perform()

    def go_to_resources(self):
        if self.server not in self.current_url:
            raise InternalSeleniumException('not even in travian')

        if self.current_url == self.server + URLS['RESOURCES']:
            return

        try:
            resources_button = self.driver.find_element(By.ID, 'navigation').find_element(By.CLASS_NAME, 'resourceView')
        except NoSuchElementException:
            raise InternalSeleniumException('resources button isn\'t found')

        action_chains = ActionChains(self.driver)
        action_chains.click(resources_button)
        action_chains.pause(2)
        action_chains.perform()

    def go_to_village_center(self):
        if self.server not in self.current_url:
            raise InternalSeleniumException('not even in travian')

        if self.current_url == self.server + URLS['INSIDE_VILLAGE']:
            return

        try:
            building_button = self.driver.find_element(By.ID, 'navigation').find_element(By.CLASS_NAME, 'buildingView')
        except NoSuchElementException:
            raise InternalSeleniumException('building button isn\'t found')

        action_chains = ActionChains(self.driver)
        action_chains.click(building_button)
        action_chains.pause(2)
        action_chains.perform()

    def open_solar(self, solar_id):
        if self.server not in self.current_url:
            raise InternalSeleniumException('not even in travian')

        if 0 < solar_id < 19:
            self.go_to_resources()
        elif 19 <= solar_id < 41:
            self.go_to_village_center()
        else:
            raise InternalSeleniumException(f'cant find solar {solar_id}')

        try:
            if self.current_url == self.server + URLS['INSIDE_VILLAGE']:
                solar_button = self.driver.find_element(By.ID, 'villageContent').\
                    find_element(By.CLASS_NAME, 'a'+str(solar_id))
            else:
                solar_button = self.driver.find_element(By.CLASS_NAME, f'buildingSlot{solar_id}')
        except NoSuchElementException:
            raise InternalSeleniumException('solar button isn\'t found')

        action_chains = ActionChains(self.driver)
        action_chains.click(solar_button)
        action_chains.pause(2)
        action_chains.perform()

    def upgrade_field(self, construction_site_id: int):
        self.open_solar(construction_site_id)
        button = self.driver.find_element(By.CLASS_NAME, 'upgradeBuilding').find_element(By.CLASS_NAME, 'section1').\
            find_element(By.TAG_NAME, 'button')
        action_chains = ActionChains(self.driver)
        action_chains.click(button)
        action_chains.perform()

    def open_new_building_category(self, field_id: int, category_index: int):
        self.open_solar(field_id)

        category_buttons = self.driver.find_elements(By.CLASS_NAME, 'content')
        category_button = category_buttons[category_index]

        action_chains = ActionChains(self.driver)
        action_chains.click(category_button)
        action_chains.pause(2)
        action_chains.perform()

        if self.current_url != self.server + URLS['BUILD'] + str(field_id) + '&category=' + str(category_index):
            raise InternalSeleniumException('invalid category when building new building')

    def build_new_building(self, field_id: int, new_building_id: int, category_index: int):
        self.open_new_building_category(field_id, category_index)

        new_building_button = self.driver.find_element(By.ID, 'contract_building' + str(new_building_id)).\
            find_element(By.TAG_NAME, 'button')

        action_chains = ActionChains(self.driver)
        action_chains.reset_actions()
        action_chains.click(new_building_button)
        action_chains.perform()

    def switch_hero_production(self, new_resource: str):
        self.go_to_hero_profile()

        resources = ['everything', 'Wood', 'Clay', 'Iron', 'Crop']
        resources_buttons_names = ['resourceHero0', 'resourceHero1', 'resourceHero2', 'resourceHero3', 'resourceHero4']

        button_id = resources_buttons_names[resources.index(new_resource)]

        checkbox_to_check = self.driver.find_element(By.ID, button_id)

        action_chains = ActionChains(self.driver)

        action_chains.click(checkbox_to_check)
        action_chains.pause(2)
        action_chains.perform()

    def go_to_hero_adventures(self):
        hero_top_bar = self.driver.find_element(By.ID, 'topBarHero')
        adventure_button = hero_top_bar.find_element(By.CLASS_NAME, 'adventure')

        action_chains = ActionChains(self.driver)
        action_chains.click(adventure_button)
        action_chains.perform()

    def send_hero_to_adventure(self, adventure_id: int):
        self.go_to_hero_adventures()

        start_adventure_button = self.driver.find_element(By.ID, 'goToAdventure'+str(adventure_id)).\
            find_element(By.TAG_NAME, 'a')

        if start_adventure_button.get_attribute('disabled'):
            raise InternalSeleniumException('adventure is disabled, hero is busy')

        action_chains = ActionChains(self.driver)
        action_chains.click(start_adventure_button)
        action_chains.pause(2)
        action_chains.perform()

    def upgrade_hero_attribute(self, attribute: str):
        self.go_to_hero_profile()

        #attributes = ['attributepower', 'attributeoffBonus', 'attributedefBonus', 'attributeproductionPoints']
        #if attribute not in attributes:
        #    return

        upgrade_button = self.driver.find_element(By.ID, attribute).\
            find_element(By.CLASS_NAME, 'add').find_element(By.TAG_NAME, 'a')

        save_button = self.driver.find_element(By.ID, 'saveHeroAttributes')

        action_chains = ActionChains(self.driver)
        action_chains.click(upgrade_button)
        action_chains.pause(2)
        action_chains.click(save_button)
        action_chains.perform()
