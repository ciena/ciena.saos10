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
from ansible.plugins.netconf import NetconfBase, ensure_ncclient
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.netconf import (
    remove_namespaces,
)

try:
    from ncclient.operations import RPCError
    from ncclient.xml_ import to_ele, to_xml

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
        device_info = {}
        device_info["network_os"] = "waveserver5"
        filter = """
        <filter>
            <components xmlns="http://openconfig.net/yang/platform"/>
            <system xmlns="http://openconfig.net/yang/system">
                <config>
                    <hostname/>
                </config>
            </system>
        </filter>
        """
        filter = to_ele(filter)
        response = self.get(filter=filter, remove_ns=True)
        root = to_ele(response)
        model = self._extract_xpath(root, "//component[name='Waveserver']/state/description")
        network_os_version = self._extract_xpath(root, "//component[name='CM-1']/state/software-version")
        hostname = self._extract_xpath(root, "/data/system/config/hostname")
        serial_number = self._extract_xpath(root, "//component[name='Waveserver']/state/serial-no")
        platform = self._extract_xpath(root, "//component[name='Waveserver']/state/id")

        device_info["network_os_platform"] = platform
        device_info["network_os_serialnum"] = serial_number
        device_info["network_os_hostname"] = hostname
        device_info["network_os_version"] = network_os_version
        device_info["network_os_model"] = model

        return device_info

    def get(self, filter=None, with_defaults=None, remove_ns=False):
        if isinstance(filter, list):
            filter = tuple(filter)
        try:
            resp = self.m.get(filter=filter, with_defaults=with_defaults)
            if remove_ns:
                response = remove_namespaces(resp)
            else:
                response = resp.data_xml if hasattr(resp, "data_xml") else resp.xml
            return response
        except RPCError as exc:
            raise Exception(to_xml(exc.xml))

    def _extract_xpath(self, root, xpath_str, default=None):
        """Extract data using XPath and return text or default."""
        result = root.xpath(xpath_str)
        return result[0].text if result else default
