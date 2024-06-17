## Code to disable creating pycache dir after running
import sys, requests, json, os
sys.dont_write_bytecode = True
###################################################

from urllib.parse import urlencode

from .lib.schema.cluster import *

from .lib.schema.infra_env import *

from .lib.utils import *

from requests import Response

import pprint

DEBUG_MODE = False


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

        response = requests.post(url, headers=headers, data=data)
        access_token = response.json().get("access_token")
        return access_token


    def get_cluster(self, cluster_id: str=None) -> Response:
        url = self.apiBase + f"clusters/{cluster_id}"

        response = requests.get(url, headers=self.__get_headers())
        if DEBUG_MODE:
            pprint.pprint(response.json(), compact=True)  
        return response   

    def get_default_config(self) -> Response:
        url = self.apiBase + f"clusters/default-config"

        response = requests.get(url, headers=self.__get_headers())
        if DEBUG_MODE:
            pprint.pprint(response.json(), compact=True) 
        return response

    def get_clusters(self, with_hosts: bool=False, owner: str=None) -> Response:
        url = self.apiBase + "clusters"

        if with_hosts:
            if '?' not in url:
                url += '?'
            url += f'with_hosts={with_hosts}&'            

        if owner is not None:
            if '?' not in url:
                url += '?'
            url += f'owner={owner}&'
        
        response = requests.get(url, headers=self.__get_headers())
        if DEBUG_MODE:
            pprint.pprint(response.json(), compact=True) 
        return response
    
    def post_cluster(self, cluster: ClusterParams) -> Response:
        VALID_POST_PARAMS = [
            "additional_ntp_source","api_vips","base_dns_domain","cluster_network_cidr","cluster_network_host_prefix",
            "cluster_networks","cpu_architecture","disk_encryption","high_availability_mode","http_proxy","https_proxy",
            "hyperthreading","ignition_endpoint","ingress_vips","machine_networks","name","network_type","no_proxy",
            "ocp_release_image","olm_operators","openshift_version","platform","pull_secret","schedulable_masters",
            "service_network_cidr","service_networks","ssh_public_key","tags","user_managed_networking","vip_dhcp_allocation",
            ]
        
        url = self.apiBase + "clusters"

        cluster_params = filter_dict_by_keys(cluster.create_params(), VALID_POST_PARAMS)

        response = requests.post(url, headers=self.__get_headers(), json=cluster_params)    
        if DEBUG_MODE:
            pprint.pprint(response.json(), compact=True) 
        return response

    def patch_cluster(self, cluster: ClusterParams) -> Response:
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
            response = requests.Response()
            response._content = b'{"message": "cluster_id is requried to preform the patch operation"}'
            response.status_code = 404
            return response
        
        cluster_params = filter_dict_by_keys(cluster_params, VALID_PATCH_PARAMS)
        
        url = self.apiBase + f"clusters/{cluster_id}"

        response = requests.patch(url, headers=self.__get_headers(), json=cluster_params)
        if DEBUG_MODE:
            pprint.pprint(response.json(), compact=True) 
        return response

    def delete_cluster(self, cluster_id: str) -> bool:
        url = self.apiBase + f"clusters/{cluster_id}"
        response = requests.delete(url, headers=self.__get_headers())
        return True if (response.status_code == 204) else False

    def get_infrastructure_environement(self, infra_env_id: str) -> Response:
        url = self.apiBase + f"infra-envs/{infra_env_id}"

        response = requests.get(url, headers=self.__get_headers())
        if DEBUG_MODE:
            pprint.pprint(response.json(), compact=True) 
        return response

    # Method that will implement the /v2/infra-envs GET assisted installer endpoint
    def get_infrastructure_environements(self) -> Response:
        url = self.apiBase + "infra-envs"
        
        response = requests.get(url, headers=self.__get_headers())
        if DEBUG_MODE:
            pprint.pprint(response.json(), compact=True) 
        return response.json()
        
    def patch_infrastructure_environment(self, infra_env: InfraEnv) -> Response:
        VALID_PATCH_PARAMS =  [
            "additional_ntp_sources","additional_trust_bundle","ignition_config_override","image_type",
            "kernel_arguments","proxy","pull_secret","ssh_authorized_key","static_network_config",
            ]
        
        infra_params = infra_env.create_params()

        infra_env_id = infra_params.pop("infra_env_id", None)

        if infra_env_id is None:
            response = requests.Response()
            response._content = b'{"message": "infra_env_id is requried to preform the patch operation"}'
            response.status_code = 404
            return response
        
        infra_params = filter_dict_by_keys(infra_params, VALID_PATCH_PARAMS)
        
        url = self.apiBase + f"infra-envs/{infra_env_id}"

        response = requests.patch(url, headers=self.__get_headers(), json=infra_params)
        if DEBUG_MODE:
            pprint.pprint(response.json(), compact=True) 
        return response

    def post_infrastructure_environment(self, infra_env: InfraEnv) -> Response:
        VALID_POST_PARAMS = [
            "additional_ntp_sources","additional_trust_bundle","cluster_id","cpu_architecture",
            "ignition_config_override","image_type","kernel_arguments","name","openshift_version",
            "proxy","pull_secret","ssh_authorized_key","static_network_config",
            ]
        
        url = self.apiBase + "infra-envs"

        infra_env_params = filter_dict_by_keys(infra_env.create_params(), VALID_POST_PARAMS)

        response = requests.post(url, headers=self.__get_headers(), json=infra_env_params)
        if DEBUG_MODE:
            pprint.pprint(response.json(), compact=True) 
        return response
    
    def delete_infrastructure_environment(self, infra_env_id: str) -> bool:
        url = self.apiBase + f"infra-envs/{infra_env_id}"

        response = requests.delete(url, headers=self.__get_headers())
        return True if (response.status_code == 204) else False

    def cluster_action_allow_add_hosts(self, cluster_id: str):
        url = self.apiBase + f"clusters/{cluster_id}/actions/allow-add-hosts"

        response = requests.post(url, headers=self.__get_headers())
        if DEBUG_MODE:
            pprint.pprint(response.json(), compact=True) 
        return response

    def cluster_action_allow_add_workers(self, cluster_id: str):
        url = self.apiBase + f"clusters/{cluster_id}/actions/allow-add-workers"

        response = requests.post(url, headers=self.__get_headers())
        if DEBUG_MODE:
            pprint.pprint(response.json(), compact=True) 
        return response

    def cluster_action_cancel(self, cluster_id: str):
        url = self.apiBase + f"clusters/{cluster_id}/actions/cancel"

        response = requests.post(url, headers=self.__get_headers())
        print(f"Successfully canceled installation for cluster: {cluster_id}") 
        if DEBUG_MODE:
            pprint.pprint(response.json(), compact=True) 
        return response

    def cluster_action_complete_installation(self, cluster_id: str):
        url = self.apiBase + f"clusters/{cluster_id}/actions/complete-installation"
        
        response = requests.post(url, headers=self.__get_headers())
        print(f"Successfully complete installation for cluster: {cluster_id}")      
        if DEBUG_MODE:
            pprint.pprint(response.json(), compact=True) 
        return response

    def cluster_action_reset(self, cluster_id: str):
        url = self.apiBase + f"clusters/{cluster_id}/actions/reset"

        response = requests.post(url, headers=self.__get_headers())
        if DEBUG_MODE:
            pprint.pprint(response.json(), compact=True) 
        return response

    def cluster_action_install(self, cluster_id: str):

        url = self.apiBase + f"clusters/{cluster_id}/actions/install"
        response = requests.post(url, headers=self.__get_headers())
        print(f"Successfully initiated cluster install for cluster: {cluster_id}")
        if DEBUG_MODE:
            pprint.pprint(response.json(), compact=True) 
        return response
        
    def cluster_get_credentials(self, cluster_id: str, credentials: str = None):
        endpoint = f"clusters/{cluster_id}/downloads/credentials" if credentials is not None else f"clusters/{cluster_id}/credentials"
        url = self.apiBase + endpoint
        
        query_string = {"file_name": credentials}

        if credentials is not None:
            response = requests.get(url, headers=self.__get_headers(), params=query_string)
            if DEBUG_MODE:
                print(response.text)
            return response
        else:
            response = requests.get(url, headers=self.__get_headers())
            if DEBUG_MODE:
                pprint.pprint(response.json(), compact=True) 
            return response

    def cluster_get_files(self, cluster_id: str, file_name: str = "install-config.yaml"):
        url = self.apiBase + f"clusters/{cluster_id}/downloads/files"
        
        query_string = {"file_name": file_name}

        response = requests.get(url, headers=self.__get_headers(), params=query_string)
        if DEBUG_MODE:
            print(response.text)
        return response

    def get_infrastructure_environement_hosts(self, infra_env_id: str) -> Response:
        url = self.apiBase + f"infra-envs/{infra_env_id}/hosts"

        response = requests.get(url, headers=self.__get_headers())
        if DEBUG_MODE:
            pprint.pprint(response.json(), compact=True) 
        return response

    def get_infrastructure_environement_host(self, infra_env_id: str, host_id: str) -> Response:
        url = self.apiBase + f"infra-envs/{infra_env_id}/hosts/{host_id}"

        response = requests.get(url, headers=self.__get_headers())
        if DEBUG_MODE:
            pprint.pprint(response.json(), compact=True) 
        return response