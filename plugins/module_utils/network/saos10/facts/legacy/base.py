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
from ansible.module_utils._text import to_text

__metaclass__ = type
import platform
from ansible_collections.ciena.saos10.plugins.module_utils.network.saos10.saos10 import (
    get_configuration,
    get_capabilities,
)

try:
    from lxml.etree import tostring as xml_to_string

    HAS_LXML = True
except ImportError:
    from xml.etree.ElementTree import tostring as xml_to_string

    HAS_LXML = False


class FactsBase(object):
    COMMANDS = frozenset()

    def __init__(self, module):
        self.module = module
        self.facts = dict()
        self.warnings = list()
        self.responses = None

    def tostring(self, element, encoding="UTF-8"):
        if HAS_LXML:
            return xml_to_string(element, encoding="unicode")
        else:
            return to_text(xml_to_string(element, encoding), encoding=encoding)

    def populate(self):
        raise NotImplementedError


class Default(FactsBase):
    def populate(self):
        self.facts.update(self.platform_facts())

    def platform_facts(self):
        platform_facts = {}

        resp = get_capabilities(self.module)
        device_info = resp["device_info"]

        platform_facts["system"] = device_info["network_os"]

        for item in ("image", "model", "version", "hostname", "platform", "serialnum"):
            val = device_info.get("network_os_%s" % item)
            if val:
                platform_facts[item] = val

        platform_facts["api"] = resp["network_api"]
        platform_facts["python_version"] = platform.python_version()

        return platform_facts


class Config(FactsBase):
    def populate(self):
        config_format = self.module.params["config_format"]
        config_format = "xml"
        reply = get_configuration(self.module, format="xml")

        if config_format == "xml":
            config = xml_to_string(reply)

        elif config_format == "text":
            raise Exception("text Not yet Implemented")

        elif config_format == "json":
            raise Exception("json Not yet Implemented")

        self.facts["config"] = config
