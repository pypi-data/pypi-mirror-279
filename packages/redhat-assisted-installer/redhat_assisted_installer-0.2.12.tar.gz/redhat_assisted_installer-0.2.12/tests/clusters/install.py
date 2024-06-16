import sys, os
## Code to disable creating pycache dir after running
sys.dont_write_bytecode = True
###################################################

sys.path.append(os.path.abspath(f"{os.getcwd()}/src/"))

from redhat_assisted_installer import assisted_installer
from requests.exceptions import HTTPError

installer = assisted_installer.assisted_installer()

try:
    cluster = installer.post_cluster(name="pypi-testing", openshift_version="4.15", base_dns_domain="example.com")
    
    installer.patch_cluster(cluster['id'], base_dns_domain="batchelor.live")

    installer.install_cluster(cluster['id'])

    installer.delete_cluster(cluster['id'])

except HTTPError as e:
    print("bad response code")
    print(e)


except Exception as e:
    print(e)
