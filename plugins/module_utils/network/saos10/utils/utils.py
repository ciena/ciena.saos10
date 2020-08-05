#
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# utils

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.errors import AnsibleError
from ansible.module_utils.six import string_types
import io

try:
    import textfsm

    HAS_TEXTFSM = True
except ImportError:
    HAS_TEXTFSM = False


def parse_cli_textfsm(value, template):
    if not HAS_TEXTFSM:
        raise AnsibleError(
            "parse_cli_textfsm filter requires TextFSM library to be installed"
        )

    if not isinstance(value, string_types):
        raise AnsibleError(
            "parse_cli_textfsm input should be a string, but was given a input of %s"
            % (type(value))
        )

    temp = template.decode("utf-8")

    re_table = textfsm.TextFSM(io.StringIO(temp))
    fsm_results = re_table.ParseText(value)

    results = list()
    for item in fsm_results:
        results.append(dict(zip(re_table.header, item)))

    return results
