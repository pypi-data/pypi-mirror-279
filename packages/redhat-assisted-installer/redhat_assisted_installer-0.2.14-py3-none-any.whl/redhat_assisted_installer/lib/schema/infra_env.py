import os

from ..utils import *

class InfraEnv:
    def __init__(self,
                 infra_env_id: str = None,
                 name: str = None,
                 pull_secret: str = os.environ.get("REDHAT_PULL_SECRET"),
                 additional_ntp_source: str = None, 
                 additional_trust_bundle: str = None, 
                 cluster_id: str = None,
                 cpu_architecture: str = None,
                 ignition_config_override: str = None, 
                 image_type: str = None,
                 openshift_version: str = None,
                 ssh_authorized_key: str = None,
                 ):
        self.params = {}

        if name is not None:
            self.params['name'] = name

        if infra_env_id is not None:
            self.params['infra_env_id'] = infra_env_id

        if openshift_version is not None and is_valid_openshift_version(openshift_version):
            self.params['openshift_version'] = openshift_version

        if cluster_id is not None:
            self.params['cluster_id'] = cluster_id

        if pull_secret is not None and is_valid_json(pull_secret):
            self.params['pull_secret'] = pull_secret

        if additional_ntp_source is not None and is_valid_ip(additional_ntp_source):
            self.params['additional_ntp_source'] = additional_ntp_source

        if additional_trust_bundle is not None:
            self.params['additional_trust_bundle'] = additional_trust_bundle

        if ignition_config_override is not None and is_valid_json(ignition_config_override):
            self.params['ignition_config_override'] = ignition_config_override

        if image_type is not None and (image_type):
            self.params['image_type'] = image_type

        if cpu_architecture is not None and is_valid_cpu_architecture(cpu_architecture):
            self.params['cpu_architecture'] = cpu_architecture

        if ssh_authorized_key is not None :
            self.params['ssh_authorized_key'] = ssh_authorized_key


    def create_params(self):
        return {key: value for key, value in self.params.items() if value is not None}
    