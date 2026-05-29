# Copyright 2026 Ciena Corp
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from unittest.mock import MagicMock

import pytest

from ansible.errors import AnsibleConnectionFailure
from ansible_collections.ciena.saos10.plugins.cliconf.saos10 import Cliconf


def _make_cliconf(prompt_sequence):
    """Build a Cliconf with a mocked connection whose get_prompt() returns the
    next value in the sequence each call. Tracks send_command calls.
    """
    connection = MagicMock()
    connection.get_prompt.side_effect = list(prompt_sequence)
    cliconf = Cliconf(connection)
    cliconf.send_command = MagicMock(return_value="")
    return cliconf, connection


def test_ensure_root_prompt_noop_at_operator():
    cliconf, _conn = _make_cliconf([b"3984-13> "])
    cliconf._ensure_root_prompt()
    cliconf.send_command.assert_not_called()


def test_ensure_root_prompt_noop_on_fresh_connection():
    cliconf, _conn = _make_cliconf([None])
    cliconf._ensure_root_prompt()
    cliconf.send_command.assert_not_called()


def test_ensure_root_prompt_noop_in_diag_shell():
    # User explicitly entered diag shell; we must not blindly 'exit'.
    cliconf, _conn = _make_cliconf([b"diag@3984-13$ "])
    cliconf._ensure_root_prompt()
    cliconf.send_command.assert_not_called()


def test_ensure_root_prompt_single_exit_from_config_mode():
    cliconf, _conn = _make_cliconf([b"diag@3984-13# ", b"3984-13> "])
    cliconf._ensure_root_prompt()
    assert cliconf.send_command.call_count == 1
    cliconf.send_command.assert_called_with("exit")


def test_ensure_root_prompt_three_exits_on_nested_submodes():
    cliconf, _conn = _make_cliconf(
        [
            b"diag@3984-13(license-management-config)(server-config)# ",
            b"diag@3984-13(license-management-config)# ",
            b"diag@3984-13# ",
            b"3984-13> ",
        ]
    )
    cliconf._ensure_root_prompt()
    assert cliconf.send_command.call_count == 3


def test_ensure_root_prompt_raises_when_stuck():
    cliconf, _conn = _make_cliconf([b"diag@3984-13# "] * 8)
    with pytest.raises(AnsibleConnectionFailure):
        cliconf._ensure_root_prompt(max_attempts=2)


def test_get_device_info_caches_across_calls():
    connection = MagicMock()
    connection.get_prompt.return_value = b"3984-13> "
    cliconf = Cliconf(connection)
    cliconf.send_command = MagicMock(
        side_effect=[
            "Running package version : saos-10-11-02-0199",
            "| name           | 5170 ",
        ]
    )
    info1 = cliconf.get_device_info()
    info2 = cliconf.get_device_info()
    assert info1 is info2
    # Only the initial pair of show commands runs (no exit needed).
    assert cliconf.send_command.call_count == 2
    assert info1["network_os"] == "ciena.saos10.saos10"
    assert info1["network_os_version"] == "saos-10-11-02-0199"
    assert info1["network_os_model"] == "5170"
