import sys, os
## Code to disable creating pycache dir after running
sys.dont_write_bytecode = True
###################################################
sys.path.append(os.path.abspath(f"{os.getcwd()}/src/"))
from redhat_assisted_installer import assisted_installer
