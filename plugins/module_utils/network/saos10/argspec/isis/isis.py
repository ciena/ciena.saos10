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
The arg spec for the saos10_isis module
"""
from __future__ import absolute_import, division, print_function


__metaclass__ = type


class IsisArgs(object):  # pylint: disable=R0903
    """The arg spec for the saos10_isis module"""

    def __init__(self, **kwargs):
        pass

    argument_spec = {
        "config": {
            "type": "list",
            "elements": "dict",
            "options": {
                "tag": {"type": "str", "required": True},
                "admin_state": {"type": "bool"},
                "cspf_flag": {"type": "bool"},
                "distance": {"type": "int"},
                "distribute": {
                    "type": "dict",
                    "options": {
                        "bgp_ls_id": {"type": "int"},
                        "protocol": {"type": "str", "choices": ["bgp-ls"]},
                        "throttle": {"type": "int"},
                    },
                },
                "dynamic_hostname": {"type": "bool"},
                "fast_reroute": {
                    "type": "dict",
                    "options": {
                        "hold_timer": {"type": "int"},
                        "level": {
                            "type": "list",
                            "elements": "dict",
                            "options": {
                                "level_type": {"type": "str", "choices": ["level-1", "level-2"], "required": True},
                                "lfa": {
                                    "type": "dict",
                                    "options": {
                                        "per_prefix_enable": {"type": "bool"},
                                        "preference": {
                                            "type": "list",
                                            "elements": "dict",
                                            "options": {
                                                "address_family": {
                                                    "type": "str",
                                                    "choices": ["ipv4"],
                                                    "required": True,
                                                },
                                                "priority": {
                                                    "type": "list",
                                                    "elements": "dict",
                                                    "options": {
                                                        "tie_breaker": {
                                                            "type": "str",
                                                            "choices": [
                                                                "primary-path",
                                                                "node-protecting",
                                                                "secondary-path",
                                                                "downstream-path",
                                                            ],
                                                            "required": True,
                                                        },
                                                        "value": {"type": "int"},
                                                    },
                                                },
                                            },
                                        },
                                        "remote_lfa": {
                                            "type": "dict",
                                            "options": {
                                                "per_prefix_enable": {"type": "bool"},
                                                "protection": {
                                                    "type": "list",
                                                    "elements": "dict",
                                                    "options": {
                                                        "protection_type": {
                                                            "type": "str",
                                                            "choices": ["downstream-protection"],
                                                            "required": True,
                                                        },
                                                        "enable": {"type": "bool"},
                                                    },
                                                },
                                                "tunnel_cost": {"type": "int"},
                                            },
                                        },
                                        "ti_lfa": {"type": "dict", "options": {"per_prefix_enable": {"type": "bool"}}},
                                    },
                                },
                            },
                        },
                    },
                },
                "graceful_restart": {
                    "type": "dict",
                    "options": {
                        "helper_enable": {"type": "bool"},
                        "max_recovery_time": {"type": "int"},
                        "max_restart_time": {"type": "int"},
                        "restart_capable": {"type": "bool"},
                    },
                },
                "interfaces": {
                    "type": "dict",
                    "options": {
                        "interface": {
                            "type": "list",
                            "elements": "dict",
                            "options": {
                                "name": {"type": "str", "required": True},
                                "address_families": {
                                    "type": "dict",
                                    "options": {
                                        "address_family": {
                                            "type": "list",
                                            "elements": "dict",
                                            "options": {
                                                "afi": {"type": "str", "choices": ["ipv4", "ipv6"], "required": True},
                                                "safi": {"type": "str", "choices": ["unicast"], "required": True},
                                            },
                                        }
                                    },
                                },
                                "admin_state": {"type": "bool"},
                                "bfd": {"type": "dict", "options": {"enable": {"type": "bool"}}},
                                "bfd_ipv6": {"type": "dict", "options": {"enable_ipv6": {"type": "bool"}}},
                                "hello_padding": {"type": "bool"},
                                "interface_type": {"type": "str", "choices": ["broadcast", "point-to-point"]},
                                "ipv4_unicast_default_disable": {"type": "bool"},
                                "ldp_igp_sync": {
                                    "type": "list",
                                    "elements": "dict",
                                    "options": {
                                        "hold_down": {"type": "str", "required": True},
                                        "level_type": {
                                            "type": "str",
                                            "choices": ["level-1", "level-2", "level-1-2"],
                                            "required": True,
                                        },
                                    },
                                },
                                "level_1": {
                                    "type": "dict",
                                    "options": {
                                        "auth_type": {"type": "str", "choices": ["md5", "text"]},
                                        "csnp_interval": {"type": "int"},
                                        "gr_restart_hello_interval": {"type": "int"},
                                        "hello_interval": {"type": "int"},
                                        "hello_multiplier": {"type": "int"},
                                        "lfa_candidate_enable": {"type": "bool"},
                                        "metric": {"type": "int"},
                                        "password": {"type": "str", "no_log": True},
                                        "priority": {"type": "int"},
                                        "send_only": {"type": "bool"},
                                        "tag": {"type": "int"},
                                        "wide_metric": {"type": "int"},
                                    },
                                },
                                "level_2": {
                                    "type": "dict",
                                    "options": {
                                        "auth_type": {"type": "str", "choices": ["md5", "text"]},
                                        "csnp_interval": {"type": "int"},
                                        "gr_restart_hello_interval": {"type": "int"},
                                        "hello_interval": {"type": "int"},
                                        "hello_multiplier": {"type": "int"},
                                        "lfa_candidate_enable": {"type": "bool"},
                                        "metric": {"type": "int"},
                                        "password": {"type": "str", "no_log": True},
                                        "priority": {"type": "int"},
                                        "send_only": {"type": "bool"},
                                        "tag": {"type": "int"},
                                        "wide_metric": {"type": "int"},
                                    },
                                },
                                "level_type": {"type": "str", "choices": ["level-1", "level-2", "level-1-2"]},
                                "lsp_interval": {"type": "int"},
                                "lsp_retransmit_interval": {"type": "int"},
                            },
                        }
                    },
                },
                "ispf_levels": {"type": "str", "choices": ["level-1", "level-2", "level-1-2"]},
                "level_1": {
                    "type": "dict",
                    "options": {
                        "area_auth": {
                            "type": "dict",
                            "options": {
                                "auth_type": {"type": "str", "choices": ["md5", "text"]},
                                "password": {"type": "str", "no_log": True},
                                "send_only": {"type": "bool"},
                                "snp_auth": {"type": "bool"},
                            },
                        },
                        "lsp_gen_interval": {"type": "int"},
                        "lsp_mtu": {"type": "int"},
                        "recovery_time": {"type": "int"},
                        "spf_max_delay": {"type": "int"},
                        "spf_min_delay": {"type": "int"},
                    },
                },
                "level_2": {
                    "type": "dict",
                    "options": {
                        "domain_auth": {
                            "type": "dict",
                            "options": {
                                "auth_type": {"type": "str", "choices": ["md5", "text"]},
                                "password": {"type": "str", "no_log": True},
                                "send_only": {"type": "bool"},
                                "snp_auth": {"type": "bool"},
                            },
                        },
                        "lsp_gen_interval": {"type": "int"},
                        "lsp_mtu": {"type": "int"},
                        "recovery_time": {"type": "int"},
                        "spf_max_delay": {"type": "int"},
                        "spf_min_delay": {"type": "int"},
                    },
                },
                "level_type": {"type": "str", "choices": ["level-1", "level-2", "level-1-2"]},
                "lsp_lifetime": {"type": "int"},
                "lsp_refresh": {"type": "int"},
                "metric_style": {"type": "str", "choices": ["wide"]},
                "microloop_avoidance": {
                    "type": "dict",
                    "options": {"enable": {"type": "bool"}, "rib_update_delay": {"type": "int"}},
                },
                "mpls_te": {"type": "dict", "options": {"level_type": {"type": "str"}, "router_id": {"type": "str"}}},
                "multi_topology": {
                    "type": "list",
                    "elements": "dict",
                    "options": {
                        "level": {"type": "str", "choices": ["level-1", "level-2", "level-1-2"], "required": True},
                        "transition": {"type": "bool"},
                    },
                },
                "net": {"type": "list", "elements": "str"},
                "overload": {
                    "type": "dict",
                    "options": {
                        "on_startup": {"type": "str", "choices": ["wait-for-bgp", "time-out"]},
                        "suppress": {
                            "type": "str",
                            "choices": ["external", "interlevel", "external-interlevel", "interlevel-external"],
                        },
                        "timeout": {"type": "int"},
                    },
                },
                "passive": {
                    "type": "list",
                    "elements": "dict",
                    "options": {"passive_if_name": {"type": "str", "required": True}},
                },
                "proto_ipv4": {
                    "type": "dict",
                    "options": {
                        "redistribute": {
                            "type": "dict",
                            "options": {
                                "level": {
                                    "type": "list",
                                    "elements": "dict",
                                    "options": {
                                        "type": {"type": "str", "choices": ["1to2", "2to1"], "required": True},
                                        "prefix_list": {"type": "str"},
                                    },
                                },
                                "origin": {"type": "str", "choices": ["originate", "originate-always"]},
                                "policy": {"type": "str"},
                                "protocol": {
                                    "type": "list",
                                    "elements": "dict",
                                    "options": {
                                        "name": {
                                            "type": "str",
                                            "choices": ["connected", "static", "ospf", "bgp"],
                                            "required": True,
                                        },
                                        "level": {"type": "str", "choices": ["level-1", "level-2", "level-1-2"]},
                                        "metric": {"type": "int"},
                                        "policy": {"type": "str"},
                                    },
                                },
                            },
                        },
                        "summary_address": {
                            "type": "list",
                            "elements": "dict",
                            "options": {
                                "address": {"type": "str", "required": True},
                                "metric": {"type": "int", "required": True},
                                "level": {"type": "str", "choices": ["level-1", "level-2", "level-1-2"]},
                            },
                        },
                    },
                },
                "proto_ipv6": {
                    "type": "dict",
                    "options": {
                        "redistribute": {
                            "type": "dict",
                            "options": {
                                "adjacency_check": {"type": "bool"},
                                "distance": {"type": "int"},
                                "level": {
                                    "type": "list",
                                    "elements": "dict",
                                    "options": {
                                        "type": {"type": "str", "choices": ["1to2", "2to1"], "required": True},
                                        "prefix_list": {"type": "str"},
                                    },
                                },
                                "origin": {"type": "str", "choices": ["originate"]},
                                "policy": {"type": "str"},
                                "protocol": {
                                    "type": "list",
                                    "elements": "dict",
                                    "options": {
                                        "name": {
                                            "type": "str",
                                            "choices": ["connected", "static", "ospf", "bgp"],
                                            "required": True,
                                        },
                                        "level": {"type": "str", "choices": ["level-1", "level-2", "level-1-2"]},
                                        "metric": {"type": "int"},
                                        "policy": {"type": "str"},
                                    },
                                },
                            },
                        },
                        "summary_address": {
                            "type": "list",
                            "elements": "dict",
                            "options": {
                                "address": {"type": "str", "required": True},
                                "metric": {"type": "int", "required": True},
                                "level": {"type": "str", "choices": ["level-1", "level-2", "level-1-2"]},
                            },
                        },
                    },
                },
                "segment_routing": {
                    "type": "dict",
                    "options": {
                        "bindings": {
                            "type": "dict",
                            "options": {"advertise": {"type": "bool"}, "receive": {"type": "bool"}},
                        },
                        "enabled": {"type": "bool"},
                        "force_php": {"type": "dict", "options": {"enable": {"type": "bool"}}},
                        "srgb": {
                            "type": "list",
                            "elements": "dict",
                            "options": {
                                "lower_bound": {"type": "int", "required": True},
                                "upper_bound": {"type": "int", "required": True},
                            },
                        },
                    },
                },
            },
        },
        "state": {"type": "str", "default": "merged", "choices": ["merged", "deleted"]},
    }  # pylint: disable=C0301
