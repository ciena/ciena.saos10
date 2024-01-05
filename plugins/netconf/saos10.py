from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
author:
  - Jeff Groom (@jgroom33)
netconf: saos10
short_description: Use saos10 netconf plugin to run netconf commands on Ciena saos10
  platform
description:
- This saos10 plugin provides low level abstraction apis for sending and receiving
  netconf commands from Ciena saos10 network devices.
version_added: 1.0.0
options:
  ncclient_device_handler:
    type: str
    default: default
    description:
    - Specifies the ncclient device handler name for Ciena saos10 network os. To
      identify the ncclient device handler name refer ncclient library documentation.
"""

import json
import re

from ansible.module_utils._text import to_text, to_native
from ansible.errors import AnsibleConnectionFailure
from ansible.plugins.netconf import NetconfBase, ensure_ncclient

try:
    from ncclient import manager
    from ncclient.transport.errors import SSHUnknownHostError

    HAS_NCCLIENT = True
except (
    ImportError,
    AttributeError,
):  # paramiko and gssapi are incompatible and raise AttributeError not ImportError
    HAS_NCCLIENT = False


class Netconf(NetconfBase):
    def get_text(self, ele, tag):
        try:
            return to_text(ele.find(tag).text, errors="surrogate_then_replace").strip()
        except AttributeError:
            pass

    def get_capabilities(self):
        result = dict()
        result["rpc"] = self.get_base_rpc() + [
            "commit",
            "discard_changes",
            "lock",
            "unlock",
            "execute_rpc",
            "load_configuration",
            "get_configuration",
            "reboot",
            "halt",
        ]
        result["network_api"] = "netconf"
        result["device_info"] = self.get_device_info()
        result["server_capabilities"] = list(self.m.server_capabilities)
        result["client_capabilities"] = list(self.m.client_capabilities)
        result["session_id"] = self.m.session_id
        result["device_operations"] = self.get_device_operations(
            result["server_capabilities"]
        )
        return json.dumps(result)

    @ensure_ncclient
    def get_device_info(self):
        device_info = dict()
        device_info["network_os"] = "saos10"
        return device_info

    @staticmethod
    @ensure_ncclient
    def guess_network_os(obj):
        """
        Guess the remote network os name
        :param obj: Netconf connection class object
        :return: Network OS name
        """
        try:
            m = manager.connect(
                host=obj._play_context.remote_addr,
                port=obj._play_context.port or 830,
                username=obj._play_context.remote_user,
                password=obj._play_context.password,
                key_filename=obj.key_filename,
                hostkey_verify=obj.get_option("host_key_checking"),
                look_for_keys=obj.get_option("look_for_keys"),
                allow_agent=obj._play_context.allow_agent,
                timeout=obj.get_option("persistent_connect_timeout"),
                # We need to pass in the path to the ssh_config file when guessing
                # the network_os so that a jumphost is correctly used if defined
                ssh_config=obj._ssh_config,
            )
        except SSHUnknownHostError as exc:
            raise AnsibleConnectionFailure(to_native(exc))

        guessed_os = None
        for c in m.server_capabilities:
            if re.search("saos-10", c):
                guessed_os = "saos10"

        m.close_session()
        return guessed_os
