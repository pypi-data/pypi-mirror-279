# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""libmonty - logging"""

# imports: library
import logging.config

# imports: project
from libmonty_logging import configs
from libmonty_logging import paths


def apply_config(config: dict) -> None:
    """Apply config to logging module"""

    logging.config.dictConfig(config)


def apply_default_console_only() -> None:
    """Apply config to logging module"""

    config: dict = configs.get(configs.Config.STDOUT_V1)
    apply_config(config)


def apply_default_console_and_file(program_name: str, program_version: str) -> None:
    """Apply config to logging module"""

    log_file_path: str = paths.get(
        paths.LogDirPath.XDG_STATE_HOME_WITH_NAME_V1,
        paths.LogFilename.NAME_DASH_VERSION_V1,
        program_name=program_name,
        program_version=program_version
    )
    config = configs.get(configs.Config.STDOUT_AND_FILE_V1, log_file_path=log_file_path)
    apply_config(config)
