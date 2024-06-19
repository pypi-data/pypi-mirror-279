import sys, os
## Code to disable creating pycache dir after running
sys.dont_write_bytecode = True
###################################################

sys.path.append(os.path.abspath(f"{os.getcwd()}/tests/"))

from utils import *

sys.path.append(os.path.abspath(f"{os.getcwd()}/src/"))


from redhat_assisted_installer.assisted_installer import *
from redhat_assisted_installer.lib.schema.cluster import *

import pprint


additional_ntp_sources = "time.google.com"

api_vips = [APIVIP(cluster_id=None,
                  ip="10.128.0.3",
                  )]

base_dns_domain = "example.com"

cluster_networks = [ClusterNetworks(cidr="10.128.0.0/14",
                                    )]

cpu_acrchitecture = "x86_64"

disk_encryption = DiskEncryption(enable_on="none",
                                 )

high_availability_mode = None

http_proxy="http://test:test@192.168.5.1:80"

https_proxy="http://test:test@192.168.6.1:443"

hyperthreading = "all"

# ingnition_endpoint = IgnitionEndpoint()

ingress_vips = [IngressVIP(ip="10.128.0.2",
                           
                           )]

machine_networks = [MachineNetwork(cidr="10.128.0.0/14",
                                   
                                   )]

name = "pypi-testing"

network_type = "OVNKubernetes"

no_proxy = "192.168.7.1"

openshift_version = "4.15"

external_platform = PlatformExternal()

platform = Platform(external=external_platform,
                    type="baremetal",
                    )

schedulable_masters = False

service_networks = [ServiceNetwork(cidr="172.30.0.0/16")]

tags = "openshift,production"

user_managed_networking = False

vip_dhcp_allocation = False

cluster = Cluster(additional_ntp_source=additional_ntp_sources,
                 api_vips=api_vips,
                 base_dns_domain=base_dns_domain,
                 cluster_networks=cluster_networks,
                 cpu_architecture=cpu_acrchitecture,
                 disk_encryption=disk_encryption,     
                 high_availability_mode=high_availability_mode,
                 http_proxy=http_proxy,
                 https_proxy=https_proxy,
                 hyperthreading=hyperthreading,
                #  ignition_endpoint=ingnition_endpoint,
                 ingress_vips=ingress_vips,
                 machine_networks=machine_networks,
                 name=name, 
                 network_type=network_type,
                 no_proxy=no_proxy,
                #  ocp_release_image = None,
                #  olm_operator=olm_operators,
                 openshift_version=openshift_version,
                 platform=platform,
                 pull_secret = os.environ.get("REDHAT_PULL_SECRET"),
                 schedulable_masters=schedulable_masters,
                 service_networks=service_networks,
                #  ssh_public_key=ssh_public_key,
                 tags=tags,
                 user_managed_networking=user_managed_networking,
                 vip_dhcp_allocation=vip_dhcp_allocation,
                #  cluster_id = None,
                 )

pprint.pprint(cluster.create_params())

try: 
    api_response = post_cluster(cluster)
    api_response.raise_for_status()
    pprint.pprint(api_response.json())

except Exception as e:
    print(e)
    print(api_response.json())