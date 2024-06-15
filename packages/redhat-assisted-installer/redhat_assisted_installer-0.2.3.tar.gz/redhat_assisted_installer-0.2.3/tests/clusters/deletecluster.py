import sys, os
## Code to disable creating pycache dir after running
sys.dont_write_bytecode = True
###################################################

sys.path.append(os.path.abspath(f"{os.getcwd()}/src/"))

import redhat_assisted_installer.assisted_installer as assisted_installer

installer = assisted_installer.assisted_installer()

try:
    installer.delete_cluster(input("Please enter cluster_id you want to delete "))

except Exception as e:
    print("Found Exception")
    print(e)
