import logging
from sanic.request import Request


async def log_request(request: Request) -> None:
    logger = logging.getLogger('bot.server')

    logger.info(f'URL: {request.url}')
    logger.info(f'Request METHOD: {request.method}')
    logger.info(f'Request IP: {request.ip}')
    logger.info(f'Request HEADER: {request.headers}')
    logger.info(f'Request BODY: {request.body}')
    logger.info(f'--------------------------------')
