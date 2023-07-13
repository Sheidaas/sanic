from .pages import Page


class Service:

    def __init__(self, name: str):
        self.name: str = name
        self.pages: list[Page] = []
