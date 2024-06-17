import os

from ..utils import *

class ClusterParams:
    def __init__(self, 
                 name: str = None, 
                 openshift_version: str = None,
                 cluster_id: str = None, 
                 pull_secret: str = os.environ.get("REDHAT_PULL_SECRET"),
                 additional_ntp_source: str = None,
                 api_vip: str = None,
                 base_dns_domain: str = None,
                 cluster_network_cidr: str = None,
                 cluster_network_host_prefix: int = None,
                 cpu_architecture: str = None,
                 high_availability_mode: str = None,
                 http_proxy: str = None,
                 https_proxy: str = None,
                 hyperthreading: str = None,
                 ingress_vip: str = None,
                 network_type: str = None,
                 service_network_cidr: str = None,
                 user_managed_networking: bool = None,
                 ssh_authorized_key: str = None,
                 vip_dhcp_allocation: bool = None,
                ):
        self.params = {}

        if name is not None:
            self.params['name'] = name

        if openshift_version is not None and is_valid_openshift_version(openshift_version):
            self.params['openshift_version'] = openshift_version

        if cluster_id is not None:
            self.params['cluster_id'] = cluster_id

        if pull_secret is not None and is_valid_json(pull_secret):
            self.params['pull_secret'] = pull_secret

        if additional_ntp_source is not None and is_valid_ip(additional_ntp_source):
            self.params['additional_ntp_source'] = additional_ntp_source

        if api_vip is not None and is_valid_ip(api_vip):
            self.params['api_vip'] = api_vip

        if base_dns_domain is not None and is_valid_base_domain(base_dns_domain):
            self.params['base_dns_domain'] = base_dns_domain

        if cluster_network_cidr is not None and is_valid_cidr(cluster_network_cidr):
            self.params['cluster_network_cidr'] = cluster_network_cidr

        if cluster_network_host_prefix is not None and isinstance(cluster_network_host_prefix, int) and cluster_network_host_prefix > 0 and cluster_network_host_prefix < 128:
            self.params['cluster_network_host_prefix'] = cluster_network_host_prefix

        if cpu_architecture is not None and is_valid_cpu_architecture(cpu_architecture):
            self.params['cpu_architecture'] = cpu_architecture

        if high_availability_mode is not None and is_valid_ha_mode(high_availability_mode):
            self.params['high_availability_mode'] = high_availability_mode

        if http_proxy is not None and is_valid_ip(http_proxy):
            self.params['http_proxy'] = http_proxy

        if https_proxy is not None and is_valid_ip(https_proxy):
            self.params['https_proxy'] = https_proxy

        if hyperthreading is not None and is_valid_hyperthread(hyperthreading):
            self.params['hyperthreading'] = hyperthreading

        if ingress_vip is not None and is_valid_ip(ingress_vip):
            self.params['ingress_vip'] = ingress_vip

        if network_type is not None and is_valid_network_type(network_type):
            self.params['network_type'] = network_type

        if service_network_cidr is not None and is_valid_cidr(service_network_cidr):
            self.params['service_network_cidr'] = service_network_cidr

        if ssh_authorized_key is not None:
            self.params['ssh_authorized_key'] = ssh_authorized_key

        if user_managed_networking is not None:
            self.params['user_managed_networking'] = user_managed_networking

        if vip_dhcp_allocation is not None:
            self.params['vip_dhcp_allocation'] = vip_dhcp_allocation

    def create_params(self):
        return {key: value for key, value in self.params.items() if value is not None}
    


