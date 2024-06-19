import sys, os
## Code to disable creating pycache dir after running
sys.dont_write_bytecode = True

sys.path.append(os.path.abspath(f"{os.getcwd()}/tests/"))

from utils import *

sys.path.append(os.path.abspath(f"{os.getcwd()}/src/"))

from redhat_assisted_installer import assisted_installer

import pprint

try:
    infra = assisted_installer.get_infrastructure_environements()
    pprint.pprint(infra.json(), compact=True)
    print(len(infra.json()))

except Exception as e:
    print(e)