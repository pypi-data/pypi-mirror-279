'''
# Azure Resource Group Construct

This Construct represents a Resource Group in Azure. It provides a convenient way to manage Azure resources within a single group.

## What is a Resource Group?

In Azure, a Resource Group is a container that holds related resources for an Azure solution. It's a logical group for resources deployed on Azure. All the resources in a group should have the same lifecycle and the same permissions, which makes it easier to manage, monitor, and analyze collectively.

You can learn more about Resource Groups in the [official Azure documentation](https://docs.microsoft.com/en-us/azure/azure-resource-manager/management/manage-resource-groups-portal).

## Resource Group Best Practices

* Use a consistent naming convention for your resource groups and other Azure resources.
* Group resources that share the same lifecycle and permissions.
* Avoid putting too many resources in a single group. If one resource experiences an issue, it may be harder to diagnose the problem if it's in a group with many other resources.
* Use resource groups to separate resources that are managed by different teams.

## Azure Resource Group Construct Properties

This Construct has several properties that control the Resource Group's behaviour:

* `location`: The Azure Region where the Resource Group will be deployed.
* `name`: The name of the Azure Resource Group.
* `rbacGroups`: The RBAC groups to assign to the Resource Group.
* `tags`: The tags to assign to the Resource Group.
* `ignoreChanges`: The lifecycle rules to ignore changes.

## Deploying the Resource Group

You can deploy a Resource Group using this Construct like so:

```python
const azureResourceGroup = new AzureResourceGroup(this, 'myResourceGroup', {
  location: 'West US',
  name: 'myResourceGroup',
  tags: {
    'env': 'production',
  },
});
```
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

import cdktf as _cdktf_9a9027ec
import cdktf_cdktf_provider_azurerm.resource_group as _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf
import constructs as _constructs_77d1e7e8
from ..core_azure import AzureResource as _AzureResource_74eec1c4


class Group(
    _AzureResource_74eec1c4,
    metaclass=jsii.JSIIMeta,
    jsii_type="@microsoft/terraform-cdk-constructs.azure_resourcegroup.Group",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        ignore_changes: typing.Optional[typing.Sequence[builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Represents an Azure Resource Group.

        This class is responsible for the creation and management of an Azure Resource Group, which is a container that holds
        related resources for an Azure solution. A resource group includes those resources that you want to manage as a group.
        You decide how to allocate resources to resource groups based on what makes the most sense for your organization.

        :param scope: - The scope in which to define this construct, typically representing the Cloud Development Kit (CDK) stack.
        :param id: - The unique identifier for this instance of the Resource Group.
        :param ignore_changes: The lifecycle rules to ignore changes.
        :param location: The Azure Region to deploy.
        :param name: The name of the Azure Resource Group.
        :param tags: The tags to assign to the Resource Group.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28366b9cbb85cc322b3ef2755d7f96dae164903b33f2dcc65ba007c860e5b4d1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GroupProps(
            ignore_changes=ignore_changes, location=location, name=name, tags=tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "GroupProps":
        return typing.cast("GroupProps", jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__863a91908c470e9a72b0c809f3d8826895c52dfe6ccf6a11ecbea4984575fb57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="idOutput")
    def id_output(self) -> _cdktf_9a9027ec.TerraformOutput:
        return typing.cast(_cdktf_9a9027ec.TerraformOutput, jsii.get(self, "idOutput"))

    @id_output.setter
    def id_output(self, value: _cdktf_9a9027ec.TerraformOutput) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8be16f4160ff2bf3fd5b0cde5c96a5dff9cfa2ecda217c5398e648ff6ec0a5e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idOutput", value)

    @builtins.property
    @jsii.member(jsii_name="locationOutput")
    def location_output(self) -> _cdktf_9a9027ec.TerraformOutput:
        return typing.cast(_cdktf_9a9027ec.TerraformOutput, jsii.get(self, "locationOutput"))

    @location_output.setter
    def location_output(self, value: _cdktf_9a9027ec.TerraformOutput) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__757de5ae0a79f96e9ff422bf2771a4bfd85b5557abcd73d71e0d4697dc320d1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locationOutput", value)

    @builtins.property
    @jsii.member(jsii_name="nameOutput")
    def name_output(self) -> _cdktf_9a9027ec.TerraformOutput:
        return typing.cast(_cdktf_9a9027ec.TerraformOutput, jsii.get(self, "nameOutput"))

    @name_output.setter
    def name_output(self, value: _cdktf_9a9027ec.TerraformOutput) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d26b71fe6df2495c6c302da681e1f6f0f2812cd859898a81a37b18f19a45878a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nameOutput", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__57416344b94a6578833c6453e4ec9c1939e1182fbd79e966a4bdb6477a07512e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroup", value)


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_resourcegroup.GroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "ignore_changes": "ignoreChanges",
        "location": "location",
        "name": "name",
        "tags": "tags",
    },
)
class GroupProps:
    def __init__(
        self,
        *,
        ignore_changes: typing.Optional[typing.Sequence[builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for the resource group.

        :param ignore_changes: The lifecycle rules to ignore changes.
        :param location: The Azure Region to deploy.
        :param name: The name of the Azure Resource Group.
        :param tags: The tags to assign to the Resource Group.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cf28a39ce41ce37b370b8d109f1e2b60b50663e19393f14d4459cd453d5bb4d)
            check_type(argname="argument ignore_changes", value=ignore_changes, expected_type=type_hints["ignore_changes"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ignore_changes is not None:
            self._values["ignore_changes"] = ignore_changes
        if location is not None:
            self._values["location"] = location
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def ignore_changes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The lifecycle rules to ignore changes.'''
        result = self._values.get("ignore_changes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The Azure Region to deploy.'''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the Azure Resource Group.'''
        result = self._values.get("name")
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
        return "GroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Group",
    "GroupProps",
]

publication.publish()

def _typecheckingstub__28366b9cbb85cc322b3ef2755d7f96dae164903b33f2dcc65ba007c860e5b4d1(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    ignore_changes: typing.Optional[typing.Sequence[builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__863a91908c470e9a72b0c809f3d8826895c52dfe6ccf6a11ecbea4984575fb57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8be16f4160ff2bf3fd5b0cde5c96a5dff9cfa2ecda217c5398e648ff6ec0a5e9(
    value: _cdktf_9a9027ec.TerraformOutput,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__757de5ae0a79f96e9ff422bf2771a4bfd85b5557abcd73d71e0d4697dc320d1e(
    value: _cdktf_9a9027ec.TerraformOutput,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d26b71fe6df2495c6c302da681e1f6f0f2812cd859898a81a37b18f19a45878a(
    value: _cdktf_9a9027ec.TerraformOutput,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57416344b94a6578833c6453e4ec9c1939e1182fbd79e966a4bdb6477a07512e(
    value: _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cf28a39ce41ce37b370b8d109f1e2b60b50663e19393f14d4459cd453d5bb4d(
    *,
    ignore_changes: typing.Optional[typing.Sequence[builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
