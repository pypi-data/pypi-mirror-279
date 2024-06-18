#
# Copyright (C) 2024 RomanLabs, Rafael Roman Otero
# This file is part of RLabs Mini Gitlab.
#
# RLabs Mini Gitlab is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# RLabs Mini Gitlab is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with RLabs Mini Gitlab. If not, see <http://www.gnu.org/licenses/>.
#
'''
    Gitlab
'''
from typing import Optional
from typing import cast
from typing import ClassVar
from pathlib import Path
from typing import Type
from rlabs_mini_api.request import Request
import logging

from rlabs_mini_gitlab import logger
from rlabs_mini_gitlab.error import ConfigError
from rlabs_mini_gitlab.api.groups import Groups as GitlabGroups
from rlabs_mini_gitlab.api.projects import Projects as GitlabProjects

class Gitlab:
    '''
        Gitlab
    '''
    log_level: ClassVar[Optional[int]]
    logger: ClassVar[logging.Logger]
    response_log_dir: ClassVar[Optional[Path]] = None

    # make all Gitlab APIs available to the user
    Groups: ClassVar[Type[GitlabGroups]] = GitlabGroups
    Projects: ClassVar[Type[GitlabProjects]] = GitlabProjects

    def __init__(self) -> None:
        '''
            __init__
        '''
        pass

    @staticmethod
    def config(
        gitlab_url: str,
        gitlab_token: str,
        log_level: Optional[int] = None,
        logger_override: Optional[logging.Logger] = None,
        response_log_dir: Optional[Path] = None
    ) -> None:
        '''
            config

            Configures the Gitlab class.
        '''
        Gitlab.log_level = log_level
        Gitlab.response_log_dir = response_log_dir

        if response_log_dir is not None and not isinstance(response_log_dir, Path):
            raise ConfigError(
                "'response_log_dir' must be of type Path"
            )

        # Set up logging
        if log_level and logger_override:
            raise ValueError(
                "log_level and logger_override are mutually exclusive. "
                "Please provide one or the other."
            )

        if not log_level and not logger_override:
            raise ValueError(
                "log_level or logger_override must be provided."
            )

        if logger_override:
            Gitlab.logger = logger_override
            Gitlab.log_level = logger_override.getEffectiveLevel()
        else:
            Gitlab.logger = logger.stdout(
                __name__,
                cast(
                    int,
                    log_level
                )
            )
            Gitlab.log_level = log_level

        logger.enable_pretty_tracebacks()

        Request.config(
            base_url=gitlab_url,
            headers={
                "PRIVATE-TOKEN": gitlab_token
            },
            logger_override=Gitlab.logger,
            response_log_dir=Gitlab.response_log_dir
        )

        #
        # configure all APIs
        #
        Gitlab.Groups.config(
            logger=Gitlab.logger
        )
        Gitlab.Projects.config(
            logger=Gitlab.logger
        )




