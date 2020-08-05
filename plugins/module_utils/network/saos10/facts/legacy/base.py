# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The SAOS 10 Legacy fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type
import platform
import re
from ansible_collections.ciena.saos10.plugins.module_utils.network.saos10.saos10 import (
    run_commands,
    get_capabilities,
)
from ansible_collections.ciena.saos10.plugins.module_utils.network.saos10.utils.utils import (
    parse_cli_textfsm,
)


class FactsBase(object):

    COMMANDS = frozenset()

    def __init__(self, module):
        self.module = module
        self.facts = dict()
        self.warnings = list()
        self.responses = None

    def populate(self):
        self.responses = run_commands(
            self.module, commands=self.COMMANDS, check_rc=False
        )

    def run(self, cmd):
        return run_commands(self.module, commands=cmd, check_rc=False)


class Default(FactsBase):

    COMMANDS = ["show system components"]

    def populate(self):
        super(Default, self).populate()
        data = self.responses[0]
        self.facts["serialnum"] = self.parse_serialnum(data)
        self.facts.update(self.platform_facts())

    def parse_serialnum(self, data):
        match = re.search(r"\| serial-no +\| +(\S+)", data)
        if match:
            return match.group(1)

    def platform_facts(self):
        platform_facts = {}

        resp = get_capabilities(self.module)
        device_info = resp["device_info"]

        platform_facts["system"] = device_info["network_os"]

        for item in ("model", "image", "version", "platform", "hostname"):
            val = device_info.get("network_os_%s" % item)
            if val:
                platform_facts[item] = val

        platform_facts["api"] = resp["network_api"]
        platform_facts["python_version"] = platform.python_version()

        return platform_facts


class Config(FactsBase):

    COMMANDS = ["show running"]

    def populate(self):
        super(Config, self).populate()
        self.facts["config"] = self.responses[0]


class Interfaces(FactsBase):

    COMMANDS = ["show logical-ports state"]

    def populate(self):
        super(Interfaces, self).populate()

        fsm = r"""#
Value port (\S+)
Value AdminState (\S+)
Value MTU (\S+)
Value Description (\S+)
Value MacAddress (\S+)
Value OperState (\S+)

Start
  ^\| *Name *\| ${port}
  ^\| *Admin State *\| ${AdminState}
  ^\| *MTU *\| ${MTU}
  ^\| *Description *\| ${Description}
  ^\| *Mac Address *\| ${MacAddress}
  ^\| *Oper State *\| ${OperState} -> Record

EOF
"""
        interfaces = []
        ports = re.findall(
            r"^\| (\S+) +\| +[updown]+ +\|", self.responses[0], re.M
        )
        for port in ports:
            command = "show logical-ports logical-port %s" % port
            port_response = self.run([command])
            interface = parse_cli_textfsm(port_response[0], fsm)
            interfaces.append(interface[0])
        self.facts["interfaces"] = interfaces


class Neighbors(FactsBase):

    COMMANDS = ["show lldp", "show lldp neighbors"]

    def populate(self):
        super(Neighbors, self).populate()

        fsm = r"""#
Value localPort (\S+)
Value chassisId (\S+)
Value remotePort (\S+)
Value systemDesc (.+)
Value systemName (\S+)
Value mgmtAddr (\S+)

Start
  ^\| interface +\| ${localPort} +\|
  ^\| chassis\-id  +\| ${chassisId} +\|
  ^\| port\-id  +\| ${remotePort} +\|
  ^\| system\-description  +\| ${systemDesc} +\|
  ^\| system\-name  +\| ${systemName} +\|
  ^\| man\-address  +\| ${mgmtAddr} +\|
  ^\+[-]+ -> Record
"""

        show_lldp = self.responses[0]
        if "True" in show_lldp:
            neighbors = parse_cli_textfsm(self.responses[1], fsm)
            self.facts["neighbors"] = neighbors
