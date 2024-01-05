#
# (c) 2016 Red Hat Inc.
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

import sys
import copy

from ansible_collections.ansible.netcommon.plugins.action.network import (
    ActionModule as ActionNetworkModule,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    load_provider,
)
from ansible.utils.display import Display

display = Display()

CLI_SUPPORTED_MODULES = [
    "saos10_netconf",
    "saos10_ping",
    "saos10_command",
    "saos10_classifiers",
    "saos10_fds",
    "saos10_fps",
]


class ActionModule(ActionNetworkModule):
    def run(self, tmp=None, task_vars=None):
        del tmp  # tmp no longer has any effect

        module_name = self._task.action.split(".")[-1]
        self._config_module = True if module_name == "saos_config" else False
        persistent_connection = self._play_context.connection.split(".")[-1]
        warnings = []

        if persistent_connection in ("netconf", "network_cli"):
            provider = self._task.args.get("provider", {})
            if any(provider.values()):
                if not (module_name == "saos10_facts"):
                    display.warning(
                        "provider is unnecessary when using %s and will be ignored"
                        % self._play_context.connection
                    )
                    del self._task.args["provider"]

            if (
                persistent_connection == "network_cli"
                and module_name not in CLI_SUPPORTED_MODULES
            ) or (
                persistent_connection == "netconf"
                and module_name in CLI_SUPPORTED_MODULES[0:2]
            ):
                return {
                    "failed": True,
                    "msg": "Connection type '%s' is not valid for '%s' module. "
                    "Please see https://docs.ansible.com/ansible/latest/network/user_guide/platform_junos.html"
                    % (self._play_context.connection, module_name),
                }
        else:
            return {
                "failed": True,
                "msg": "Connection type %s is not valid for this module"
                % self._play_context.connection,
            }

        result = super(ActionModule, self).run(task_vars=task_vars)
        if warnings:
            if "warnings" in result:
                result["warnings"].extend(warnings)
            else:
                result["warnings"] = warnings
        return result
