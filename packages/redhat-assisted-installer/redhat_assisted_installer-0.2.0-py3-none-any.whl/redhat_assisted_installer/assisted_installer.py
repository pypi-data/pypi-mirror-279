## Code to disable creating pycache dir after running
import sys, requests, json, os
sys.dont_write_bytecode = True
###################################################

from urllib.parse import urlencode

from .lib.schemas import *


class assisted_installer:
    def __init__(self) -> None:
        self.apiBase = "https://api.openshift.com/api/assisted-install/v2/"


    def __get_headers(self):
        return  {
            "Authorization": "Bearer {}".format(self.__get_access_token()),
            "Content-Type": "application/json"
        }


    def __get_access_token(self):
        # URL for the token request
        url = "https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token"

        # Headers to be sent with the request
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        # Data to be sent in the request, explicitly encoding each variable
        data = urlencode({
            "grant_type": "refresh_token",
            "client_id": "cloud-services",
            "refresh_token": os.environ.get("REDHAT_OFFLINE_TOKEN") if "REDHAT_OFFLINE_TOKEN" in os.environ else ""
        })

        try:
            # Make the POST request
            response = requests.post(url, headers=headers, data=data)

            # Handle response
            if response.status_code == 200:
                # Extract access token from the response JSON
                access_token = response.json().get("access_token")
                return access_token
            else:
                # raise response.raise_for_status()
                return response.json()
        except Exception as e:
            print("Exception found in __get_access_token()")
            print(e)


    def get_cluster(self, id):
        url = self.apiBase + f"clusters/{id}"
        
        if '?' not in url:
            url += '?'
        url += f'cluster_id={id}'
        
        try:
            response = requests.get(url, headers=self.__get_headers())
            print(response.json())
            return response.json()
        
        except Exception as e:
            print("Exception found in get_cluster()")
            print(e)

    def get_default_config(self):
        url = self.apiBase + f"clusters/default-config"

        try:
            response = requests.get(url, headers=self.__get_headers())
            print(response.json())
            return response.json()
        
        except Exception as e:
            print("Exception found in get_cluster()")
            print(e)

    def get_clusters(self, with_hosts=False, owner=None):
        url = self.apiBase + "clusters"
        if with_hosts:
            if '?' not in url:
                url += '?'
            url += f'with_hosts={with_hosts}'            

        if owner is not None:
            if '?' not in url:
                url += '?'
            url += f'owner={owner}'
        
        try:
            response = requests.get(url, headers=self.__get_headers())
            print(response.json())
            return response.json()
        
        except Exception as e:
            print("Exception found in getClusters()")
            print(e)

    def post_cluster(self, name: str, openshift_version: str, pull_secret: str = os.environ.get("REDHAT_PULL_SECRET") if "REDHAT_PULL_SECRET" in os.environ else "",
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
        
        url = self.apiBase + "clusters"

        cluster_create_params = ClusterCreateParams(name=name, openshift_version=openshift_version, pull_secret=pull_secret, additional_ntp_source=additional_ntp_source, api_vips=api_vips, 
                                                    base_dns_domain=base_dns_domain, cluster_network_cidr=cluster_network_cidr, cluster_network_host_prefix=cluster_network_host_prefix, 
                                                    cluster_networks=cluster_networks, cpu_architecture=cpu_architecture, disk_encryption=disk_encryption, high_availability_mode=high_availability_mode, 
                                                    http_proxy=http_proxy, https_proxy=https_proxy, hyperthreading=hyperthreading, ignition_endpoint=ignition_endpoint, ingress_vips=ingress_vips, 
                                                    machine_networks=machine_networks, network_type=network_type, no_proxy=no_proxy, ocp_release_image=ocp_release_image, olm_operators=olm_operators, 
                                                    platform=platform, schedulable_masters=schedulable_masters, service_network_cidr=service_network_cidr,service_networks=service_networks, 
                                                    ssh_public_key=ssh_public_key, tags=tags, user_managed_networking=user_managed_networking, vip_dhcp_allocation=vip_dhcp_allocation)
        data = cluster_create_params.to_dict()

        try:
            response = requests.post(url, headers=self.__get_headers(), json=data)
            if response.status_code == 201:
                print("Successfully created cluster:")
            else: 
                print(f"Failed to create cluster")
            print(response.json())
            return response.json()

        except Exception as e:
            print("Exception found in post_cluster()")
            print(e)


    def patch_cluster(self, id: str, pull_secret: str =  os.environ.get("REDHAT_PULL_SECRET") if "REDHAT_PULL_SECRET" in os.environ else "",
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
                 schedulable_masters: Optional[bool] = None,
                 service_network_cidr: Optional[str] = None,
                 service_networks: Optional[List[Dict[str, Any]]] = None,
                 ssh_public_key: Optional[str] = None,
                 tags: Optional[str] = None,
                 user_managed_networking: Optional[bool] = None,
                 vip_dhcp_allocation: Optional[bool] = None):
        
        url = self.apiBase + f"clusters/{id}"

        update_cluster_params = ClusterUpdateParams(name=name, pull_secret=pull_secret, olm_operators=olm_operators, additional_ntp_source=additional_ntp_source, 
                                                    api_vip_dns_name=api_vip_dns_name, api_vips=api_vips, base_dns_domain=base_dns_domain, cluster_network_cidr=cluster_network_cidr, 
                                                    cluster_network_host_prefix=cluster_network_host_prefix, cluster_networks=cluster_networks, platform=platform, disk_encryption=disk_encryption, 
                                                    http_proxy=http_proxy, https_proxy=https_proxy, hyperthreading=hyperthreading, ingress_vips=ingress_vips, machine_networks=machine_networks, 
                                                    network_type=network_type, no_proxy=no_proxy, schedulable_masters=schedulable_masters, service_network_cidr=service_network_cidr,service_networks=service_networks, 
                                                    ssh_public_key=ssh_public_key, tags=tags, user_managed_networking=user_managed_networking, vip_dhcp_allocation=vip_dhcp_allocation)
        
        data = update_cluster_params.to_dict()

        try:
            response = requests.patch(url, headers=self.__get_headers(), json=data)

            if response.status_code == 201:
                print(f"Successfully patched cluster: {id}")
                
            else:
                print(f"Failed to patch cluster: {id}")
            print(response.json())
            return response.json()

        except Exception as e:
            print("Exception found in patch_cluster()")
            print(e)


    def delete_cluster(self, id):
        url = self.apiBase + f"clusters/{id}"

        try:
            response = requests.delete(url, headers=self.__get_headers())

            if response.status_code == 204:
                print(f"Successfully deleted cluster: {id}")
                return True
            else:
                print(f"Failed to delete cluster: {id}")
                return False 

        except Exception as e:
            print("Exception found in delete_cluster()")
            print(e)


    def get_infrastructure_environement(self, id):
        url = self.apiBase + f"infra-envs/{id}"

        try:
            response = requests.get(url, headers=self.__get_headers())
            print(response.json())
            return response.json()
            
        except Exception as e:
            print("Exception found in get_infrastructure_environment()")
            print(e)   

    # Method that will implement the /v2/infra-envs GET assisted installer endpoint
    def get_infrastructure_environements(self, cluster_id=None, owner=None):
        url = self.apiBase + "infra-envs"
        if cluster_id is not None and owner is not None:
            url += f'?cluster_id={cluster_id}&owner={owner}'
        else:
            if cluster_id is not None:
                url += f'?cluster_id={cluster_id}'
            if owner is not None:
                url += f'?owner={owner}'
        
        try:
            response = requests.get(url, headers=self.__get_headers())
            print(response.json())
            return response.json()
            
        except Exception as e:
            print("Exception found in get_infrastructure_environments()")
            print(e)

    def patch_infrastructure_environment(self, id: str, 
                 additional_ntp_sources: Optional[str] = None,
                 additional_trust_bundle: Optional[str] = None,
                 ignition_config_override: Optional[str] = None,
                 image_type: Optional[str] = None,
                 kernel_arguments: Optional[KernelArguments] = None,
                 proxy: Optional[Proxy] = None,
                 pull_secret: str = os.environ.get("REDHAT_PULL_SECRET") if "REDHAT_PULL_SECRET" in os.environ else "",
                 ssh_authorized_key: Optional[str] = None,
                 static_network_config: Optional[List[HostStaticNetworkConfig]] = None):
        
        url = self.apiBase + f"infra-envs/{id}"

        update_cluster_params = InfraEnvUpdateParams(pull_secret=pull_secret, additional_ntp_sources=additional_ntp_sources, additional_trust_bundle=additional_trust_bundle, 
                                                     ignition_config_override=ignition_config_override, image_type=image_type, kernel_arguments=kernel_arguments, proxy=proxy,
                                                     ssh_authorized_key=ssh_authorized_key, static_network_config=static_network_config) 
        data = update_cluster_params.to_dict()

        try:
            response = requests.patch(url, headers=self.__get_headers(), json=data)

            if response.status_code == 201:
                print(f"Successfully patched infra-env: {id}")
            else:
                print(f"Failed to patch infra-env: {id}")
            print(response.json())
            return response.json()

        except Exception as e:
            print("Exception found in patch_infrastructure_environment()")
            print(e)


    def post_infrastructure_environment(self, name: str, pull_secret: str = os.environ.get("REDHAT_PULL_SECRET") if "REDHAT_PULL_SECRET" in os.environ else "",
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
        
        url = self.apiBase + "infra-envs"


        infra_env_create_params = InfraEnvCreateParams(name=name, pull_secret=pull_secret, additional_ntp_sources=additional_ntp_sources, additional_trust_bundle=additional_trust_bundle, 
                                                       cluster_id=cluster_id, cpu_architecture=cpu_architecture, ignition_config_override=ignition_config_override, image_type=image_type, 
                                                       kernel_arguments=kernel_arguments, openshift_version=openshift_version,proxy=proxy, ssh_authorized_key=ssh_authorized_key, static_network_config=static_network_config)
        
        data = infra_env_create_params.to_dict()

        try:
            response = requests.post(url, headers=self.__get_headers(), json=data)
            if response.status_code == 201:
                print("Successfully created infra-env:")
            else: 
                print(f"Failed to create infra-env")
            print(response.json())
            return response.json()


        except Exception as e:
            print("Exception found in post_infrastructure_environment()")
            print(e)

    def delete_infrastructure_environment(self, id):
        url = self.apiBase + f"infra-envs/{id}"

        try:
            response = requests.delete(url, headers=self.__get_headers())

            if response.status_code == 204:
                print(f"Successfully deleted infra-env: {id}")
                return True
            else:
                print(f"Failed to delete infra-env: {id}")
                return False 

        except Exception as e:
            print("Exception found in delete_infrastructure_environment()")
            print(e)


    def cluster_action_allow_add_hosts(self, id):
        url = self.apiBase + f"clusters/{id}/actions/allow-add-hosts"

        try:
            response = requests.post(url, headers=self.__get_headers())

            if response.status_code == 202:
                print(f"Successfully initiated action 'allow-add-hosts' for cluster: {id}")
            else:
                print(f"Failed to initiate action 'allow-add-hosts' for cluster: {id}")
            print(response.json())
            return response.json()

        except Exception as e:
            print("Exception found in allow_add_hosts()")
            print(e)


    def cluster_action_allow_add_workers(self, id):
        url = self.apiBase + f"clusters/{id}/actions/allow-add-workers"

        try:
            response = requests.post(url, headers=self.__get_headers())

            if response.status_code == 202:
                print(f"Successfully initiated action 'allow-add-workers' for cluster: {id}")
            else:
                print(f"Failed to initiate action 'allow-add-workers' for cluster: {id}")
            print(response.json())
            return response.json()

        except Exception as e:
            print("Exception found in cluster_action_allow_add_workers()")
            print(e)

    def cluster_action_cancel(self, id):
        url = self.apiBase + f"clusters/{id}/actions/cancel"

        try:
            response = requests.post(url, headers=self.__get_headers())

            if response.status_code == 202:
                print(f"Successfully canceled installation for cluster: {id}")
            else:
                print(f"Failed to cancel installation for cluster: {id}")
            print(response.json())
            return response.json()

        except Exception as e:
            print("Exception found in cluster_action_cancel()")
            print(e)

    def cluster_action_complete_installation(self, id):
        url = self.apiBase + f"clusters/{id}/actions/complete-installation"

        try:
            response = requests.post(url, headers=self.__get_headers())

            if response.status_code == 202:
                print(f"Successfully complete installation for cluster: {id}")
            else:
                print(f"Failed to complete installation for cluster: {id}")
            print(response.json())
            return response.json()

        except Exception as e:
            print("Exception found in cluster_action_complete_installation()")
            print(e)


    def cluster_action_reset(self, id):
        url = self.apiBase + f"clusters/{id}/actions/reset"

        try:
            response = requests.post(url, headers=self.__get_headers())

            if response.status_code == 202:
                print(f"Successfully reset cluster: {id}")
            else:
                print(f"Failed to reset cluster: {id}")
            print(response.json())
            return response.json()

        except Exception as e:
            print("Exception found in cluster_action_reset()")
            print(e)


    def cluster_action_install(self, id):
        url = self.apiBase + f"clusters/{id}/actions/install"

        try:
            response = requests.post(url, headers=self.__get_headers())

            if response.status_code == 202:
                print(f"Successfully initiated cluster install for cluster: {id}")
            else:
                print(f"Failed to initiate cluster install for cluster: {id}")
            print(response.json())
            return response.json()

        except Exception as e:
            print("Exception found in cluster_action_install()")
            print(e)

    def cluster_get_credentials(self, id: str, credentials: Optional[str] = None):
        endpoint = f"clusters/{id}/downloads/credentials" if credentials is not None else f"clusters/{id}/credentials"
        url = self.apiBase + endpoint
        
        query_string = {"file_name": credentials}

        try:
            if credentials is not None:
                response = requests.get(url, headers=self.__get_headers(), params=query_string)
                print(response.text)
                return response.text
            else:
                response = requests.get(url, headers=self.__get_headers())
                print(response.json())
                return response.json()
        
        except Exception as e:
            print("Exception found in cluster_get_credentials()")
            print(e)


    def cluster_get_files(self, id: str, file_name: str = "install-config.yaml"):
        url = self.apiBase + f"clusters/{id}/downloads/files"
        
        query_string = {"file_name": file_name}

        try:
            response = requests.get(url, headers=self.__get_headers(), params=query_string)
            print(response.text)
            return response.text
        
        except Exception as e:
            print("Exception found in cluster_get_files()")
            print(e)


    def get_infrastructure_environement_hosts(self, infra_env_id: str):
        url = self.apiBase + f"infra-envs/{infra_env_id}/hosts"
        
        try:
            response = requests.get(url, headers=self.__get_headers())
            print(response.json())
            return response.json()
            
        except Exception as e:
            print("Exception found in get_infrastructure_environement_hosts()")
            print(e)

    def get_infrastructure_environement_host(self, infra_env_id: str, host_id: str):
        url = self.apiBase + f"infra-envs/{infra_env_id}/hosts/{host_id}"
        
        try:
            response = requests.get(url, headers=self.__get_headers())
            print(response.json())
            return response.json()
            
        except Exception as e:
            print("Exception found in get_infrastructure_environement_host()")
            print(e)

    def post_infrastructure_environement_host(self, infra_env_id: str, host_id: str, discovery_agent_version: Optional[str] = None):
        url = self.apiBase + f"infra-envs/{infra_env_id}/hosts"
        
        host_create_params = HostCreateParams(host_id=host_id, discovery_agent_version=discovery_agent_version)

        data = host_create_params.to_dict()
        try:
            response = requests.post(url, headers=self.__get_headers(), json=data)
            if response.status_code == 201:
                print(f"Successfully created new openshift host: {response.json()['id']}")
            else:
                print("Failed to create new openshift host")
            print(response.json())
            return response.json()
            
        except Exception as e:
            print("Exception found in post_infrastructure_environement_host()")
            print(e)


    def delete_infrastructure_environement_host(self, infra_env_id: str, host_id: str):
        url = self.apiBase + f"infra-envs/{infra_env_id}/hosts/{host_id}"

        try:
            response = requests.delete(url, headers=self.__get_headers())

            if response.status_code == 204:
                print(f"Successfully deleted host {host_id} from infra-env {infra_env_id}")
                return True
            else:
                print(f"Failed to delete host {host_id} from infra-env {infra_env_id}")
                return False 

        except Exception as e:
            print("Exception found in delete_infrastructure_environement_host()")
            print(e)


    def host_actions_bind(self, infra_env_id: str, host_id: str):
        url = self.apiBase + f"infra-envs/{infra_env_id}/hosts/{host_id}/actions/bind"

        bind_host_parmas = BindHostParams(cluster_id=self.get_infrastructure_environement(infra_env_id)['cluster_id'])

        data = bind_host_parmas.to_dict()

        try:
            response = requests.post(url, headers=self.__get_headers(), json=data)

            if response.status_code == 200:
                print(f"Successfully bound host {host_id} to infra-env {infra_env_id} to cluster-id {data['cluster_id']}")
           
            else:
                print(f"Failed to bind host {host_id} to infra-env {infra_env_id}")

        except Exception as e:
            print("Exception found in host_actions_bind()")
            print(e)


    def host_actions_unbind(self, infra_env_id: str, host_id: str):
        url = self.apiBase + f"infra-envs/{infra_env_id}/hosts/{host_id}/actions/unbind"

        try:
            response = requests.post(url, headers=self.__get_headers())

            if response.status_code == 200:
                print(f"Successfully unbound host {host_id} from infra-env {infra_env_id}")
           
            else:
                print(f"Failed to unbind host {host_id} from infra-env {infra_env_id}")

        except Exception as e:
            print("Exception found in host_actions_unbind()")
            print(e)


    def host_actions_install(self, infra_env_id: str, host_id: str):
        url = self.apiBase + f"infra-envs/{infra_env_id}/hosts/{host_id}/actions/install"

        try:
            response = requests.post(url, headers=self.__get_headers())

            if response.status_code == 202:
                print(f"Successfully initiated host installation for {host_id} from infra-env {infra_env_id}")
            else:
                print(f"Failed to initiate host installation {host_id} from infra-env {infra_env_id}")

        except Exception as e:
            print("Exception found in host_actions_install()")
            print(e)

    def host_actions_reset(self, infra_env_id: str, host_id: str):
        url = self.apiBase + f"infra-envs/{infra_env_id}/hosts/{host_id}/actions/reset"

        try:
            response = requests.post(url, headers=self.__get_headers())

            if response.status_code == 200:
                print(f"Successfully initiated host installation for {host_id} from infra-env {infra_env_id}")
            else:
                print(f"Failed to initiate host installation {host_id} from infra-env {infra_env_id}")

        except Exception as e:
            print("Exception found in host_actions_reset()")
            print(e)