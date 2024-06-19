import sys, os
## Code to disable creating pycache dir after running
sys.dont_write_bytecode = True
###################################################

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

    create_api_response = assisted_installer.post_infrastructure_environment(infra_env=infra)
    create_api_response.raise_for_status()
    pprint.pprint(create_api_response.json(), compact=True)

    if assisted_installer.delete_infrastructure_environment(infra_env_id=create_api_response.json()['id']):
        print(f"Successfully delete infra_env: {create_api_response.json()['id']}")
        infra_envs = assisted_installer.get_infrastructure_environements()
        pprint.pprint(infra_envs.json(), compact=True)
        print(len([infra_envs.json()]))
    else:
        print(f"Failed to delete infra_env: {create_api_response.json()['id']}")

except Exception as e:
    print(f"Failed to create infra_env: {create_api_response.json()['id']}")
