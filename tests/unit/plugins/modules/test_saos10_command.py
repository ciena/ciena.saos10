# Copyright 2026 Ciena Corp
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Regression test for the check-mode show-only filter in saos10_command.

History: the original check used ``str.contains(" show ")`` (an AttributeError
since ``str`` has no ``contains`` method), so check_mode never actually filtered
anything. A first patch replaced it with ``" show " not in item["command"]``
which required *leading and trailing* spaces around ``show`` and therefore
dropped every realistic show command. This test pins the behaviour to a
word-boundary match.
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from unittest.mock import MagicMock, patch

import pytest

from ansible_collections.ciena.saos10.plugins.modules import saos10_command


@pytest.mark.parametrize(
    "command,kept",
    [
        ("software show", True),     # SAOS "<subject> show" form
        ("show version", True),      # SAOS "show <subject>" form
        ("show", True),              # bare show
        ("show foo bar", True),      # show with arguments
        ("config", False),           # config-mode command
        ("shutdown", False),         # not a show
        ("software-show", False),    # identifier, not a show
        ("showme", False),           # prefix collision
    ],
)
def test_check_mode_only_keeps_show_commands(command, kept):
    module = MagicMock()
    module.check_mode = True
    with patch.object(saos10_command, "transform_commands", return_value=[{"command": command}]):
        result = saos10_command.parse_commands(module, warnings=[])
    if kept:
        assert result == [{"command": command}]
    else:
        assert result == []
