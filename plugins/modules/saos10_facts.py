#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type
"""
The module file for saos10_facts
"""


DOCUMENTATION = """
module: saos10_facts
short_description: Get facts about saos10 devices.
description:
- Collects facts from network devices running the saos10 operating system. This module
  places the facts gathered in the fact tree keyed by the respective resource name.  The
  facts module will always collect a base set of facts from the device and can enable
  or disable collection of additional facts.
version_added: 1.0.0
author:
- Jeff Groom
notes:
- Tested against SAOS 10-4.
options:
  gather_subset:
    description:
    - When supplied, this argument will restrict the facts collected to a given subset.  Possible
      values for this argument include all, default, config, and neighbors. Can specify
      a list of values to include a larger subset. Values can also be used with an
      initial C(M(!)) to specify that a specific subset should not be collected.
    required: false
    default: '!config'
  gather_network_resources:
    description:
      - When supplied, this argument will restrict the facts collected
        to a given subset. Possible values for this argument include
        all and the resources like interfaces, vlans etc.
        Can specify a list of values to include a larger subset. Values
        can also be used with an initial C(M(!)) to specify that a
        specific subset should not be collected.
    required: false
"""

EXAMPLES = """
# Gather all facts
- saos10_facts:
    gather_subset: all
    gather_network_resources: all

# Collect only the classifiers facts
- saos10_facts:
    gather_subset:
      - !all
      - !min
    gather_network_resources:
      - classifiers

# Do not collect classifiers facts
- saos10_facts:
    gather_network_resources:
      - "!classifiers"

# Collect classifiers and minimal default facts
- saos10_facts:
    gather_subset: min
    gather_network_resources: classifiers
"""

RETURN = """
ansible_net_config:
  description: The running-config from the device
  returned: when config is configured
  type: str
ansible_net_model:
  description: The device model string
  returned: always
  type: str
ansible_net_serialnum:
  description: The serial number of the device
  returned: always
  type: str
ansible_net_version:
  description: The version of the software running
  returned: always
  type: str
ansible_net_neighbors:
  description: The set of LLDP neighbors
  returned: when interface is configured
  type: list
ansible_net_gather_subset:
  description: The list of subsets gathered by the module
  returned: always
  type: list
ansible_net_api:
  description: The name of the transport
  returned: always
  type: str
ansible_net_python_version:
  description: The Python version Ansible controller is using
  returned: always
  type: str
ansible_net_gather_network_resources:
  description: The list of fact resource subsets collected from the device
  returned: always
  type: list
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ciena.saos10.plugins.module_utils.network.saos10.argspec.facts.facts import (
    FactsArgs,
)
from ansible_collections.ciena.saos10.plugins.module_utils.network.saos10.facts.facts import (
    Facts,
)


def main():
    """
    Main entry point for module execution

    :returns: ansible_facts
    """

    module = AnsibleModule(
        argument_spec=FactsArgs.argument_spec, supports_check_mode=True
    )

    warnings = []
    if module.params["gather_subset"] == "!config":
        warnings.append(
            "default value for `gather_subset` will be changed to `min` from `!config` v2.11 onwards"
        )

    result = Facts(module).get_facts()

    ansible_facts, additional_warnings = result
    warnings.extend(additional_warnings)

    module.exit_json(ansible_facts=ansible_facts, warnings=warnings)


if __name__ == "__main__":
    main()
