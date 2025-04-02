#
# -*- coding: utf-8 -*-
# Copyright 2025 Ciena
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The saos10_fps class
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to it's desired end-state is
created
"""
from __future__ import absolute_import, division, print_function


__metaclass__ = type

try:
    from lxml.etree import tostring as xml_to_string, Element

    HAS_LXML = True
except ImportError:
    from xml.etree.ElementTree import Element
    from xml.etree.ElementTree import tostring as xml_to_string

    HAS_LXML = False


from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.cfg.base import (
    ConfigBase,
)
from ansible_collections.ciena.saos10.plugins.module_utils.network.saos10.facts.facts import (
    Facts,
)
from ansible_collections.ciena.saos10.plugins.module_utils.network.saos10.utils.utils import (
    config_is_diff,
)

NAMESPACE = "urn:ciena:params:xml:ns:yang:ciena-pn:ciena-mef-fp"
ROOT_KEY = "fps"
RESOURCE = "fps"
XML_ITEMS = "fp"
XML_ITEMS_KEY = "name"


class Fps(ConfigBase):
    """
    The saos10_fps class
    """

    gather_subset = ["!all", "!min"]
    gather_network_resources = [RESOURCE]

    def __init__(self, module):
        super(Fps, self).__init__(module)

    def get_facts(self):
        """Get the 'facts' (the current configuration)

        :rtype: A dictionary
        :returns: The current configuration as a dictionary
        """
        facts, _warnings = Facts(self._module).get_facts(self.gather_subset, self.gather_network_resources)
        result = facts["ansible_network_resources"].get(RESOURCE)
        if not result:
            return []
        return result

    def execute_module(self):
        """Execute the module

        :rtype: A dictionary
        :returns: The result from module execution
        """
        result = {"changed": False}
        have = self.get_facts()
        config_dict = self.set_config(have)

        if config_dict:
            config_xml = self._create_xml_config_generic(config_dict)
            config = '<nc:config xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">' f"{config_xml}" "</nc:config>"
            try:
                self._module._connection.edit_config(config=config, target="running")
            except Exception as e:
                return {"failed": True, "msg": str(e)}

            result["changed"] = True
            result["xml"] = config_xml

        changed_facts = self.get_facts()

        result["changed"] = config_is_diff(have, changed_facts)

        result["before"] = have
        if self.state in self.ACTION_STATES:
            if result["changed"]:
                result["after"] = changed_facts

        elif self.state == "gathered":
            result["gathered"] = have

        return result

    def set_config(self, have):
        """Collect the configuration from the args passed to the module,
            collect the current configuration (as a dict from facts)

        :rtype: A list
        :returns: the commands necessary to migrate the current configuration
                  to the desired configuration
        """
        want = self._module.params["config"]
        state = self._module.params["state"]
        state_methods = {
            "merged": self._state_merged,
            "deleted": self._state_deleted,
        }
        config_dict = state_methods[state](want, have) if state in self.ACTION_STATES else {}
        return config_dict

    def _populate_xml_subtree(self, parent: Element, data: dict):
        for key, value in data.items():
            sanitized_key = key.replace("_", "-")
            if isinstance(value, dict):
                subelem = Element(sanitized_key)
                self._populate_xml_subtree(subelem, value)
                parent.append(subelem)
            elif isinstance(value, list):
                for list_item in value:
                    subelem = Element(sanitized_key)
                    self._populate_xml_subtree(subelem, list_item)
                    parent.append(subelem)
            else:
                subelem = Element(sanitized_key)
                subelem.text = str(value)
                if value is not None:
                    parent.append(subelem)

    def _create_xml_config_generic(self, config_dict_or_list):
        if isinstance(config_dict_or_list, dict):
            return self.create_xml_config_from_dict(config_dict_or_list)
        elif isinstance(config_dict_or_list, list):
            return self.create_xml_config_from_list(config_dict_or_list)
        else:
            raise TypeError(f"Expected a dictionary or a list, got a {type(config_dict_or_list)}")

    def _init_xml_root(self):
        return Element("{%s}%s" % (NAMESPACE, ROOT_KEY), nsmap={None: NAMESPACE})

    def create_xml_config_from_dict(self, config_dict: dict) -> str:
        root = self._init_xml_root()
        self._populate_xml_subtree(root, config_dict)
        return xml_to_string(root).decode()

    def create_xml_config_from_list(self, config_list: list) -> str:
        root = self._init_xml_root()
        for list_item in config_list:
            if not isinstance(list_item, dict):
                raise ValueError("List items must be dictionaries.")
            subroot = Element(XML_ITEMS)
            operation = list_item.pop("operation", None)
            self._populate_xml_subtree(subroot, list_item)
            if operation:
                subroot.set("operation", operation)
            root.append(subroot)
        return xml_to_string(root).decode()

    def _state_merged(self, want, have):
        if isinstance(want, list):
            return self._state_merged_list(want, have)
        elif isinstance(want, dict):
            return self._state_merged_dict(want, have)

    def _state_merged_dict(self, want, have) -> dict:
        response = {}
        for key, value in want.items():
            if value is None:
                continue
            if key in have and have[key] == value:
                continue
            response[key] = value
        return response

    def _state_merged_list(self, want, have) -> list:
        response = []
        for w_item in want:
            if w_item in have:
                continue
            response.append(w_item)
        return response

    def _state_deleted(self, want, have):
        response = []
        if not want:
            want = have
        for config in want:
            response.append({"name": config["name"], "operation": "delete"})
        return response
