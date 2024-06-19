import sys, os
## Code to disable creating pycache dir after running
sys.dont_write_bytecode = True

sys.path.append(os.path.abspath(f"{os.getcwd()}/tests/"))

from utils import *

sys.path.append(os.path.abspath(f"{os.getcwd()}/src/"))

from redhat_assisted_installer import assisted_installer
from redhat_assisted_installer.lib.schema.infra_env import InfraEnv

import pprint


try:
    infra = InfraEnv(
        name=get_input("Please enter the name of the infra_env to create: "),
        openshift_version=get_input("Please enter the OpenShift version: "),
        pull_secret=get_input("Please enter the pull secret: ") or os.environ.get("REDHAT_PULL_SECRET"),
        additional_ntp_source=get_input("Please enter additional NTP sources: "),
        additional_trust_bundle=get_input("Please enter additional trust bundle: "),
        cpu_architecture=get_input("Please enter the CPU architecture: "),
        cluster_id=get_input("Please enter the cluster id: "),
        image_type=get_input("Please enter the image type: "),
        ssh_authorized_key=get_input("Please enter the SSH authorized key: "),
    )

    api_response = assisted_installer.post_infrastructure_environment(infra_env=infra)
    api_response.raise_for_status()
    pprint.pprint(api_response.json(), compact=True)
    print(len([api_response.json()]))

except Exception as e:
    print(e)
