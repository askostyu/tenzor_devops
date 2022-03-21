#!/usr/bin/python

import re

from ansible.errors import (
    AnsibleFilterTypeError
)


def to_mac(string):
    '''
        Converts string to mac-address
    '''
    is_mac_valid_pattern = r"^[0-9A-Fa-f]{12}$"
    if not re.search(is_mac_valid_pattern, string):
        raise AnsibleFilterTypeError(f"Cant convert string {string} to mac-address")
    mac_address = ":".join(re.findall(r"[0-9A-Fa-f]{2}", string))  
    return mac_address


class FilterModule(object):
    def filters(self):
        return {
            'filter_function': to_mac
        }
