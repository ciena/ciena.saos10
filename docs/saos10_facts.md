# saos10_facts

## description:
- Collects facts from network devices running the saos10 operating system. This module
  places the facts gathered in the fact tree keyed by the respective resource name.  The
  facts module will always collect a base set of facts from the device and can enable
  or disable collection of additional facts.

## version_added: 1.0.0

## notes:
- Tested against SAOS 10-4.

## options:
###  gather_subset:
    description:
    - When supplied, this argument will restrict the facts collected to a given subset.  Possible
      values for this argument include all, default, config, and neighbors. Can specify
      a list of values to include a larger subset. Values can also be used with an
      initial C(M(!)) to specify that a specific subset should not be collected.
    required: false
    default: '!config'

###  gather_network_resources:
    description:
    - When supplied, this argument will restrict the facts collected to a given subset.
      Possible values for this argument include all and the resources like interfaces.
      Can specify a list of values to include a larger subset. Values can also be
      used with an initial C(M(!)) to specify that a specific subset should not be
      collected. Valid subsets are 'all', 'interfaces', 'l3_interfaces', 'lag_interfaces',
      'lldp_global', 'lldp_interfaces', 'static_routes', 'firewall_rules', 'firewall_global',
      'firewall_interfaces', 'ospfv3', 'ospfv2'.
    required: false

## EXAMPLES

```yml
# Gather all facts
- ciena.saos10.saos10_facts:
    gather_subset: all
    gather_network_resources: all
```

```yml
# collect only the config and default facts
- ciena.saos10.saos10_facts:
    gather_subset: config
```

```yml
# collect everything exception the config
- ciena.saos10.saos10_facts:
    gather_subset: '!config'
```
