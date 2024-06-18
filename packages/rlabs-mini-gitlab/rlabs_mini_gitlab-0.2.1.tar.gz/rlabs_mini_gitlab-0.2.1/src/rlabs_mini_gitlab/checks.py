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
    Checks
'''

from rlabs_mini_gitlab.error import MustCallConfigFirstError

def class_is_configured(
        cls,
    ) -> None:
    '''
        Class is Configured

        Checks if the class was configured by calling the config() method.

        Args:
            cls: The class to check.

        Raises:
            ValueError: If the class was not configured.
    '''
    if not cls._configured:
        raise MustCallConfigFirstError(
            cls.__name__
        )
