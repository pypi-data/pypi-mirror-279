import sys, os
## Code to disable creating pycache dir after running
sys.dont_write_bytecode = True
###################################################

sys.path.append(os.path.abspath(f"{os.getcwd()}/src/"))

from redhat_assisted_installer import assisted_installer
from requests.exceptions import HTTPError
from redhat_assisted_installer.lib.schema.cluster import ClusterParams

installer = assisted_installer.assisted_installer()

try:
    cluster_params = ClusterParams(
        name="pypi-testing",
        openshift_version="4.15",
        cpu_architecture="None",
        vip_dhcp_allocation=False,
        high_availability_mode="None",
        base_dns_domain="batchelor.live"
    )

    cluster = installer.patch_cluster(cluster=cluster_params)
    print(cluster)

except HTTPError as e:
    print("bad response code")
    print(e)

except Exception as e:
    print(e)