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
    error.py
'''
from rlabs_mini_gitlab import logger

class PrettyError(Exception):
    '''
        Custom Base Error

        This is the base class for all custom errors.

        Pretty Logs error to stdout and exits with -1
    '''
    def __init__(self, msg: str):
        super().__init__(msg)

class ConfigError(PrettyError):
    '''
        ConfigError
    '''
    def __init__(self, msg: str) -> None:
        super().__init__(msg)

class MustCallConfigFirstError(PrettyError):
    '''
        MustCallConfigFirstError
    '''
    def __init__(self, class_name: str) -> None:
        super().__init__(
            f"class '{class_name}' must be configured before use. "
            f"This error occurs when the class 'Gitlab' is not configured, "
            f"since Gitlab's config configures {class_name}. \n\n"
            f"Please Call 'Gitlab.config(...)' first."
        )
