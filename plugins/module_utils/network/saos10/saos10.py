# This code is part of Ansible, but is an independent component.
# This particular file snippet, and this file snippet only, is BSD licensed.
# Modules you write using this snippet, which is embedded dynamically by Ansible
# still belong to the author of the module, and may assign their own license
# to the complete work.
#
# (c) 2016 Red Hat Inc.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the documentation
#      and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
from __future__ import absolute_import, division, print_function

__metaclass__ = type
import json

from ansible.module_utils._text import to_text
from ansible.module_utils.connection import Connection, ConnectionError
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.netconf import (
    NetconfConnection,
)

try:
    from lxml.etree import tostring as xml_to_string

    HAS_LXML = True
except ImportError:
    from xml.etree.ElementTree import tostring as xml_to_string

    HAS_LXML = False

_DEVICE_CONFIGS = {}
CONFIG_FORMATS = frozenset(["xml"])


def tostring(element, encoding="UTF-8", pretty_print=False):
    if HAS_LXML:
        return xml_to_string(
            element,
            encoding="unicode",
            pretty_print=pretty_print,
        )
    else:
        return to_text(
            xml_to_string(element, encoding),
            encoding=encoding,
        )


def get_connection(module):
    if hasattr(module, "_saos10_connection"):
        return module._saos10_connection

    capabilities = get_capabilities(module)
    network_api = capabilities.get("network_api")
    if network_api == "cliconf":
        module._saos10_connection = Connection(module._socket_path)
    elif network_api == "netconf":
        module._saos10_connection = NetconfConnection(module._socket_path)
    else:
        module.fail_json(msg="Invalid connection type %s" % network_api)

    return module._saos10_connection


def get_capabilities(module):
    if hasattr(module, "_saos10_capabilities"):
        return module._saos10_capabilities

    try:
        capabilities = Connection(module._socket_path).get_capabilities()
    except ConnectionError as exc:
        module.fail_json(msg=to_text(exc, errors="surrogate_then_replace"))

    module._saos10_capabilities = json.loads(capabilities)
    return module._saos10_capabilities


def is_netconf(module):
    capabilities = get_capabilities(module)
    return True if capabilities.get("network_api") == "netconf" else False


def get_config(module, flags=None, format=None):
    flags = [] if flags is None else flags
    global _DEVICE_CONFIGS

    if _DEVICE_CONFIGS != {}:
        return _DEVICE_CONFIGS
    else:
        connection = get_connection(module)
        try:
            out = connection.get_config(flags=flags, format=format)
        except ConnectionError as exc:
            module.fail_json(msg=to_text(exc, errors="surrogate_then_replace"))
        cfg = to_text(out, errors="surrogate_then_replace").strip()
        _DEVICE_CONFIGS = cfg
        return cfg


def get_configuration(module, source="running", format="xml", filter=None):
    if format not in CONFIG_FORMATS:
        module.fail_json(msg="invalid config format specified")

    conn = get_connection(module)
    try:
        reply = conn.get_config(source=source)
    except ConnectionError as exc:
        module.fail_json(msg=to_text(exc, errors="surrogate_then_replace"))
    return reply


def run_commands(module, commands, check_rc=True):
    connection = get_connection(module)
    try:
        response = connection.run_commands(commands=commands, check_rc=check_rc)
    except ConnectionError as exc:
        module.fail_json(msg=to_text(exc, errors="surrogate_then_replace"))
    return response


def load_config(module, commands, commit=False, comment=None):
    connection = get_connection(module)

    try:
        response = connection.edit_config(candidate=commands, commit=commit, comment=comment)
    except ConnectionError as exc:
        module.fail_json(msg=to_text(exc, errors="surrogate_then_replace"))

    return response.get("diff")
