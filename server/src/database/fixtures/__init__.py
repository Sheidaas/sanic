import logging
import random
from ..models.travian_server import TravianServer
from ...utils.dictionaries import LOGGERS_NAMES
"""
This module provides methods to create advanced entities in database
"""
root_logger = logging.getLogger(LOGGERS_NAMES['ROOT'])
error_logger = logging.getLogger(LOGGERS_NAMES['ERROR'])


class Fixture:

    def __init__(self, _database):
        self.database = _database

    async def save(self, model_to_save) -> None:
        return await self.database.async_insert(model_to_save)


class TravianServerFixture(Fixture):

    PREPARED_DATA = [
        {
            'name': 'FIRST_TRAVIAN_SERVER_NAME',
            'url': 'FIRST_TRAVIAN_SERVER_URL',
            'speed': 1,
        },
        {
            'name': 'SECOND_TRAVIAN_SERVER_NAME',
            'url': 'SECOND_TRAVIAN_SERVER_URL',
            'speed': 2,
        },
        {
            'name': 'THIRD_TRAVIAN_SERVER_NAME',
            'url': 'THIRD_TRAVIAN_SERVER_URL',
            'speed': 3,
        }
    ]

    def prepare_model_from_dict(self, raw_dict: dict) -> TravianServer:
        name = raw_dict.get('name')
        url = raw_dict.get('url')
        speed = raw_dict.get('speed')

        if not name or not url or not speed:
            error_logger.info(f'TravianServer dict model is broken {name}, {url}, {speed}')
            raise AttributeError

        ts = TravianServer()
        ts.name = name
        ts.speed = speed
        ts.url = url
        return ts

    async def one(self, random_enitity=True, which_one_index=0, from_data=PREPARED_DATA):
        prepared_data_length = len(from_data)
        if which_one_index > len(from_data) - 1:
            error_logger.info(f'TravianServer fixture chosen data index {which_one_index} is bigger than prepared data length {prepared_data_length}')
            raise IndexError

        def get_index_of_chosen_entity() -> int:
            if which_one_index >= 0 and not random_enitity:
                return which_one_index
            return random.randrange(0, prepared_data_length)

        index_to_fixture = get_index_of_chosen_entity()
        entity_to_fixture = from_data[index_to_fixture]
        await self.save(self.prepare_model_from_dict(entity_to_fixture))

    async def some(self, how_many=4, from_data=PREPARED_DATA):
        prepared_data_length = len(from_data)

        for index, prepared_entity in enumerate(from_data):
            if index >= prepared_data_length:
                if prepared_data_length > how_many:
                    error_logger.info(f'TravianServer fixture prepared data ends at {index}, but user demands more {how_many}')
                    return
                return
            elif index >= how_many:
                return

            await self.save(self.prepare_model_from_dict(prepared_entity))
