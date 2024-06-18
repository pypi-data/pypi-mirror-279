'''
# Azure Kubernetes Service (AKS) Construct

This documentation details the Azure Kubernetes Service (AKS) Construct, a specialized class designed to simplify the deployment and management of AKS clusters in Azure. It encapsulates the complexities of AKS configuration into an easy-to-use construct, making it straightforward to create and manage Kubernetes clusters.

## What is Azure Kubernetes Service (AKS)?

Azure Kubernetes Service (AKS) is a managed container orchestration service, based on Kubernetes, that facilitates the deployment, management, and scaling of containerized applications on Azure. It eliminates the complexity of handling the Kubernetes infrastructure, providing users with a serverless Kubernetes, an integrated continuous integration and continuous delivery (CI/CD) experience, and enterprise-grade security and governance.

Learn more about AKS in the official Azure documentation.

## Best Practices for AKS

* **Node Pool Management**: Utilize multiple node pools to separate workloads and manage them efficiently.
* **Security and Identity**: Leverage Azure Active Directory (AAD) integration for AKS to manage user access and maintain security.
* **Monitoring and Diagnostics**: Implement Azure Monitor for containers to gain insights into your AKS clusters and workloads.
* **Cost Management**: Use Azure Advisor to optimize your AKS cluster's performance and manage costs effectively.

## AKS Class Properties

The class offers numerous properties for tailoring the AKS cluster:

* **name**: The unique name of the AKS cluster.
* **location**: The Azure region where the AKS cluster will be deployed.
* **resourceGroup**: The Azure Resource Group that the AKS cluster belongs to.
* **defaultNodePool**: Configuration for the default node pool, including size, type, and other settings.
* **identity**: Specifies the identity used for the AKS cluster, such as SystemAssigned or UserAssigned.
* **tags**: Key-value pairs for resource tagging and categorization.

## Deploying the AKS Cluster

```python
const myAKSCluster = new Cluster(this, 'myAKSCluster', {
  name: 'myCluster',
  location: 'East US',
  defaultNodePool: {
    name: "default",
    nodeCount: 3,
    vmSize: "Standard_DS2_v2",
  },
  resourceGroup: myResourceGroup,
  identity: {
    type: "SystemAssigned",
  },
  // Additional properties
});
```

This code snippet demonstrates how to create a new AKS cluster with specified properties, including the setup of a default node pool.

## Setting Up a Resource Group

If a resource group is not specified, the construct will automatically create one based on the AKS cluster's name and location. This is handled within the setupResourceGroup method, ensuring that the AKS cluster is associated with a resource group, either existing or newly created.

## Integrating with Azure Active Directory (AAD)

For enhanced security, integrate AKS with Azure Active Directory (AAD) for authentication and authorization. This can be specified in the identity property of the AKS class.

## Monitoring and Management

Leverage Azure Monitor and Azure Policy to monitor the health and performance of your AKS cluster and enforce organizational policies. These services help maintain the security and compliance of your Kubernetes applications.

By using this AKS Construct, developers can more efficiently manage Kubernetes clusters in Azure, benefiting from the scalability, reliability, and security features of AKS. This construct abstracts away the complexity, making it easier to deploy and operate Kubernetes workloads in the cloud.
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *

import cdktf_cdktf_provider_azurerm.kubernetes_cluster as _cdktf_cdktf_provider_azurerm_kubernetes_cluster_92bbcedf
import cdktf_cdktf_provider_azurerm.resource_group as _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf
import constructs as _constructs_77d1e7e8
from ..core_azure import AzureResource as _AzureResource_74eec1c4


class Cluster(
    _AzureResource_74eec1c4,
    metaclass=jsii.JSIIMeta,
    jsii_type="@microsoft/terraform-cdk-constructs.azure_kubernetes.Cluster",
):
    '''Class representing the AKS cluster resource.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        default_node_pool: typing.Union[_cdktf_cdktf_provider_azurerm_kubernetes_cluster_92bbcedf.KubernetesClusterDefaultNodePool, typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        api_server_authorized_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        azure_active_directory_role_based_access_control: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_kubernetes_cluster_92bbcedf.KubernetesClusterAzureActiveDirectoryRoleBasedAccessControl, typing.Dict[builtins.str, typing.Any]]] = None,
        identity: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_kubernetes_cluster_92bbcedf.KubernetesClusterIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
        resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Represents an Azure Kubernetes Service (AKS) cluster resource in Azure.

        This class is responsible for the creation and management of an AKS cluster, allowing for the deployment and orchestration
        of containerized applications using Kubernetes within the Azure cloud platform.

        :param scope: - The scope in which to define this construct, typically representing the Cloud Development Kit (CDK) stack.
        :param id: - The unique identifier for this instance of the AKS cluster.
        :param default_node_pool: Configuration for the default node pool of the AKS cluster.
        :param location: The Azure region where the AKS cluster will be deployed.
        :param name: The name of the AKS cluster. Must be unique within the Azure region.
        :param api_server_authorized_ip_ranges: A list of IP address ranges that are authorized to access the AKS API server. This enhances the security of your cluster by ensuring that only traffic from these IP ranges can communicate with the Kubernetes API server. Specifying this list helps to protect your cluster from unauthorized access attempts. It's a critical security measure for clusters that are exposed to the internet. If you specify an empty array, no IP addresses will be allowed to access the API server, effectively blocking all access. If this property is not defined, all IP addresses are allowed by default, which is not recommended for production environments. Example: apiServerAuthorizedIpRanges: ['203.0.113.0/24', '198.51.100.0/24'] It's important to configure this property carefully, based on your organization's network policies and access requirements.
        :param azure_active_directory_role_based_access_control: Configures integration of Azure Active Directory (AAD) with Kubernetes Role-Based Access Control (RBAC) for the AKS cluster. This feature enables the use of AAD to manage user and group access permissions to the Kubernetes cluster resources, leveraging AAD's robust identity and access management capabilities. Utilizing AAD with Kubernetes RBAC provides: - Enhanced security through AAD's identity protection features. - Simplified user and group management by leveraging existing AAD definitions. - Streamlined access control for Kubernetes resources, allowing for the definition of roles and role bindings based on AAD identities. This property is optional but highly recommended for clusters where security and access governance are a priority. It allows for finer-grained access control and integrates the cluster's authentication and authorization processes with corporate identity management systems. Example configuration might include specifying the AAD tenant details, enabling Azure RBAC for Kubernetes authorization, and optionally defining specific AAD groups for cluster admin roles.
        :param identity: The identity used for the AKS cluster. Can be either SystemAssigned or UserAssigned. Optional.
        :param resource_group: The Azure Resource Group where the AKS cluster will be deployed. Optional. If not provided, a new resource group will be created.
        :param tags: Tags to be applied to the AKS cluster resources for organizational purposes. Key-value pairs. Optional.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6b77c9c195f92f6162e6aea4254e8f0f8e70d38a830c7d18363eb25079b709e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ClusterProps(
            default_node_pool=default_node_pool,
            location=location,
            name=name,
            api_server_authorized_ip_ranges=api_server_authorized_ip_ranges,
            azure_active_directory_role_based_access_control=azure_active_directory_role_based_access_control,
            identity=identity,
            resource_group=resource_group,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''The unique identifier of the AKS cluster resource.'''
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f9dd7483ce17741f78c42ef8a805c73d4067ad671051e85a0fa94f6bd7ab3c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="resourceGroup")
    def resource_group(
        self,
    ) -> _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup:
        '''The Resource Group associated with the AKS cluster.'''
        return typing.cast(_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup, jsii.get(self, "resourceGroup"))

    @resource_group.setter
    def resource_group(
        self,
        value: _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1b786454b7f043135b451fd7668fc137f16801e24c654bc75aa7933876273f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroup", value)


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_kubernetes.ClusterProps",
    jsii_struct_bases=[],
    name_mapping={
        "default_node_pool": "defaultNodePool",
        "location": "location",
        "name": "name",
        "api_server_authorized_ip_ranges": "apiServerAuthorizedIpRanges",
        "azure_active_directory_role_based_access_control": "azureActiveDirectoryRoleBasedAccessControl",
        "identity": "identity",
        "resource_group": "resourceGroup",
        "tags": "tags",
    },
)
class ClusterProps:
    def __init__(
        self,
        *,
        default_node_pool: typing.Union[_cdktf_cdktf_provider_azurerm_kubernetes_cluster_92bbcedf.KubernetesClusterDefaultNodePool, typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        api_server_authorized_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        azure_active_directory_role_based_access_control: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_kubernetes_cluster_92bbcedf.KubernetesClusterAzureActiveDirectoryRoleBasedAccessControl, typing.Dict[builtins.str, typing.Any]]] = None,
        identity: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_kubernetes_cluster_92bbcedf.KubernetesClusterIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
        resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Interface defining the properties required to create an AKS cluster.

        :param default_node_pool: Configuration for the default node pool of the AKS cluster.
        :param location: The Azure region where the AKS cluster will be deployed.
        :param name: The name of the AKS cluster. Must be unique within the Azure region.
        :param api_server_authorized_ip_ranges: A list of IP address ranges that are authorized to access the AKS API server. This enhances the security of your cluster by ensuring that only traffic from these IP ranges can communicate with the Kubernetes API server. Specifying this list helps to protect your cluster from unauthorized access attempts. It's a critical security measure for clusters that are exposed to the internet. If you specify an empty array, no IP addresses will be allowed to access the API server, effectively blocking all access. If this property is not defined, all IP addresses are allowed by default, which is not recommended for production environments. Example: apiServerAuthorizedIpRanges: ['203.0.113.0/24', '198.51.100.0/24'] It's important to configure this property carefully, based on your organization's network policies and access requirements.
        :param azure_active_directory_role_based_access_control: Configures integration of Azure Active Directory (AAD) with Kubernetes Role-Based Access Control (RBAC) for the AKS cluster. This feature enables the use of AAD to manage user and group access permissions to the Kubernetes cluster resources, leveraging AAD's robust identity and access management capabilities. Utilizing AAD with Kubernetes RBAC provides: - Enhanced security through AAD's identity protection features. - Simplified user and group management by leveraging existing AAD definitions. - Streamlined access control for Kubernetes resources, allowing for the definition of roles and role bindings based on AAD identities. This property is optional but highly recommended for clusters where security and access governance are a priority. It allows for finer-grained access control and integrates the cluster's authentication and authorization processes with corporate identity management systems. Example configuration might include specifying the AAD tenant details, enabling Azure RBAC for Kubernetes authorization, and optionally defining specific AAD groups for cluster admin roles.
        :param identity: The identity used for the AKS cluster. Can be either SystemAssigned or UserAssigned. Optional.
        :param resource_group: The Azure Resource Group where the AKS cluster will be deployed. Optional. If not provided, a new resource group will be created.
        :param tags: Tags to be applied to the AKS cluster resources for organizational purposes. Key-value pairs. Optional.
        '''
        if isinstance(default_node_pool, dict):
            default_node_pool = _cdktf_cdktf_provider_azurerm_kubernetes_cluster_92bbcedf.KubernetesClusterDefaultNodePool(**default_node_pool)
        if isinstance(azure_active_directory_role_based_access_control, dict):
            azure_active_directory_role_based_access_control = _cdktf_cdktf_provider_azurerm_kubernetes_cluster_92bbcedf.KubernetesClusterAzureActiveDirectoryRoleBasedAccessControl(**azure_active_directory_role_based_access_control)
        if isinstance(identity, dict):
            identity = _cdktf_cdktf_provider_azurerm_kubernetes_cluster_92bbcedf.KubernetesClusterIdentity(**identity)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dcfbe3e3bbbed5a4eec60aa68b388884bb7f833bc1d27e64e538b3ca65ba191)
            check_type(argname="argument default_node_pool", value=default_node_pool, expected_type=type_hints["default_node_pool"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument api_server_authorized_ip_ranges", value=api_server_authorized_ip_ranges, expected_type=type_hints["api_server_authorized_ip_ranges"])
            check_type(argname="argument azure_active_directory_role_based_access_control", value=azure_active_directory_role_based_access_control, expected_type=type_hints["azure_active_directory_role_based_access_control"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument resource_group", value=resource_group, expected_type=type_hints["resource_group"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_node_pool": default_node_pool,
            "location": location,
            "name": name,
        }
        if api_server_authorized_ip_ranges is not None:
            self._values["api_server_authorized_ip_ranges"] = api_server_authorized_ip_ranges
        if azure_active_directory_role_based_access_control is not None:
            self._values["azure_active_directory_role_based_access_control"] = azure_active_directory_role_based_access_control
        if identity is not None:
            self._values["identity"] = identity
        if resource_group is not None:
            self._values["resource_group"] = resource_group
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def default_node_pool(
        self,
    ) -> _cdktf_cdktf_provider_azurerm_kubernetes_cluster_92bbcedf.KubernetesClusterDefaultNodePool:
        '''Configuration for the default node pool of the AKS cluster.'''
        result = self._values.get("default_node_pool")
        assert result is not None, "Required property 'default_node_pool' is missing"
        return typing.cast(_cdktf_cdktf_provider_azurerm_kubernetes_cluster_92bbcedf.KubernetesClusterDefaultNodePool, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The Azure region where the AKS cluster will be deployed.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the AKS cluster.

        Must be unique within the Azure region.
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_server_authorized_ip_ranges(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of IP address ranges that are authorized to access the AKS API server.

        This enhances the security of your cluster by ensuring that only traffic from these IP ranges can communicate with the Kubernetes API server.

        Specifying this list helps to protect your cluster from unauthorized access attempts. It's a critical security measure for clusters that are exposed to the internet. If you specify an empty array, no IP addresses will be allowed to access the API server, effectively blocking all access. If this property is not defined, all IP addresses are allowed by default, which is not recommended for production environments.

        Example:
        apiServerAuthorizedIpRanges: ['203.0.113.0/24', '198.51.100.0/24']

        It's important to configure this property carefully, based on your organization's network policies and access requirements.
        '''
        result = self._values.get("api_server_authorized_ip_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def azure_active_directory_role_based_access_control(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_kubernetes_cluster_92bbcedf.KubernetesClusterAzureActiveDirectoryRoleBasedAccessControl]:
        '''Configures integration of Azure Active Directory (AAD) with Kubernetes Role-Based Access Control (RBAC) for the AKS cluster.

        This feature enables the use of AAD to manage user and group access permissions to the Kubernetes cluster resources, leveraging AAD's robust identity and access management capabilities.

        Utilizing AAD with Kubernetes RBAC provides:

        - Enhanced security through AAD's identity protection features.
        - Simplified user and group management by leveraging existing AAD definitions.
        - Streamlined access control for Kubernetes resources, allowing for the definition of roles and role bindings based on AAD identities.

        This property is optional but highly recommended for clusters where security and access governance are a priority. It allows for finer-grained access control and integrates the cluster's authentication and authorization processes with corporate identity management systems.

        Example configuration might include specifying the AAD tenant details, enabling Azure RBAC for Kubernetes authorization, and optionally defining specific AAD groups for cluster admin roles.
        '''
        result = self._values.get("azure_active_directory_role_based_access_control")
        return typing.cast(typing.Optional[_cdktf_cdktf_provider_azurerm_kubernetes_cluster_92bbcedf.KubernetesClusterAzureActiveDirectoryRoleBasedAccessControl], result)

    @builtins.property
    def identity(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_kubernetes_cluster_92bbcedf.KubernetesClusterIdentity]:
        '''The identity used for the AKS cluster.

        Can be either SystemAssigned or UserAssigned.
        Optional.
        '''
        result = self._values.get("identity")
        return typing.cast(typing.Optional[_cdktf_cdktf_provider_azurerm_kubernetes_cluster_92bbcedf.KubernetesClusterIdentity], result)

    @builtins.property
    def resource_group(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup]:
        '''The Azure Resource Group where the AKS cluster will be deployed.

        Optional. If not provided, a new resource group will be created.
        '''
        result = self._values.get("resource_group")
        return typing.cast(typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Tags to be applied to the AKS cluster resources for organizational purposes.

        Key-value pairs. Optional.
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClusterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Cluster",
    "ClusterProps",
]

publication.publish()

def _typecheckingstub__a6b77c9c195f92f6162e6aea4254e8f0f8e70d38a830c7d18363eb25079b709e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    default_node_pool: typing.Union[_cdktf_cdktf_provider_azurerm_kubernetes_cluster_92bbcedf.KubernetesClusterDefaultNodePool, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    api_server_authorized_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    azure_active_directory_role_based_access_control: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_kubernetes_cluster_92bbcedf.KubernetesClusterAzureActiveDirectoryRoleBasedAccessControl, typing.Dict[builtins.str, typing.Any]]] = None,
    identity: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_kubernetes_cluster_92bbcedf.KubernetesClusterIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f9dd7483ce17741f78c42ef8a805c73d4067ad671051e85a0fa94f6bd7ab3c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1b786454b7f043135b451fd7668fc137f16801e24c654bc75aa7933876273f6(
    value: _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dcfbe3e3bbbed5a4eec60aa68b388884bb7f833bc1d27e64e538b3ca65ba191(
    *,
    default_node_pool: typing.Union[_cdktf_cdktf_provider_azurerm_kubernetes_cluster_92bbcedf.KubernetesClusterDefaultNodePool, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    api_server_authorized_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    azure_active_directory_role_based_access_control: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_kubernetes_cluster_92bbcedf.KubernetesClusterAzureActiveDirectoryRoleBasedAccessControl, typing.Dict[builtins.str, typing.Any]]] = None,
    identity: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_kubernetes_cluster_92bbcedf.KubernetesClusterIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
