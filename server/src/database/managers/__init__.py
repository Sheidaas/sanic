from typing import Callable
from sqlalchemy.orm import Session


class Manager:
    def __init__(self, get_session_function: Callable) -> None:
        self.get_session: Callable[[], Session] = get_session_function
