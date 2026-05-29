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


def test_ensure_root_prompt_diag_shell_raises():
    # The diag shell is a bash session; running CLI commands there returns
    # 'command not found' and would poison the device_info cache.
    cliconf, _conn = _make_cliconf([b"diag@3984-13$ "])
    with pytest.raises(AnsibleConnectionFailure):
        cliconf._ensure_root_prompt()
    cliconf.send_command.assert_not_called()


def test_ensure_root_prompt_empty_then_probes_then_recovers():
    # Mid-session, get_prompt() can return empty transiently. We send one
    # newline probe and re-read before giving up.
    cliconf, _conn = _make_cliconf([b"", b"3984-13> "])
    cliconf._ensure_root_prompt()
    cliconf.send_command.assert_called_once_with("")


def test_ensure_root_prompt_persistent_empty_returns():
    # If even the probe doesn't surface a prompt, give up silently rather
    # than hang. This matches the fresh-connection case.
    cliconf, _conn = _make_cliconf([b"", b""])
    cliconf._ensure_root_prompt()
    cliconf.send_command.assert_called_once_with("")


def test_ensure_root_prompt_noop_on_none_prompt():
    cliconf, _conn = _make_cliconf([None, None])
    cliconf._ensure_root_prompt()
    cliconf.send_command.assert_called_once_with("")


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


def test_get_device_info_caches_only_on_full_success():
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
    assert cliconf.send_command.call_count == 2
    assert info1["network_os_version"] == "saos-10-11-02-0199"
    assert info1["network_os_model"] == "5170"


def test_get_device_info_does_not_cache_partial_result():
    # If the version regex matches but the model regex misses (e.g. paging
    # truncated the components table), we MUST NOT cache the partial dict --
    # otherwise the connection would be stuck without a model forever and the
    # only recovery would be 'meta: reset_connection'.
    connection = MagicMock()
    connection.get_prompt.return_value = b"3984-13> "
    cliconf = Cliconf(connection)
    cliconf.send_command = MagicMock(
        side_effect=[
            "Running package version : saos-10-11-02-0199",
            "(truncated output, no model line)",
            "Running package version : saos-10-11-02-0199",
            "| name           | 5170 ",
        ]
    )
    first = cliconf.get_device_info()
    assert "network_os_model" not in first
    assert cliconf._device_info == {}  # not cached
    second = cliconf.get_device_info()
    assert second["network_os_model"] == "5170"
    assert cliconf._device_info == second  # now cached
