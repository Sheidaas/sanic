import datetime
from .process import WorkerProcess
import undetected_chromedriver as uc
from ..navigator import Navigator
from ..services import Service
from datetime import timedelta
from ...utils import get_random_time
from ...utils.dictionaries import DRIVER_MODES, WORKER_STATES, IMPLICITLY_WAIT_STATES
import multiprocessing as mp
from multiprocessing.connection import Connection


CONFIG = {
    'no_tasks_time': timedelta(days=0, hours=0, minutes=5, seconds=0, milliseconds=0, microseconds=0),
    'driver_mode': DRIVER_MODES['UNDETECTED'],
    'implicitly_wait_mode': IMPLICITLY_WAIT_STATES['RANDOM_FROM_RANGE'],
    'times': {
        'implicitly_wait_time': 1.0,
        'implicitly_wait_time_random_min': 1.0,
        'implicitly_wait_time_random_max': 10.0,
    }
}


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

    # TODO: VALIDATE CONFIG ON INIT
    def __init__(self, service, service_user, config=CONFIG) -> None:
        self.id: str = ''
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
            tasks_process_to_worker_conn=self.tasks_process_to_worker_conn,
            tasks_worker_to_process_conn=self.tasks_worker_to_process_conn,
        )


    @staticmethod
    def get_driver(driver_mode: str) -> uc.Chrome:
        if driver_mode == DRIVER_MODES['UNDETECTED']:
            options = uc.ChromeOptions()
            options.headless = False
            options.add_argument("--window-size=1920x1080")
            options.add_argument("--disable-blink-features=AutomationControlled")
            driver = uc.Chrome(options=options)
            driver.implicitly_wait(get_random_time(2, 7))
            return driver

        else:
            raise AttributeError('driver not supported')

