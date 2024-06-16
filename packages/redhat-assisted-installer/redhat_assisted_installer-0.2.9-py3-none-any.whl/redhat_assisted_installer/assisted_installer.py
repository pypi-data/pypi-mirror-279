## Code to disable creating pycache dir after running
import sys, requests, json, os
sys.dont_write_bytecode = True
###################################################

from urllib.parse import urlencode

from .lib.schemas import *

from requests.exceptions import HTTPError

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
            response.raise_for_status()
            access_token = response.json().get("access_token")
            return access_token

        except requests.exceptions.HTTPError as e:
            print(f"Failed to __get_access_token")
            print("__get_access_token() returned a bad status code")
            print(e)


        except Exception as e:
            print("Exception found in __get_access_token()")
            print(e)


    def get_cluster(self, cluster_id: Optional[str]=None):
        url = self.apiBase + f"clusters/{cluster_id}"

        try:
            response = requests.get(url, headers=self.__get_headers())
            response.raise_for_status()
            print([response.json()])
            return [response.json()]
        
        except requests.exceptions.HTTPError as e:
            print("get_cluster() returned a bad status code")
            print(e)

        except Exception as e:
            print("Exception found in get_cluster()")
            print(e)

    def get_default_config(self):
        url = self.apiBase + f"clusters/default-config"

        try:
            response = requests.get(url, headers=self.__get_headers())
            response.raise_for_status()
            print(response.json())
            return response.json()
        
        except requests.exceptions.HTTPError as e:
            print("get_default_config() returned a bad status code")
            print(e)
            
        except Exception as e:
            print("Exception found in get_default_config()")
            print(e)

    def get_clusters(self,  with_hosts: Optional[bool]=False, owner: Optional[str]=None):
        url = self.apiBase + "clusters"

        if with_hosts:
            if '?' not in url:
                url += '?'
            url += f'with_hosts={with_hosts}&'            

        if owner is not None:
            if '?' not in url:
                url += '?'
            url += f'owner={owner}&'
        
        try:
            response = requests.get(url, headers=self.__get_headers())
            response.raise_for_status()
            print(response.json())
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            print("get_clusters() returned a bad status code")
            print(e)
            
        except Exception as e:
            print("Exception found in getClusters()")
            print(e)

    def post_cluster(self, 
                     name: str, 
                     openshift_version: str, 
                     pull_secret: str,
                     additional_ntp_source: Optional[str] = None,
                     base_dns_domain: Optional[str] = None,
                     cluster_network_cidr: Optional[str] = "10.128.0.0/14",
                     cluster_network_host_prefix: Optional[int] = 23,
                     cpu_architecture: Optional[str] = "x86_64",
                     high_availability_mode: Optional[str] = "Full",
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
        
        url = self.apiBase + "clusters"

        cluster_create_params = ClusterCreateParams(name=name, 
                                                    openshift_version=openshift_version, 
                                                    pull_secret=pull_secret, 
                                                    additional_ntp_source=additional_ntp_source,
                                                    base_dns_domain=base_dns_domain, 
                                                    cluster_network_cidr=cluster_network_cidr, 
                                                    cluster_network_host_prefix=cluster_network_host_prefix, 
                                                    cpu_architecture=cpu_architecture, 
                                                    high_availability_mode=high_availability_mode, 
                                                    http_proxy=http_proxy, 
                                                    https_proxy=https_proxy, 
                                                    hyperthreading=hyperthreading, 
                                                    network_type=network_type, 
                                                    no_proxy=no_proxy, 
                                                    ocp_release_image=ocp_release_image,
                                                    schedulable_masters=schedulable_masters, 
                                                    service_network_cidr=service_network_cidr,
                                                    ssh_public_key=ssh_public_key, 
                                                    tags=tags, 
                                                    user_managed_networking=user_managed_networking, 
                                                    vip_dhcp_allocation=vip_dhcp_allocation,
                                                    )
        data = cluster_create_params.to_dict()

        try:
            response = requests.post(url, headers=self.__get_headers(), json=data)
            response.raise_for_status()    
            print("Successfully created cluster:")
            print([response.json()])
            return [response.json()]
        
        except requests.exceptions.HTTPError as e:
            print(f"Failed to create cluster")
            print("post_cluster() returned a bad status code")
            print(e)

        except Exception as e:
            print("Exception found in post_cluster()")
            print(e)


    def patch_cluster(self, 
                      cluster_id: str,
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
        
        url = self.apiBase + f"clusters/{cluster_id}"

        update_cluster_params = ClusterUpdateParams(name=name, 
                                                    pull_secret=pull_secret, 
                                                    additional_ntp_source=additional_ntp_source, 
                                                    api_vip_dns_name=api_vip_dns_name, 
                                                    base_dns_domain=base_dns_domain, 
                                                    cluster_network_cidr=cluster_network_cidr, 
                                                    cluster_network_host_prefix=cluster_network_host_prefix, 
                                                    http_proxy=http_proxy, 
                                                    https_proxy=https_proxy, 
                                                    hyperthreading=hyperthreading, 
                                                    network_type=network_type, 
                                                    no_proxy=no_proxy, 
                                                    schedulable_masters=schedulable_masters, 
                                                    service_network_cidr=service_network_cidr,
                                                    ssh_public_key=ssh_public_key, 
                                                    tags=tags, 
                                                    user_managed_networking=user_managed_networking, 
                                                    vip_dhcp_allocation=vip_dhcp_allocation,
                                                    )
        
        data = update_cluster_params.to_dict()

        try:
            response = requests.patch(url, headers=self.__get_headers(), json=data)
            response.raise_for_status()
            print(f"Successfully patched cluster: {cluster_id}")
            print([response.json()])
            return [response.json()]
        
        except requests.exceptions.HTTPError as e:
            print(f"Failed to patch cluster: {cluster_id}")
            print("patch_cluster() returned a bad status code")
            print(e)

        except Exception as e:
            print("Exception found in patch_cluster()")
            print(e)


    def delete_cluster(self, cluster_id):
        url = self.apiBase + f"clusters/{cluster_id}"

        try:
            response = requests.delete(url, headers=self.__get_headers())
            response.raise_for_status()
            print(f"Successfully deleted cluster: {cluster_id}")
            return True

        except requests.exceptions.HTTPError as e:
            print(f"Failed to delete cluster: {cluster_id}")
            print("delete_cluster() returned a bad status code")
            print(e)

        except Exception as e:
            print(f"Failed to delete cluster: {cluster_id}")
            print("Exception found in delete_cluster()")
            print(e)


    def get_infrastructure_environement(self, infra_env_id):
        url = self.apiBase + f"infra-envs/{infra_env_id}"

        try:
            response = requests.get(url, headers=self.__get_headers())
            response.raise_for_status()
            print([response.json()])
            return [response.json()]
            
        except requests.exceptions.HTTPError as e:
            print("get_infrastructure_environement() returned a bad status code")
            print(e)
    
        except Exception as e:
            print("Exception found in get_infrastructure_environment()")
            print(e)   

    # Method that will implement the /v2/infra-envs GET assisted installer endpoint
    def get_infrastructure_environements(self):
        url = self.apiBase + "infra-envs"
        
        try:
            response = requests.get(url, headers=self.__get_headers())
            response.raise_for_status()
            print(response.json())
            return response.json()
        
        except requests.exceptions.HTTPError as e:
            print("get_infrastructure_environements() returned a bad status code")
            print(e)
            
        except Exception as e:
            print("Exception found in get_infrastructure_environments()")
            print(e)

    def patch_infrastructure_environment(self, 
                                         infra_env_id: str,
                                         pull_secret: str,
                                         additional_ntp_sources: Optional[str] = None,
                                         additional_trust_bundle: Optional[str] = None,
                                         ignition_config_override: Optional[str] = None,
                                         image_type: Optional[str] = None,
                                         ssh_authorized_key: Optional[str] = None,
                 ):
        
        url = self.apiBase + f"infra-envs/{infra_env_id}"

        update_cluster_params = InfraEnvUpdateParams(pull_secret=pull_secret, 
                                                     additional_ntp_sources=additional_ntp_sources, 
                                                     additional_trust_bundle=additional_trust_bundle, 
                                                     ignition_config_override=ignition_config_override, 
                                                     image_type=image_type,
                                                     ssh_authorized_key=ssh_authorized_key,
                                                     ) 
        data = update_cluster_params.to_dict()

        try:
            response = requests.patch(url, headers=self.__get_headers(), json=data)
            response.raise_for_status()
            print(f"Successfully patched infra-env: {infra_env_id}")
            print([response.json()])
            return [response.json()]

        except requests.exceptions.HTTPError as e:
            print("patch_infrastructure_environment() returned a bad status code")
            print(e)
            

        except Exception as e:
            print("Exception found in patch_infrastructure_environment()")
            print(e)


    def post_infrastructure_environment(self, 
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
        
        url = self.apiBase + "infra-envs"


        infra_env_create_params = InfraEnvCreateParams(name=name, 
                                                       pull_secret=pull_secret, 
                                                       additional_ntp_sources=additional_ntp_sources, 
                                                       additional_trust_bundle=additional_trust_bundle, 
                                                       cluster_id=cluster_id, 
                                                       cpu_architecture=cpu_architecture, 
                                                       ignition_config_override=ignition_config_override, 
                                                       openshift_version=openshift_version, 
                                                       ssh_authorized_key=ssh_authorized_key,
                                                       )
        
        data = infra_env_create_params.to_dict()

        try:
            response = requests.post(url, headers=self.__get_headers(), json=data)
            response.raise_for_status()
            print("Successfully created infra-env:") 
            print([response.json()])
            return [response.json()]
        
        except requests.exceptions.HTTPError as e:
            print(f"Failed to create infra-env")
            print("post_infrastructure_environment() returned a bad status code")
            print(e)

        except Exception as e:
            print("Exception found in post_infrastructure_environment()")
            print(e)

    def delete_infrastructure_environment(self, infra_env_id: str):
        url = self.apiBase + f"infra-envs/{infra_env_id}"

        try:
            response = requests.delete(url, headers=self.__get_headers())
            response.raise_for_status()
            print(f"Successfully deleted infra-env: {infra_env_id}")
            return True

        except requests.exceptions.HTTPError as e:
            print(f"Failed to delete infra-env")
            print("delete_infrastructure_environment() returned a bad status code")
            print(e)

        except Exception as e:
            print("Exception found in delete_infrastructure_environment()")
            print(e)


    def cluster_action_allow_add_hosts(self, cluster_id: str):
        url = self.apiBase + f"clusters/{cluster_id}/actions/allow-add-hosts"

        try:
            response = requests.post(url, headers=self.__get_headers())
            response.raise_for_status()
            print(f"Successfully initiated action 'allow-add-hosts' for cluster: {cluster_id}")
            print([response.json()])
            return [response.json()]

        except requests.exceptions.HTTPError as e:
            print(f"Failed to initiate action 'allow-add-hosts' for cluster: {cluster_id}")
            print("cluster_action_allow_add_hosts() returned a bad status code")
            print(e)

        except Exception as e:
            print("Exception found in allow_add_hosts()")
            print(e)


    def cluster_action_allow_add_workers(self, cluster_id: str):
        url = self.apiBase + f"clusters/{cluster_id}/actions/allow-add-workers"

        try:
            response = requests.post(url, headers=self.__get_headers())
            response.raise_for_status()
            print(f"Successfully initiated action 'allow-add-workers' for cluster: {cluster_id}")  
            print([response.json()])
            return [response.json()]

        except requests.exceptions.HTTPError as e:
            print(f"Failed to initiate action 'cluster_action_allow_add_workers' for cluster: {cluster_id}")
            print("cluster_action_allow_add_workers() returned a bad status code")
            print(e)

        except Exception as e:
            print("Exception found in cluster_action_allow_add_workers()")
            print(e)

    def cluster_action_cancel(self, cluster_id: str):
        url = self.apiBase + f"clusters/{cluster_id}/actions/cancel"

        try:
            response = requests.post(url, headers=self.__get_headers())
            response.raise_for_status()
            print(f"Successfully canceled installation for cluster: {cluster_id}") 
            print([response.json()])
            return [response.json()]

        except requests.exceptions.HTTPError as e:
            print(f"Failed to cancel installation for cluster: {cluster_id}")
            print("cluster_action_cancel() returned a bad status code")
            print(e)

        except Exception as e:
            print("Exception found in cluster_action_cancel()")
            print(e)

    def cluster_action_complete_installation(self, cluster_id: str):
        url = self.apiBase + f"clusters/{cluster_id}/actions/complete-installation"
        
        try:
            response = requests.post(url, headers=self.__get_headers())
            response.raise_for_status()
            print(f"Successfully complete installation for cluster: {cluster_id}")      
            print([response.json()])
            return [response.json()]

        except requests.exceptions.HTTPError as e:
            print(f"Failed to complete installation for cluster: {cluster_id}")
            print("cluster_action_complete_installation() returned a bad status code")
            print(e)

        except Exception as e:
            print("Exception found in cluster_action_complete_installation()")
            print(e)


    def cluster_action_reset(self, cluster_id: str):
        url = self.apiBase + f"clusters/{cluster_id}/actions/reset"

        try:
            response = requests.post(url, headers=self.__get_headers())
            response.raise_for_status()
            print(f"Successfully reset cluster: {cluster_id}")
            print([response.json()])
            return [response.json()]

        except requests.exceptions.HTTPError as e:
            print(f"Failed to reset cluster: {cluster_id}")
            print("cluster_action_reset() returned a bad status code")
            print(e)

        except Exception as e:
            print("Exception found in cluster_action_reset()")
            print(e)


    def cluster_action_install(self, cluster_id: str):
        url = self.apiBase + f"clusters/{cluster_id}/actions/install"

        try:
            response = requests.post(url, headers=self.__get_headers())
            response.raise_for_status()
            print(f"Successfully initiated cluster install for cluster: {cluster_id}")
            print([response.json()])
            return [response.json()]
        
        except requests.exceptions.HTTPError as e:
            print(f"Failed to initiate cluster install for cluster: {cluster_id}")
            print("cluster_action_install() returned a bad status code")
            print(e)

        except Exception as e:
            print("Exception found in cluster_action_install()")
            print(e)

    def cluster_get_credentials(self, cluster_id: str, credentials: Optional[str] = None):
        endpoint = f"clusters/{cluster_id}/downloads/credentials" if credentials is not None else f"clusters/{cluster_id}/credentials"
        url = self.apiBase + endpoint
        
        query_string = {"file_name": credentials}

        try:
            if credentials is not None:
                response = requests.get(url, headers=self.__get_headers(), params=query_string)
                response.raise_for_status()
                print(response.text)
                return response.text
            else:
                response = requests.get(url, headers=self.__get_headers())
                response.raise_for_status()
                print([response.json()])
                return [response.json()]
            
        except requests.exceptions.HTTPError as e:
            print("cluster_get_credentials() returned a bad status code")
            print(e)
        
        except Exception as e:
            print("Exception found in cluster_get_credentials()")
            print(e)


    def cluster_get_files(self, cluster_id: str, file_name: str = "install-config.yaml"):
        url = self.apiBase + f"clusters/{cluster_id}/downloads/files"
        
        query_string = {"file_name": file_name}

        try:
            response = requests.get(url, headers=self.__get_headers(), params=query_string)
            response.raise_for_status()
            print(response.text)
            return response.text

        except requests.exceptions.HTTPError as e:
            print("cluster_get_files() returned a bad status code")
            print(e)

        except Exception as e:
            print("Exception found in cluster_get_files()")
            print(e)


    def get_infrastructure_environement_hosts(self, infra_env_id: str):
        url = self.apiBase + f"infra-envs/{infra_env_id}/hosts"
        
        try:
            response = requests.get(url, headers=self.__get_headers())
            response.raise_for_status()
            print(response.json())
            return response.json()

        except requests.exceptions.HTTPError as e:
            print("get_infrastructure_environement_hosts() returned a bad status code")
            print(e)

        except Exception as e:
            print("Exception found in get_infrastructure_environement_hosts()")
            print(e)

    def get_infrastructure_environement_host(self, infra_env_id: str, host_id: str):
        url = self.apiBase + f"infra-envs/{infra_env_id}/hosts/{host_id}"
        try:
            response = requests.get(url, headers=self.__get_headers())
            response.raise_for_status()
            print([response.json()])
            return [response.json()]

        except requests.exceptions.HTTPError as e:
            print("get_infrastructure_environement_host() returned a bad status code")
            print(e)

        except Exception as e:
            print("Exception found in get_infrastructure_environement_host()")
            print(e)

    def post_infrastructure_environement_host(self, infra_env_id: str, host_id: str, discovery_agent_version: Optional[str] = None):
        url = self.apiBase + f"infra-envs/{infra_env_id}/hosts"
        
        host_create_params = HostCreateParams(host_id=host_id, discovery_agent_version=discovery_agent_version)

        data = host_create_params.to_dict()
        try:
            response = requests.post(url, headers=self.__get_headers(), json=data)
            response.raise_for_status()
            print(f"Successfully created new openshift host: {response.json()['id']}")
            print([response.json()])
            return [response.json()]

        except requests.exceptions.HTTPError as e:
            print("Failed to create new openshift host")
            print("post_infrastructure_environement_host() returned a bad status code")
            print(e)

        except Exception as e:
            print("Exception found in post_infrastructure_environement_host()")
            print(e)


    def delete_infrastructure_environement_host(self, infra_env_id: str, host_id: str):
        url = self.apiBase + f"infra-envs/{infra_env_id}/hosts/{host_id}"

        try:
            response = requests.delete(url, headers=self.__get_headers())
            response.raise_for_status()
            print(f"Successfully deleted host {host_id} from infra-env {infra_env_id}")
            return True

        except requests.exceptions.HTTPError as e:
            print(f"Failed to delete host {host_id} from infra-env {infra_env_id}")
            print("post_infrastructure_environement_host() returned a bad status code")
            print(e)

        except Exception as e:
            print("Exception found in delete_infrastructure_environement_host()")
            print(e)


    def host_actions_bind(self, infra_env_id: str, host_id: str):
        url = self.apiBase + f"infra-envs/{infra_env_id}/hosts/{host_id}/actions/bind"

        bind_host_parmas = BindHostParams(cluster_id=self.get_infrastructure_environement(infra_env_id)['cluster_id'])

        data = bind_host_parmas.to_dict()

        try:
            response = requests.post(url, headers=self.__get_headers(), json=data)
            response.raise_for_status()
            print(f"Successfully bound host {host_id} to infra-env {infra_env_id} to cluster-id {data['cluster_id']}")
            print([response.json()])
            return [response.json()]

        except requests.exceptions.HTTPError as e:
            print(f"Failed to bind host {host_id} to infra-env {infra_env_id}")
            print("host_actions_bind() returned a bad status code")
            print(e)

        except Exception as e:
            print("Exception found in host_actions_bind()")
            print(e)


    def host_actions_unbind(self, infra_env_id: str, host_id: str):
        url = self.apiBase + f"infra-envs/{infra_env_id}/hosts/{host_id}/actions/unbind"

        try:
            response = requests.post(url, headers=self.__get_headers())
            response.raise_for_status()
            print(f"Successfully unbound host {host_id} from infra-env {infra_env_id}")
            print([response.json()])
            return [response.json()]

        except requests.exceptions.HTTPError as e:
            print(f"Failed to unbind host {host_id} from infra-env {infra_env_id}")
            print("host_actions_unbind() returned a bad status code")
            print(e)

        except Exception as e:
            print("Exception found in host_actions_unbind()")
            print(e)
        

    def host_actions_install(self, infra_env_id: str, host_id: str):
        url = self.apiBase + f"infra-envs/{infra_env_id}/hosts/{host_id}/actions/install"

        try:
            response = requests.post(url, headers=self.__get_headers())
            response.raise_for_status()
            print(f"Successfully initiated host installation for {host_id} from infra-env {infra_env_id}") 
            print([response.json()])
            return [response.json()]

        except requests.exceptions.HTTPError as e:
            print(f"Failed to initiate host installation {host_id} from infra-env {infra_env_id}")
            print("host_actions_install() returned a bad status code")
            print(e)

        except Exception as e:
            print("Exception found in host_actions_install()")
            print(e)

    def host_actions_reset(self, infra_env_id: str, host_id: str):
        url = self.apiBase + f"infra-envs/{infra_env_id}/hosts/{host_id}/actions/reset"

        try:
            response = requests.post(url, headers=self.__get_headers())
            response.raise_for_status()
            print(f"Successfully initiated host installation for {host_id} from infra-env {infra_env_id}")
            print([response.json()])
            return [response.json()]

        except requests.exceptions.HTTPError as e:
            print(f"Failed to initiate host installation {host_id} from infra-env {infra_env_id}")
            print("host_actions_reset() returned a bad status code")
            print(e)

        except Exception as e:
            print("Exception found in host_actions_reset()")
            print(e)