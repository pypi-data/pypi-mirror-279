"""
Copyright 2023-2023 VMware Inc.
SPDX-License-Identifier: Apache-2.0

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import click
import sys
from hcs_cli.service.admin import template
import hcs_core.sglib.cli_options as cli
from hcs_core.ctxp import recent


@click.command()
@click.argument("id", type=str, required=False)
@cli.org_id
@cli.wait
def retry(id: str, org: str, wait: str):
    """Retry necessary operations on a template by ID"""
    org_id = cli.get_org_id(org)
    id = recent.require(id, "template")
    t = template.get(id, org_id)
    if not t:
        return

    def _cancel_provision():
        try:
            template.action(id, org_id, "CANCEL_PROVISIONING")
        except Exception as e:
            print(str(e), file=sys.stderr)

        # wait for the template
        target_status = ["READY", "INIT", "PARTIALLY_PROVISIONED"]
        unexpected_status = ["DELETING"]
        template.wait_for(id, org_id, target_status=target_status, unexpected_status=unexpected_status, timeout="1m")

    # Template status:
    # READY, EXPANDING, SHRINKING, DELETING, INIT, PARTIALLY_PROVISIONED, ERROR

    status = t.get("reportedStatus", {}).get("status")
    if status == "EXPANDING":
        _cancel_provision()
    elif status == "SHRINKING":
        _cancel_provision()
    elif status == "INIT":
        _cancel_provision()
    elif status == "READY":
        return t
    elif status == "DELETING":
        return t
    elif status == "PARTIALLY_PROVISIONED":
        pass
    elif status == "ERROR":
        pass
    else:
        return "Unknown template status: " + status, 1

    t = template.action(id, org_id, "RETRY_PROVISIONING")

    t = template.wait_for(id, org_id, ["EXPANDING", "SHRINKING", "READY"], unexpected_status=[], timeout="20s")
    status = t.get("reportedStatus", {}).get("status")
    if status != "READY" and wait != "0":
        t = template.wait_for_ready(id, org_id, wait)
    return t
