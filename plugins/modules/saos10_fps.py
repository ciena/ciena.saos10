#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2021 Ciena
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#############################################
#                WARNING                    #
#############################################
#
# This file is auto generated by the resource
#   module builder playbook.
#
# Do not edit this file manually.
#
# Changes to this file will be over written
#   by the resource module builder.
#
# Changes should be made in the model used to
#   generate this file or in the resource module
#   builder template.
#
#############################################

"""
The module file for saos10_fps
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "network",
}

DOCUMENTATION = """
---
module: saos10_fps
version_added: 1.5.0
short_description: Manage forwarding domains on Ciena SAOS 10 devices
description: This module provides declarative management of a forwarding domain
author: Ciena
requirements:
  - ncclient (>=v0.6.4)
  - xmltodict (>=0.12.0)
options:
  config:
    description: A dictionary of forwarding domain options
    type: list
    elements: dict
    suboptions:
      name:
        description: This object indicates the flow point identifier.
        type: str
        required: True
      logical-port:
        description: The logical-port associated with the flow-point.
        type: str
      fd-name:
        description: The name of the forwarding domain.
        type: str

  state:
    choices:
    - merged
    - overridden
    - deleted
    default: merged
    description:
    - The state the configuration should be left in
    type: str
"""
EXAMPLES = """
# Using merged

- name: Configure interfaces
  ciena.saos10.saos10_fps:
    config:
      - name: fp1
        fd-name: foo
        logical-port: 1
    state: merged


# Using overridden

- name: Configure interfaces
  ciena.saos10.saos10_fps:
    config:
      - name: fp1
        fd-name: foo
        logical-port: 1
    state: overridden


# Using deleted

- name: Configure interfaces
  ciena.saos10.saos10_fps:
    config:
      - name: fp1
    state: deleted


"""
RETURN = """
before:
  description: The configuration prior to the model invocation.
  returned: always
  sample: >
    The configuration returned will always be in the same format
     of the parameters above.
after:
  description: The resulting configuration model invocation.
  returned: when changed
  sample: >
    The configuration returned will always be in the same format
     of the parameters above.
xml:
  description: The set of xml commands pushed to the remote device.
  returned: always
  type: list
  sample: ['<system xmlns="http://openconfig.net/yang/system"><config><hostname>foo</hostname></config></system>']
"""


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ciena.saos10.plugins.module_utils.network.saos10.argspec.fps.fps import (
    FpsArgs,
)
from ansible_collections.ciena.saos10.plugins.module_utils.network.saos10.config.fps.fps import (
    Fps,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=FpsArgs.argument_spec, supports_check_mode=True
    )

    result = Fps(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
