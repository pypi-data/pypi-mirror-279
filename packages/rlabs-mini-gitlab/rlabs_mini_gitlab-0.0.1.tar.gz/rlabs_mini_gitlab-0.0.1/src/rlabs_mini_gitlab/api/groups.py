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
    Groups API

    /groups

    https://docs.gitlab.com/ee/api/groups.html
'''
import logging
import inspect
from logging import getLogger
from typing import ClassVar
from typing import Any
from rlabs_mini_api.request import GET
from rlabs_mini_box.data import Box

from rlabs_mini_gitlab import checks
from rlabs_mini_gitlab import api_kwargs
from rlabs_mini_gitlab import config as global_config


class Groups:
    '''
        Groups
    '''
    logger: ClassVar[logging.Logger] = getLogger("dummy")   # dummy logger to avoid type errors
                                                            # will never be used
    _configured: ClassVar[bool] = False

    @classmethod
    def config(
        cls,
        logger: logging.Logger
    ) -> None:
        '''
            config

            Configures the class logger
        '''
        cls.logger = logger
        cls._configured = True

    @classmethod
    def groups(
            cls,
            per_page: int = global_config.per_page_default,
            **kwargs: Any,
        ) -> Box:
        '''
            Groups

            GET /groups
        '''
        checks.class_is_configured(
            cls
        )

        cls.logger.info(
            "Getting groups"
        )

        api_kwargs.remove_current_function_params(
            cls,
            kwargs
        )

        collected: list = []
        page = 1

        while True:

            kwargs.update({
                "per_page": per_page,
                "page": page
            })

            response = (
                GET
                    .groups(**kwargs)
                    .exec(3,2)
            )

            if not response.python_data:
                    break

            collected += response.python_data
            page += 1

        return Box(collected)

    @classmethod
    def descendent_groups(
            cls,
            group_id: int,
            per_page: int = global_config.per_page_default,
            **kwargs: Any,
        ) -> Box:
        '''
            Descendent Groups

            GET /groups/:id/descendant_groups
        '''
        checks.class_is_configured(
            cls
        )

        cls.logger.info(
            "Getting descendant groups for group with ID: %s",
            group_id
        )

        api_kwargs.remove_current_function_params(
            cls,
            kwargs
        )

        collected: list = []
        page = 1

        while True:

            kwargs.update({
                "per_page": per_page,
                "page": page
            })

            response = (
                GET
                    .groups
                    .id(group_id)
                    .descendant_groups(**kwargs)
                    .exec(3,2)
            )

            if not response.python_data:
                break

            collected += response.python_data
            page += 1

        return Box(collected)

    @classmethod
    def subgroups(
            cls,
            group_id: int,
            per_page: int = global_config.per_page_default,
            **kwargs: Any,
        ) -> Box:
        '''
            Subgroups

            GET /groups/:id/subgroups
        '''
        checks.class_is_configured(
            cls
        )

        cls.logger.info(
            "Getting subgroups for group with ID: %s",
            group_id
        )

        api_kwargs.remove_current_function_params(
            cls,
            kwargs
        )

        collected: list = []
        page = 1

        while True:

            kwargs.update({
                "per_page": per_page,
                "page": page
            })

            response = (
                GET
                    .groups
                    .id(group_id)
                    .subgroups(**kwargs)
                    .exec(3,2)
            )

            if not response.python_data:
                break

            collected += response.python_data
            page += 1

        return Box(collected)

    @classmethod
    def projects(
            cls,
            group_id: int,
            per_page: int = global_config.per_page_default,
            **kwargs: Any,
        ) -> Box:
        '''
            Projects

            GET /groups/:id/projects
        '''
        checks.class_is_configured(
            cls
        )

        cls.logger.info(
            "Getting projects for group with ID: %s",
            group_id
        )

        api_kwargs.remove_current_function_params(
            cls,
            kwargs
        )

        collected: list = []
        page = 1

        while True:

            kwargs.update({
                "per_page": per_page,
                "page": page
            })

            response = (
                GET
                    .groups
                    .id(group_id)
                    .projects(**kwargs)
                    .exec(3,2)
            )

            if not response.python_data:
                break

            collected += response.python_data
            page += 1

        return Box(collected)






