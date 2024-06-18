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
    Directory
'''
import shutil
from pathlib import Path

def remove_dir(dir: Path, recreate: bool = False):
    '''
        Remove directory. If recreate is True, create the directory
    '''
    if dir.exists():
        shutil.rmtree(dir)

    if recreate:
        dir.mkdir(
            parents=True,
            exist_ok=True
        )

def remove_file(file: Path, recreate: bool = False):
    '''
        Remove file. If recreate is True, create the file
    '''
    if file.exists():
        file.unlink()

    if recreate:
        file.touch()

def create_empty_dir(dir_path: Path) -> None:
    '''
        Creates empty directory at dir_path

        Replace the directory if it exists
    '''
    if dir_path.exists():
        shutil.rmtree(dir_path)

    dir_path.mkdir(
        parents=True,
        exist_ok=True
    )
