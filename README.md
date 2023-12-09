# ansible-pikvm
Quick Ansible playbook for PiKVM

## Usage Notes
It is assumed that ssh key authentication will be used and the ansible-core
package is already installed. Please check the Ansible documentation for
the latest information at https://docs.ansible.com/.

Before running the playbooks, review and modify any of the desired configs
under the `files/` subdirectory and modify the inventory to suit your
environment. Review the `ansible.cfg` for defaults and read the `main.yml`
playbook and be sure you are comfortable with it.

Once ready, you may execute the playbook with the following command:

```
ansible-playbook main.yml
```

If all goes well, your PiKVM packages will be updated and the configuration
will be applied to all of your PiKVM devices. Some of mine use different
overrides, I've included copies of my TESmart 16-port and EZCoo configs
along with the default (example) override.yaml.

## Setting Passwords
To avoid repo scanners from reporting false positives, I haven't included
any default passwords or default password files. If the playbook is run
without first setting any passwords, passwords will be generated and stored
in the following locations along with the salts used for idempotency:

- `files/password-root`
- `files/password-admin`

If these are populated with the desired passwords and, optionally, salts,
these will be used instead. If a new salt is generated, it will be added
to the file on the same line as the provided password.

For security, sha512 will be used for the root password and bcrypt will
be used for the nginx proxy. These have both been tested and verified to
work with the current package set used.

## What the playbook does
The playbook will update the package mirrorlist to the one specified and
update all installed packages. Additional packages will be installed for
maintaining the firmware and communicating via SNMP.

After the package maintenance, passwords will be configured, overrides
will be set as specified for each PiKVM host. For support of CyberPower
ATS (Automatic Transfer Switch), Switched PDUs (Power Distribution Units),
and UPS (Uninterruptible Power Supply) devices, the CyberPower MIB (Management
Information Base) will also be deployed.

# Additional Information
The playbook and files are as-is with no warranty. Please review the files,
if any of the changes make your device unusable, you may need to reimage
your SD card using an appropriate image from https://pikvm.org/download/.

This has been tested with the November 20, 2023 image updates. If you have
a new PiKVM, I might recommend reimaging your device rather than updating
it before using this playbook. If you have any suggestions for improvement
of this playbook, please log an issue or submit a pull request.
