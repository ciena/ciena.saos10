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
The module file for saos10_fds
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
module: saos10_fds
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
        description: A unique name for the forwarding domain
        type: str
        required: True
      mode:
        description: Forwarding mode of the forwarding-domain
        type: str
        choices:
          - vpls
          - vpws
          - fxc
          - tdm-vpls
          - tdm-vpws
          - evpn-vpws
          - evpn-vpls
      vlan-id:
        description: The id of VLAN associated with forwarding-domain.
        type: int
      pfg-profile:
        description: Reference to a Private Forwarding Group Profile.
        type: str
      initiate-l2-transform:
        description: For an L2-frame that is initiated/injected via this forwarding domain, this specifies the l2-transform to be applied to the frame.
          e.g. an L3-frame injected via this forwarding domain to L2 datapath.
        type: dict
        suboptions:
          vlan-stack:
            description: For an L2-frame that is initiated/injected via this forwarding domain, this specifies the VLAN related l2-transform to be
              applied to the frame.
            type: list
            elements: dict
            suboptions:
              tag:
                description: Dependent on the transform operation, the tag numbers are push => '1' represents push outermost, '2' represents push outermost
                  (always push to outer)
                type: int
              push-tpid:
                description: Represents the TPID value of the vlan tag for the tag being pushed
                type: str
                default: tpid-8100
                choices:
                  - tpid-8100
                  - tpid-88a8
                  - tpid-9100
              push-pcp:
                description: Represents the PCP value of the vlan tag for the tag being pushed. When the PCP value is mapped using a cos-to-frame-map,
                  'map' is specified.
                type: str
                choices:
                  - pcp-0
                  - pcp-1
                  - pcp-2
                  - pcp-3
                  - pcp-4
                  - pcp-5
                  - pcp-6
                  - pcp-7
                  - map
              push-dei:
                description: Represents the DEI value of the vlan tag for the tag being pushed.
                type: str
                choices:
                  - enabled
                  - disabled
              push-vid:
                description: Represents the VID value of the vlan tag for the tag being pushed
                type: str
                required: True
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

- name: Configure forwarding domain
  ciena.saos10.saos10_fds:
    config:
      - name: remote-fd
        mode: vpls
        initiate-l2-transform:
          vlan-stack:
            - tag: 1
              push-tpid: tpid-8100
              push-pcp: map
              push-vid: 127
    state: merged


# Using overridden

- name: Configure forwarding domain
  ciena.saos10.saos10_fds:
    config:
      - name: remote-fd
        mode: vpls
        initiate-l2-transform:
          vlan-stack:
            - tag: 1
              push-tpid: tpid-8100
              push-pcp: map
              push-vid: 127
    state: overridden


# Using deleted

- name: Delete forwading domain
  ciena.saos10.saos10_fds:
    config:
      - name: remote-fd
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
from ansible_collections.ciena.saos10.plugins.module_utils.network.saos10.argspec.fds.fds import (
    FdsArgs,
)
from ansible_collections.ciena.saos10.plugins.module_utils.network.saos10.config.fds.fds import (
    Fds,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=FdsArgs.argument_spec, supports_check_mode=True
    )

    result = Fds(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
