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
    remove_ns,
)

from ansible_collections.ansible.netcommon.plugins.module_utils.network.netconf.netconf import (
    get,
)

try:
    from lxml.etree import tostring as xml_to_string

    HAS_LXML = True
except ImportError:
    from xml.etree.ElementTree import (
        tostring as xml_to_string,
    )

    HAS_LXML = False


class FactsBase(object):

    COMMANDS = frozenset()

    def __init__(self, module):
        self.module = module
        self.facts = dict()
        self.warnings = list()
        self.responses = None

    def tostring(element, encoding="UTF-8"):
        if HAS_LXML:
            return xml_to_string(element, encoding="unicode")
        else:
            return to_text(xml_to_string(element, encoding), encoding=encoding)

    def populate(self):
        raise NotImplementedError


class Default(FactsBase):
    def populate(self):
        self.facts.update(self.platform_facts())
        config_filter = (
            '<components xmlns="http://openconfig.net/yang/platform"/>'
        )
        reply = get(self.module, filter=("subtree", config_filter))
        root = remove_ns(reply)
        serial_number = root.xpath(
            "/data/components/component[1]/state/serial-no"
        )[0].text
        model = root.xpath(
            "/data/components/component[1]/component-properties/component-property[name = 'hw-model']/value"
        )[0].text
        platform = root.xpath("/data/components/component[1]/state/name")[
            0
        ].text
        self.facts["serialnum"] = serial_number
        self.facts["model"] = model
        self.facts["platform"] = platform

        config_filter = '<software-state xmlns="http://www.ciena.com/ns/yang/ciena-software-mgmt"/>'
        reply = get(self.module, filter=("subtree", config_filter))
        root = remove_ns(reply)
        network_os_version = root.xpath(
            "/data/software-state/running-package/package-version"
        )[0].text
        self.facts["version"] = network_os_version

        config_filter = '<system xmlns="http://openconfig.net/yang/system"><config><hostname/></config></system>'
        reply = get(self.module, filter=("subtree", config_filter))
        root = remove_ns(reply)
        hostname = root.xpath("/data/system/config/hostname")[0].text
        self.facts["hostname"] = hostname

    def platform_facts(self):
        platform_facts = {}

        resp = get_capabilities(self.module)
        device_info = resp["device_info"]

        platform_facts["system"] = device_info["network_os"]

        for item in ("image", "version", "hostname"):
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
            config = xml_to_string(remove_ns(reply))

        elif config_format == "text":
            raise Exception("text Not yet Implemented")

        elif config_format == "json":
            raise Exception("json Not yet Implemented")

        self.facts["config"] = config
