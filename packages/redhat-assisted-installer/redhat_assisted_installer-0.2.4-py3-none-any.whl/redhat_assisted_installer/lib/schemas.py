from typing import List, Optional, Dict, Any, Union

class APIVip:
    def __init__(self, cluster_id: str, ip: str, verification: str):
        self.cluster_id = cluster_id
        self.ip = ip
        self.verification = verification

    def to_dict(self):
        return {
            "cluster_id": self.cluster_id,
            "ip": self.ip,
            "verification": self.verification
        }

class ClusterNetwork:
    def __init__(self, cidr: str, cluster_id: str, host_prefix: int):
        self.cidr = cidr
        self.cluster_id = cluster_id
        self.host_prefix = host_prefix

    def to_dict(self):
        return {
            "cidr": self.cidr,
            "cluster_id": self.cluster_id,
            "host_prefix": self.host_prefix
        }

class DiskEncryption:
    def __init__(self, enable_on: str, mode: str, tang_servers: Optional[str] = None):
        self.enable_on = enable_on
        self.mode = mode
        self.tang_servers = tang_servers

    def to_dict(self):
        return {
            "enable_on": self.enable_on,
            "mode": self.mode,
            "tang_servers": self.tang_servers
        }

class IgnitionEndpoint:
    def __init__(self, url: str, ca_certificate: Optional[str] = None):
        self.url = url
        self.ca_certificate = ca_certificate

    def to_dict(self):
        return {
            "url": self.url,
            "ca_certificate": self.ca_certificate
        }

class IngressVip:
    def __init__(self, cluster_id: str, ip: str, verification: str):
        self.cluster_id = cluster_id
        self.ip = ip
        self.verification = verification

    def to_dict(self):
        return {
            "cluster_id": self.cluster_id,
            "ip": self.ip,
            "verification": self.verification
        }

class MachineNetwork:
    def __init__(self, cidr: str, cluster_id: str):
        self.cidr = cidr
        self.cluster_id = cluster_id

    def to_dict(self):
        return {
            "cidr": self.cidr,
            "cluster_id": self.cluster_id
        }

class OperatorCreateParams:
    def __init__(self, name: str, namespace: str):
        self.name = name
        self.namespace = namespace

    def to_dict(self):
        return {
            "name": self.name,
            "namespace": self.namespace
        }

class Platform:
    def __init__(self, type: str):
        self.type = type

    def to_dict(self):
        return {
            "type": self.type
        }
    
class Proxy:
    def __init__(self, http_proxy: Optional[str] = None, https_proxy: Optional[str] = None, no_proxy: Optional[str] = None):
        self.http_proxy = http_proxy
        self.https_proxy = https_proxy
        self.no_proxy = no_proxy

    def to_dict(self):
        return {
            "http_proxy": self.http_proxy,
            "https_proxy": self.https_proxy,
            "no_proxy": self.no_proxy
        }
    
class ImageType:
    def __init__(self, type: str):
        self.type = type

    def to_dict(self):
        return {
            "type": self.type
        }

class KernelArguments:
    def __init__(self, args: List[str]):
        self.args = args

    def to_dict(self):
        return {
            "args": self.args
        }

class HostStaticNetworkConfig:
    def __init__(self, network_yaml: str):
        self.network_yaml = network_yaml

    def to_dict(self):
        return {
            "network_yaml": self.network_yaml
        }

class ClusterCreateParams:
    def __init__(self, name: str, openshift_version: str, pull_secret: str,
                 additional_ntp_source: Optional[str] = None,
                 api_vips: Optional[List[APIVip]] = None,
                 base_dns_domain: Optional[str] = None,
                 cluster_network_cidr: Optional[str] = "10.128.0.0/14",
                 cluster_network_host_prefix: Optional[int] = 23,
                 cluster_networks: Optional[List[ClusterNetwork]] = None,
                 cpu_architecture: Optional[str] = "x86_64",
                 disk_encryption: Optional[DiskEncryption] = None,
                 high_availability_mode: Optional[str] = "Full",
                 http_proxy: Optional[str] = None,
                 https_proxy: Optional[str] = None,
                 hyperthreading: Optional[str] = "all",
                 ignition_endpoint: Optional[IgnitionEndpoint] = None,
                 ingress_vips: Optional[List[IngressVip]] = None,
                 machine_networks: Optional[List[MachineNetwork]] = None,
                 network_type: Optional[str] = None,
                 no_proxy: Optional[str] = None,
                 ocp_release_image: Optional[str] = None,
                 olm_operators: Optional[List[OperatorCreateParams]] = None,
                 platform: Optional[Platform] = None,
                 schedulable_masters: Optional[bool] = False,
                 service_network_cidr: Optional[str] = "172.30.0.0/16",
                 service_networks: Optional[List[Dict[str, Any]]] = None,
                 ssh_public_key: Optional[str] = None,
                 tags: Optional[str] = None,
                 user_managed_networking: Optional[bool] = False,
                 vip_dhcp_allocation: Optional[bool] = False):
        self.name = name
        self.openshift_version = openshift_version
        self.pull_secret = pull_secret
        self.additional_ntp_source = additional_ntp_source
        self.api_vips = api_vips
        self.base_dns_domain = base_dns_domain
        self.cluster_network_cidr = cluster_network_cidr
        self.cluster_network_host_prefix = cluster_network_host_prefix
        self.cluster_networks = cluster_networks
        self.cpu_architecture = cpu_architecture
        self.disk_encryption = disk_encryption
        self.high_availability_mode = high_availability_mode
        self.http_proxy = http_proxy
        self.https_proxy = https_proxy
        self.hyperthreading = hyperthreading
        self.ignition_endpoint = ignition_endpoint
        self.ingress_vips = ingress_vips
        self.machine_networks = machine_networks
        self.network_type = network_type
        self.no_proxy = no_proxy
        self.ocp_release_image = ocp_release_image
        self.olm_operators = olm_operators
        self.platform = platform
        self.schedulable_masters = schedulable_masters
        self.service_network_cidr = service_network_cidr
        self.service_networks = service_networks
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
            "api_vips": [vip.to_dict() for vip in self.api_vips] if self.api_vips else None,
            "base_dns_domain": self.base_dns_domain,
            "cluster_network_cidr": self.cluster_network_cidr,
            "cluster_network_host_prefix": self.cluster_network_host_prefix,
            "cluster_networks": [network.to_dict() for network in self.cluster_networks] if self.cluster_networks else None,
            "cpu_architecture": self.cpu_architecture,
            "disk_encryption": self.disk_encryption.to_dict() if self.disk_encryption else None,
            "high_availability_mode": self.high_availability_mode,
            "http_proxy": self.http_proxy,
            "https_proxy": self.https_proxy,
            "hyperthreading": self.hyperthreading,
            "ignition_endpoint": self.ignition_endpoint.to_dict() if self.ignition_endpoint else None,
            "ingress_vips": [vip.to_dict() for vip in self.ingress_vips] if self.ingress_vips else None,
            "machine_networks": [network.to_dict() for network in self.machine_networks] if self.machine_networks else None,
            "network_type": self.network_type,
            "no_proxy": self.no_proxy,
            "ocp_release_image": self.ocp_release_image,
            "olm_operators": [operator.to_dict() for operator in self.olm_operators] if self.olm_operators else None,
            "platform": self.platform.to_dict() if self.platform else None,
            "schedulable_masters": self.schedulable_masters,
            "service_network_cidr": self.service_network_cidr,
            "service_networks": self.service_networks,
            "ssh_public_key": self.ssh_public_key,
            "tags": self.tags,
            "user_managed_networking": self.user_managed_networking,
            "vip_dhcp_allocation": self.vip_dhcp_allocation
        }


class InfraEnvCreateParams:
    def __init__(self, name: str, pull_secret: str,
                 additional_ntp_sources: Optional[str] = None,
                 additional_trust_bundle: Optional[str] = None,
                 cluster_id: Optional[str] = None,
                 cpu_architecture: Optional[str] = "x86_64",
                 ignition_config_override: Optional[str] = None,
                 image_type: Optional[ImageType] = None,
                 kernel_arguments: Optional[KernelArguments] = None,
                 openshift_version: Optional[str] = None,
                 proxy: Optional[Proxy] = None,
                 ssh_authorized_key: Optional[str] = None,
                 static_network_config: Optional[List[HostStaticNetworkConfig]] = None):
        self.name = name
        self.pull_secret = pull_secret
        self.additional_ntp_sources = additional_ntp_sources
        self.additional_trust_bundle = additional_trust_bundle
        self.cluster_id = cluster_id
        self.cpu_architecture = cpu_architecture
        self.ignition_config_override = ignition_config_override
        self.image_type = image_type
        self.kernel_arguments = kernel_arguments
        self.openshift_version = openshift_version
        self.proxy = proxy
        self.ssh_authorized_key = ssh_authorized_key
        self.static_network_config = static_network_config

    def to_dict(self):
        return {
            "name": self.name,
            "pull_secret": self.pull_secret,
            "additional_ntp_sources": self.additional_ntp_sources,
            "additional_trust_bundle": self.additional_trust_bundle,
            "cluster_id": self.cluster_id,
            "cpu_architecture": self.cpu_architecture,
            "ignition_config_override": self.ignition_config_override,
            "image_type": self.image_type.to_dict() if self.image_type else None,
            "kernel_arguments": self.kernel_arguments.to_dict() if self.kernel_arguments else None,
            "openshift_version": self.openshift_version,
            "proxy": self.proxy.to_dict() if self.proxy else None,
            "ssh_authorized_key": self.ssh_authorized_key,
            "static_network_config": [config.to_dict() for config in self.static_network_config] if self.static_network_config else None
        }


class ClusterUpdateParams:
    def __init__(self,
                 additional_ntp_source: Optional[str] = None,
                 api_vip_dns_name: Optional[str] = None,
                 api_vips: Optional[List[APIVip]] = None,
                 base_dns_domain: Optional[str] = None,
                 cluster_network_cidr: Optional[str] = None,
                 cluster_network_host_prefix: Optional[int] = None,
                 cluster_networks: Optional[List[Dict[str, Any]]] = None,
                 disk_encryption: Optional[DiskEncryption] = None,
                 http_proxy: Optional[str] = None,
                 https_proxy: Optional[str] = None,
                 hyperthreading: Optional[str] = None,
                 ingress_vips: Optional[List[str]] = None,
                 machine_networks: Optional[List[MachineNetwork]] = None,
                 name: Optional[str] = None,
                 network_type: Optional[str] = None,
                 no_proxy: Optional[str] = None,
                 olm_operators: Optional[List[OperatorCreateParams]] = None,
                 platform: Optional[Platform] = None,
                 pull_secret: Optional[str] = None,
                 schedulable_masters: Optional[bool] = None,
                 service_network_cidr: Optional[str] = None,
                 service_networks: Optional[List[Dict[str, Any]]] = None,
                 ssh_public_key: Optional[str] = None,
                 tags: Optional[str] = None,
                 user_managed_networking: Optional[bool] = None,
                 vip_dhcp_allocation: Optional[bool] = None):
        self.additional_ntp_source = additional_ntp_source
        self.api_vip_dns_name = api_vip_dns_name
        self.api_vips = api_vips
        self.base_dns_domain = base_dns_domain
        self.cluster_network_cidr = cluster_network_cidr
        self.cluster_network_host_prefix = cluster_network_host_prefix
        self.cluster_networks = cluster_networks
        self.disk_encryption = disk_encryption
        self.http_proxy = http_proxy
        self.https_proxy = https_proxy
        self.hyperthreading = hyperthreading
        self.ingress_vips = ingress_vips
        self.machine_networks = machine_networks
        self.name = name
        self.network_type = network_type
        self.no_proxy = no_proxy
        self.olm_operators = olm_operators
        self.platform = platform
        self.pull_secret = pull_secret
        self.schedulable_masters = schedulable_masters
        self.service_network_cidr = service_network_cidr
        self.service_networks = service_networks
        self.ssh_public_key = ssh_public_key
        self.tags = tags
        self.user_managed_networking = user_managed_networking
        self.vip_dhcp_allocation = vip_dhcp_allocation

    def to_dict(self):
        return {
            "additional_ntp_source": self.additional_ntp_source,
            "api_vip_dns_name": self.api_vip_dns_name,
            "api_vips": [vip.to_dict() for vip in self.api_vips] if self.api_vips else None,
            "base_dns_domain": self.base_dns_domain,
            "cluster_network_cidr": self.cluster_network_cidr,
            "cluster_network_host_prefix": self.cluster_network_host_prefix,
            "cluster_networks": self.cluster_networks,
            "disk_encryption": self.disk_encryption.to_dict() if self.disk_encryption else None,
            "http_proxy": self.http_proxy,
            "https_proxy": self.https_proxy,
            "hyperthreading": self.hyperthreading,
            "ingress_vips": self.ingress_vips,
            "machine_networks": [network.to_dict() for network in self.machine_networks] if self.machine_networks else None,
            "name": self.name,
            "network_type": self.network_type,
            "no_proxy": self.no_proxy,
            "olm_operators": [operator.to_dict() for operator in self.olm_operators] if self.olm_operators else None,
            "platform": self.platform.to_dict() if self.platform else None,
            "pull_secret": self.pull_secret,
            "schedulable_masters": self.schedulable_masters,
            "service_network_cidr": self.service_network_cidr,
            "service_networks": self.service_networks,
            "ssh_public_key": self.ssh_public_key,
            "tags": self.tags,
            "user_managed_networking": self.user_managed_networking,
            "vip_dhcp_allocation": self.vip_dhcp_allocation
        }
    
class InfraEnvUpdateParams:
    def __init__(self,
                 additional_ntp_sources: Optional[str] = None,
                 additional_trust_bundle: Optional[str] = None,
                 ignition_config_override: Optional[str] = None,
                 image_type: Optional[str] = None,
                 kernel_arguments: Optional[KernelArguments] = None,
                 proxy: Optional[Proxy] = None,
                 pull_secret: Optional[str] = None,
                 ssh_authorized_key: Optional[str] = None,
                 static_network_config: Optional[List[HostStaticNetworkConfig]] = None):
        self.additional_ntp_sources = additional_ntp_sources
        self.additional_trust_bundle = additional_trust_bundle
        self.ignition_config_override = ignition_config_override
        self.image_type = image_type
        self.kernel_arguments = kernel_arguments
        self.proxy = proxy
        self.pull_secret = pull_secret
        self.ssh_authorized_key = ssh_authorized_key
        self.static_network_config = static_network_config

    def to_dict(self):
        return {
            "additional_ntp_sources": self.additional_ntp_sources,
            "additional_trust_bundle": self.additional_trust_bundle,
            "ignition_config_override": self.ignition_config_override,
            "image_type": self.image_type,
            "kernel_arguments": self.kernel_arguments.to_dict() if self.kernel_arguments else None,
            "proxy": self.proxy.to_dict() if self.proxy else None,
            "pull_secret": self.pull_secret,
            "ssh_authorized_key": self.ssh_authorized_key,
            "static_network_config": [config.to_dict() for config in self.static_network_config] if self.static_network_config else None
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