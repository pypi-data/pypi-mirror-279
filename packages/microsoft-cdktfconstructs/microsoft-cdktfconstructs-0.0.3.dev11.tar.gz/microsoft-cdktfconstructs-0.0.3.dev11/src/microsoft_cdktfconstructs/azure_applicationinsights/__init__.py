'''
# Azure Application Insights Construct

This class represents an Application Insights resource in Azure. It provides a convenient way to manage Azure Application Insights resources.

## What is Azure Application Insights?

Azure Application Insights is an extensible Application Performance Management (APM) service for developers and DevOps professionals. Use it to monitor your live applications. It automatically detects performance anomalies, and includes powerful analytics tools to help you diagnose issues and to understand what users actually do with your app.

You can learn more about Azure Application Insights in the [official Azure documentation](https://docs.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview).

## Application Insights Best Practices

* Enable Application Insights during development and use it for all environments, including production.
* Use multiple Application Insights resources for different environments and use Azure resource tags to filter and identify them.
* Leverage the data retention policy to retain data according to your requirements.

## Application Insights Class Properties

This class has several properties that control the Application Insights resource's behaviour:

* `name`: The name of the Application Insights resource.
* `location`: The Azure Region where the Application Insights resource will be deployed.
* `resource_group_name`: The name of the Azure Resource Group.
* `retention_in_days`: The number of days of retention.
* `tags`: The tags to assign to the Application Insights resource.
* `application_type`: The Application type.
* `daily_data_cap_in_gb`: The Application Insights daily data cap in GB.
* `daily_data_cap_notification_disabled`: The Application Insights daily data cap notifications disabled.
* `workspace_id`: The id of the Log Analytics Workspace.

## Deploying the Application Insights

You can deploy an Application Insights resource using this class like so:

```python
const azureAppInsights = new AzureApplicationInsights(this, 'myAppInsights', {
  name: 'myAppInsights',
  location: 'West US',
  resource_group_name: 'myResourceGroup',
  application_type: 'web',
  daily_data_cap_in_gb: 10,
  daily_data_cap_notification_disabled: false,
  retention_in_days: 90,
  workspace_id: 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx',
  tags: {
    'env': 'production',
  },
});
```

This code will create a new Application Insights resource named myAppInsights in the West US Azure region with a production environment tag. The resource belongs to the resource group myResourceGroup, it has a daily data cap of 10 GB, sends notifications when the daily data cap is reached, retains data for 90 days, and uses the provided workspace ID.
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


class AppInsights(
    _AzureResource_74eec1c4,
    metaclass=jsii.JSIIMeta,
    jsii_type="@microsoft/terraform-cdk-constructs.azure_applicationinsights.AppInsights",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        application_type: builtins.str,
        location: builtins.str,
        name: builtins.str,
        daily_data_cap_in_gb: typing.Optional[jsii.Number] = None,
        daily_data_cap_notification_disabled: typing.Optional[builtins.bool] = None,
        resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
        retention_in_days: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        workspace_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Constructs a new Azure Application Insights resource.

        :param scope: - The scope in which to define this construct.
        :param id: - The ID of this construct.
        :param application_type: The Application type.
        :param location: The Azure Region to deploy.
        :param name: The name of the Application Insights resource.
        :param daily_data_cap_in_gb: The Application Insights daily data cap in GB.
        :param daily_data_cap_notification_disabled: The Application Insights daily data cap notifications disabled.
        :param resource_group: An optional reference to the resource group in which to deploy the Application Insights. If not provided, the Application Insights will be deployed in the default resource group.
        :param retention_in_days: The number of days of retention. Possible values are 30, 60, 90, 120, 180, 270, 365, 550 or 730. Defaults to 90. Default: 90
        :param tags: The tags to assign to the Application Insights resource.
        :param workspace_id: The id of the Log Analytics Workspace. Default: - If no workspace id is provided, a new one will be created automatically in the same resource group. The name will be the same as the Application Insights resource with a "-la" suffix.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d4b8c71ca92596f9110e479740b5f222f59c2481e089dc27fe01d85d3ddfb96)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AppInsightsProps(
            application_type=application_type,
            location=location,
            name=name,
            daily_data_cap_in_gb=daily_data_cap_in_gb,
            daily_data_cap_notification_disabled=daily_data_cap_notification_disabled,
            resource_group=resource_group,
            retention_in_days=retention_in_days,
            tags=tags,
            workspace_id=workspace_id,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="saveIKeyToKeyVault")
    def save_i_key_to_key_vault(
        self,
        key_vault_id: builtins.str,
        key_vault_secret_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Saves the Application Insights instrumentation key to an Azure Key Vault.

        This method creates a new secret in the specified Azure Key Vault with the
        instrumentation key of the Application Insights resource. This enables secure storage
        and management of the instrumentation key, facilitating secure access across various
        Azure services.

        :param key_vault_id: - The unique identifier of the Azure Key Vault where the secret will be stored.
        :param key_vault_secret_name: - The name of the secret within the Key Vault. Defaults to 'instrumentation-key'. This name can be used to retrieve the secret in client applications. Example usage:: appInsightsInstance.saveIKeyToKeyVault('my-key-vault-id');
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ab25147fd544a8a1c78f6c8c150e0eea1424fbb238afb85b75d0a9ecde637ad)
            check_type(argname="argument key_vault_id", value=key_vault_id, expected_type=type_hints["key_vault_id"])
            check_type(argname="argument key_vault_secret_name", value=key_vault_secret_name, expected_type=type_hints["key_vault_secret_name"])
        return typing.cast(None, jsii.invoke(self, "saveIKeyToKeyVault", [key_vault_id, key_vault_secret_name]))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "AppInsightsProps":
        return typing.cast("AppInsightsProps", jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97fa5018455ab90c6bbc179025dd90c7ae8faf283ee2c884829a94b7abeac7c5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e275638079dae2995cb8ad8bbbdd8b6897d70abca72db4f333367f1fe25fc7f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroup", value)


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_applicationinsights.AppInsightsProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_type": "applicationType",
        "location": "location",
        "name": "name",
        "daily_data_cap_in_gb": "dailyDataCapInGb",
        "daily_data_cap_notification_disabled": "dailyDataCapNotificationDisabled",
        "resource_group": "resourceGroup",
        "retention_in_days": "retentionInDays",
        "tags": "tags",
        "workspace_id": "workspaceId",
    },
)
class AppInsightsProps:
    def __init__(
        self,
        *,
        application_type: builtins.str,
        location: builtins.str,
        name: builtins.str,
        daily_data_cap_in_gb: typing.Optional[jsii.Number] = None,
        daily_data_cap_notification_disabled: typing.Optional[builtins.bool] = None,
        resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
        retention_in_days: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        workspace_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for the resource group.

        :param application_type: The Application type.
        :param location: The Azure Region to deploy.
        :param name: The name of the Application Insights resource.
        :param daily_data_cap_in_gb: The Application Insights daily data cap in GB.
        :param daily_data_cap_notification_disabled: The Application Insights daily data cap notifications disabled.
        :param resource_group: An optional reference to the resource group in which to deploy the Application Insights. If not provided, the Application Insights will be deployed in the default resource group.
        :param retention_in_days: The number of days of retention. Possible values are 30, 60, 90, 120, 180, 270, 365, 550 or 730. Defaults to 90. Default: 90
        :param tags: The tags to assign to the Application Insights resource.
        :param workspace_id: The id of the Log Analytics Workspace. Default: - If no workspace id is provided, a new one will be created automatically in the same resource group. The name will be the same as the Application Insights resource with a "-la" suffix.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cd1f93969139bc6d1064ad804b9d35fbafea5d6e73b90732b004f5fe5d03a04)
            check_type(argname="argument application_type", value=application_type, expected_type=type_hints["application_type"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument daily_data_cap_in_gb", value=daily_data_cap_in_gb, expected_type=type_hints["daily_data_cap_in_gb"])
            check_type(argname="argument daily_data_cap_notification_disabled", value=daily_data_cap_notification_disabled, expected_type=type_hints["daily_data_cap_notification_disabled"])
            check_type(argname="argument resource_group", value=resource_group, expected_type=type_hints["resource_group"])
            check_type(argname="argument retention_in_days", value=retention_in_days, expected_type=type_hints["retention_in_days"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument workspace_id", value=workspace_id, expected_type=type_hints["workspace_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_type": application_type,
            "location": location,
            "name": name,
        }
        if daily_data_cap_in_gb is not None:
            self._values["daily_data_cap_in_gb"] = daily_data_cap_in_gb
        if daily_data_cap_notification_disabled is not None:
            self._values["daily_data_cap_notification_disabled"] = daily_data_cap_notification_disabled
        if resource_group is not None:
            self._values["resource_group"] = resource_group
        if retention_in_days is not None:
            self._values["retention_in_days"] = retention_in_days
        if tags is not None:
            self._values["tags"] = tags
        if workspace_id is not None:
            self._values["workspace_id"] = workspace_id

    @builtins.property
    def application_type(self) -> builtins.str:
        '''The Application type.'''
        result = self._values.get("application_type")
        assert result is not None, "Required property 'application_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The Azure Region to deploy.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the Application Insights resource.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def daily_data_cap_in_gb(self) -> typing.Optional[jsii.Number]:
        '''The Application Insights daily data cap in GB.'''
        result = self._values.get("daily_data_cap_in_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def daily_data_cap_notification_disabled(self) -> typing.Optional[builtins.bool]:
        '''The Application Insights daily data cap notifications disabled.'''
        result = self._values.get("daily_data_cap_notification_disabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def resource_group(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup]:
        '''An optional reference to the resource group in which to deploy the Application Insights.

        If not provided, the Application Insights will be deployed in the default resource group.
        '''
        result = self._values.get("resource_group")
        return typing.cast(typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup], result)

    @builtins.property
    def retention_in_days(self) -> typing.Optional[jsii.Number]:
        '''The number of days of retention.

        Possible values are 30, 60, 90, 120, 180, 270, 365, 550 or 730. Defaults to 90.

        :default: 90
        '''
        result = self._values.get("retention_in_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The tags to assign to the Application Insights resource.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def workspace_id(self) -> typing.Optional[builtins.str]:
        '''The id of the Log Analytics Workspace.

        :default:

        - If no workspace id is provided, a new one will be created automatically
        in the same resource group. The name will be the same as the Application Insights
        resource with a "-la" suffix.
        '''
        result = self._values.get("workspace_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppInsightsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AppInsights",
    "AppInsightsProps",
]

publication.publish()

def _typecheckingstub__7d4b8c71ca92596f9110e479740b5f222f59c2481e089dc27fe01d85d3ddfb96(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    application_type: builtins.str,
    location: builtins.str,
    name: builtins.str,
    daily_data_cap_in_gb: typing.Optional[jsii.Number] = None,
    daily_data_cap_notification_disabled: typing.Optional[builtins.bool] = None,
    resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
    retention_in_days: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    workspace_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ab25147fd544a8a1c78f6c8c150e0eea1424fbb238afb85b75d0a9ecde637ad(
    key_vault_id: builtins.str,
    key_vault_secret_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97fa5018455ab90c6bbc179025dd90c7ae8faf283ee2c884829a94b7abeac7c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e275638079dae2995cb8ad8bbbdd8b6897d70abca72db4f333367f1fe25fc7f0(
    value: _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cd1f93969139bc6d1064ad804b9d35fbafea5d6e73b90732b004f5fe5d03a04(
    *,
    application_type: builtins.str,
    location: builtins.str,
    name: builtins.str,
    daily_data_cap_in_gb: typing.Optional[jsii.Number] = None,
    daily_data_cap_notification_disabled: typing.Optional[builtins.bool] = None,
    resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
    retention_in_days: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    workspace_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
