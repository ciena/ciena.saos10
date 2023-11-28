# Ciena SAOS 10 Collection

The Ansible Ciena SAOS collection includes a variety of Ansible content to help automate the management of Ciena SAOS 10.x network appliances.

This collection has been tested against saos-10-09-00-0307-GA

<!--start requires_ansible-->
## Ansible version compatibility

This collection has been tested against following Ansible versions:

  * 2.10
  * 2.16

For collections that support Ansible 2.9, please ensure you update your `network_os` to use the
fully qualified collection name (for example, `ciena.saos10.saos10`).
Plugins and modules within a collection may be tested with only specific Ansible versions.
A collection may contain metadata that identifies these versions.
PEP440 is the schema used to describe the versions of Ansible.
<!--end requires_ansible-->

### Supported connections

The Ciena SAOS 10 collection supports `network_cli` and `netconf` connections.

## Included content

<!--start collection content-->
### Cliconf plugins
Name | Description
--- | ---
[ciena.saos10.saos10](https://github.com/ciena/ciena.saos10/blob/master/docs/ciena.saos10.saos10_cliconf.rst)|Use saos10 cliconf to run command on Ciena saos10 platform

### Netconf plugins
Name | Description
--- | ---
[ciena.saos10.saos10](https://github.com/ciena/ciena.saos10/blob/master/docs/ciena.saos10.saos10_netconf.rst)|Use saos10 netconf plugin to run netconf commands on Ciena saos10 platform

### Modules
Name | Description
--- | ---
[ciena.saos10.saos10_classifiers](https://github.com/ciena/ciena.saos10/blob/master/docs/ciena.saos10.saos10_classifiers_module.rst)|Manage classifiers on Ciena SAOS 10 devices
[ciena.saos10.saos10_command](https://github.com/ciena/ciena.saos10/blob/master/docs/ciena.saos10.saos10_command_module.rst)|Run commands on remote devices running Ciena SAOS 10
[ciena.saos10.saos10_facts](https://github.com/ciena/ciena.saos10/blob/master/docs/ciena.saos10.saos10_facts_module.rst)|Get facts about saos10 devices.
[ciena.saos10.saos10_fds](https://github.com/ciena/ciena.saos10/blob/master/docs/ciena.saos10.saos10_fds_module.rst)|Manage forwarding domains on Ciena SAOS 10 devices
[ciena.saos10.saos10_fps](https://github.com/ciena/ciena.saos10/blob/master/docs/ciena.saos10.saos10_fps_module.rst)|Manage flow points on Ciena SAOS 10 devices
[ciena.saos10.xmldiff](https://github.com/ciena/ciena.saos10/blob/master/docs/ciena.saos10.xmldiff_module.rst)|return diff for a pair of xml inputs

<!--end collection content-->

## Installing this collection

Install the Ciena SAOS 10 collection with the Ansible Galaxy CLI:

```bash
ansible-galaxy collection install ciena.saos10
```

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: ciena.saos10
```

## Using this collection

This collection includes [network resource modules](https://docs.ansible.com/ansible/latest/network/user_guide/network_resource_modules.html).

### Using modules from the Ciena SAOS 10 collection in your playbooks

You can call modules by their Fully Qualified Collection Namespace (FQCN), such as `ciena.saos10.saos10_command`.
The following example task replaces configuration changes in the existing configuration on a Ciena SAOS 10 network device, using the FQCN:

```yaml
---
- hosts: all
  collections:
    - ciena.saos10
  gather_facts: false
  name: Gather facts for ciena device Saos 10
  tasks:
    - name: get device facts for Saos 10
      ciena.saos10.saos10_facts:
        gather_subset:
          - all
        gather_network_resources:
          - classifiers
      connection: netconf
    - name: saos10_command with diag shell
      ciena.saos10.saos10_command:
        commands:
        - software show
        - diag shell host
        - ls /
      connection: network_cli
  - name: Set port config
    ciena.saos10.saos10_command:
      commands:
      - config
      - oc-if:interfaces interface 2 config name 2 description myport
      - exit
```

## Contributing to this collection

We welcome community contributions to this collection. If you find problems, please open an issue or create a PR against the [Ciena SAOS 10 collection repository](https://github.com/ciena/ciena.saos10).

Release is done automatically using Github Actions as part of merging to master.

### Resource Module Builder

The modules in this project were built using the [resource module builder hosted by Ciena](https://github.com/ciena/resource_module_builder).

## Changelogs

[CHANGELOG](CHANGELOG.md)

## Licensing

See [LICENSE](LICENSE) to see the full text.
