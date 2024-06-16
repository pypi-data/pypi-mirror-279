# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Logging formatters"""

# imports: library
from enum import Enum


class Formatter(Enum):
    """Enum of formatters"""
    TIME_AND_LEVEL_8_V1 = 1
    DATETIME_AND_LEVEL_8_V1 = 2


_configs: dict[Formatter, dict[str, str]] = {
    Formatter.TIME_AND_LEVEL_8_V1: {
        'format': '[%(asctime)s] [%(levelname)-8s] %(message)s',
        'datefmt': '%H:%M:%S'
    },
    Formatter.DATETIME_AND_LEVEL_8_V1: {
        'format': '[%(asctime)s] [%(levelname)-8s] %(message)s'
    },
}


def get(identifier: Formatter) -> tuple[str, dict[str, str]]:
    """Get formatter by identifier"""

    name: str = f'formatter{identifier.value}'
    config: dict[str, str] = _configs[identifier]

    return name, config
