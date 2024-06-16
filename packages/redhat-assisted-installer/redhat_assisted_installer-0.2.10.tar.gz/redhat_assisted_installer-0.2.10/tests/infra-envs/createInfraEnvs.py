import sys, os
## Code to disable creating pycache dir after running
sys.dont_write_bytecode = True



sys.path.append(os.path.abspath(f"{os.getcwd()}/src/"))

from redhat_assisted_installer import assisted_installer
from requests.exceptions import HTTPError

installer = assisted_installer.assisted_installer()

installer.post_infrastructure_environment("testing-infra", version="4.15")