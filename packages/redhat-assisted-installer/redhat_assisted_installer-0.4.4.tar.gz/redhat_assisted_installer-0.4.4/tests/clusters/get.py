import sys, os
## Code to disable creating pycache dir after running
sys.dont_write_bytecode = True

sys.path.append(os.path.abspath(f"{os.getcwd()}/tests/"))

from utils import *

sys.path.append(os.path.abspath(f"{os.getcwd()}/src/"))
from redhat_assisted_installer import assisted_installer

import pprint

try:
    id = input("Please enter the cluster id you want to get (leave blank to get all): ")
    if id == "":
        cluster_response = assisted_installer.get_clusters()
        cluster_response.raise_for_status()
        pprint.pprint(cluster_response.json())
        print(len(cluster_response.json()))
    else:
        cluster_response = assisted_installer.get_cluster(cluster_id=id)
        cluster_response.raise_for_status()
        pprint.pprint(cluster_response.json())

except Exception as e:
    print(e)