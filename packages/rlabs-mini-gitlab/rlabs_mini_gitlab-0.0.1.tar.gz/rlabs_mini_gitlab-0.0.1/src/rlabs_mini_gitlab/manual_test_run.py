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
    Run Manual Test
    (entry point)

    For help type:
      poetry run manual-test-run --help

'''
import os
from pathlib import Path
import logging

from rlabs_mini_gitlab.gitlab import Gitlab

GITLAB_API_V4_URL = "https://gitlab.com/api/v4"
TOKEN = os.environ['TOKEN']
TEST_GROUP_RLABS_MINI_GITLAB_ID = 88902018
TEST_GROUP_ID = TEST_GROUP_RLABS_MINI_GITLAB_ID

def main():
    '''
        main
    '''
    Gitlab.config(
        gitlab_url=GITLAB_API_V4_URL,
        gitlab_token=TOKEN,
        log_level=logging.DEBUG,
        response_log_dir=Path("../logs")
    )

    #
    # GET /groups?search=Test&sort=desc
    #
    groups = (
        Gitlab.Groups.groups(
            search="Test",
            sort="desc",
            per_page=1
        )
        .select([
            "name"
        ])
        .map(
            lambda group: group['name']
        )
        .to_json(
            indent=2
        )
        .data()
    )

    print(
        groups
    )

    #
    # GET /groups/id/descendent_groups?order_by=name&sort=desc
    #
    descendent_groups = (
        Gitlab.Groups.descendent_groups(
            TEST_GROUP_ID,
            order_by="name",
            sort="desc",
            per_page=1
        )
        .select([
            "name",
        ])
        .map(
            lambda group: group['name']
        )
        .to_json(
            indent=2
        )
        .data()
    )

    print(
        descendent_groups
    )
    #
    # GET /groups/id/subgroups
    #
    subgroups = (
        Gitlab.Groups.subgroups(
            TEST_GROUP_ID,
            per_page=1
        )
        .select([
            "name"
        ])
        .map(
            lambda group: group['name']
        )
        .to_json(
            indent=2
        )
        .data()
    )

    print(
        subgroups
    )

    #
    # GET /groups/id/projects
    #
    projects = (
        Gitlab.Groups.projects(
            TEST_GROUP_ID,
            per_page=1
        )
        .select([
            "name"
        ])
        .map(
            lambda project: project['name']
        )
        .to_json(
            indent=2
        )
        .data()
    )
    print(
        projects
    )

    #
    # GET /projects
    #
    projects = (
        Gitlab.Projects.projects(
            visibility="private",
            per_page=1
        )
        .select([
            "name"
        ])
        .map(
            lambda project: project['name']
        )
        .to_json()
        .data()
    )


    print(
        projects
    )



