import sys, os
## Code to disable creating pycache dir after running
sys.dont_write_bytecode = True
###################################################

sys.path.append(os.path.abspath(f"{os.getcwd()}/tests/"))

from utils import *

sys.path.append(os.path.abspath(f"{os.getcwd()}/src/"))

from redhat_assisted_installer import assisted_installer
from redhat_assisted_installer.lib.schema.cluster import ClusterParams

sys.path.append(os.path.abspath(f"{os.getcwd()}/tests/"))
import pprint

from utils import *

try:
    params = ClusterParams(
        name=get_input("Please enter the name of the cluster to create: "),
        openshift_version=get_input("Please enter the OpenShift version: "),
        pull_secret=get_input("Please enter the pull secret: ") or os.environ.get("REDHAT_PULL_SECRET"),
        additional_ntp_source=get_input("Please enter additional NTP sources: "),
        api_vip=get_input("Please enter the API VIP: "),
        base_dns_domain=get_input("Please enter the base DNS domain: "),
        cluster_network_cidr=get_input("Please enter the cluster network CIDR: "),
        cluster_network_host_prefix=get_input("Please enter the cluster network host prefix: ", int),
        cpu_architecture=get_input("Please enter the CPU architecture: "),
        high_availability_mode=get_input("Please enter the high availability mode: "),
        http_proxy=get_input("Please enter the HTTP proxy URL: "),
        https_proxy=get_input("Please enter the HTTPS proxy URL: "),
        hyperthreading=get_input("Please enter the hyperthreading setting: "),
        ingress_vip=get_input("Please enter the ingress VIP: "),
        network_type=get_input("Please enter the network type: "),
        service_network_cidr=get_input("Please enter the service network CIDR: "),
        user_managed_networking=get_input("Is the networking managed by the user? (True/False): ", lambda x: x.lower() == 'true'),
        ssh_authorized_key=get_input("Please enter the SSH authorized key: "),
        vip_dhcp_allocation=get_input("Is VIP DHCP allocation enabled? (True/False): ", lambda x: x.lower() == 'true')
    )

    create_api_response = assisted_installer.post_cluster(params)
    create_api_response.raise_for_status()
    print(f"Successfully created cluster: {create_api_response.json()['id']}")
    
    if assisted_installer.delete_cluster(cluster_id=create_api_response.json()['id']):
        print(f"Successfully delete cluster: {create_api_response.json()['id']}")
        clusters = assisted_installer.get_clusters()
        pprint.pprint(clusters.json(), compact=True)
        print(len([clusters.json()]))
    else:
        print(f"Failed to delete cluster: {create_api_response.json()['id']}")

except Exception as e:
    print(e)

    