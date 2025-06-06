#
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
The arg spec for the saos10_mpls module
"""
from __future__ import absolute_import, division, print_function


__metaclass__ = type


class MplsArgs(object):  # pylint: disable=R0903
    """The arg spec for the saos10_mpls module"""

    def __init__(self, **kwargs):
        pass

    argument_spec = {
        "config": {
            "type": "dict",
            "options": {
                "interfaces": {
                    "type": "dict",
                    "options": {
                        "interface": {
                            "type": "list",
                            "elements": "dict",
                            "options": {"name": {"type": "str", "required": True}, "label_switching": {"type": "bool"}},
                        }
                    },
                },
                "label_management": {
                    "type": "dict",
                    "options": {
                        "allocation_mode": {
                            "type": "dict",
                            "options": {
                                "all_vrfs": {
                                    "type": "dict",
                                    "options": {
                                        "address_family": {
                                            "type": "list",
                                            "elements": "dict",
                                            "options": {
                                                "af_type": {
                                                    "type": "str",
                                                    "choices": ["ipv4", "ipv6"],
                                                    "required": True,
                                                },
                                                "mode": {"type": "str", "choices": ["per-prefix", "per-vrf"]},
                                            },
                                        }
                                    },
                                },
                                "vrf": {
                                    "type": "list",
                                    "elements": "dict",
                                    "options": {
                                        "name": {"type": "str", "required": True},
                                        "address_family": {
                                            "type": "list",
                                            "elements": "dict",
                                            "options": {
                                                "af_type": {
                                                    "type": "str",
                                                    "choices": ["ipv4", "ipv6"],
                                                    "required": True,
                                                },
                                                "mode": {"type": "str", "choices": ["per-prefix", "per-vrf"]},
                                            },
                                        },
                                    },
                                },
                            },
                        },
                        "label_blocks": {
                            "type": "dict",
                            "options": {
                                "label_block": {
                                    "type": "list",
                                    "elements": "dict",
                                    "options": {
                                        "index": {"type": "int", "required": True},
                                        "protocol": {
                                            "type": "list",
                                            "elements": "dict",
                                            "options": {
                                                "end_label": {"type": "int", "required": True},
                                                "name": {
                                                    "type": "str",
                                                    "choices": [
                                                        "ldp",
                                                        "bgp",
                                                        "default",
                                                        "rsvp",
                                                        "srgb",
                                                        "srlb",
                                                        "static-vc",
                                                        "static-tunnel",
                                                    ],
                                                    "required": True,
                                                },
                                                "start_label": {"type": "int", "required": True},
                                            },
                                        },
                                    },
                                }
                            },
                        },
                    },
                },
                "tunnel_statistics": {
                    "type": "dict",
                    "options": {
                        "entry": {
                            "type": "list",
                            "elements": "dict",
                            "options": {
                                "fec_address": {"type": "str", "required": True},
                                "owner": {"type": "str", "choices": ["ldp", "bgp", "bgp_lu", "sr"], "required": True},
                                "role": {"type": "str", "choices": ["ingress", "transit"], "required": True},
                            },
                        }
                    },
                },
            },
        },
        "state": {"type": "str", "default": "merged", "choices": ["merged", "deleted"]},
    }  # pylint: disable=C0301
