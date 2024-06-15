import sys, os
## Code to disable creating pycache dir after running
sys.dont_write_bytecode = True
###################################################

sys.path.append(os.path.abspath(f"{os.getcwd()}/src/"))

import redhat_assisted_installer.assisted_installer as assisted_installer

installer = assisted_installer.assisted_installer()

try:
    cluster = installer.get_default_config()
    
except Exception as e:
    print(e)
