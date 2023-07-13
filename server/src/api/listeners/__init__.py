import logging
from sanic import Sanic
from ...utils.dictionaries import LOGGERS_NAMES
from ...utils.dictionaries.logs import SERVER_MESSAGES, ACCESS_MESSAGES, ROOT_MESSAGES, ERROR_MESSAGES
from ...database.models import Base


async def after_server_start(app: Sanic, *args, **kwargs):
    '''
    Checking loggers
    root = logging.getLogger(LOGGERS_NAMES['ROOT'])
    error = logging.getLogger(LOGGERS_NAMES['ERROR'])
    access = logging.getLogger('bot.access')
    server = logging.getLogger('bot.server')

    root.info(ROOT_MESSAGES['init'])
    error.info(ERROR_MESSAGES['init'])
    access.info(ACCESS_MESSAGES['init'])
    server.info(SERVER_MESSAGES['init'])
    '''
    root = logging.getLogger(LOGGERS_NAMES['ROOT'])
    root.info(f'Root path is {app.ctx.get("ROOT_PATH")}')

    tables = Base.metadata.tables.keys()
    root_logger = logging.getLogger(LOGGERS_NAMES['ROOT'])
    root_logger.info(f'Database tables are {tables}')
