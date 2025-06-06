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
The module file for saos10_classifiers
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: saos10_classifiers
short_description: List of classifier templates. Classifiers can be referenced by various entities (flow-point/access-flow/qos-flow etc.), to
  define their incoming classification.Manage the classifiers classifier configuration of a Ciena saos10 device
description: "List of classifier templates. Classifiers can be referenced by various entities (flow-point/access-flow/qos-flow etc.), to define\
  \ their incoming classification.\n List of classifier templates. Classifiers can be referenced by various entities (flow-point/access-flow/qos-flow\
  \ etc.) to define their incoming classification."
author: Ciena
options:
  config:
    description: List of classifier templates. Classifiers can be referenced by various entities (flow-point/access-flow/qos-flow etc.) to define
      their incoming classification.
    type: list
    elements: dict
    suboptions:
      filter_entry:
        description: Add one filtering rule for this classifier.
        type: list
        elements: dict
        suboptions:
          any:
            description: Accept any classification. Wide-Open classifier
            type: list
            required: false
            elements: str
            choices:
            - 'null'
          base_ethertype:
            description: Base Ethernet type.
            type: int
            required: false
          destination_address:
            description: Classification on IP destination-address (v4/v6) and masking.
            type: str
            required: false
          destination_mac:
            description: Destination MAC address.
            type: str
            required: false
          destination_mac_mask:
            description: The mask of destination MAC address.
            type: str
            required: false
          destination_max:
            description: Maximum value of L4 destination port number.
            type: int
            required: false
          destination_min:
            description: Exact/Minimum value of L4 destination port number.
            type: int
            required: false
          dscp_mask:
            description: Allow DSCP values to be optionally coupled with a mask in a single classifier. Mutually exclusive to dscp-max
            type: int
            required: false
          dscp_max:
            description: The maximum value of DSCP for ranged DSCP values in a single classifier. Mutually exclusive to dscp-mask
            type: int
            required: false
          dscp_min:
            description: The minimum value of DSCP.
            type: int
            required: false
          filter_parameter:
            description: 'Indicates which filter parameter is used by this filter entry (Key for list: filter-entry)'
            type: str
            required: true
            choices:
            - dscp
            - icmp
            - ip-protocol
            - tcp-flags
            - filter-param-type
            - internal-cos
            - l4-application
            - local-termination
            - ip-version
            - destination-ip
            - l4-destination-port
            - any
            - base-etype
            - destination-mac
            - vtag-stack
            - l4-source-port
            - source-ip
            - ip-fragment
            - source-mac
            - mpls-label
          icmp_message_type:
            description: ICMP Message type.
            type: str
            required: false
            choices:
            - echo-reply
            - destination-unreachable
            - redirect-message
            - echo-request
            - router-advertisement
            - router-solicitation
            - time-exceeded
            - parameter-problem
            - timestamp
            - timestamp-reply
          icmp_type:
            description: ICMP type.
            type: int
            required: false
          internal_cos:
            description: To specify the Internal Class-Of-Service for the classifier.
            type: int
            required: false
          internal_cos_mask:
            description: Allow internal-COS values to be optionally coupled with a mask in a single classifier.
            type: int
            required: false
          ip_fragment:
            description: IP-fragment bit true/false
            type: bool
            required: false
          ip_version:
            description: To specify the IP version for the classifier.
            type: str
            required: false
            choices:
            - ipv4
            - ipv6
          l2cp_exclude_priority_tagged:
            description: L2CP exclude priority tagged.
            type: bool
            required: false
          l4_application:
            description: L4 application.
            type: str
            required: false
            choices:
            - twamp
          local_termination:
            description: Classification of frames which are locally terminated.
            type: bool
            required: false
          logical_not:
            description: Opposite of what is specified in the filter-parameters. If the filter-parameter specifies a tpid as tpid-8100, then anything
              other than tpid-8100 is considered an acceptable packet.
            type: bool
            required: false
          max_prot:
            description: Maximum value of IP protocol.
            type: int
            required: false
          min_prot:
            description: Exact/Minimum value of IP protocol.
            type: int
            required: false
          mpls_labels:
            description: List of MPLS labels.
            type: list
            elements: dict
            suboptions:
              label:
                description: 'No description available (Key for list: mpls-labels)'
                type: int
                required: true
              label_any:
                description: Any value of mpls-label.
                type: list
                required: false
                elements: str
                choices:
                - 'null'
              mpls_label:
                description: A specific value of mpls-label.
                type: int
                required: false
              tc_any:
                description: Any value of mpls TC.
                type: list
                required: false
                elements: str
                choices:
                - 'null'
              tc_value:
                description: A specific value of mpls TC.
                type: int
                required: false
            key: label
          source_address:
            description: Classification on IP source-address (v4/v6) and masking.
            type: str
            required: false
          source_mac:
            description: Source MAC address.
            type: str
            required: false
          source_mac_mask:
            description: The mask of source MAC address.
            type: str
            required: false
          source_max:
            description: Maximum value of L4 source port number.
            type: int
            required: false
          source_min:
            description: Exact/Minimum value of L4 source port number.
            type: int
            required: false
          tcp_flags:
            description: List of TCP flags.
            type: list
            required: false
            elements: str
            choices:
            - fin
            - syn
            - rst
            - psh
            - ack
            - urg
            - ece
            - cwr
            - ns
          untagged_exclude_priority_tagged:
            description: Untagged exclude priority tagged.
            type: bool
            required: false
          vtags:
            description: List of VLAN tags.
            type: list
            elements: dict
            suboptions:
              dei:
                description: Discard Eligibility Indication
                type: str
                required: false
                choices:
                - discard-eligible
                - not-discard-eligible
              pcp:
                description: A specific value of VLAN Tag PCP.
                type: int
                required: false
              pcp_mask:
                description: Allow PCP values to be optionally coupled with a mask in a single classifier
                type: int
                required: false
              tag:
                description: '''1'' represents outer most tag, ''2'' next outer most, etc (Key for list: vtags)'
                type: int
                required: true
              tpid:
                description: A specific value of VLAN Tag EtherType.
                type: str
                required: false
                choices:
                - tpid-8100
                - tpid-88a8
                - tpid-9100
              vlan_id:
                description: A specific value of VLAN Tag VLAN-ID.
                type: int
                required: false
              vlan_id_max:
                description: The maximum value of VLAN ID for ranged VLAN-ID values.
                type: int
                required: false
            key: tag
        key: filter-parameter
      filter_operation:
        description: Choose the scope of application of the rule
        type: str
        required: false
        choices:
        - match-all
        - match-any
      name:
        description: 'A unique name for the classifier. (Key for list: classifier)'
        type: str
        required: true
    key: name
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
# Using merged

- name: Configure classifier
  ciena.saos10.saos10_classifiers:
    config:
      - name: untagged
        filter_entry:
          - filter_parameter: vtag-stack
            untagged_exclude_priority_tagged: false
      - name: foo-100
        filter_entry:
          - filter_parameter: vtag-stack
            vtags:
              - tag: 1
                vlan_id: 100
    state: merged
# Using deleted

- name: Delete classifier
  ciena.saos10.saos10_classifiers:
    config:
      - name: untagged
      - name: foo-100
    state: deleted
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
from ansible_collections.ciena.saos10.plugins.module_utils.network.saos10.argspec.classifiers.classifiers import (
    ClassifiersArgs,
)
from ansible_collections.ciena.saos10.plugins.module_utils.network.saos10.config.classifiers.classifiers import (
    Classifiers,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(argument_spec=ClassifiersArgs.argument_spec, supports_check_mode=True)

    result = Classifiers(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
