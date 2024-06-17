import sys, os
## Code to disable creating pycache dir after running
sys.dont_write_bytecode = True
###################################################

sys.path.append(os.path.abspath(f"{os.getcwd()}/src/"))

from redhat_assisted_installer import assisted_installer
from requests.exceptions import HTTPError

installer = assisted_installer.assisted_installer()

try:
    installer.delete_cluster(input("Please enter cluster_id you want to delete "))

except HTTPError as e:
    print("bad response code")
    print(e)

except Exception as e:
    print("Found Exception")
    print(e)
