from ...utils import get_database


class Form:

    def __init__(self, raw_data: dict):
        self.raw_data = raw_data
        self.cleaned_instance = None
        self.errors: list[dict] = []

    async def save(self):
        return await get_database().insert(self.cleaned_instance)

    async def is_valid(self):
        return


