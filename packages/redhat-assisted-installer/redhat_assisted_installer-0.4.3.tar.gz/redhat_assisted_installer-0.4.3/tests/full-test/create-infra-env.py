import sys, os
## Code to disable creating pycache dir after running
sys.dont_write_bytecode = True
###################################################

sys.path.append(os.path.abspath(f"{os.getcwd()}/tests/"))

from utils import *

sys.path.append(os.path.abspath(f"{os.getcwd()}/src/"))


from redhat_assisted_installer.assisted_installer import *
from redhat_assisted_installer.lib.schema.infra_env import *

import pprint

mac_interface_map = [MacInterfaceMap(logical_nic_name="log-nic-0",
                                     mac_address="00:1b:63:84:45:e6",
                                    )]

yaml_data = """
interfaces:
  - name: eth0
    type: ethernet
    state: up
    mac-address: 00:1A:2B:3C:4D:5E
    ipv4:
      enabled: true
      address:
        - ip: 192.168.1.10
          prefix-length: 24
      dhcp: false
    ipv6:
      enabled: false

  - name: eth1
    type: ethernet
    state: up
    mac-address: 00:1A:2B:3C:4D:5F
    ipv4:
      enabled: true
      dhcp: true
    ipv6:
      enabled: false

dns-resolver:
  config:
    server:
      - 8.8.8.8
      - 8.8.4.4

routes:
  config:
    - destination: 0.0.0.0/0
      next-hop-address: 192.168.1.1
      next-hop-interface: eth0
      table-id: 254
"""

static_network_config = [StaticNetworkConfig(mac_interface_map=mac_interface_map,
                                            network_yaml=yaml_data,)]

proxy = Proxy(http_proxy="http://test:test@192.168.5.1:80",
              https_proxy="http://test:test@192.168.6.1:443",
              no_proxy="192.168.7.1")

val = """
rd.net.timeout.carrier=60
isolcpus=1,2,10-20,100-2000:2/25
quiet
"""

kernel_args = [KernelArgument(operation="append",
                              value=val
                              )]


infra_env = InfraEnv(additional_ntp_source="",
                     additional_trust_bundle="",
                     cpu_architecture="x86_64",
                     ignition_config_override="",
                     image_type="full-iso",
                     kernel_arguments=kernel_args,
                     name="pypi-testing",
                     openshift_version="4.15",
                     proxy=proxy,
                     static_network_config=static_network_config,
                     )

pprint.pprint(infra_env.create_params())


try: 
    api_response = post_infrastructure_environment(infra_env)
    api_response.raise_for_status()
    pprint.pprint(api_response.json(), compact=False)

except Exception as e:
    print(e)
    pprint.pprint(api_response.json())