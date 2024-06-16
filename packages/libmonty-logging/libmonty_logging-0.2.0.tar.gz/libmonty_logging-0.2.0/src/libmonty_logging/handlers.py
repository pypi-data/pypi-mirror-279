# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Logging handlers"""

# imports: library
from enum import Enum


class Handler(Enum):
    """Enum of handlers"""
    STDOUT_V1 = 1
    FILE_V1 = 2


_configs: dict[Handler, dict[str, str]] = {
    Handler.STDOUT_V1: {
        'class': 'logging.StreamHandler',
        'level': 'INFO',
        'formatter': None,
        'stream': 'ext://sys.stdout'
    },
    Handler.FILE_V1: {
        'class': 'logging.FileHandler',
        'level': 'INFO',
        'formatter': None,
        'filename': None,
        'mode': 'w',
        'encoding': 'UTF-8'
    }
}


def get(identifier: Handler,
        formatter_name: str,
        filename: str = None
        ) -> tuple[str, dict[str, str]]:
    """Get formatter by identifier"""

    name: str = f'handler{identifier.value}'
    config: dict[str, str] = _configs[identifier]
    config['formatter'] = formatter_name
    if filename is not None:
        config['filename'] = filename

    for key, value in config.items():
        if value is None:
            raise ValueError(f'Value not set in handler config: "{key}"')

    return name, config
