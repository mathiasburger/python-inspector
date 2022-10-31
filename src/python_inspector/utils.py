#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) nexB Inc. and others. All rights reserved.
# ScanCode is a trademark of nexB Inc.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/nexB/python-inspector for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#

import json
import os
from typing import Dict
from typing import List
from typing import NamedTuple

import requests


def get_netrc_auth(url, netrc):
    """
    Return login and password if url is in netrc
    else return login and password as None
    """
    if netrc.get(url):
        return (netrc[url].get("login"), netrc[url].get("password"))
    return (None, None)


def contain_string(string: str, files: List) -> bool:
    """
    Return True if the ``string`` is contained in any of the ``files`` list of file paths.
    """
    for file in files:
        if not os.path.exists(file):
            continue
        with open(file, encoding="utf-8") as f:
            # TODO also consider other file names
            if string in f.read():
                return True
    return False


def write_output_in_file(output, location):
    """
    Write headers, requirements and resolved_dependencies as JSON to ``json_output``.
    Return the output data.
    """
    json.dump(output, location, indent=2)
    return output


class Candidate(NamedTuple):
    """
    A candidate is a package that can be installed.
    """

    name: str
    version: str
    extras: str


def get_response(url: str) -> Dict:
    """
    Return a mapping of the JSON response from fetching ``url``
    or None if the ``url`` cannot be fetched..
    """
    resp = requests.get(url)
    if resp.status_code == 200:
        return resp.json()
