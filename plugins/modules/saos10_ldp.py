#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2025 Ciena
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
The module file for saos10_ldp
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: saos10_ldp
short_description: Ldp config container.Manage the ldp instance configuration of a Ciena saos10 device
description: "Ldp config container.\n Tag is default ldp instance."
author: Ciena
options:
  config:
    description: Tag is default ldp instance.
    type: list
    elements: dict
    suboptions:
      control_mode:
        description: Used for label processing. Ordered processing sets the mode to strict chain of command. An LSR replies to a request packet
          from an LSR higher in the chain only after it receives a label from an LSR lower in the chain. Independent processing sets the mode
          to instant replies.
        type: str
        required: false
        choices:
        - independent
        - ordered
      graceful_restart:
        description: LDP graceful restart capabilities.
        type: dict
        suboptions:
          enable:
            description: Enable or disable graceful restart, which is disabled by default.
            type: bool
            required: false
          helper_enable:
            description: Enable graceful restart helper mode, which is enabled by default.
            type: bool
            required: false
          timers:
            description: No description available
            type: dict
            suboptions:
              max_recovery:
                description: Configures the time the LSR is willing to retain its label-FEC bindings that it preserved across the restart. The
                  time is from the moment the LSR sends the Initialization message that carries the Fault Tolerant (FT) Session TLV after restart.
                  The actual time is the lesser of this timer value and the Recovery Time advertised by the neighbor in the FT Session TLV.
                type: int
                required: false
              neighbor_liveness:
                description: Configures the amount of time a neighbor should retain its label-FEC bindings until the restarting LSR is able to
                  exchange LDP messages again following a restart. The actual time is the lesser of this timer value and the Reconnect Timeout
                  value received in the neighbor's Fault Tolerant Session TLV.
                type: int
                required: false
      hello_holdtime:
        description: Hold-time specifies the time an LSR maintains its record of hellos from a peer on not receiving another hello from that peer.
        type: int
        required: false
      hello_interval:
        description: Hello interval in seconds. This is the value used to send hello messages.
        type: int
        required: false
      inter_area_lsp:
        description: Enable inter-area lsp which is disabled by default.
        type: bool
        required: false
      interfaces:
        description: Ldp interfaces container.
        type: dict
        suboptions:
          interface:
            description: Ldp interface config list.
            type: list
            elements: dict
            suboptions:
              enable_ipv4:
                description: Enabling LDP on ipv4 interface which is disabled by default.
                type: bool
                required: false
              hello_holdtime:
                description: Hold-time per interface specifies the time an LSR maintains its record of hellos from a peer on not receiving another
                  hello from that peer.
                type: int
                required: false
              hello_interval:
                description: Hello interval per interface in seconds. This is the value used to send hello messages.
                type: int
                required: false
              keepalive_interval:
                description: The Keepalive interval determines how often a message is sent over the session to ensure that the keepalive timeout
                  is not exceeded.If no LDP traffic is sent over the session in this much time,a keepalive message is sent.
                type: int
                required: false
              keepalive_timeout:
                description: After an Ldp session is established,messages must be exchanged periodically to ensure that the session is still working.The
                  keepalive timeout is the amount of time that the neighbor LDP node waits before deciding that the session is failed.
                type: int
                required: false
              ldp_igp_sync_delay_interval:
                description: This field is used to configure a synchronization delay interval, that is, a delay for notifications of LDP convergence
                  to the IGP protocol used, which can be either IS-IS or OSPF.
                type: int
                required: false
              name:
                description: 'Refers to L3 interface name. (Key for list: interface)'
                type: str
                required: true
            key: name
      keepalive_interval:
        description: The Keepalive interval determines how often a message is sent over the session to ensure that the keepalive timeout is not
          exceeded.If no LDP traffic is sent over the session in this much time,a keepalive message is sent.
        type: int
        required: false
      keepalive_timeout:
        description: After an Ldp session is established,messages must be exchanged periodically to ensure that the session is still working.The
          keepalive timeout is the amount of time that the neighbor LDP node waits before deciding that the session is failed.
        type: int
        required: false
      lsr_id:
        description: Specify the value to act as the LDP LSR ID.If this attribute is not specified, LDP uses the router ID as determined by the
          system.
        type: str
        required: false
      peers:
        description: Peers configuration attributes.
        type: dict
        suboptions:
          peer:
            description: List of peers.
            type: list
            elements: dict
            suboptions:
              lsr_id:
                description: 'The LSR ID of the peer, to identify the globally unique LSR. This is the first four octets of the LDP ID. (Key for
                  list: peer)'
                type: str
                required: true
              password:
                description: Assigns an encrypted MD5 password to an LDP peer
                type: str
                required: false
            key: lsr-id
      pw_status_tlv:
        description: Enabling pw-status-tlv to signal the pseudowire status which is disabled by default.
        type: bool
        required: false
      tag:
        description: 'Only the "default" instance is supported. (Key for list: instance)'
        type: str
        required: true
      target_ldp:
        description: Targeted Ldp container.
        type: dict
        suboptions:
          peers:
            description: A targeted session is an LDP session between non-directly connected LSRs.
            type: list
            elements: dict
            suboptions:
              address:
                description: 'Target address is targeted IPv4 LDP peer mode (Key for list: peers)'
                type: str
                required: true
              hello_holdtime:
                description: Target Hold-time specifies the time an LSR maintains its record of hellos from a peer on not receiving another hello
                  from that peer for target LDP. If not configured, default value is inherited from global value.
                type: int
                required: false
              hello_interval:
                description: Target Hello interval in seconds. This is the value used to send hello messages in target LDP. If not configured,
                  default value is inherited from global value.
                type: int
                required: false
            key: address
      targeted_hello_holdtime:
        description: The time interval for which an LDP targeted Hello adjacency is maintained in the absence of targeted Hello messages from
          an LDP neighbor
        type: int
        required: false
      targeted_hello_interval:
        description: The interval between consecutive LDP targeted Hello messages used in extended LDP discovery.
        type: int
        required: false
      transport:
        description: Ldp transport address config container.
        type: dict
        suboptions:
          address:
            description: The transport address advertised in LDP Hello messages.
            type: str
            required: false
    key: tag
  state:
    description:
    - The state of the configuration
    type: str
    choices:
    - merged
    - deleted
    default: merged

"""
EXAMPLES = """
"""

RETURN = """
before:
  description: The configuration prior to the model invocation.
  returned: always
  type: dict
  sample: >
    The configuration returned will always be in the same format
     of the parameters above.
after:
  description: The resulting configuration model invocation.
  returned: when changed
  type: dict
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
from ansible_collections.ciena.saos10.plugins.module_utils.network.saos10.argspec.ldp.ldp import (
    LdpArgs,
)
from ansible_collections.ciena.saos10.plugins.module_utils.network.saos10.config.ldp.ldp import (
    Ldp,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(argument_spec=LdpArgs.argument_spec, supports_check_mode=True)

    result = Ldp(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
