import sys, os
## Code to disable creating pycache dir after running
sys.dont_write_bytecode = True
###################################################

sys.path.append(os.path.abspath(f"{os.getcwd()}/tests/"))

from utils import *

sys.path.append(os.path.abspath(f"{os.getcwd()}/src/"))

from redhat_assisted_installer import assisted_installer

import pprint

try:
    if assisted_installer.delete_infrastructure_environment(input("Please enter infra_env_id you want to delete ")):
        print("Successfully deleted infra_env")
    else:
        print("Failed to delete infra_env")

    infra_envs = assisted_installer.get_infrastructure_environements()
    infra_envs.raise_for_status()
    pprint.pprint(infra_envs.json(), compact=True)
    print(len(infra_envs.json()))

except Exception as e:
    print("Found Exception")
    print(e)
