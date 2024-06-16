import sys, os
## Code to disable creating pycache dir after running
sys.dont_write_bytecode = True
###################################################

sys.path.append(os.path.abspath(f"{os.getcwd()}/src/"))

from redhat_assisted_installer import assisted_installer
from requests.exceptions import HTTPError

installer = assisted_installer.assisted_installer()


try:
    infras = installer.get_infrastructure_environements()

except HTTPError as e:
    print("bad response code")
    print(e)

except Exception as e:
    print(e)
