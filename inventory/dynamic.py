#!/usr/bin/env python3
"""
A dynamic inventory modified from the example originally written by
Jose Vicente Nunez Zuleta (kodegeek.com@protonmail.com) from
https://www.redhat.com/sysadmin/ansible-dynamic-inventory-python

Basically self-maintaining as long as inventory/host_vars has a static
definition for each of the hosts. Brian Beaudoin (bbeaudoin@redhat.com)
"""
import json
import os
import argparse

def get_empty_vars():
    return json.dumps({})

def get_list(pretty=False) -> str:
    data = {
        '_meta': {
          'hostvars': {}
        },
        'all': {
            'children': [
                'ungrouped'
            ]
        },
        'ungrouped': {
            'hosts': os.listdir(os.path.dirname(os.path.realpath(__file__)) + "/host_vars")
        }
    }
    return json.dumps(data, indent=pretty)

if __name__ == '__main__':

    arg_parser = argparse.ArgumentParser(
        description=__doc__,
        prog=__file__
    )
    arg_parser.add_argument(
        '--pretty',
        action='store_true',
        default=False,
        help="Pretty print JSON"
    )
    mandatory_options = arg_parser.add_mutually_exclusive_group()
    mandatory_options.add_argument(
        '--list',
        action='store',
        nargs="*",
        default="dummy",
        help="Show JSON of all managed hosts"
    )
    mandatory_options.add_argument(
        '--host',
        action='store',
        help="Display vars related to the host"
    )

    try:
        args = arg_parser.parse_args()
        if args.host:
            print(get_empty_vars())
        elif len(args.list) >= 0:
            print(get_list(args.pretty))
        else:
            raise ValueError("Expecting either --host $HOSTNAME or --list")

    except ValueError:
        raise
