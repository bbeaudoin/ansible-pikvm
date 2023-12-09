# ansible-pikvm
## Introduction
This repository serves primarily as a backup for my base configuration,
the things I spend the most time doing when I maintain or reimage my
devices. Sometimes it's quicker not to automate changes, Usually I only
spend a few minutes a month but recently I reimaged all of my devices
so it made sense to represent my manual activities as code.

It took a few minutes to write the basic playbook. Testing more general
or more flexible automation to make this more useful for others took more
time as did addressing the concerns of a security scanner that reacted
to my initial password hashes, using password lookups and generators,
writing documentation, and extending the playbook for others took hours.

## Motivation

Automation is often a trade-off based on scale. If I spend 5 minutes a
month manually configuring a reimaged PiKVM or an hour a year vs. an
hour or more automating and maintaining a playbook, the effort doesn't
necessarily pay off. But if I can save an hour of effort for five, ten,
or even a thousand others, it's possible to return that time to the
community for other efforts.

My personal time "savings" by automating and sharing my automation is
definitely in the negative when I publish the work for others to use.
That said, if 100 or even 1000 people in the user community can use this
code for their installation and maintenance, even if only a portion of
that time saving is returned back to the community, it makes this effort
worthwhile.

## Prerequisites
If you have any questions about using Ansible or writing Ansible playbooks,
it may be helpful to review the documentation at https://docs.ansible.com/.

Ansible is a configuration management and automation tool. If you are not
familiar with Ansible at all and need an easier entry point than the docs,
you might refer to https://www.ansible.com/overview/how-ansible-works for
the beginner's guide and introductory information. This project's focus is
primarily for my own use to automate my PiKVM deployments but it may be
useful to others as an example on how to maintain their own deployments,
even general Linux system deployments as the same concepts apply.

You will need a system that is capable of acting as an Ansible control node,
this generally means a Linux or macOS system with Python3 and Ansible Core
deployed using your operating system's package management tooling. If you
are running on a macOS system, you may be able to install the tools using
Homebrew (https://brew.sh/) on your device.

General installation and usage is outside of the scope of this document but
I will provide some getting started information based on my own systems and
use cases.

## Quickstart
Generate your keys using `ssh-keygen`, copy them to your hosts using the
`ssh-copy-id` command, register passphrase protected private keys with
`ssh-agent`, if needed, clone the ansible-pikvm repo to your home directory,
review the files, modify the configuration, inventory, and playbook for your
needs, and, once ready, invoke the playbook using the following command:

```
ansible-playbook main.yml
```

If all goes well, your PiKVM packages will be updated and the configuration
will be applied to all of your PiKVM devices. Some of mine use different
overrides, I've included copies of my TESmart 16-port and EZCoo configs
along with the default (example) override.yaml.

Although I consider the rest to be generally out-of-scope for my own use,
I've added some additional information for those that may need help getting
started.

## General git and Ansible Installation and Usage

If you're running on Linux, you should install `ansible-core` using `apt`,
`dnf`, or other package manager appropriate for your operating system. You
should also install the `python-passlib` or `python3-passlib` module, the
`crypt` functionality will be removed from Python 2.17 and 3.13.

The `git` command is also needed to be able to clone the repository and has
been added to the package installation examples below.

### Examples
Debian-based systems
```
apt install ansible-core python3-passlib git
```
Fedora-based systems
```
dnf install ansible-core python3-passlib git
```
Arch-based systems
```
pacman -Sy ansible-core python-passlib git
```

### Checking out the repository
The repository may be cloned to your system using the following command:

```
git clone https://github.com/bbeaudoin/ansible-pikvm.git
```

If desired, set up your upstream, remotes, and branches if you plan on
maintaining your own customizations or improving the code and submitting
pull requests later.

### Ansible and Playbook Configuration
The primary ansible.cfg lives in /etc/ansible/ansible.cfg along with the
primary inventory in /etc/ansible/hosts. It is often best to use a local
ansible.cfg and inventory file or directory, I've used ansible.cfg and an
inventory directory with the primary hosts file in `./inventory/main.yml`.

The inventory contains host-specific configuration information and both
host and group variables. Hosts and variables in the `all` section are
global, group and host-specific variables will override global variables.

## Preparing your environment and remote hosts
Ansible usually uses SSH public key authentication with a private key
located either on the control host or through keys located on the user's
own host. This may be managed by an agent or an option may be passed to
Ansible to prompt the user for passwords.

If you have not yet generated an SSH public/private keypair, use the
`ssh-keygen` command with defaults. If you provide a passphrase to protect
your private key, using `ssh-agent` is recommended.

### Generating a public/private keypair
```
[bbeaudoin@cerebus ansible-pikvm]$ ssh-keygen
Generating public/private rsa key pair.
Enter file in which to save the key (/home/bbeaudoin/.ssh/id_rsa):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /home/bbeaudoin/.ssh/id_rsa.
Your public key has been saved in /home/bbeaudoin/.ssh/id_rsa.pub.
The key fingerprint is:
SHA256:iA2NoZiJYEPAW3bZyiCuioWcGHOYS8pPQdMOTAmLfzs bbeaudoin@cerebus.openhappens.org
```

### Using ssh-agent to manage protected keys
```
[bbeaudoin@cerebus ansible-pikvm]$ eval $(ssh-agent)
Agent pid 379169
[bbeaudoin@cerebus ansible-pikvm]$ ssh-add
Enter passphrase for /home/bbeaudoin/.ssh/id_rsa:
Identity added: /home/bbeaudoin/.ssh/id_rsa (bbeaudoin@cerebus.openhappens.org)
```

### Copying keys to managed hosts
Note, for PiKVM, the filesystem must be read-write before copying the keys
```
[bbeaudoin@cerebus ansible-pikvm]$ ssh root@10.0.2.18 rw
root@10.0.2.18's password:

[bbeaudoin@cerebus ansible-pikvm]$ ssh-copy-id root@10.0.2.18
/usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
/usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
root@10.0.2.18's password:

Number of key(s) added: 1

Now try logging into the machine, with:   "ssh 'root@10.0.2.18'"
and check to make sure that only the key(s) you wanted were added.
```

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
