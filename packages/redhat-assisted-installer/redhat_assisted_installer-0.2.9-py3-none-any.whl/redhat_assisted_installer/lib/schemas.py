from typing import List, Optional, Dict, Any, Union


class ClusterCreateParams:
    def __init__(self, 
                 name: str, 
                 openshift_version: str, 
                 pull_secret: str,
                 additional_ntp_source: Optional[str] = None,
                 base_dns_domain: Optional[str] = None,
                 cluster_network_cidr: Optional[str] = "10.128.0.0/14",
                 cluster_network_host_prefix: Optional[int] = 23,
                 cpu_architecture: Optional[str] = "x86_64",
                 high_availability_mode: Optional[str] = "None",
                 http_proxy: Optional[str] = None,
                 https_proxy: Optional[str] = None,
                 hyperthreading: Optional[str] = "all",
                 network_type: Optional[str] = None,
                 no_proxy: Optional[str] = None,
                 ocp_release_image: Optional[str] = None,
                 schedulable_masters: Optional[bool] = False,
                 service_network_cidr: Optional[str] = "172.30.0.0/16",
                 ssh_public_key: Optional[str] = None,
                 tags: Optional[str] = None,
                 user_managed_networking: Optional[bool] = False,
                 vip_dhcp_allocation: Optional[bool] = False,
                ):
        self.name = name
        self.openshift_version = openshift_version
        self.pull_secret = pull_secret
        self.additional_ntp_source = additional_ntp_source
        self.base_dns_domain = base_dns_domain
        self.cluster_network_cidr = cluster_network_cidr
        self.cluster_network_host_prefix = cluster_network_host_prefix
        self.cpu_architecture = cpu_architecture
        self.high_availability_mode = high_availability_mode
        self.http_proxy = http_proxy
        self.https_proxy = https_proxy
        self.hyperthreading = hyperthreading
        self.network_type = network_type
        self.no_proxy = no_proxy
        self.ocp_release_image = ocp_release_image
        self.schedulable_masters = schedulable_masters
        self.service_network_cidr = service_network_cidr        
        self.ssh_public_key = ssh_public_key
        self.tags = tags
        self.user_managed_networking = user_managed_networking
        self.vip_dhcp_allocation = vip_dhcp_allocation

    def to_dict(self):
        return {
            "name": self.name,
            "openshift_version": self.openshift_version,
            "pull_secret": self.pull_secret,
            "additional_ntp_source": self.additional_ntp_source,
            "base_dns_domain": self.base_dns_domain,
            "cluster_network_cidr": self.cluster_network_cidr,
            "cluster_network_host_prefix": self.cluster_network_host_prefix,
            "cpu_architecture": self.cpu_architecture,
            "high_availability_mode": self.high_availability_mode,
            "http_proxy": self.http_proxy,
            "https_proxy": self.https_proxy,
            "hyperthreading": self.hyperthreading,
            "network_type": self.network_type,
            "no_proxy": self.no_proxy,
            "ocp_release_image": self.ocp_release_image,
            "schedulable_masters": self.schedulable_masters,
            "service_network_cidr": self.service_network_cidr,
            "ssh_public_key": self.ssh_public_key,
            "tags": self.tags,
            "user_managed_networking": self.user_managed_networking,
            "vip_dhcp_allocation": self.vip_dhcp_allocation
        }


class InfraEnvCreateParams:
    def __init__(self, 
                 name: str, 
                 pull_secret: str,
                 additional_ntp_sources: Optional[str] = None,
                 additional_trust_bundle: Optional[str] = None,
                 cluster_id: Optional[str] = None,
                 cpu_architecture: Optional[str] = "x86_64",
                 ignition_config_override: Optional[str] = None,
                 openshift_version: Optional[str] = None,
                 ssh_authorized_key: Optional[str] = None,
                 ):
        self.name = name
        self.pull_secret = pull_secret
        self.additional_ntp_sources = additional_ntp_sources
        self.additional_trust_bundle = additional_trust_bundle
        self.cluster_id = cluster_id
        self.cpu_architecture = cpu_architecture
        self.ignition_config_override = ignition_config_override
        self.openshift_version = openshift_version
        self.ssh_authorized_key = ssh_authorized_key

    def to_dict(self):
        return {
            "name": self.name,
            "pull_secret": self.pull_secret,
            "additional_ntp_sources": self.additional_ntp_sources,
            "additional_trust_bundle": self.additional_trust_bundle,
            "cluster_id": self.cluster_id,
            "cpu_architecture": self.cpu_architecture,
            "ignition_config_override": self.ignition_config_override,
            "openshift_version": self.openshift_version,
            "ssh_authorized_key": self.ssh_authorized_key,
        }


class ClusterUpdateParams:
    def __init__(self,
                 pull_secret: str,
                 additional_ntp_source: Optional[str] = None,
                 api_vip_dns_name: Optional[str] = None,
                 base_dns_domain: Optional[str] = None,
                 cluster_network_cidr: Optional[str] = None,
                 cluster_network_host_prefix: Optional[int] = None,
                 http_proxy: Optional[str] = None,
                 https_proxy: Optional[str] = None,
                 hyperthreading: Optional[str] = None,
                 name: Optional[str] = None,
                 network_type: Optional[str] = None,
                 no_proxy: Optional[str] = None,
                 schedulable_masters: Optional[bool] = None,
                 service_network_cidr: Optional[str] = None,
                 ssh_public_key: Optional[str] = None,
                 tags: Optional[str] = None,
                 user_managed_networking: Optional[bool] = None,
                 vip_dhcp_allocation: Optional[bool] = None,
                 ):
        self.additional_ntp_source = additional_ntp_source
        self.api_vip_dns_name = api_vip_dns_name
        self.base_dns_domain = base_dns_domain
        self.cluster_network_cidr = cluster_network_cidr
        self.cluster_network_host_prefix = cluster_network_host_prefix
        self.http_proxy = http_proxy
        self.https_proxy = https_proxy
        self.hyperthreading = hyperthreading
        self.name = name
        self.network_type = network_type
        self.no_proxy = no_proxy
        self.pull_secret = pull_secret
        self.schedulable_masters = schedulable_masters
        self.service_network_cidr = service_network_cidr
        self.ssh_public_key = ssh_public_key
        self.tags = tags
        self.user_managed_networking = user_managed_networking
        self.vip_dhcp_allocation = vip_dhcp_allocation

    def to_dict(self):
        return {
            "additional_ntp_source": self.additional_ntp_source,
            "api_vip_dns_name": self.api_vip_dns_name,
            "base_dns_domain": self.base_dns_domain,
            "cluster_network_cidr": self.cluster_network_cidr,
            "cluster_network_host_prefix": self.cluster_network_host_prefix,
            "http_proxy": self.http_proxy,
            "https_proxy": self.https_proxy,
            "hyperthreading": self.hyperthreading,
            "name": self.name,
            "network_type": self.network_type,
            "no_proxy": self.no_proxy,
            "pull_secret": self.pull_secret,
            "schedulable_masters": self.schedulable_masters,
            "service_network_cidr": self.service_network_cidr,
            "ssh_public_key": self.ssh_public_key,
            "tags": self.tags,
            "user_managed_networking": self.user_managed_networking,
            "vip_dhcp_allocation": self.vip_dhcp_allocation
        }
    
class InfraEnvUpdateParams:
    def __init__(self,
                 pull_secret: str,
                 additional_ntp_sources: Optional[str] = None,
                 additional_trust_bundle: Optional[str] = None,
                 ignition_config_override: Optional[str] = None,
                 image_type: Optional[str] = None,
                 ssh_authorized_key: Optional[str] = None,
                 ):
        self.additional_ntp_sources = additional_ntp_sources
        self.additional_trust_bundle = additional_trust_bundle
        self.ignition_config_override = ignition_config_override
        self.image_type = image_type
        self.pull_secret = pull_secret
        self.ssh_authorized_key = ssh_authorized_key

    def to_dict(self):
        return {
            "additional_ntp_sources": self.additional_ntp_sources,
            "additional_trust_bundle": self.additional_trust_bundle,
            "ignition_config_override": self.ignition_config_override,
            "image_type": self.image_type,
            "pull_secret": self.pull_secret,
            "ssh_authorized_key": self.ssh_authorized_key,
        }
    
class HostCreateParams:
    def __init__(self, host_id: str, discovery_agent_version: Optional[str] = None):
        self.host_id = host_id
        self.discovery_agent_version = discovery_agent_version

    def to_dict(self):
        return {
            "host_id": self.host_id,
            "discovery_agent_version": self.discovery_agent_version
        }
    
class BindHostParams:
    def __init__(self, cluster_id: str):
        self.cluster_id = cluster_id

    def to_dict(self):
        return {
            "cluster_id": self.cluster_id
        }