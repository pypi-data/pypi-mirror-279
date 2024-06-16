import sys, os
## Code to disable creating pycache dir after running
sys.dont_write_bytecode = True

sys.path.append(os.path.abspath(f"{os.getcwd()}/src/"))
from redhat_assisted_installer import assisted_installer
from requests.exceptions import HTTPError


installer = assisted_installer()

try:
    # cluster = installer.get_cluster(cluster_id="72d3187a-8997-4c14-a78d-dfee19f5a295")
    cluster = installer.get_cluster(cluster_id="2c478929-bdec-4c02-9bcf-1e7b6b7bdcde")
    clusters = installer.get_clusters()

except HTTPError as e:
    print("bad response code")
    print(e)


except Exception as e:
    print(e)