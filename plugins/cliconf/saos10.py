# (c) 2020 Red Hat Inc.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
name: saos10
author:
  - Jeff Groom (@jgroom33)
short_description: Use saos10 cliconf to run command on Ciena saos10 platform
description:
  - This saos10 plugin provides low level abstraction apis for
    sending and receiving CLI commands from Ciena saos10 network devices.
"""

import re
import json
import time
from itertools import chain

from ansible.errors import AnsibleConnectionFailure
from ansible.module_utils.common._collections_compat import Mapping
from ansible.module_utils._text import to_text
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    to_list,
)
from ansible.plugins.cliconf import CliconfBase


# SAOS 10 prompt forms (see plugins/terminal/saos10.py):
#   - Operator:    "<host>> "                 (top level, the desired "root")
#   - Config:      "<user>@<host># "          (one or more levels deep)
#   - Diag shell:  "diag@<host>$ "            (lower-level shell; user-entered)
# Nested config sub-modes also share the trailing "# " and may add "(...)"
# context segments. We treat any prompt that does NOT end with "> " (and is not
# a diag shell "$") as "needs an exit to reach the operator prompt".
_ROOT_PROMPT_RE = re.compile(rb"[>\$]\s*$")


class Cliconf(CliconfBase):
    def __init__(self, *args, **kwargs):
        super(Cliconf, self).__init__(*args, **kwargs)
        self._device_info = {}

    def _ensure_root_prompt(self, max_attempts=4):
        """Send 'exit' until the prompt is at the SAOS operator level ("> ").

        SAOS logs the user out if 'exit' is issued at the operator prompt, so
        we never send 'exit' once the prompt already ends with "> ". The diag
        shell ("$") is treated as root too -- the user explicitly entered it
        and we should not be sending CLI commands from inside cliconf anyway.
        """
        for _attempt in range(max_attempts):
            prompt = self._connection.get_prompt()
            if not prompt:
                return
            if _ROOT_PROMPT_RE.search(prompt):
                return
            self.send_command("exit")
        prompt = self._connection.get_prompt()
        if prompt and not _ROOT_PROMPT_RE.search(prompt):
            raise AnsibleConnectionFailure(
                "Unable to recover SAOS10 operator prompt after %d 'exit' attempts; "
                "current prompt=%r" % (max_attempts, prompt)
            )

    def get_device_info(self):
        if self._device_info:
            return self._device_info
        self._ensure_root_prompt()
        device_info = {}
        device_info["network_os"] = "ciena.saos10.saos10"
        reply = self.get("software show")
        data = to_text(reply, errors="surrogate_or_strict").strip()

        match = re.search(r"Running package version +\: (\S+)", data)
        if match:
            device_info["network_os_version"] = match.group(1).strip(",")
        time.sleep(0.2)
        reply = self.get("show system components")
        data = to_text(reply, errors="surrogate_or_strict").strip()

        model_search = re.search(r"^\| name +\| (\S+)", data)
        if model_search:
            device_info["network_os_model"] = model_search.group(1)

        self._device_info = device_info
        return device_info

    def get_config(self, source="running", flags=None, format="text"):
        self._ensure_root_prompt()
        cmd = "show running"
        out = self.send_command(cmd)
        return out

    def edit_config(self, command):
        self._ensure_root_prompt()
        for cmd in chain(["config"], to_list(command), ["exit"]):
            self.send_command(cmd)

    def get_capabilities(self):
        result = super(Cliconf, self).get_capabilities()
        return json.dumps(result)

    def get(
        self,
        command=None,
        prompt=None,
        answer=None,
        sendonly=False,
        newline=True,
        output=None,
        check_all=False,
    ):
        if not command:
            raise ValueError("must provide value of command to execute")
        if output:
            raise ValueError("'output' value %s is not supported for get" % output)

        return self.send_command(
            command=command,
            prompt=prompt,
            answer=answer,
            sendonly=sendonly,
            newline=newline,
            check_all=check_all,
        )

    def run_commands(self, commands=None, check_rc=True):
        if commands is None:
            raise ValueError("'commands' value is required")

        self._ensure_root_prompt()
        responses = list()
        for cmd in to_list(commands):
            if not isinstance(cmd, Mapping):
                cmd = {"command": cmd}

            output = cmd.pop("output", None)
            if output:
                raise ValueError("'output' value %s is not supported for run_commands" % output)

            try:
                out = self.send_command(**cmd)
            except AnsibleConnectionFailure as e:
                if check_rc:
                    raise
                out = getattr(e, "err", e)

            responses.append(out)

        return responses
