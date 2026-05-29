# Live SAOS 10 integration tests

A self-contained playbook that exercises every module in the collection against a real SAOS 10.x device.

**Warning:** the playbook makes configuration changes. Use a lab device only.

## Run

```bash
cd tests/integration/live
ansible-playbook -i inventory.yml playbook.yml -vv
```

Tags are available per module so you can run a subset:

```bash
ansible-playbook -i inventory.yml playbook.yml --tags bug-repro,classifiers
```

## Validation matrix (SAOS 10-11-02-0206-RS1 on CN3984)

| Module | merged | deleted | facts | Notes |
|---|---|---|---|---|
| `saos10_facts` | n/a | n/a | OK | |
| `saos10_command` (network_cli) | OK | OK | n/a | |
| `saos10_command` bug-repro | OK | n/a | n/a | Confirms cliconf `_ensure_root_prompt` fix |
| `saos10_classifiers` | OK | OK | OK | |
| `saos10_fds` | OK | OK | OK | |
| `saos10_fps` | OK | OK | OK | Parent FD must exist before merge |
| `saos10_bgp` | OK | OK | OK | |
| `saos10_ldp` | OK | OK | OK | SAOS only supports `tag: default` |
| `saos10_isis` | OK (using `dynamic_hostname`) | OK | n/a | `admin_state` requires the `admin-control` YANG feature; this 3984 build doesn't advertise it in its `ciena-isis@2025-07-11` capability so the playbook uses `dynamic_hostname: true` instead. Module + argspec are fine. |
| `saos10_mpls` | FAIL | FAIL | n/a | Module raises `list index out of range`; real code bug in `plugins/module_utils/network/saos10/config/mpls/mpls.py`. Needs follow-up. |
| `saos10_logical_ports` | not exercised | not exercised | OK | merge requires chassis-specific port id |
| `saos10_ptps` | not exercised | not exercised | OK | merge requires chassis-specific ptp-id |

## Known follow-ups

1. **`saos10_mpls`** — `list index out of range` regardless of input shape. Reproduce with the `mpls` tag. Probably an indexing bug introduced during the 1.8.0 array-suboptions rework.
2. **`saos10_isis`** — `admin_state` is gated by the `admin-control` YANG feature; re-test against a device that advertises it.
3. **`saos10_logical_ports` / `saos10_ptps`** — extend this playbook with a chassis-aware merge test (read first PTP id, then merge a no-op change).
