# red-hat-assisted-installer
Python package to implement the RedHat Assisted Installer API.

## Description
Python package that implements the [RedHat Assisted Installer API](https://developers.redhat.com/api-catalog/api/assisted-install-service#content-operations). This


## Installation

    pip install redhat-assisted-installer

## Package Requirements

### Packages
    pip install requests

### Environment Variables

- `REDHAT_PULL_SECRET`: The pull secret associated with your RedHat Hybrid Cloud account

- `REDHAT_OFFLINE_TOKEN`: The offline token associated with your RedHat Hybrid Cloud account


**_You can find these credentials by navigating to https://console.redhat.com/openshift/overview. In the side panel navigate to `Downloads`, and at the bottom of the page you should see the pull secret and token_**

![](https://raw.githubusercontent.com/JustinBatchelor/red-hat-assisted-installer/c33b2eb3570ab498e85944035e71156ee192a816/docs/downloads_console.png)


## How to use

### Create AssistedInstaller instance

    # import package
    import redhat_assisted_installer.assistedinstaller as assistedinstaller

    # Method 1:
    # set assisted installer token value as an evironment variable
    os.environ['REDHAT_OFFLINE_TOKEN'] = <str> token
    # set assisted installer pull_secret value as an evironment variable
    os.environ['REDHAT_PULL_SECRET'] = <str> pull_secret

    # Method 2:
    # You can also set env in virtual environment `activate` file via export.. you may have to restart your session
    # export REDHAT_OFFLINE_TOKEN= '<token>'
    # export REDHAT_PULL_SECRET= '<pull_secret>'

    # create installer instance
    installer = assistedinstaller.assistedinstaller()

On init the class will lookup the environment variables specified in requirements, and attempt to set those as attributes of itself.

### API ENDPOINTS Implemented

#### /v2/clusters

**GET**

Retrieves the list of OpenShift clusters.

Query Parameters

| name | type | description | required |
| ---- | ---- | ----------- | -------- |
| openshift_cluster_id | string | A specific cluster to retrieve. | False |
| with_hosts | boolean | Include hosts in the returned list. | False |
| owner | string | returns only clusters that are owned by the specified user. | False |

**EXAMPLES**

    import redhat_assisted_installer.assistedinstaller as assistedinstaller

    installer = assistedinstaller.assistedinstaller()

    # return all clusters associated with this account
    clusters = installer.getClusters()

    # return cluster by id... still returns an array so remember to access via index (i.e clusters[0])
    clusters = installer.getClusters(cluster_id=<cluster_id>)

    # return all clusters and include the hosts associated with each cluster
    clusters = installer.getClusters(with_hosts=True=<bool>)

**POST**

Creates a new OpenShift cluster definition.

Body Parameters

| name | type | description | required |
| ---- | ---- | ----------- | -------- | 
| name | string | Name of cluster definition. | True |
| version | string | OpenShift version to use. | True | 
| basedomain | string | The base dns domain to use for the cluster. | True |
| hamode | string | Determine if the cluster will be single node or highly available | False | 
| cpuarchitecture | string  | The cpu arch of the baremetal hardware this cluster will run on | False | ["x86_64", "aarch64", "arm64", "ppc64le", "s390x", "multi"] | "x86_64" |

**EXAMPLES**

    import redhat_assisted_installer.assistedinstaller as assistedinstaller

    installer = assistedinstaller.assistedinstaller()

    # create a single node openshift cluster running version 4.15  
    cluster = installer.postCluster("ocp-testing-sno", "4.15", "example.com")

    # create a highly available cluster running 3 control plane nodes
    cluster = installer.postCluster("ocp-testing-ha", "4.15", "example.com", hamode="Full")


#### /v2/clusters/{cluster_id}

**DELETE**

Deletes an OpenShift cluster definition.

Path Parameters

| name | type | description | required |
| ---- | ---- | ----------- | -------- |
| cluster_id | string | The cluster to be deregistered. | True |

**EXAMPLES**

    import redhat_assisted_installer.assistedinstaller as assistedinstaller

    installer = assistedinstaller.assistedinstaller()

    # get cluster by id
    clusters = installer.getClusters(cluster_id=<cluster_id>)

    # return object is an array, so we can safely delete any clusters with that id by using a for loop
    for cluster in clusters:
        installer.deleteCluster(cluster['id'])


#### /v2/infra-envs

**GET**

Retrieves the list of infra-envs.

Query Parameters

| name | type | description | required |
| ---- | ---- | ----------- | -------- |
| cluster_id | string | returns only infra-envs which directly reference this cluster. | False |
| owner | string | returns only clusters that are owned by the specified user. | False |


**EXAMPLES**

    import redhat_assisted_installer.assistedinstaller as assistedinstaller

    installer = assistedinstaller.assistedinstaller()
    # get all infra-envs registered to this account
    infra_envs = installer.getInfrastructureEnvironments()

    # get all infra-envs registered to this account
    infra_envs = installer.getInfrastructureEnvironments()

    # get all infra-envs that directly reference cluster_id
    infra_env = installer.getInfrastructureEnvironments(cluster_id=<cluster_id>)


**POST**

Creates a new OpenShift Discovery ISO.

Body Parameters

| name | type | description | required | 
| ---- | ---- | ----------- | -------- | 
| name | string | Name of cluster definition. | True |
| version | string | OpenShift version to use. | False | 
| cluster_id | string | The cluster this infra-env will reference | False | 
| cpuarchitecture | string  | The cpu arch of the baremetal hardware this cluster will run on | False |

**EXAMPLES**

    import redhat_assisted_installer.assistedinstaller as assistedinstaller

    installer = assistedinstaller.assistedinstaller()

    # create min infra-env
    installer.postInfrastructureEnvironment(name="testing-infra")


#### /v2/infra-envs/{infra-env-id}

**DELETE**

Deletes an infra-env.

Path Parameters

| name | type | description | required |
| ---- | ---- | ----------- | -------- |
| infra_env_id | string | The infra-env to be deleted. | True |

**EXAMPLES**

    import redhat_assisted_installer.assistedinstaller as assistedinstaller

    installer = assistedinstaller.assistedinstaller()

    # get all infra-envs registered to this account
    infras = installer.getInfrastructureEnvironments()

    # return object is an array, so we can safely delete any infra-envs with that id by using a for loop
    for infra in infras:
        installer.deleteInfrastructureEnvironment(infra['id'])


## References

- [RedHat Assisted Installer API | Docs](https://developers.redhat.com/api-catalog/api/assisted-install-service#content-operations).

- [RedHat Hybrid Cloud | Console](https://console.redhat.com/)