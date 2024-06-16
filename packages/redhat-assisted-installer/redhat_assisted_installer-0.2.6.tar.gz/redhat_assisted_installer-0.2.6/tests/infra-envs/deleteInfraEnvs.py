import sys, os
## Code to disable creating pycache dir after running
sys.dont_write_bytecode = True
###################################################

sys.path.append(os.path.abspath(f"{os.getcwd()}/src/"))

import redhat_assisted_installer.assisted_installer as assisted_installer

installer = assisted_installer.assistedinstaller()

infras = installer.getInfrastructureEnvironments()

for infra in infras:
    installer.deleteInfrastructureEnvironment(infra['id'])