import sys, os
## Code to disable creating pycache dir after running
sys.dont_write_bytecode = True
###################################################

sys.path.append(os.path.abspath(f"{os.getcwd()}/src/"))

from redhat_assisted_installer import assisted_installer
from requests.exceptions import HTTPError

installer = assisted_installer.assisted_installer()

try:
    cluster = installer.post_cluster("pypi-testing", "4.15")
    installer.delete_cluster(cluster[0]['id'])
    clusters = installer.get_clusters()
    print(len(clusters))
except HTTPError as e:
    print("bad response code")
    print(e)

except Exception as e:
    print(e)



