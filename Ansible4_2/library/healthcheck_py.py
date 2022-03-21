#!/usr/bin/python3
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule
import requests


DOCUMENTATION = r'''
---
module: healthcheck
author: Pupkin V.
short_description: healthcheck of site
description:
  - healthcheck of site with or without TLS
version_added: 1.0.0
requirements:
  - requests
  - python >= 3.6
options:
  addr:
    description:
      - Address of site we want to check
      - This is a required parameter
    type: str
  tls:
    description:
      - Whether site using certificates or not
      - Default value is 'True'
    type: bool
'''

EXAMPLES = r'''
- name: Check availability of site
  healthcheck:
    addr: mysite.example
  connection: local

- name: Check availability of site without certs
  healthcheck:
    addr: mysite.example
    tls: false
  connection: local
'''

RETURN = r'''
msg:
  description: Errors if occured
  returned: always
  type: str
  sample: ""
site_status:
  description: State status
  returned: always
  type: str
  sample: Available
rc:
  description: Return code
  returned: always
  type: int
  sample: 200
'''

def check_web_server(addr, tls):
    msg=""
    rc = None
    if tls:
        url = f"https://{addr}"
    else:
        url = f"http://{addr}"
    try:
        response = requests.get(url, allow_redirects=False)
    except Exception as ex:
        msg = str(ex)
        site_status="Unavailable"
    else:
        site_status="Available"
        rc = response.status_code
    return msg, site_status, rc

def main():
    # Аргументы для модуля
    arguments = dict(
        addr=dict(required=True, type='str'),
        tls=dict(type='bool', default="True")
    )
    # Создаем объект - модуль
    module = AnsibleModule(
        argument_spec=arguments,
        supports_check_mode=False
    )
    # Получаем аргументы
    addr = module.params["addr"]
    tls = module.params["tls"]

    msg, site_status, rc = check_web_server(addr, tls)
    module.exit_json(changed=False,
                      failed=False,
                      result_str=site_status,
                      rc=rc,
                      msg=msg)



if __name__ == "__main__":
    main()