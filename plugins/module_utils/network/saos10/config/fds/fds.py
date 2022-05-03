#
# -*- coding: utf-8 -*-
# Copyright 2021 Ciena
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The saos10_fds class
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


class Fds(ConfigBase):
    """
    The saos10_fds class
    """

    gather_subset = ["!all", "!min"]
    gather_network_resources = ["fds"]

    def __init__(self, module):
        super(Fds, self).__init__(module)

    def get_fds_facts(self):
        """ Get the 'facts' (the current configuration)

        :rtype: A dictionary
        :returns: The current configuration as a dictionary
        """
        facts, _warnings = Facts(self._module).get_facts(
            self.gather_subset, self.gather_network_resources
        )
        fds_facts = facts["ansible_network_resources"].get("fds")
        if not fds_facts:
            return []
        return fds_facts

    def execute_module(self):
        """ Execute the module

        :rtype: A dictionary
        :returns: The result from module execution
        """
        result = {"changed": False}
        existing_fds_facts = self.get_fds_facts()
        config_xmls = self.set_config(existing_fds_facts)

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
        changed_fds_facts = self.get_fds_facts()

        result["changed"] = config_is_diff(existing_fds_facts, changed_fds_facts)

        result["before"] = existing_fds_facts
        if result["changed"]:
            result["after"] = changed_fds_facts

        return result

    def set_config(self, existing_fds_facts):
        """ Collect the configuration from the args passed to the module,
            collect the current configuration (as a dict from facts)

        :rtype: A list
        :returns: the commands necessary to migrate the current configuration
                  to the desired configuration
        """
        want = self._module.params["config"]
        have = existing_fds_facts
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
        root = build_root_xml_node("fds")
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
        fds_xml = []
        fds_xml.extend(self._state_deleted(want, have))
        fds_xml.extend(self._state_merged(want, have))
        return fds_xml

    def _state_overridden(self, want, have):
        """ The command generator when state is overridden

        :rtype: A list
        :returns: the xml necessary to migrate the current configuration
                  to the desired configuration
        """
        fds_xml = []
        fds_xml.extend(self._state_deleted(have, have))
        fds_xml.extend(self._state_merged(want, have))
        return fds_xml

    def _state_deleted(self, want, have):
        """ The command generator when state is deleted

        :rtype: A list
        :returns: the xml necessary to migrate the current configuration
                  to the desired configuration
        """
        fds_xml = []
        if not want:
            want = have
        delete = dict(delete="delete")
        for config in want:
            fd_root = build_root_xml_node("fd")
            build_child_xml_node(fd_root, "fd", config["name"])
            fd_root.attrib.update(delete)
            fds_xml.append(fd_root)
        return fds_xml

    def _state_merged(self, want, have):
        """The command generator when state is merged

        :rtype: A list
        :returns: the xml necessary to migrate the current configuration
                  to the desired configuration
        """
        fds_xml = []
        for fd in want:
            fds_root = build_root_xml_node("fds")
            fd_node = build_child_xml_node(fds_root, "fd")
            build_child_xml_node(fd_node, "name", fd["name"])
            if fd["mode"]:
                build_child_xml_node(fd_node, "mode", fd["mode"])
            if fd["pfg-profile"]:
                build_child_xml_node(fd_node, "pfg-profile", fd["pfg-profile"])
            initiate_l2_transform = fd["initiate-l2-transform"]
            initiate_l2_transform_node = build_child_xml_node(
                fd_node, "initiate-l2-transform"
            )
            for vlan_stack in initiate_l2_transform["vlan-stack"]:
                vlan_stack_node = build_child_xml_node(
                    initiate_l2_transform_node, "vlan-stack"
                )
                if vlan_stack["tag"]:
                    build_child_xml_node(vlan_stack_node, "tag", vlan_stack["tag"])
                if vlan_stack["push-tpid"]:
                    build_child_xml_node(
                        vlan_stack_node, "push-tpid", vlan_stack["push-tpid"]
                    )
                if vlan_stack["push-pcp"]:
                    build_child_xml_node(
                        vlan_stack_node, "push-pcp", vlan_stack["push-pcp"]
                    )
                if vlan_stack["push-dei"]:
                    build_child_xml_node(
                        vlan_stack_node, "push-dei", vlan_stack["push-dei"]
                    )
                if vlan_stack["push-vid"]:
                    build_child_xml_node(
                        vlan_stack_node, "push-vid", vlan_stack["push-vid"]
                    )

            fds_xml.append(fd_node)
        return fds_xml
