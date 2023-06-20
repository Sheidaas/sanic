class InternalSeleniumException(Exception):

    def __init__(self, error: dict[str, str]):
        self.error = error
