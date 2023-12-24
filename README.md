# Ansible Playbook to secure and configure PiKVM
## Introduction
As someone who uses immutable infrastructure, declarative GitOps, infrastructure as code, and values automation to set, maintain, and secure my IoT (Internet of Things) devices with a lot of PiKVM hosts to manage, I decided to write and maintain a set of playbooks and extend them for others to use as well.

## Disclaimers
_**These playbooks are provided as-is, without warranty. Please read the information here and be sure you understand the risks before using.**_

I'm just a user. I'm employed in the IT industry and a health sciences student at my local university. I am neither affiliated with PiKVM nor do they endorse this project. My employer permits me to contribute my own code to the community, this code is not my employer's code nor do they support or endorse this project in any way. My opinions are my own and do not reflect those of my employer, my school, nor the PiKVM project.

Please note I do not provide support for PiKVM, if you need help from the community please see the documentation at https://docs.pikvm.org/, I will not respond to general questions. I will do my best to help with the playbooks, however, as time permits.

# Using the playbook (Quick Start)
This project is about a week old, my Ansible skills have gotten rusty, there have been lots of changes to Ansible over the past 18 months, and I have to make things work as best as I can with the upstream project in a way that makes sense, both to me and to the PiKVM installations I'm working with. That said much of what is already defined shouldn't change without good reason but any variables in group or host vars that aren't used may never be used or may not have the same format once I start writing the tasks to use them. The `override*.yaml` files will definitely be going away in the future though.

## Warning (Important Note)
Although this project does not make any firmware changes, persisting changes only to the SD card, it is possible that the code or pre-existing software or physical state of the SD card (damage, corruption, etc.) when used with this playbook or the configuration can leave your PiKVM OS inaccessible or in worse state.

Please use a fresh SD card and fresh image from https://pikvm.org/download/. If you have any pre-existing configuration, please back it up somewhere safe before using the playbooks.

## High Level Overview
If you have used both Git and Ansible before and are familiar with the directory structure, YAML, playbooks, tasks, inventories, etc. you should not find any surprises here. If you haven't, you may be more comfortable learning one or more of the above topics.

1. Install git and ansible-core on a Linux or MacOS machine. If you're on Windows, you can install Linux from the Windows store.
2. Clone this repository on your compatible system or virtual machine.
3. Generate an SSH public-private keypair using `ssh-keygen` and copy to the PiKVM hosts using `ssh-copy-id root@<host>`
4. Put the root and admin passwords you want into the following files by default:
   1. `./ansible-pikvm/files/password-root`
   2. `./ansible-pikvm/files/password-admin`
5. Note, if you do not provide custom passwords, random passwords will be generated and written to these files.
6. If your passwords get reset, you should be able to use the SSH keys installed in step 3 to access your PiKVMs.
7. If you set a passphrase on your SSH keys, you may need to use `ssh-agent` and `ssh-add`
   1. Tip: Add `eval $(ssh-agent)` to `~/.bash_profile` so it runs on login.
   2. Tip: Also add `kill ${SSH_AGENT_PID}` to `~/.bash_logout` to prevent leaving 100 unused agents running.
8. Your main configuration files will be the following:
   1. For configuration common to all hosts: `./ansible-pikvm/inventory/group_vars/all.yml`
   2. For host-specific configuration: `./ansible-pikvm/inventory/host_vars/pikvm.yml`
9. Remove any other inventory `host_vars` files after using them as examples for your own hosts.
10. DO NOT REMOVE THE `./ansible-pikvm/inventory/dynamic.py` script. That is used to create the inventory.
11. Currently the example overrides are not templated and are in the `files` subdirectory.
    1. The default configuration will overwrite any overrides on existing hosts.
    2. Change or replace the existing `override*.yaml` files as needed to fit your configuration.
13. If you haven't already, use `cd` to enter `ansible-pikvm` subdirectory itself.
14. If you haven't already, read the task list in the playbook in `main.yml`
    1. Comment out or remove any tasks you do not want to perform.
    2. Some will exclude themselves if certain conditions are not met (variable is not defined).
    3. Leave the read-write, read-only, recovery block, and restart/reboot tasks at a minimum.
    4. You can always make a backup of `main.yml` or use `git reset --hard` to discard all changes.
16. Check your host inventory and variables, using `ansible-inventory --list`.
17. Check the main.yaml playbook using `ansible-playbook --syntax-check main.yml`.
18. If you don't see any errors, you can run without changes using `ansible-playbook --check main.yml`.
19. After ensuring the dry-run completes successfully, you can use `ansible-playbook main.yml`.

As the playbook and templates, even the configuration variables and formats or task lists aren't final, I haven't gone into too much detail. It is likely any changes you make locally will conflict with my changes so you may not be able to use `git pull` to download the latest updates and your configuration files may not be compatible with future changes to the playbook.

# Questions and Answers
It would be a misnomer to call this a "Frequently Asked Questions" section because nobody has really asked any questions yet. Moreso they are critical of the effort to standardize and automate configuration with one person saying I'm creating a "snowflake". That's certainly not the goal of consistent automation. I'll also most certainly change if there are upstream changes that make sense or become necessary.

## What is PiKVM?
PiKVM (https://pikvm.org/) is an IP KVM based on the Raspberry Pi platform. Users can build their own DIY PiKVM or purchase a device.

If you are here you probably
1. Have built a DIY or purchased a PiKVM and want to automate configuration and restores
2. Are considering building or buying your own PiKVM and wondering how to maintain it
3. Got lost on the Internet looking for https://google.com/.

For those in one of the first two categories, I hope you find this project helpful. If you're in the last category, hopefully you find the project and PiKVM worth looking into further and find the links and PiKVM useful.

## What does this playbook do?
In short, it's a set of tasks that performs both basic and advanced configuration of a PiKVM based on the Arch Linux Arm operating system. It's a work in progress but the following has been tested and verified against the DIY (V2), V3 (HAT), V4 Mini (CM4, no USB or HDMI output), and V4 Plus models. This has not been tested against the V1 or discontinued V0 versions.

## What are the benefits of this playbook?
The playbook automates all of the currently supported configuration against one or more PiKVM installations. It runs quickly and consistently (or as consistently as your network permits). Enthusastically speaking, the playbook benefits you by ensuring that

1. Your configuration is always backed up on the Ansible control host and can always be restored
2. Default passwords are replaced with your own strong passwords hashed with strong trusted cryptographic functions
3. An additional layer of network security is installed and configured on your PiKVM using firewalld
4. Software is updated to the latest available packages from Arch Linux Arm or the PiKVM project mirrors
5. Configuration settings specified for PiKVM are never lost, forgotten, or left default when replacing the SD card
6. Any non-default packages or services can be deployed and maintained on one or more of your installations
7. You can add or remove customizations automatically by pushing changes to PiKVM's override configuration
8. Automatically recover from errors that can leave your PiKVM vulnerable to power loss damage

Before writing a playbook, I did very little customizations that I wasn't willing to loose when my SD card became corrupted or unusable due to bad package updates. I was consistently forgetting to switch the SD card to read-only, rewriting and debugging override files, and often had to refer to my own GitHub Gists for configurations I had used in the past because I didn't have a local copy on my control host.

## What doesn't the playbook do?
There's a non-exhaustive list of what isn't in the playbooks yet:

1. Certificate installation and rotation. I'm doing this manually at the moment
2. Upload files to the MSD automatically or do anything really with PST.
3. Tailscale, Janus, OLED, fans, audio, edid, mouse jigglers, etc.

Read-write of root is still a requirement of most things so PST doesn't necessarily make sense to me to use yet. Nothing really supports it on PiKVM, if things move there and make sense to do, I'll move it into PST but there's no Ansible module for that, it would all be using `ansible.builtin.command` which is not idempotent.

## What will this project specifically avoid?
There are some things I'm specifically avoiding with this playbook for safety and compatibility.

1. There will not be any firmware modifications performed, nor exceptions.
2. Configuration that is contrary to the purpose of the upstream project is not accepted.
3. Unless there is good reason, this playbook will not break existing OS standards.
   1. This is contentious as the playbook seeks to minimize non-standard changes
   2. Until conventions become a baseline configuration standard, existing ones will be followed
4. Nothing that violates the spirit of the project or other's rights will be accepted.
5. Backward compatibility for older or legacy builds are explicitly out-of-scope.
6. Products or systems that are incompatible with the supported PiKVM software or OS.

There is a desire to keep this project open, inclusive, usable, and available.

## My General Motivations

The first playbook took minutes to write and probably saved me hours of effort. Looking back, less than 20% of that time was to meet my critical use cases, more than 80% of my time has been on extending, testing, scaling out the test to cover more systems, troubleshooting, linting, and documenting. It's my hope that when I'm done templating the files, managing the certificate configurations, and adding other features, that others might find this even more useful.

If others find this project useful, I'll have saved them much more time and effort than I have my own. If automation leads to more installations being standard, it may save the PiKVM project maintainers time and some of these changes might be adopted in the upstream project.

Next semester when my studies start again I won't have much time to maintain this code so I'm trying to get as much done now. Not only am I refreshing my Ansible skills that I can use in my job, I hope that I won't have to individually maintain my PiKVM installations or the automation aside from small updates to keep compatible with upsstream changes, especially as it's been suggested some standard configuration will move to a new data partition in the future.

# Credits
Credit for the dynamic inventory goes to Jose Vicente Nunez Zuleta. This saved me a lot of time and his licensing allows me to modify, publish with my modifications, and relicense the portions used under the project's license. You may see his original work in the following places:

https://www.redhat.com/sysadmin/ansible-dynamic-inventory-python
https://github.com/josevnz/ExtendingAnsibleWithPython

The PiKVM project (https://pikvm.org/) and documentation (https://docs.pikvm.org/) deserves a lot of credit. I previously used some of their comments and configuration examples in my files under the GNU General Public License v3.0. As the examples do not match the official YAML style guides and won't be helpful when the overrides are templated as Jinja2, I've removed the comments.

# Previous documentation that hasn't been updated
Ansible and YAML are meant to be both human and machine readable, but code is, first and foremost, supposed to be easy for machines to read. That humans can read it is a fortunate coincidence, while that's a consideration, humans aren't the intended audience for those files.

So much time is spent writing documentation that writing too much documentation while writing, testing, and developing code, that I'm not able to complete my goals quickly enough before I visit with my parents over the holidays. That said, I've removed anything in the following sections that might contradict what I've written more recently or is completely outdated with the latest changes. This section is the last of the updated documentation in the readme.

The following sections were meant to help those who didn't understand git, Ansible, SSH, etc. as a way to possibly help. That said, reading the documentation, learning how to write playbooks and tasks, and how to manage inventories may be best left to the other project's documentation than here, especially if writing and maintaining such things is duplicating efforts from those projects and their communities.

I'll shift my focus on the code and try to keep it understandable and add documentation in the form of comments where I belive things may be unclear to others. Please refer to the files, templates, playbooks, and examples of my own host configurations until I'm able to update the documentation here again.

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
ansible.cfg and inventory file or directory.

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

## Additional Information
The playbook and files are as-is with no warranty. Please review the files,
if any of the changes make your device unusable, you may need to reimage
your SD card using an appropriate image from https://pikvm.org/download/.

This has been tested with the November 20, 2023 image updates. If you have
a new PiKVM, I might recommend reimaging your device rather than updating
it before using this playbook. If you have any suggestions for improvement
of this playbook, please log an issue or submit a pull request.
