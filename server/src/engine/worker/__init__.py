from selenium import webdriver
from .process import WorkerProcess
import undetected_chromedriver as uc
from ..navigator import Navigator
from ..services import Service
from ...utils import get_random_time
from ...utils.dictionaries import DRIVER_MODES, WORKER_STATES
from ...utils.worker import CONFIG, check_worker_starting_config_dictionary
import multiprocessing as mp
from multiprocessing.connection import Connection


class Worker:

    """
    self.state: one state of STATES

    self.: Interval, is checking two points of time, last finished task time and current
    self.last_time_finished_task:

    self.tasks:
    self.tasks_parent_conn:
    self.tasks_child_conn:
    self.process:

    self.navigator:
    self.driver: undetected.Chrome
    self.service:
    self.service_user:
    """

    def __init__(self, service, service_user, config=CONFIG) -> None:
        check_worker_starting_config_dictionary(config)

        self.id: str = config.get('worker_id')
        self.group: str = config.get('worker_group')
        self.state: str = WORKER_STATES['STOPPED']
        self.config: dict = config

        self.driver: uc.Chrome = self.get_driver(config.get('driver_mode'))
        self.service: Service = service
        self.service_user: ServiceUser = service_user
        self.navigator: Navigator | None = None

        self.tasks: list = []

        pipe = mp.Pipe()
        self.tasks_worker_to_process_conn: Connection = pipe[0]
        self.tasks_process_to_worker_conn: Connection = pipe[1]
        self.process: WorkerProcess = WorkerProcess(
            worker_id=self.id,
            worker_group=self.group,
            tasks_process_to_worker_conn=self.tasks_process_to_worker_conn,
            tasks_worker_to_process_conn=self.tasks_worker_to_process_conn,
        )

    @staticmethod
    def get_driver(driver_mode: str) -> uc.Chrome | webdriver.Chrome:
        options = webdriver.ChromeOptions
        options.headless = False
        options.add_argument("--window-size=1920x1080")
        options.add_argument("--disable-blink-features=AutomationControlled")
        if driver_mode == DRIVER_MODES['UNDETECTED']:
            '''
            options = uc.ChromeOptions()
            options.headless = False
            options.add_argument("--window-size=1920x1080")
            options.add_argument("--disable-blink-features=AutomationControlled")
            '''
            driver = uc.Chrome(options=options)
            driver.implicitly_wait(get_random_time(2, 7))
            return driver
        elif driver_mode == DRIVER_MODES['NORMAL']:
            driver = webdriver.Chrome(options=options)
            driver.implicitly_wait(get_random_time(2, 7))
            return driver
        else:
            raise AttributeError('driver not supported')

