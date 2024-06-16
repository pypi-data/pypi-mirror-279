import sys, os
## Code to disable creating pycache dir after running
sys.dont_write_bytecode = True
###################################################

sys.path.append(os.path.abspath(f"{os.getcwd()}/src/"))

import redhat_assisted_installer.assisted_installer as assisted_installer

installer = assisted_installer.assisted_installer()

try:
    installer.cluster_get_files("2c478929-bdec-4c02-9bcf-1e7b6b7bdcde")
except Exception as e:
    print(e)