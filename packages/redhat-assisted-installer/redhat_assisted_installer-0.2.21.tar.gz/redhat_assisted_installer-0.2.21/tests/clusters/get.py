import sys, os
## Code to disable creating pycache dir after running
sys.dont_write_bytecode = True

sys.path.append(os.path.abspath(f"{os.getcwd()}/src/"))
from redhat_assisted_installer import assisted_installer
from requests.exceptions import HTTPError


installer = assisted_installer.assisted_installer()

try:
    id = input("Please enter the cluster id you want to get (leave blank to get all): ")
    if id == "":
        cluster = installer.get_clusters()
        print(len(cluster))
    else:
        cluster = installer.get_cluster(cluster_id=id)
        

except HTTPError as e:
    print("bad response code")
    print(e)


except Exception as e:
    print(e)