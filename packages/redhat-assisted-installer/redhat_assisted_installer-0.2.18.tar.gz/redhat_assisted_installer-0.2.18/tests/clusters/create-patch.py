import sys, os
## Code to disable creating pycache dir after running
sys.dont_write_bytecode = True
###################################################

sys.path.append(os.path.abspath(f"{os.getcwd()}/src/"))

from redhat_assisted_installer import assisted_installer
from requests.exceptions import HTTPError
from redhat_assisted_installer.lib.schema.cluster import ClusterParams

sys.path.append(os.path.abspath(f"{os.getcwd()}/tests/"))
from utils import *

installer = assisted_installer.assisted_installer()

try:
    create_params = ClusterParams(
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
    cluster = installer.post_cluster(cluster=create_params)

    patch_parms = ClusterParams(
        cluster_id=get_input("Please enter the cluster id of the cluster to patch: "),
        name=get_input("Please enter the name of the cluster to patch: "),
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
    
    patched_cluster = installer.patch_cluster(cluster=patch_parms)

    clusters = installer.get_clusters()
    print(len(clusters))

except HTTPError as e:
    print("bad response code")
    print(e)

except Exception as e:
    print(e)