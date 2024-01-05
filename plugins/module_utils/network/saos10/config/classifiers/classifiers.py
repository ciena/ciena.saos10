#
# -*- coding: utf-8 -*-
# Copyright 2021 Ciena
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The saos10_classifiers class
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to it's desired end-state is
created
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.cfg.base import (
    ConfigBase,
)
from ansible.module_utils._text import to_text, to_bytes

from ansible_collections.ciena.saos10.plugins.module_utils.network.saos10.saos10 import (
    xml_to_string,
    fromstring,
)

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    to_list,
)
from ansible_collections.ciena.saos10.plugins.module_utils.network.saos10.facts.facts import (
    Facts,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.netconf import (
    remove_namespaces,
    build_root_xml_node,
    build_child_xml_node,
)

from ansible_collections.ciena.saos10.plugins.module_utils.network.saos10.utils.utils import (
    config_is_diff,
)


class Classifiers(ConfigBase):
    """
    The saos10_classifiers class
    """

    gather_subset = ["!all", "!min"]
    gather_network_resources = ["classifiers"]

    def __init__(self, module):
        super(Classifiers, self).__init__(module)

    def get_classifiers_facts(self):
        """ Get the 'facts' (the current configuration)

        :rtype: A dictionary
        :returns: The current configuration as a dictionary
        """
        facts, _warnings = Facts(self._module).get_facts(
            self.gather_subset, self.gather_network_resources
        )
        classifiers_facts = facts["ansible_network_resources"].get("classifiers")
        if not classifiers_facts:
            return []
        return classifiers_facts

    def execute_module(self):
        """ Execute the module

        :rtype: A dictionary
        :returns: The result from module execution
        """
        result = {"changed": False}
        existing_classifiers_facts = self.get_classifiers_facts()
        config_xmls = self.set_config(existing_classifiers_facts)

        for config_xml in to_list(config_xmls):
            config = f'<config>{config_xml.decode("utf-8")}</config>'
            kwargs = {
                "config": config,
                "target": "running",
                "default_operation": "merge",
                "format": "xml",
            }

            self._module._connection.edit_config(**kwargs)

        result["xml"] = config_xmls
        changed_classifiers_facts = self.get_classifiers_facts()

        result["changed"] = config_is_diff(
            existing_classifiers_facts, changed_classifiers_facts
        )

        result["before"] = existing_classifiers_facts
        if result["changed"]:
            result["after"] = changed_classifiers_facts

        return result

    def set_config(self, existing_classifiers_facts):
        """ Collect the configuration from the args passed to the module,
            collect the current configuration (as a dict from facts)

        :rtype: A list
        :returns: the commands necessary to migrate the current configuration
                  to the desired configuration
        """
        want = self._module.params["config"]
        have = existing_classifiers_facts
        resp = self.set_state(want, have)
        return to_list(resp)

    def set_state(self, want, have):
        """ Select the appropriate function based on the state provided

        :param want: the desired configuration as a dictionary
        :param have: the current configuration as a dictionary
        :rtype: A list
        :returns: the commands necessary to migrate the current configuration
                  to the desired configuration
        """
        root = build_root_xml_node("classifiers")
        state = self._module.params["state"]
        if state == "overridden":
            config_xmls = self._state_overridden(want, have)
        elif state == "deleted":
            config_xmls = self._state_deleted(want, have)
        elif state == "merged":
            config_xmls = self._state_merged(want, have)
        elif state == "replaced":
            config_xmls = self._state_replaced(want, have)

        for xml in config_xmls:
            root.append(xml)
        data = remove_namespaces(xml_to_string(root))
        root = fromstring(to_bytes(data, errors="surrogate_then_replace"))

        return xml_to_string(root)

    def _state_replaced(self, want, have):
        """ The command generator when state is replaced

        :rtype: A list
        :returns: the xml necessary to migrate the current configuration
                  to the desired configuration
        """
        classifiers_xml = []
        classifiers_xml.extend(self._state_deleted(want, have))
        classifiers_xml.extend(self._state_merged(want, have))
        return classifiers_xml

    def _state_overridden(self, want, have):
        """ The command generator when state is overridden

        :rtype: A list
        :returns: the xml necessary to migrate the current configuration
                  to the desired configuration
        """
        classifiers_xml = []
        classifiers_xml.extend(self._state_deleted(have, have))
        classifiers_xml.extend(self._state_merged(want, have))
        return classifiers_xml

    def _state_deleted(self, want, have):
        """ The command generator when state is deleted

        :rtype: A list
        :returns: the xml necessary to migrate the current configuration
                  to the desired configuration
        """
        classifiers_xml = []
        if not want:
            want = have
        for config in want:
            classifier_root = build_root_xml_node("classifier")
            build_child_xml_node(classifier_root, "name", config["name"])
            classifier_root.attrib["operation"] = "remove"
            classifiers_xml.append(classifier_root)
        return classifiers_xml

    def _state_merged(self, want, have):
        """The command generator when state is merged

        :rtype: A list
        :returns: the xml necessary to migrate the current configuration
                  to the desired configuration
        """
        classifiers_xml = []
        for classifier in want:
            classifiers_root = build_root_xml_node("classifiers")
            classifier_node = build_child_xml_node(classifiers_root, "classifier")
            build_child_xml_node(classifier_node, "name", classifier["name"])
            if classifier["filter-operation"]:
                build_child_xml_node(
                    classifier_node, "filter-operation", classifier["filter-operation"]
                )
            for filter_entry in classifier["filter-entry"]:
                filter_entry_node = build_child_xml_node(
                    classifier_node, "filter-entry"
                )
                if filter_entry["filter-parameter"]:
                    build_child_xml_node(
                        filter_entry_node,
                        "filter-parameter",
                        filter_entry["filter-parameter"],
                    )
                if filter_entry["logical-not"]:
                    build_child_xml_node(
                        filter_entry_node, "logical-not", filter_entry["logical-not"]
                    )
                for vtags in filter_entry["vtags"]:
                    vtags_node = build_child_xml_node(filter_entry_node, "vtags")
                    if vtags["tag"]:
                        build_child_xml_node(vtags_node, "tag", vtags["tag"])
                    if vtags["vlan-id"]:
                        build_child_xml_node(vtags_node, "vlan-id", vtags["vlan-id"])

            classifiers_xml.append(classifier_node)
        return classifiers_xml
