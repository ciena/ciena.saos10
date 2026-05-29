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

- Config builders for all nine resource modules (bgp, classifiers, fds, fps, isis, ldp, logical_ports, mpls, ptps) used ``str(value)`` when populating XML, serializing Python ``True`` / ``False`` as the YANG-invalid strings ``"True"`` / ``"False"`` instead of ``"true"`` / ``"false"``. Bool-typed fields are now lowercased to match RFC 7950 §9.5. Caught while investigating an ISIS ``unknown object`` failure on SAOS 10.11.
- cliconf/saos10 - automatically return to the operator prompt before sending ``software show`` / ``show system components`` / any ``run_commands`` / ``get_config`` call. Previously, when a task left the CLI in a nested config-mode prompt (for example ``host(config)(license-management-config)#``), the next module invocation failed with ``SHELL PARSER FAILURE``, forcing users to insert ``meta: reset_connection`` between tasks. The plugin now inspects the current prompt and issues just enough ``exit`` commands to return to the operator prompt, avoiding the destructive ``exit`` that would log the session out from the root. NOTE: this is a behaviour change for playbooks that intentionally chained ``saos10_command`` tasks relying on the prompt persisting in config mode -- those should now use a single task that includes the closing ``exit`` commands.
- cliconf/saos10 - cache ``get_device_info`` results per persistent connection so ``software show`` is only invoked once per session instead of once per task.
- cliconf/saos10 - refuse to run SAOS CLI commands when the session is in the diag (bash) shell, and only cache ``get_device_info`` on a fully populated result. The previous patch silently dispatched ``software show`` into bash when the prompt ended in ``$``, and would cache an incomplete ``{network_os: ...}`` dict if either show command returned unexpected output -- both states stuck for the life of the persistent connection.
- saos10_command - check-mode now correctly keeps every ``show`` command. The original code called ``str.contains(" show ")`` (no such method, latent ``AttributeError``); a first replacement used ``" show " not in cmd`` which required leading AND trailing spaces and therefore dropped real commands like ``software show`` and ``show version``. The check is now a word-boundary test (``"show" in cmd.split()``).
- saos10_facts - fix ``ImportError`` raised on every gather attempt: ``facts.py`` imported a non-existent ``Logical_portsFacts`` class. Renamed to ``LogicalPortsFacts`` to match the actual class definition.
- saos10_mpls (config) - MPLS is a singleton YANG container, but the code-generation template assumed it was a list of keyed items (the file shipped with ``XML_ITEMS = "None"`` and ``XML_ITEMS_KEY = "None"`` as literal strings, and ``_state_deleted`` did ``config["None"]``). Rewrote ``_state_deleted`` so that an empty ``config:`` removes the whole ``<mpls>`` subtree (and is a no-op when nothing is configured) and taught ``create_xml_config_from_dict`` to honour an ``_operation`` sentinel that promotes itself to ``operation="..."`` on the root element.
- saos10_mpls (facts) - guard ``data.xpath("//mpls")[0]`` against an empty result. On any device with no MPLS subtree configured the facts gather raised ``IndexError: list index out of range`` before the module could even compose an edit-config, breaking both ``state: merged`` and ``state: deleted``.
