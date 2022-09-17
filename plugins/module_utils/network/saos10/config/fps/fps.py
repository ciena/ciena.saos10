#
# -*- coding: utf-8 -*-
# Copyright 2021 Ciena
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The saos10_fps class
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to it's desired end-state is
created
"""
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


class Fps(ConfigBase):
    """
    The saos10_fps class
    """

    gather_subset = ["!all", "!min"]
    gather_network_resources = ["fps"]

    def __init__(self, module):
        super(Fps, self).__init__(module)

    def get_fps_facts(self):
        """ Get the 'facts' (the current configuration)

        :rtype: A dictionary
        :returns: The current configuration as a dictionary
        """
        facts, _warnings = Facts(self._module).get_facts(
            self.gather_subset, self.gather_network_resources
        )
        fps_facts = facts["ansible_network_resources"].get("fps")
        if not fps_facts:
            return []
        return fps_facts

    def execute_module(self):
        """ Execute the module

        :rtype: A dictionary
        :returns: The result from module execution
        """
        result = {"changed": False}
        existing_fps_facts = self.get_fps_facts()
        config_xmls = self.set_config(existing_fps_facts)

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
        changed_fps_facts = self.get_fps_facts()

        result["changed"] = config_is_diff(existing_fps_facts, changed_fps_facts)

        result["before"] = existing_fps_facts
        if result["changed"]:
            result["after"] = changed_fps_facts

        return result

    def set_config(self, existing_fps_facts):
        """ Collect the configuration from the args passed to the module,
            collect the current configuration (as a dict from facts)

        :rtype: A list
        :returns: the commands necessary to migrate the current configuration
                  to the desired configuration
        """
        want = self._module.params["config"]
        have = existing_fps_facts
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
        root = build_root_xml_node("fps")
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
        fps_xml = []
        fps_xml.extend(self._state_deleted(want, have))
        fps_xml.extend(self._state_merged(want, have))
        return fps_xml

    def _state_overridden(self, want, have):
        """ The command generator when state is overridden

        :rtype: A list
        :returns: the xml necessary to migrate the current configuration
                  to the desired configuration
        """
        fps_xml = []
        fps_xml.extend(self._state_deleted(have, have))
        fps_xml.extend(self._state_merged(want, have))
        return fps_xml

    def _state_deleted(self, want, have):
        """ The command generator when state is deleted

        :rtype: A list
        :returns: the xml necessary to migrate the current configuration
                  to the desired configuration
        """
        fps_xml = []
        if not want:
            want = have
        for config in want:
            fp_root = build_root_xml_node("fp")
            build_child_xml_node(fp_root, "name", config["name"])
            fp_root.attrib["operation"] = "remove"
            fps_xml.append(fp_root)
        return fps_xml

    def _state_merged(self, want, have):
        """The command generator when state is merged

        :rtype: A list
        :returns: the xml necessary to migrate the current configuration
                  to the desired configuration
        """
        fps_xml = []
        for fp in want:
            fps_root = build_root_xml_node("fps")
            fp_node = build_child_xml_node(fps_root, "fp")
            build_child_xml_node(fp_node, "name", fp["name"])
            if fp["logical-port"]:
                build_child_xml_node(fp_node, "logical-port", fp["logical-port"])
            if fp["fd-name"]:
                build_child_xml_node(fp_node, "fd-name", fp["fd-name"])
            fps_xml.append(fp_node)
        return fps_xml
