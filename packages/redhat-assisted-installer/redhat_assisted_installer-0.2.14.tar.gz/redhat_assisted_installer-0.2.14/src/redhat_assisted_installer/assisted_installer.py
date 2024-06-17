## Code to disable creating pycache dir after running
import sys, requests, json, os
sys.dont_write_bytecode = True
###################################################

from urllib.parse import urlencode

from .lib.schema.cluster import *

from .lib.schema.infra_env import *

from .lib.utils import *

from requests.exceptions import HTTPError

import pprint


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
            "refresh_token": os.environ.get("REDHAT_OFFLINE_TOKEN")
        })

        try:
            # Make the POST request
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()
            access_token = response.json().get("access_token")
            return access_token

        except HTTPError as e:
            print(f"Failed to __get_access_token")
            print("__get_access_token() returned a bad status code")
            pprint.pprint(response.json(), compact=True)
            return response.json()

        except Exception as e:
            print("Exception found in __get_access_token()")
            print(e)


    def get_cluster(self, cluster_id: str=None):
        url = self.apiBase + f"clusters/{cluster_id}"

        try:
            response = requests.get(url, headers=self.__get_headers())
            response.raise_for_status()
            pprint.pprint(response.json(), compact=True)
            return [response.json()]
        
        except HTTPError as e:
            print("get_cluster() returned a bad status code")
            pprint.pprint(response.json(), compact=True)
            return response.json()

        except Exception as e:
            print("Exception found in get_cluster()")
            print(e)

    def get_default_config(self):
        url = self.apiBase + f"clusters/default-config"

        try:
            response = requests.get(url, headers=self.__get_headers())
            response.raise_for_status()
            pprint.pprint(response.json(), compact=True)
            return response.json()
        
        except HTTPError as e:
            print("get_default_config() returned a bad status code")
            pprint.pprint(response.json(), compact=True)
            return response.json()

        except Exception as e:
            print("Exception found in get_default_config()")
            print(e)

    def get_clusters(self, with_hosts: bool=False, owner: str=None):
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
            pprint.pprint(response.json(), compact=True)
            return response.json()
            
        except HTTPError as e:
            print("get_clusters() returned a bad status code")
            pprint.pprint(response.json(), compact=True)
            return response.json()
            
        except Exception as e:
            print("Exception found in getClusters()")
            print(e)

    def post_cluster(self, cluster: ClusterParams):
        VALID_POST_PARAMS = [
            "additional_ntp_source","api_vips","base_dns_domain","cluster_network_cidr","cluster_network_host_prefix",
            "cluster_networks","cpu_architecture","disk_encryption","high_availability_mode","http_proxy","https_proxy",
            "hyperthreading","ignition_endpoint","ingress_vips","machine_networks","name","network_type","no_proxy",
            "ocp_release_image","olm_operators","openshift_version","platform","pull_secret","schedulable_masters",
            "service_network_cidr","service_networks","ssh_public_key","tags","user_managed_networking","vip_dhcp_allocation",
            ]
        
        url = self.apiBase + "clusters"

        cluster_params = filter_dict_by_keys(cluster.create_params(), VALID_POST_PARAMS)

        try:
            response = requests.post(url, headers=self.__get_headers(), json=cluster_params)
            response.raise_for_status()    
            print("Successfully created cluster:")
            pprint.pprint(response.json(), compact=True)
            return [response.json()]
        
        except HTTPError as e:
            print(f"Failed to create cluster:")
            print("post_cluster() returned a bad status code")
            pprint.pprint(response.json(), compact=True)
            return response.json()

        except Exception as e:
            print("Exception found in post_cluster()")
            print(e)

    def patch_cluster(self, cluster: ClusterParams):
        VALID_PATCH_PARAMS = [
            "additional_ntp_source","api_vip_dns_name","api_vips","base_dns_domain","cluster_network_cidr",
            "cluster_network_host_prefix","cluster_networks","disk_encryption","http_proxy","https_proxy","hyperthreading",
            "ignition_endpoint","ingress_vips","machine_network_cidr","machine_networks","name","network_type","no_proxy",
            "olm_operators","platform","pull_secret","schedulable_masters","service_network_cidr","service_networks",
            "ssh_public_key","tags","user_managed_networking","vip_dhcp_allocation",
            ]
        
        cluster_params = cluster.create_params()

        cluster_id = cluster_params.pop("cluster_id", None)

        if cluster_id is None:
            return {"status": "Failed", "reason": "Cluster Id is requried to preform the patch operation"}
        
        cluster_params = filter_dict_by_keys(cluster_params, VALID_PATCH_PARAMS)
        
        url = self.apiBase + f"clusters/{cluster_id}"

        try:
            response = requests.patch(url, headers=self.__get_headers(), json=cluster_params)
            response.raise_for_status()
            print(f"Successfully patched cluster: {cluster_id}")
            pprint.pprint(response.json(), compact=True)
            return [response.json()]
        
        except HTTPError as e:
            print(f"Failed to patch cluster: {cluster_id}")
            print("patch_cluster() returned a bad status code")
            pprint.pprint(response.json(), compact=True)
            return response.json()

        except Exception as e:
            print("Exception found in patch_cluster()")
            pprint.pprint(response.json(), compact=True)
            return response.json()

    def delete_cluster(self, cluster_id: str):
        url = self.apiBase + f"clusters/{cluster_id}"

        try:
            response = requests.delete(url, headers=self.__get_headers())
            response.raise_for_status()
            print(f"Successfully deleted cluster: {cluster_id}")
            return True

        except HTTPError as e:
            print(f"Failed to delete cluster: {cluster_id}")
            print("delete_cluster() returned a bad status code")
            pprint.pprint(response.json(), compact=True)
            return response.json()

        except Exception as e:
            print(f"Failed to delete cluster: {cluster_id}")
            print("Exception found in delete_cluster()")
            print(e)


    def get_infrastructure_environement(self, infra_env_id: str):
        url = self.apiBase + f"infra-envs/{infra_env_id}"

        try:
            response = requests.get(url, headers=self.__get_headers())
            response.raise_for_status()
            pprint.pprint(response.json(), compact=True)
            return [response.json()]
            
        except HTTPError as e:
            print("get_infrastructure_environement() returned a bad status code")
            pprint.pprint(response.json(), compact=True)
            return response.json()
    
        except Exception as e:
            print("Exception found in get_infrastructure_environment()")
            print(e)   

    # Method that will implement the /v2/infra-envs GET assisted installer endpoint
    def get_infrastructure_environements(self):
        url = self.apiBase + "infra-envs"
        
        try:
            response = requests.get(url, headers=self.__get_headers())
            response.raise_for_status()
            pprint.pprint(response.json(), compact=True)
            return response.json()
        
        except HTTPError as e:
            print("get_infrastructure_environements() returned a bad status code")
            pprint.pprint(response.json(), compact=True)
            return response.json()
            
        except Exception as e:
            print("Exception found in get_infrastructure_environments()")
            print(e)

    def patch_infrastructure_environment(self, infra_env: InfraEnv):
        VALID_PATCH_PARAMS =  [
            "additional_ntp_sources","additional_trust_bundle","ignition_config_override","image_type",
            "kernel_arguments","proxy","pull_secret","ssh_authorized_key","static_network_config",
            ]
        
        infra_params = infra_env.create_params()

        infra_env_id = infra_params.pop("infra_env_id", None)

        if infra_env_id is None:
            return {"status": "Failed", "reason": "infra_env_id is requried to preform the patch operation"}
        
        infra_params = filter_dict_by_keys(infra_params, VALID_PATCH_PARAMS)
        
        url = self.apiBase + f"infra-envs/{infra_env_id}"

        try:
            response = requests.patch(url, headers=self.__get_headers(), json=infra_params)
            response.raise_for_status()
            print(f"Successfully patched infra-env: {infra_env_id}")
            pprint.pprint(response.json(), compact=True)
            return [response.json()]

        except HTTPError as e:
            print("patch_infrastructure_environment() returned a bad status code")
            pprint.pprint(response.json(), compact=True)
            return response.json()

        except Exception as e:
            print("Exception found in patch_infrastructure_environment()")
            print(e)


    def post_infrastructure_environment(self, infra_env: InfraEnv):
        VALID_POST_PARAMS = [
            "additional_ntp_sources","additional_trust_bundle","cluster_id","cpu_architecture",
            "ignition_config_override","image_type","kernel_arguments","name","openshift_version",
            "proxy","pull_secret","ssh_authorized_key","static_network_config",
            ]
        
        url = self.apiBase + "infra-envs"

        infra_env_params = filter_dict_by_keys(infra_env.create_params(), VALID_POST_PARAMS)
        
        print(infra_env_params)

        try:
            response = requests.post(url, headers=self.__get_headers(), json=infra_env_params)
            response.raise_for_status()
            print("Successfully created infra-env:") 
            pprint.pprint(response.json(), compact=True)
            return [response.json()]
        
        except HTTPError as e:
            print(f"Failed to create infra-env")
            print("post_infrastructure_environment() returned a bad status code")
            pprint.pprint(response.json(), compact=True)
            return response.json()

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

        except HTTPError as e:
            print(f"Failed to delete infra-env")
            print("delete_infrastructure_environment() returned a bad status code")
            pprint.pprint(response.json(), compact=True)
            return response.json()

        except Exception as e:
            print("Exception found in delete_infrastructure_environment()")
            print(e)


    def cluster_action_allow_add_hosts(self, cluster_id: str):
        url = self.apiBase + f"clusters/{cluster_id}/actions/allow-add-hosts"

        try:
            response = requests.post(url, headers=self.__get_headers())
            response.raise_for_status()
            print(f"Successfully initiated action 'allow-add-hosts' for cluster: {cluster_id}")
            pprint.pprint(response.json(), compact=True)
            return [response.json()]

        except HTTPError as e:
            print(f"Failed to initiate action 'allow-add-hosts' for cluster: {cluster_id}")
            print("cluster_action_allow_add_hosts() returned a bad status code")
            pprint.pprint(response.json(), compact=True)
            return response.json()

        except Exception as e:
            print("Exception found in allow_add_hosts()")
            print(e)


    def cluster_action_allow_add_workers(self, cluster_id: str):
        url = self.apiBase + f"clusters/{cluster_id}/actions/allow-add-workers"

        try:
            response = requests.post(url, headers=self.__get_headers())
            response.raise_for_status()
            print(f"Successfully initiated action 'allow-add-workers' for cluster: {cluster_id}")  
            pprint.pprint(response.json(), compact=True)
            return [response.json()]

        except HTTPError as e:
            print(f"Failed to initiate action 'cluster_action_allow_add_workers' for cluster: {cluster_id}")
            print("cluster_action_allow_add_workers() returned a bad status code")
            pprint.pprint(response.json(), compact=True)
            return response.json()

        except Exception as e:
            print("Exception found in cluster_action_allow_add_workers()")
            print(e)

    def cluster_action_cancel(self, cluster_id: str):
        url = self.apiBase + f"clusters/{cluster_id}/actions/cancel"

        try:
            response = requests.post(url, headers=self.__get_headers())
            response.raise_for_status()
            print(f"Successfully canceled installation for cluster: {cluster_id}") 
            pprint.pprint(response.json(), compact=True)
            return [response.json()]

        except HTTPError as e:
            print(f"Failed to cancel installation for cluster: {cluster_id}")
            print("cluster_action_cancel() returned a bad status code")
            pprint.pprint(response.json(), compact=True)
            return response.json()

        except Exception as e:
            print("Exception found in cluster_action_cancel()")
            print(e)

    def cluster_action_complete_installation(self, cluster_id: str):
        url = self.apiBase + f"clusters/{cluster_id}/actions/complete-installation"
        
        try:
            response = requests.post(url, headers=self.__get_headers())
            response.raise_for_status()
            print(f"Successfully complete installation for cluster: {cluster_id}")      
            pprint.pprint(response.json(), compact=True)
            return [response.json()]

        except HTTPError as e:
            print(f"Failed to complete installation for cluster: {cluster_id}")
            print("cluster_action_complete_installation() returned a bad status code")
            pprint.pprint(response.json(), compact=True)
            return response.json()

        except Exception as e:
            print("Exception found in cluster_action_complete_installation()")
            print(e)


    def cluster_action_reset(self, cluster_id: str):
        url = self.apiBase + f"clusters/{cluster_id}/actions/reset"

        try:
            response = requests.post(url, headers=self.__get_headers())
            response.raise_for_status()
            print(f"Successfully reset cluster: {cluster_id}")
            pprint.pprint(response.json(), compact=True)
            return [response.json()]

        except HTTPError as e:
            print(f"Failed to reset cluster: {cluster_id}")
            print("cluster_action_reset() returned a bad status code")
            pprint.pprint(response.json(), compact=True)
            return response.json()

        except Exception as e:
            print("Exception found in cluster_action_reset()")
            print(e)


    def cluster_action_install(self, cluster_id: str):
        url = self.apiBase + f"clusters/{cluster_id}/actions/install"

        try:
            response = requests.post(url, headers=self.__get_headers())
            response.raise_for_status()
            print(f"Successfully initiated cluster install for cluster: {cluster_id}")
            pprint.pprint(response.json(), compact=True)
            return [response.json()]
        
        except HTTPError as e:
            print(f"Failed to initiate cluster install for cluster: {cluster_id}")
            print("cluster_action_install() returned a bad status code")
            pprint.pprint(response.json(), compact=True)
            return response.json()

        except Exception as e:
            print("Exception found in cluster_action_install()")
            print(e)

    def cluster_get_credentials(self, cluster_id: str, credentials: str = None):
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
                pprint.pprint(response.json(), compact=True)
                return [response.json()]
            
        except HTTPError as e:
            print("cluster_get_credentials() returned a bad status code")
            pprint.pprint(response.json(), compact=True)
            return response.json()
        
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

        except HTTPError as e:
            print("cluster_get_files() returned a bad status code")
            pprint.pprint(response.json(), compact=True)
            return response.json()

        except Exception as e:
            print("Exception found in cluster_get_files()")
            print(e)


    def get_infrastructure_environement_hosts(self, infra_env_id: str):
        url = self.apiBase + f"infra-envs/{infra_env_id}/hosts"
        
        try:
            response = requests.get(url, headers=self.__get_headers())
            response.raise_for_status()
            pprint.pprint(response.json(), compact=True)
            return response.json()

        except HTTPError as e:
            print("get_infrastructure_environement_hosts() returned a bad status code")
            pprint.pprint(response.json(), compact=True)
            return response.json()

        except Exception as e:
            print("Exception found in get_infrastructure_environement_hosts()")
            print(e)

    def get_infrastructure_environement_host(self, infra_env_id: str, host_id: str):
        url = self.apiBase + f"infra-envs/{infra_env_id}/hosts/{host_id}"
        try:
            response = requests.get(url, headers=self.__get_headers())
            response.raise_for_status()
            pprint.pprint(response.json(), compact=True)
            return [response.json()]

        except HTTPError as e:
            print("get_infrastructure_environement_host() returned a bad status code")
            pprint.pprint(response.json(), compact=True)
            return response.json()

        except Exception as e:
            print("Exception found in get_infrastructure_environement_host()")
            print(e)

    # def post_infrastructure_environement_host(self, infra_env_id: str, host_id: str, discovery_agent_version: str = None):
    #     url = self.apiBase + f"infra-envs/{infra_env_id}/hosts"
        
    #     host_create_params = HostCreateParams(host_id=host_id, discovery_agent_version=discovery_agent_version)

    #     data = host_create_params.to_dict()
    #     try:
    #         response = requests.post(url, headers=self.__get_headers(), json=data)
    #         response.raise_for_status()
    #         print(f"Successfully created new openshift host: {response.json()['id']}")
    #         pprint.pprint(response.json(), compact=True)
    #         return [response.json()]

    #     except HTTPError as e:
    #         print("Failed to create new openshift host")
    #         print("post_infrastructure_environement_host() returned a bad status code")
    #         pprint.pprint(response.json(), compact=True)
    #         return response.json()

    #     except Exception as e:
    #         print("Exception found in post_infrastructure_environement_host()")
    #         print(e)


    # def delete_infrastructure_environement_host(self, infra_env_id: str, host_id: str):
    #     url = self.apiBase + f"infra-envs/{infra_env_id}/hosts/{host_id}"

    #     try:
    #         response = requests.delete(url, headers=self.__get_headers())
    #         response.raise_for_status()
    #         print(f"Successfully deleted host {host_id} from infra-env {infra_env_id}")
    #         return True

    #     except HTTPError as e:
    #         print(f"Failed to delete host {host_id} from infra-env {infra_env_id}")
    #         print("post_infrastructure_environement_host() returned a bad status code")
    #         pprint.pprint(response.json(), compact=True)
    #         return response.json()

    #     except Exception as e:
    #         print("Exception found in delete_infrastructure_environement_host()")
    #         print(e)


    # def host_actions_bind(self, infra_env_id: str, host_id: str):
    #     url = self.apiBase + f"infra-envs/{infra_env_id}/hosts/{host_id}/actions/bind"

    #     bind_host_parmas = BindHostParams(cluster_id=self.get_infrastructure_environement(infra_env_id)['cluster_id'])

    #     data = bind_host_parmas.to_dict()

    #     try:
    #         response = requests.post(url, headers=self.__get_headers(), json=data)
    #         response.raise_for_status()
    #         print(f"Successfully bound host {host_id} to infra-env {infra_env_id} to cluster-id {data['cluster_id']}")
    #         pprint.pprint(response.json(), compact=True)
    #         return [response.json()]

    #     except HTTPError as e:
    #         print(f"Failed to bind host {host_id} to infra-env {infra_env_id}")
    #         print("host_actions_bind() returned a bad status code")
    #         pprint.pprint(response.json(), compact=True)
    #         return response.json()

    #     except Exception as e:
    #         print("Exception found in host_actions_bind()")
    #         print(e)


    # def host_actions_unbind(self, infra_env_id: str, host_id: str):
    #     url = self.apiBase + f"infra-envs/{infra_env_id}/hosts/{host_id}/actions/unbind"

    #     try:
    #         response = requests.post(url, headers=self.__get_headers())
    #         response.raise_for_status()
    #         print(f"Successfully unbound host {host_id} from infra-env {infra_env_id}")
    #         pprint.pprint(response.json(), compact=True)
    #         return [response.json()]

    #     except HTTPError as e:
    #         print(f"Failed to unbind host {host_id} from infra-env {infra_env_id}")
    #         print("host_actions_unbind() returned a bad status code")
    #         pprint.pprint(response.json(), compact=True)

    #     except Exception as e:
    #         print("Exception found in host_actions_unbind()")
    #         print(e)
        

    # def host_actions_install(self, infra_env_id: str, host_id: str):
    #     url = self.apiBase + f"infra-envs/{infra_env_id}/hosts/{host_id}/actions/install"

    #     try:
    #         response = requests.post(url, headers=self.__get_headers())
    #         response.raise_for_status()
    #         print(f"Successfully initiated host installation for {host_id} from infra-env {infra_env_id}") 
    #         pprint.pprint(response.json(), compact=True)
    #         return [response.json()]

    #     except HTTPError as e:
    #         print(f"Failed to initiate host installation {host_id} from infra-env {infra_env_id}")
    #         print("host_actions_install() returned a bad status code")
    #         pprint.pprint(response.json(), compact=True)
    #         return response.json()

    #     except Exception as e:
    #         print("Exception found in host_actions_install()")
    #         print(e)

    # def host_actions_reset(self, infra_env_id: str, host_id: str):
    #     url = self.apiBase + f"infra-envs/{infra_env_id}/hosts/{host_id}/actions/reset"

    #     try:
    #         response = requests.post(url, headers=self.__get_headers())
    #         response.raise_for_status()
    #         print(f"Successfully initiated host installation for {host_id} from infra-env {infra_env_id}")
    #         pprint.pprint(response.json(), compact=True)
    #         return [response.json()]

    #     except HTTPError as e:
    #         print(f"Failed to initiate host installation {host_id} from infra-env {infra_env_id}")
    #         print("host_actions_reset() returned a bad status code")
    #         pprint.pprint(response.json(), compact=True)
    #         return response.json()

    #     except Exception as e:
    #         print("Exception found in host_actions_reset()")
    #         print(e)