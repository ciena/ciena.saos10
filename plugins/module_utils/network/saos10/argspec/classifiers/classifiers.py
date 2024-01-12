#
# -*- coding: utf-8 -*-
# Copyright 2023 Ciena
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
The arg spec for the saos10_classifiers module
"""
from __future__ import absolute_import, division, print_function


__metaclass__ = type


class ClassifiersArgs(object):  # pylint: disable=R0903
    """The arg spec for the saos10_classifiers module"""

    def __init__(self, **kwargs):
        pass

    argument_spec = {
        "config": {
            "type": "list",
            "elements": "dict",
            "options": {
                "filter_entry": {
                    "type": "list",
                    "elements": "dict",
                    "options": {
                        "any": {"type": "str"},
                        "base_ethertype": {"type": "int"},
                        "destination_address": {"type": "str"},
                        "destination_mac": {"type": "str"},
                        "destination_mac_mask": {"type": "str"},
                        "destination_max": {"type": "int"},
                        "destination_min": {"type": "int"},
                        "dscp_mask": {"type": "int"},
                        "dscp_max": {"type": "int"},
                        "dscp_min": {"type": "int"},
                        "filter_parameter": {"type": "str"},
                        "icmp_message_type": {
                            "type": "str",
                            "choices": [
                                "echo-reply",
                                "destination-unreachable",
                                "redirect-message",
                                "echo-request",
                                "router-advertisement",
                                "router-solicitation",
                                "time-exceeded",
                                "parameter-problem",
                                "timestamp",
                                "timestamp-reply",
                            ],
                        },
                        "icmp_type": {"type": "int"},
                        "internal_cos": {"type": "int"},
                        "internal_cos_mask": {"type": "int"},
                        "ip_fragment": {"type": "bool"},
                        "ip_version": {"type": "str", "choices": ["ipv4", "ipv6"]},
                        "l2cp_exclude_priority_tagged": {"type": "bool"},
                        "l4_application": {"type": "str", "choices": ["twamp"]},
                        "local_termination": {"type": "bool"},
                        "logical_not": {"type": "bool"},
                        "max_prot": {"type": "int"},
                        "min_prot": {"type": "int"},
                        "mpls_labels": {
                            "type": "list",
                            "elements": "dict",
                            "options": {
                                "label": {"type": "int"},
                                "label_any": {"type": "str"},
                                "mpls_label": {"type": "int"},
                                "tc_any": {"type": "str"},
                                "tc_value": {"type": "int"},
                            },
                        },
                        "source_address": {"type": "str"},
                        "source_mac": {"type": "str"},
                        "source_mac_mask": {"type": "str"},
                        "source_max": {"type": "int"},
                        "source_min": {"type": "int"},
                        "tcp_flags": {"type": "str"},
                        "untagged_exclude_priority_tagged": {"type": "bool"},
                        "vtags": {
                            "type": "list",
                            "elements": "dict",
                            "options": {
                                "dei": {"type": "str", "choices": ["discard-eligible", "not-discard-eligible"]},
                                "pcp": {"type": "int"},
                                "pcp_mask": {"type": "int"},
                                "tag": {"type": "int"},
                                "tpid": {"type": "str", "choices": ["tpid-8100", "tpid-88a8", "tpid-9100"]},
                                "vlan_id": {"type": "int"},
                                "vlan_id_max": {"type": "int"},
                            },
                        },
                    },
                },
                "filter_operation": {"type": "str", "choices": ["match-all", "match-any"]},
                "name": {"type": "str"},
            },
        }
    }  # pylint: disable=C0301
