#!/usr/bin/python

# Copyright: (c) 2021, Your Name <jgroom@ciena.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: saos10_format_xml

short_description: Format saos XML

version_added: "1.0.0"

description: remove namespaces and other useless things from saos xml config

options:
    xml_string:
        description: xml config
        required: true
        type: str

author:
    - Jeff Groom (jgroom@ciena.com)
"""

EXAMPLES = r"""
# Pass in an xml config
- name: Test with a config
  ciena.saos10.saos10_format_xml:
    xml_string: '<data>....</data>'
"""

RETURN = r"""
# These are examples of possible return values, and in general should use other names for return values.
result:
    description: formatted xml
    type: str
    returned: always
    sample: '<config>....</config>'
"""

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_bytes

import traceback
import re

from io import BytesIO

LXML_IMP_ERR = None
try:
    from lxml import etree

    HAS_LXML = True
except ImportError:
    LXML_IMP_ERR = traceback.format_exc()
    HAS_LXML = False


def run_module():
    module_args = dict(
        xml_string=dict(type="str", required=True),
    )
    result = dict(
        changed=False,
        result="",
    )
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    if module.check_mode:
        module.exit_json(**result)

    xml_string = module.params["xml_string"]

    # replace <data> with <config>
    regex = re.compile(
        r'<data xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:ncx="http://netconfcentral.org/ns/yuma-ncx">(.*)<\/data>'
    )
    replaced = regex.sub(
        r'<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">\1</config>',
        xml_string,
    )

    inbytes = BytesIO(to_bytes(replaced, errors="surrogate_or_strict"))

    # Try to parse in the target XML file
    try:
        parser = etree.XMLParser(remove_blank_text=True, strip_cdata=False)
        doc = etree.parse(inbytes, parser)
    except etree.XMLSyntaxError as e:
        module.fail_json(
            msg="Error while parsing document: %s (%s)" % ("xml_string", e)
        )

    # format the xml so line by line regex can be used
    pretty = etree.tostring(
        doc, xml_declaration=True, encoding="UTF-8", pretty_print=True
    )

    # replace namespaces (these will error the config)
    regex = r"(>.+:)"
    subst = ">"
    replaced = re.sub(regex, subst, pretty.decode("utf-8"), 0, re.MULTILINE)

    result["result"] = replaced

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
