======================================
Ciena SAOS 10 Collection Release Notes
======================================

.. contents:: Topics

v1.9.0
======

Minor Changes
-------------

- CI matrix and ``requirements-test.txt`` updated to the current Python and Ansible versions; old sanity ignore files for unsupported ansible-core versions (2.9, 2.13, 2.14, 2.15) have been removed.
- Collection validated against SAOS 10-11-02-0206-RS1. Module documentation ``notes`` updated accordingly.
- Raise the minimum supported ``ansible-core`` to ``2.16`` and the minimum ``ansible.netcommon`` to ``6.0.0`` to align with the current Ansible support policy.
- ``meta/runtime.yml`` now declares an ``saos10`` action group and adds plugin_routing entries for all eleven modules (previously only five were routed).

Bugfixes
--------

- cliconf/saos10 - automatically return to the root prompt before sending ``software show`` / ``show system components`` / any ``run_commands`` / ``get_config`` call. Previously, when a task left the CLI in a nested config-mode prompt (for example ``host(config)(license-management-config)#``), the next module invocation failed with ``SHELL PARSER FAILURE``, forcing users to insert ``meta: reset_connection`` between tasks. The plugin now inspects the current prompt and issues just enough ``exit`` commands to return to the root prompt, avoiding the destructive ``exit`` that would log the session out from the root.
- cliconf/saos10 - cache ``get_device_info`` results per persistent connection so ``software show`` is only invoked once per session instead of once per task.
- saos10_command - fix latent ``AttributeError`` in check-mode (``str.contains`` does not exist; replaced with a Pythonic ``in`` membership test).
- saos10_facts - fix ``ImportError`` raised on every gather attempt: ``facts.py`` imported a non-existent ``Logical_portsFacts`` class. Renamed to ``LogicalPortsFacts`` to match the actual class definition.
- Config builders for all nine resource modules (bgp, classifiers, fds, fps, isis, ldp, logical_ports, mpls, ptps) used ``str(value)`` when populating XML, serializing Python ``True`` / ``False`` as the YANG-invalid strings ``"True"`` / ``"False"`` instead of ``"true"`` / ``"false"``. Bool-typed fields are now lowercased to match RFC 7950 §9.5. Caught while investigating an ISIS ``unknown object`` failure on SAOS 10.11.

Known Issues
------------

- saos10_isis - the argspec exposes ``admin_state`` directly under the instance, but ``ciena-isis@2025-07-11`` only defines ``admin-state`` under ``instance/interfaces/interface`` (via the ``admin-control`` grouping). Passing ``admin_state`` at the instance level therefore returns ``unknown object`` from netconf. Use leaves that ARE valid directly under the instance (``dynamic_hostname``, ``distance``, ``level_type``, ``net``, ``lsp_refresh``, ``lsp_lifetime`` etc.) until the argspec is regenerated against the current YANG.
- saos10_mpls - `state: merged` and `state: deleted` raise ``IndexError: list index out of range`` on SAOS 10.11.x. Suspected bug in the config builder under ``plugins/module_utils/network/saos10/config/mpls``. Tracked for a follow-up fix; the module currently cannot apply MPLS configuration.
