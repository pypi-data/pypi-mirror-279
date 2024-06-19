import sys, os
## Code to disable creating pycache dir after running
sys.dont_write_bytecode = True
###################################################

sys.path.append(os.path.abspath(f"{os.getcwd()}/tests/"))

from utils import *

sys.path.append(os.path.abspath(f"{os.getcwd()}/src/"))

from redhat_assisted_installer import assisted_installer


try:
    assisted_installer.delete_cluster(input("Please enter cluster_id you want to delete "))

except Exception as e:
    print("Found Exception")
    print(e)
