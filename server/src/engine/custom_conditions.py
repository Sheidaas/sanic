class ExpectedUrl:

    def __init__(self, expected_url):
        self.expected_url = expected_url

    def __call__(self, driver):
        if driver.current_url == self.expected_url:
            return True
        return False
