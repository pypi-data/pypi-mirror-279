import sys, os
## Code to disable creating pycache dir after running
sys.dont_write_bytecode = True
###################################################

sys.path.append(os.path.abspath(f"{os.getcwd()}/src/"))

import redhat_assisted_installer.assisted_installer as assisted_installer

installer = assisted_installer.assisted_installer()


try:
    infra_env = installer.post_infrastructure_environment("pypi-testing")
    installer.delete_infrastructure_environment(infra_env['id'])
    print(installer.get_infrastructure_environements())

except Exception as e:
    print("Raised Exception")
    print(e)


