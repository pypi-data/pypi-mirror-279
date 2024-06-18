'''
# Azure Container Registry Construct

This class represents an Azure Container Registry resource. It provides a way to manage Azure Container Registry resources conveniently.

## What is Azure Container Registry?

Azure Container Registry is a managed Docker registry service for building, storing, and managing container images and artifacts in a secure, scalable way. Azure Container Registry integrates well with orchestrators hosted in Azure Container Service, including Docker Swarm, Kubernetes, and DC/OS, as well as other Azure Services such as Service Fabric and Batch.

You can learn more about Azure Container Registry in the [official Azure documentation](https://docs.microsoft.com/en-us/azure/container-registry/container-registry-intro).

## Container Registry Best Practices

* Enable the admin account only when necessary and disable it when not in use.
* Use role-based access control (RBAC) to manage access to your Azure Container Registry.
* Regularly remove untagged and unused images to manage costs.

## Container Registry Class Properties

This class has several properties that control the Azure Container Registry resource's behaviour:

* `name`: The name of the Azure Container Registry.
* `location`: The Azure Region where the Azure Container Registry will be deployed.
* `resource_group_name`: The name of the Azure Resource Group.
* `sku`: The SKU of the Azure Container Registry.
* `tags`: The tags to assign to the Azure Container Registry.
* `admin_enabled`: A flag to specify whether the admin account is enabled.
* `georeplication_locations`: The locations to configure replication.

## Deploying the Azure Container Registry

You can deploy an Azure Container Registry resource using this class like so:

```python
const azureContainerRegistry = new AzureContainerRegistry(this, 'myContainerRegistry', {
  name: 'myContainerRegistry',
  location: 'West US',
  resource_group_name: 'myResourceGroup',
  sku: 'Premium',
  admin_enabled: true,
  georeplication_locations: ['East US', 'West Europe'],
  tags: {
    'env': 'production',
  },
});
```

This code will create a new Azure Container Registry named myContainerRegistry in the West US Azure region with a production environment tag. The resource belongs to the resource group myResourceGroup, has a Premium SKU, has the admin account enabled, and has geo-replication configured for East US and West Europe.
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

import cdktf_cdktf_provider_azurerm.resource_group as _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf
import constructs as _constructs_77d1e7e8
from ..core_azure import AzureResource as _AzureResource_74eec1c4


class Registry(
    _AzureResource_74eec1c4,
    metaclass=jsii.JSIIMeta,
    jsii_type="@microsoft/terraform-cdk-constructs.azure_containerregistry.Registry",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        admin_enabled: typing.Optional[builtins.bool] = None,
        geo_replication_locations: typing.Any = None,
        resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
        sku: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Constructs a new Azure Container Registry (ACR).

        This class creates an Azure Container Registry instance, which is a managed Docker registry service based on the Docker Registry 2.0 specification.
        This service enables you to store and manage container images across all types of Azure deployments, you can also use it to build, store, and manage images for all types of container deployments.

        :param scope: - The scope in which to define this construct, typically used for managing lifecycles and creation order.
        :param id: - The unique identifier for this construct instance.
        :param location: The Azure Region to deploy.
        :param name: The name of the Log Analytics Workspace.
        :param admin_enabled: Create enable Admin user.
        :param geo_replication_locations: Specify the locations to configure replication.
        :param resource_group: An optional reference to the resource group in which to deploy the Container Registry. If not provided, the Container Registry will be deployed in the default resource group.
        :param sku: The SKU of the Log Analytics Workspace.
        :param tags: The tags to assign to the Resource Group.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81457a31f7f2d2aeac8d8265e400e9e6cb61061a3702b9ef376cf6ecb3480e27)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = RegistryProps(
            location=location,
            name=name,
            admin_enabled=admin_enabled,
            geo_replication_locations=geo_replication_locations,
            resource_group=resource_group,
            sku=sku,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "RegistryProps":
        return typing.cast("RegistryProps", jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__facce4d6c62bd4e2d136615b79863636281c9a8d5602ca316304ef73ba43976f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="resourceGroup")
    def resource_group(
        self,
    ) -> _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup:
        return typing.cast(_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup, jsii.get(self, "resourceGroup"))

    @resource_group.setter
    def resource_group(
        self,
        value: _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3116fb173101c7b2d4633824ed00b65e3fb1f8c3a4f24b05dd435912538f57c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroup", value)


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_containerregistry.RegistryProps",
    jsii_struct_bases=[],
    name_mapping={
        "location": "location",
        "name": "name",
        "admin_enabled": "adminEnabled",
        "geo_replication_locations": "geoReplicationLocations",
        "resource_group": "resourceGroup",
        "sku": "sku",
        "tags": "tags",
    },
)
class RegistryProps:
    def __init__(
        self,
        *,
        location: builtins.str,
        name: builtins.str,
        admin_enabled: typing.Optional[builtins.bool] = None,
        geo_replication_locations: typing.Any = None,
        resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
        sku: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param location: The Azure Region to deploy.
        :param name: The name of the Log Analytics Workspace.
        :param admin_enabled: Create enable Admin user.
        :param geo_replication_locations: Specify the locations to configure replication.
        :param resource_group: An optional reference to the resource group in which to deploy the Container Registry. If not provided, the Container Registry will be deployed in the default resource group.
        :param sku: The SKU of the Log Analytics Workspace.
        :param tags: The tags to assign to the Resource Group.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcfdb54f0864825a579ba05e543e9dc9d1ac37714adaf9563ca40bb3353d14cd)
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument admin_enabled", value=admin_enabled, expected_type=type_hints["admin_enabled"])
            check_type(argname="argument geo_replication_locations", value=geo_replication_locations, expected_type=type_hints["geo_replication_locations"])
            check_type(argname="argument resource_group", value=resource_group, expected_type=type_hints["resource_group"])
            check_type(argname="argument sku", value=sku, expected_type=type_hints["sku"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "name": name,
        }
        if admin_enabled is not None:
            self._values["admin_enabled"] = admin_enabled
        if geo_replication_locations is not None:
            self._values["geo_replication_locations"] = geo_replication_locations
        if resource_group is not None:
            self._values["resource_group"] = resource_group
        if sku is not None:
            self._values["sku"] = sku
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def location(self) -> builtins.str:
        '''The Azure Region to deploy.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the Log Analytics Workspace.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def admin_enabled(self) -> typing.Optional[builtins.bool]:
        '''Create enable Admin user.'''
        result = self._values.get("admin_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def geo_replication_locations(self) -> typing.Any:
        '''Specify the locations to configure replication.'''
        result = self._values.get("geo_replication_locations")
        return typing.cast(typing.Any, result)

    @builtins.property
    def resource_group(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup]:
        '''An optional reference to the resource group in which to deploy the Container Registry.

        If not provided, the Container Registry will be deployed in the default resource group.
        '''
        result = self._values.get("resource_group")
        return typing.cast(typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup], result)

    @builtins.property
    def sku(self) -> typing.Optional[builtins.str]:
        '''The SKU of the Log Analytics Workspace.'''
        result = self._values.get("sku")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The tags to assign to the Resource Group.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RegistryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Registry",
    "RegistryProps",
]

publication.publish()

def _typecheckingstub__81457a31f7f2d2aeac8d8265e400e9e6cb61061a3702b9ef376cf6ecb3480e27(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    admin_enabled: typing.Optional[builtins.bool] = None,
    geo_replication_locations: typing.Any = None,
    resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
    sku: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__facce4d6c62bd4e2d136615b79863636281c9a8d5602ca316304ef73ba43976f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3116fb173101c7b2d4633824ed00b65e3fb1f8c3a4f24b05dd435912538f57c(
    value: _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcfdb54f0864825a579ba05e543e9dc9d1ac37714adaf9563ca40bb3353d14cd(
    *,
    location: builtins.str,
    name: builtins.str,
    admin_enabled: typing.Optional[builtins.bool] = None,
    geo_replication_locations: typing.Any = None,
    resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
    sku: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
