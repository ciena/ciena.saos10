# Copyright 2026 Ciena Corp
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Regression test: every saos10 resource-module config builder must
serialize Python booleans to YANG-conformant ``"true"`` / ``"false"`` (RFC
7950 §9.5), NOT Python-style ``"True"`` / ``"False"``. SAOS rejects the
capitalized form with ``unknown object``.
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from unittest.mock import MagicMock

import pytest

from lxml.etree import Element, tostring

from ansible_collections.ciena.saos10.plugins.module_utils.network.saos10.config.bgp.bgp import Bgp
from ansible_collections.ciena.saos10.plugins.module_utils.network.saos10.config.classifiers.classifiers import Classifiers
from ansible_collections.ciena.saos10.plugins.module_utils.network.saos10.config.fds.fds import Fds
from ansible_collections.ciena.saos10.plugins.module_utils.network.saos10.config.fps.fps import Fps
from ansible_collections.ciena.saos10.plugins.module_utils.network.saos10.config.isis.isis import Isis
from ansible_collections.ciena.saos10.plugins.module_utils.network.saos10.config.ldp.ldp import Ldp
from ansible_collections.ciena.saos10.plugins.module_utils.network.saos10.config.logical_ports.logical_ports import LogicalPorts
from ansible_collections.ciena.saos10.plugins.module_utils.network.saos10.config.mpls.mpls import Mpls
from ansible_collections.ciena.saos10.plugins.module_utils.network.saos10.config.ptps.ptps import Ptps


CONFIG_CLASSES = [Bgp, Classifiers, Fds, Fps, Isis, Ldp, LogicalPorts, Mpls, Ptps]


@pytest.mark.parametrize("cls", CONFIG_CLASSES, ids=lambda c: c.__name__)
def test_bool_serialized_as_yang_lowercase(cls):
    module = MagicMock()
    instance = cls.__new__(cls)
    instance._module = module
    root = Element("instance")
    instance._populate_xml_subtree(root, {"flag_true": True, "flag_false": False, "name": "x"})
    xml = tostring(root).decode()
    assert "<flag-true>true</flag-true>" in xml
    assert "<flag-false>false</flag-false>" in xml
    assert "True" not in xml
    assert "False" not in xml
