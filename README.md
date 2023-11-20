# ansible-pikvm
Quick Ansible playbook for PiKVM

# Note

Due to a security scanner flagging the example secrets that aren't really a
secret, I took down the original so deep scans won't continue to report any
false positives and added the proper `# notsecret` hints to anything I think
might trip the alert again.

I'm also adding a `.gitleaks.toml` with the hashes. That should allow those
hashes, or any other example hashes, to be in files without getting flagged.
I might need to add `./files/htpasswd` because it seemed that alone might
have been enough as well.

# Warning

This isn't guaranteed to work for everyone. The inventory has the hosts
(and host addresses), the playbook is general-purpose, the files will be
overwritten on the target system.

A good starting point for myself to restore my settings on a fresh microSD
card; however, I have some differences between different units and this
currently doesn't make a distinction between them.

If you use this, please note I haven't tested the hashes used in the inventory
or the htpasswd but they should set the same as the defaults. Please modify to
suit your environment.
