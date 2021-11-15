

# Ciena SAOS 10 Collection

The Ansible Ciena SAOS collection includes a variety of Ansible content to help automate the management of Ciena SAOS 10.x network appliances.

This collection has been tested against Ciena 10-4

## Ansible version compatibility

This collection has been tested against following Ansible versions: **>=2.9.10,<2.11**.

### Supported connections

The Ciena SAOS 10 collection supports ``network_cli``  connections.

## Included content

<!--start collection content-->

### Modules
Name | Description
--- | ---
[ciena.saos10.saos10_command](https://github.com/ciena/ciena.saos10/blob/master/docs/saos10_command.txt)|Run commands on remote devices running Ciena SAOS 10
[ciena.saos10.saos10_facts](https://github.com/ciena/ciena.saos10/blob/master/docs/saos10_facts.txt)|Collect facts from remote devices running Ciena SAOS 10
[ciena.saos10.xml_diff](https://github.com/ciena/ciena.saos10/blob/master/docs/xml_diff.txt)|Diff 2 xml configs

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
  - name: Execute SAOS 10 commands
    ciena.saos10.saos10_command:
      commands:
      - software show
  - name: Set port config
    ciena.saos10.saos10_command:
      commands:
      - config
      - oc-if:interfaces interface 2 config name 2 description myport
      - exit
```

## Contributing to this collection

We welcome community contributions to this collection. If you find problems, please open an issue or create a PR against the [Ciena SAOS 10 collection repository](https://github.com/ciena/ciena.saos10).

Release is done automatically use Github Actions as part of merging to master.

### Documentation generation

```bash
ansible-doc -M ./plugins/modules/ saos10_facts | sed -e 's/(\/home.*//g' | sed -e 's/> //g' > docs/saos10_facts.txt
ansible-doc -M ./plugins/modules/ saos10_command | sed -e 's/(\/home.*//g' | sed -e 's/> //g' > docs/saos10_command.txt
ansible-doc -M ./plugins/modules/ xml_diff | sed -e 's/(\/home.*//g' | sed -e 's/> //g' > docs/xml_diff.txt
```

## Changelogs

[CHANGELOG](CHANGELOG.rst)

## Roadmap

* Netconf calls

## More information

- [Ansible network resources](https://docs.ansible.com/ansible/latest/network/getting_started/network_resources.html)
- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)

## Licensing

See [LICENSE](LICENSE) to see the full text.

