# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Logging configs"""

# imports: library
from enum import Enum

# imports: project
from libmonty_logging import formatters
from libmonty_logging import handlers


class Config(Enum):
    """Enum of handlers"""
    STDOUT_AND_FILE_V1 = 1
    STDOUT_V1 = 2


def _template() -> dict:
    return {
        'version': 1,
        'formatters': {},
        'handlers': {},
        'loggers': {
            'root': {
                'level': 'NOTSET',
                'handlers': []
            }
        }
    }


def get(identifier: Config, log_file_path: str = None) -> dict:
    """Get config by identifier"""

    if identifier not in Config:
        raise ValueError(f'Unrecognized config identifier: "{identifier}"')

    chosen_formatters: dict[str, dict[str, str]] = {}
    chosen_handlers: dict[str, dict[str, str]] = {}
    constructed_config: dict = _template()

    if identifier in {Config.STDOUT_AND_FILE_V1, Config.STDOUT_V1}:
        formatter_name, formatter_config = formatters.get(
            formatters.Formatter.TIME_AND_LEVEL_8_V1
        )
        chosen_formatters[formatter_name] = formatter_config
        handler_name, handler_config = handlers.get(
            handlers.Handler.STDOUT_V1,
            formatter_name
        )
        chosen_handlers[handler_name] = handler_config

    if identifier in {Config.STDOUT_AND_FILE_V1}:
        if log_file_path is None:
            raise ValueError('Log file path required but not provided')

        formatter_name, formatter_config = formatters.get(
            formatters.Formatter.DATETIME_AND_LEVEL_8_V1
        )
        chosen_formatters[formatter_name] = formatter_config
        handler_name, handler_config = handlers.get(
            handlers.Handler.FILE_V1,
            formatter_name,
            filename=log_file_path
        )
        chosen_handlers[handler_name] = handler_config

    for formatter_name, formatter_config in chosen_formatters.items():
        constructed_config['formatters'][formatter_name] = formatter_config

    for handler_name, handler_config in chosen_handlers.items():
        constructed_config['handlers'][handler_name] = handler_config
        constructed_config['loggers']['root']['handlers'].append(handler_name)

    return constructed_config
