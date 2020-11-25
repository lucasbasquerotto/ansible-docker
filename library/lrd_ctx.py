#!/usr/bin/python

# (c) 2020, Lucas Basquerotto
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=wrong-import-position
# pylint: disable=import-error

from __future__ import absolute_import, division, print_function
__metaclass__ = type # pylint: disable=invalid-name

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: lrd_ctx
short_description: Return the context variables from the environment.
description:
   - Return the context variables from the environment.
version_added: "2.8"
options:
  ctx_name:
    description:
      - the context name
    type: str
    required: true
  env:
    description:
      - the environment dictionary.
    type: dict
    required: true
  validate:
    description:
      - specifies if the schemas should be validated
    type: bool
    default: true
notes:
   - You can any of those parameters or none (but some parameters require others).

author: "Lucas Basquerotto (@lucasbasquerotto)"
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_text
from ansible.module_utils.lrd_utils import error_text
from ansible.module_utils.lrd_util_ctx import prepare_ctx

# ===========================================
# Module execution.
#

def main():
  module = AnsibleModule(
      argument_spec=dict(
          ctx_name=dict(type='str', required=True),
          env=dict(type='dict', required=True),
          validate=dict(type='bool', default=True),
      )
  )

  ctx_name = module.params['ctx_name']
  env = module.params['env']
  validate_ctx = module.boolean(module.params['validate'])

  info = prepare_ctx(ctx_name, env, validate_ctx)

  result = info.get('result')
  error_msgs = info.get('error_msgs')

  if error_msgs:
    context = "ctx validation"
    module.fail_json(msg=to_text(error_text(error_msgs, context)))

  module.exit_json(changed=False, data=result)


if __name__ == '__main__':
  main()
