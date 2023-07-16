from datetime import timedelta
from ..dictionaries import DRIVER_MODES, IMPLICITLY_WAIT_STATES


CONFIG = dict(
    worker_id='worker_id',
    worker_group='worker_group',
    no_tasks_time=timedelta(
        days=0,
        hours=0,
        minutes=5,
        seconds=0,
        milliseconds=0,
        microseconds=0
    ),
    driver_mode=DRIVER_MODES['UNDETECTED'],
    implicitly_wait_mode=IMPLICITLY_WAIT_STATES['RANDOM_FROM_RANGE'],
    times=dict(
        implicitly_wait_time=1.0,
        implicitly_wait_time_random_min=1.0,
        implicitly_wait_time_random_max=10.0,
    )
)


_REQUIRED_CONFIG_KEYS_AND_TYPES = dict(
    worker_id=str,
    worker_group=str,
    no_tasks_time=timedelta,
    driver_mode=str,
    implicitly_wait_mode=str,
    times=dict(
        implicitly_wait_time=float,
        implicitly_wait_time_random_min=float,
        implicitly_wait_time_random_max=float,
    )
)


def check_worker_starting_config_dictionary(config_dictionary: dict):
    _required_config_keys = _REQUIRED_CONFIG_KEYS_AND_TYPES.keys()
    for config_key, config_value in config_dictionary.items():
        if config_key not in _required_config_keys:
            raise Exception
        if _REQUIRED_CONFIG_KEYS_AND_TYPES[config_key] != type(config_value):
            raise Exception

    driver_mode = config_dictionary.get('driver_mode')
    if driver_mode not in DRIVER_MODES.values():
        raise Exception

    implicitly_wait_mode = config_dictionary.get('implicitly_wait_mode')
    if implicitly_wait_mode not in IMPLICITLY_WAIT_STATES.values():
        raise Exception

    return True

