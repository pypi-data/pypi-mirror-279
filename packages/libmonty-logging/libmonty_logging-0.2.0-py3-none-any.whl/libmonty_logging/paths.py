# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Logging formatters"""

# imports: library
from enum import Enum
import os.path
from typing import Callable

# imports: dependencies
from xdg_base_dirs import xdg_state_home


class LogDirPath(Enum):
    """Enum of formatters"""
    XDG_STATE_HOME_WITH_NAME_V1 = 1


def _xdg_state_home_with_name_v1(**kwargs) -> str:
    """Get state dir path, create if non-existent"""

    if 'program_name' not in kwargs:
        raise KeyError('"program_name" not given for dir path')

    state_dir_path = os.path.join(xdg_state_home(), kwargs['program_name'])

    if not os.path.isdir(state_dir_path):
        os.makedirs(state_dir_path, mode=0o740, exist_ok=True)

    return state_dir_path


_constructors_dir_path: dict[LogDirPath, Callable] = {
    LogDirPath.XDG_STATE_HOME_WITH_NAME_V1: _xdg_state_home_with_name_v1,
}


class LogFilename(Enum):
    """Enum of formatters"""
    NAME_DASH_VERSION_V1 = 1


def _name_dash_version_v1(**kwargs) -> str:
    """Construct log file name"""

    if 'program_name' not in kwargs:
        raise KeyError('"program_name" not given for dir path')

    if 'program_version' not in kwargs:
        raise KeyError('"program_version" not given for dir path')

    return f'{kwargs["program_name"]}-{kwargs["program_version"]}.log'


_constructors_filename: dict[LogFilename, Callable] = {
    LogFilename.NAME_DASH_VERSION_V1: _name_dash_version_v1,
}


def get(id_dir_path: LogDirPath, id_filename: LogFilename, **kwargs) -> str:
    """Get formatter by identifier"""

    dir_path: str = _constructors_dir_path[id_dir_path](**kwargs)
    filename: str = _constructors_filename[id_filename](**kwargs)

    return os.path.join(dir_path, filename)
