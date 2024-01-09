#!/usr/bin/python

# Copyright: (c) 2021, Your Name <jgroom@ciena.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: xml_diff
short_description: return diff for a pair of xml inputs
version_added: 1.1.0
description: return diff for a pair of xml inputs
options:
    old:
        description: xml string of config
        required: true
        type: str
    new:
        description: xml string of config
        required: true
        type: str
author:
  - Jeff Groom (@jgroom33)
"""

EXAMPLES = """
- name: Get config differences
  ciena.saos10.saos10_xmldiff:
    new: |
        <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
            <agg-global xmlns="urn:ietf:params:xml:ns:yang:ciena-ieee-lag">
                <global-admin-state>enabled</global-admin-state>
                <marker-timeout xmlns="urn:ietf:params:xml:ns:yang:ciena-ext-lag">50</marker-timeout>
            </agg-global>
            <alarms xmlns="urn:ietf:params:xml:ns:yang:ietf-alarms">
                <control>
                <max-alarm-status-changes>16</max-alarm-status-changes>
                <notify-status-changes>false</notify-status-changes>
                </control>
            </alarms>
            <system xmlns="http://openconfig.net/yang/system">
                <config>
                <hostname>5162-1</hostname>
                <contact xmlns="http://www.ciena.com/ns/yang/ciena-system">Customer Support, Ciena</contact>
                <description xmlns="http://www.ciena.com/ns/yang/ciena-system">5162</description>
                <location xmlns="http://www.ciena.com/ns/yang/ciena-system">34.8908084,-40.820916</location>
                </config>
            </system>
        </config>
    old: |
        <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
          <agg-global xmlns="urn:ietf:params:xml:ns:yang:ciena-ieee-lag">
            <global-admin-state>enabled</global-admin-state>
            <marker-timeout xmlns="urn:ietf:params:xml:ns:yang:ciena-ext-lag">50</marker-timeout>
          </agg-global>
          <alarms xmlns="urn:ietf:params:xml:ns:yang:ietf-alarms">
            <control>
              <max-alarm-status-changes>16</max-alarm-status-changes>
              <notify-status-changes>false</notify-status-changes>
            </control>
          </alarms>
          <system xmlns="http://openconfig.net/yang/system">
            <config>
              <hostname>5162-1</hostname>
              <contact xmlns="http://www.ciena.com/ns/yang/ciena-system">Customer Support, Ciena</contact>
              <description xmlns="http://www.ciena.com/ns/yang/ciena-system">5162</description>
              <location xmlns="http://www.ciena.com/ns/yang/ciena-system">Not Specified</location>
            </config>
          </system>
        </config>
"""

RETURN = """
xmlstring:
    description: An XML string of the resulting differences
    type: str
    returned: always
    sample: |
        <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
          <system xmlns="http://openconfig.net/yang/system">
            <config>
              <hostname>5162-1</hostname>
            </config>
          </system>
        </config>
"""

import traceback

from packaging.version import parse as version_parse
from io import BytesIO

LXML_IMP_ERR = None
try:
    from lxml import etree

    HAS_LXML = True
except ImportError:
    LXML_IMP_ERR = traceback.format_exc()
    HAS_LXML = False

XMLDIFF_IMP_ERR = None
try:
    from xmldiff import main as xmldiff_main

    HAS_XMLDIFF = True
except ImportError:
    XMLDIFF_IMP_ERR = traceback.format_exc()
    HAS_XMLDIFF = False

from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible.module_utils.common.text.converters import to_bytes, to_native


def parse(xmlstring):
    bytes = BytesIO(to_bytes(xmlstring, errors="surrogate_or_strict"))
    parser = etree.XMLParser(remove_blank_text=True, strip_cdata=False)
    tree = etree.parse(bytes, parser)
    return tree


def get_deletion_list(a, b):
    result = []
    for child in b:
        element = a.find(child.tag)
        if element:
            compare = xmldiff_main.diff_trees(element, child, diff_options={"F": 0.5, "ratio_mode": "accurate"})
            if len(compare) == 0:
                result.append(child)
    return result


def strip_duplicate_elements(old_root, new_root):
    new_delete = get_deletion_list(old_root, new_root)
    old_delete = get_deletion_list(new_root, old_root)
    for item in new_delete:
        new_root.remove(item)
    for item in old_delete:
        old_root.remove(item)

    # Recursively strip duplicates for nested children
    for old_element in old_root:
        new_element = new_root.find(old_element.tag)
        if new_element:
            strip_duplicate_elements(old_element, new_element)

    return old_root, new_root


def check_libs(module):
    # Check if we have lxml 2.3.0 or newer installed
    if not HAS_LXML:
        module.fail_json(msg=missing_required_lib("lxml"), exception=LXML_IMP_ERR)
    elif version_parse(".".join(to_native(f) for f in etree.LXML_VERSION)) < version_parse("2.3.0"):
        module.fail_json(msg="The xml ansible module requires lxml 2.3.0 or newer installed on the managed machine")
    elif version_parse(".".join(to_native(f) for f in etree.LXML_VERSION)) < version_parse("3.0.0"):
        module.warn("Using lxml version lower than 3.0.0 does not guarantee predictable element attribute order.")

    if not HAS_XMLDIFF:
        module.fail_json(msg=missing_required_lib("xmldiff"), exception=XMLDIFF_IMP_ERR)


def main():
    module_args = dict(new=dict(type="str", required=True), old=dict(type="str", required=True))
    result = dict(changed=False, result="")
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    if module.check_mode:
        module.exit_json(**result)

    check_libs(module)

    new = module.params["new"]
    old = module.params["old"]

    try:
        new_tree = parse(new)
        new_root = new_tree.getroot()
    except etree.XMLSyntaxError as e:
        module.fail_json(msg="Error while parsing document: %s (%s)" % ("new", e))
    try:
        old_tree = parse(old)
        old_root = old_tree.getroot()
    except etree.XMLSyntaxError as e:
        module.fail_json(msg="Error while parsing document: %s (%s)" % ("old", e))

    old_root, new_root = strip_duplicate_elements(old_root, new_root)
    result["xmlstring"] = etree.tostring(new_root)
    module.exit_json(**result)


if __name__ == "__main__":
    main()
