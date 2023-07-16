from queue import Queue
from multiprocessing import Process
from multiprocessing.connection import Connection


class WorkerProcess:

    def __init__(self,
                 worker_id: str,
                 worker_group: str,
                 tasks_worker_to_process_conn: Connection,
                 tasks_process_to_worker_conn: Connection):
        self.worker_id: str = worker_id
        self.worker_group: str = worker_group
        self.process: Process | None = None

        # TODO: Queue max size configurable with __init__ parameter
        self.tasks: Queue = Queue(maxsize=32)
        self.tasks_worker_to_process_conn: Connection = tasks_worker_to_process_conn
        self.tasks_process_to_worker_conn: Connection = tasks_process_to_worker_conn

    def start_process(self):
        self.process = Process(
            name=f'{self.worker_id}',
            group=f'{self.worker_group}',
            target=self._process_target
        )
        self.process.start()

    def join_process(self):
        self.process.join()
        # on_process_finish

    def receive_tasks(self):
        tasks = self.tasks_worker_to_process_conn.recv()
        for task in tasks:
            self.tasks.put(task)

    def update_task(self, task):
        return
        # self.tasks_process_to_worker_conn.send()

    def _process_target(self):
        # on_process_start
        while True:
            self.receive_tasks()

