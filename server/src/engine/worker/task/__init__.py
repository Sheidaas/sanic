from queue import Queue


"""
TASK TYPES:
ACTIONS_CHAIN
DISCOVERY
"""


class Task:

    def __init__(self):
        self.id: str = ''
        self.name: str = ''
        self.description: str = ''
        self.position_in_queue: int = 0
        self.priority: int = 0
        self.type: str = ''
        self.status: str = ''
        # TODO: Queue max size configurable with __init__ parameter
        self.activities: Queue = Queue(maxsize=128)
        self.data: dict = dict(
            path='',
        )
        self.resolved_data: dict = dict(


        )

    def new(self):
        task = Task()
        attr_keys = self.__dict__.keys()

        for attr_key in attr_keys:
            setattr(task, attr_key, getattr(self, attr_key))

        return task
