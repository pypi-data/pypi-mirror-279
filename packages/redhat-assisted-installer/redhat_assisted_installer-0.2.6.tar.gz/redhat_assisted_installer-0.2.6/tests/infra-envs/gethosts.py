import sys, os
## Code to disable creating pycache dir after running
sys.dont_write_bytecode = True
###################################################

sys.path.append(os.path.abspath(f"{os.getcwd()}/src/"))

from redhat_assisted_installer import assisted_installer

installer = assisted_installer.assisted_installer()

try:

    cluster = installer.get_infrastructure_environement_hosts(infra_env_id="29da0d7c-871f-4a9e-b502-6b38954e186a")
    cluster = installer.get_infrastructure_environement_host(infra_env_id="29da0d7c-871f-4a9e-b502-6b38954e186a", host_id="614cf93e-b64a-487e-81b8-265dba35e43d")
    

except Exception as e:
    print(e)
