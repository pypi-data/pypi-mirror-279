import ipaddress, re, json

def filter_dict_by_keys(data, valid_keys):
    """
    Filters a dictionary, removing any keys not in the valid_keys list.

    Parameters:
    data (dict): The dictionary to filter.
    valid_keys (list): The list of valid keys.

    Returns:
    dict: A new dictionary with only the valid keys.
    """
    return {key: value for key, value in data.items() if key in valid_keys}


def is_valid_http_proxy(proxy: str) -> bool:
    """
    Validates if the given string is a valid HTTP proxy.

    Args:
        proxy (str): The string to be validated.

    Returns:
        bool: True if the string matches the HTTP proxy pattern, False otherwise.
    """
    pattern = r'^http:\/\/(?:[a-zA-Z0-9\-_]+(?:\:[a-zA-Z0-9\-_]+)?@)?[a-zA-Z0-9\.\-]+(?:\:[0-9]{1,5})?$'
    
    return bool(re.match(pattern, proxy))


def is_valid_cidr(ip_address: str) -> bool:
    """
    Validates if the given string is a valid IPv4 or IPv6 address with a subnet mask using a regular expression.

    Args:
        ip_address (str): The string to be validated.

    Returns:
        bool: True if the string matches the IPv4 or IPv6 pattern with subnet mask, False otherwise.
    """
    # Regular expression pattern to match either an IPv4 or IPv6 address with subnet mask
    pattern = r'^(?:(?:(?:[0-9]{1,3}\.){3}[0-9]{1,3}\/(?:(?:[0-9])|(?:[1-2][0-9])|(?:3[0-2])))|(?:(?:[0-9a-fA-F]*:[0-9a-fA-F]*){2,})/(?:(?:[0-9])|(?:[1-9][0-9])|(?:1[0-1][0-9])|(?:12[0-8])))$'
    
    # Return the result of the match as a boolean
    return bool(re.match(pattern, ip_address))

def is_valid_kernel_value(kernel_value) -> bool:
    pattern = r'^(?:(?:[^\s\t\n\r"]+)|(?:"[^"]*"))+$'
    return bool(re.match(pattern, kernel_value))

    
def is_valid_openshift_version(version) -> bool:
    """
    Validate if the given value is a valid OpenShift version.

    Parameters:
    version (str): The OpenShift version to validate.

    Returns:
    bool: True if valid, False otherwise.
    """
    pattern = re.compile(r'^\d+\.\d+$')
    return bool(pattern.match(version))

    
def is_valid_ip(ip_address: str) -> bool:
    """
    Validates if the given string is a valid IPv4 or IPv6 address using a regular expression.

    Args:
        ip_address (str): The string to be validated.

    Returns:
        bool: True if the string matches the IPv4 or IPv6 pattern, False otherwise.
    """
    # Regular expression pattern to match either an IPv4 or IPv6 address
    pattern = r'^(?:(?:(?:[0-9]{1,3}\.){3}[0-9]{1,3})|(?:(?:[0-9a-fA-F]*:[0-9a-fA-F]*){2,}))?$'
    
    # Return the result of the match as a boolean
    return bool(re.match(pattern, ip_address))


def is_valid_base_domain(domain) -> bool:
    """
    Validate if the given string is a valid base domain (e.g., example.com).

    Parameters:
    domain (str): The base domain to validate.

    Returns:
    bool: True if valid, False otherwise.
    """
    pattern = re.compile(
        r'^(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.'          # Domain
        r'[A-Za-z]{2,63}$'                           # Top-level domain (TLD)
    )
    return bool(pattern.match(domain))

def is_valid_cpu_architecture(cpu_architecture) -> bool:
    VALID_VALUES = ["x86_64", "aarch64", "arm64", "ppc64le", "s390x", "multi"]
    return cpu_architecture in VALID_VALUES

def is_valid_ha_mode(ha_mode) -> bool:
    VALID_VALUES = ["None", "Full"]
    return ha_mode in VALID_VALUES

def is_valid_hyperthread(hyperthreading) -> bool:
    VALID_VALUES = ["masters", "workers", "none", "all"]
    return hyperthreading in VALID_VALUES

def is_valid_network_type(network_type) -> bool:
    VALID_VALUES = ["OpenShiftSDN", "OVNKubernetes"]
    return network_type in VALID_VALUES

def is_valid_kernel_operation(kernel_operation) -> bool:
    VALID_VALUES = ["append", "replace", "delete"]
    return kernel_operation in VALID_VALUES

def is_valid_enable_on(enable_on) -> bool:
    VALID_VALUES = ["none", "all", "masters", "workers"]
    return enable_on in VALID_VALUES

def is_valid_mode(mode) -> bool:
    VALID_VALUES = ["tang", "tpmv2"]
    return mode in VALID_VALUES

def is_valid_verification(verification: str) -> bool:
    VALID_VALUES = ["unverified", "failed", "succeeded"]
    return verification in VALID_VALUES

def is_valid_external_platform(platform: str) -> bool:
    VALID_VALUES = ["External", ""]
    return platform in VALID_VALUES

def is_valid_platform(platform: str) -> bool:
    VALID_VALUES = ["baremetal", "nutanix", "vsphere", "none", "external"]
    return platform in VALID_VALUES