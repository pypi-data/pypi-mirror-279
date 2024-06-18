'''
# Azure Linux Function App Construct

This document provides an overview of the Azure Linux Function App construct, along with best practices for deployment and use.

## What is Azure Linux Function App?

Azure Linux Function App is a serverless compute service that enables you to run code without explicitly provisioning or managing infrastructure. It supports different programming languages and integrates with Azure services and other external services.

### Hosting Plans for Azure Linux Function App

Azure Linux Function App offers three hosting plans:

**Consumption Plan**: Automatically scales based on demand and is billed per execution. It's suitable for event-driven and intermittent workloads.

**Premium Plan**: Offers more CPU and memory than the Consumption Plan and includes features like VNet connectivity. It's suitable for more demanding, consistent workloads.

**Dedicated (App Service) Plan**: Provides dedicated resources for your functions, ideal for large-scale, continuous workloads.

#### When to Use Each Plan

**Consumption Plan**: Ideal for small, event-driven functions. Use when you expect irregular traffic and want to pay only for the compute time you use.

**Premium Plan**: Best for medium to large functions requiring more consistent performance and advanced features like VNet.

**App Service Plan**: Suited for enterprise-level applications that require constant, high-scale performance.

### Azure Service Plan SKUs Enum

The `ServicePlanSkus` enum provides various options for Azure Service Plans, ranging from Consumption to Isolated Plans. Each option caters to different scalability, performance, and cost requirements.

## Examples

By default a consumption plan Azure Function will be created. If `storageaccount`, `servicePlanId`, and `resourceGroupName` inputs are not configured, these resources will be automatically created and named after the

**Function App**

```python
new AzureLinuxFunctionApp(this, 'DefaultFA', {
      name: `MyDefaultFA`,
      location: 'eastus',
      tags: {
        "test": "test"
      }
});
```

**Consumption Plan**

```python
 new AzureLinuxFunctionApp(this, 'ConsumptionFA', {
      name: `MyConsumptionFA`,
      location: 'eastus',
      storageAccount: storageAccount,
      servicePlan: servicePlan,
      resourceGroup: resourceGroup,
      runtimeVersion: {
        pythonVersion: '3.8',
      },
      siteConfig: {
        cors: {
          allowedOrigins: ['*'],
        },
      },
      tags: {
        "test": "test"
      }
});
```

**Premium Function**

To deploy Premium Functions, use the premium SKU type. The `ServicePlanSkus` can be used to easily select available SKUs:

```python
import { ServicePlanSkus } from '../serviceplanskus';


 new AzureLinuxFunctionApp(this, 'PremiumFA', {
      name: `MyPremiumFA`,
      location: 'eastus',
      servicePlanSku: ServicePlanSkus.PremiumEP1,
      runtimeVersion: {
        dotnetVersion: '5.0',
      },
      tags: {
        "test": "test"
      }
});
```

To deploy Premium Functions, use the premium SKU type. The `ServicePlanSkus` can be used to easily select available SKUs:

**Dedicated App Service Plan**

To deploy Premium Functions, use the premium SKU type. The `ServicePlanSkus` can be used to easily select available SKUs:

```python
new AzureLinuxFunctionApp(this, 'ServicePlanFA', {
      name: `MyServicePlanFA`,
      location: 'eastus',
      servicePlanSku: ServicePlanSkus.ASPBasicB1,
      runtimeVersion: {
        pythonVersion: '3.8',
      },
      siteConfig: {
        cors: {
          allowedOrigins: ['*'],
        },
      },
      tags: {
        "test": "test"
      }
});
```

### Best Practices for Azure Linux Function App

Choose the Right Hosting Plan: Select a plan based on your function's performance, reliability, and cost needs.

Configure Storage Correctly: Ensure the storage account is in the same region as your function app and use separate accounts for different apps for improved performance.

Optimize Deployments: Use the "run from package" approach and consider continuous deployment for reliability.

Write Robust Functions: Design functions to be stateless, handle large data sets efficiently, and avoid long-running executions.

Consider Concurrency: Understand your function app’s response to load and configure triggers appropriately for scalability.

Plan for Connections: Optimize outbound connections to adhere to the plan’s connection limits.

Monitor Effectively: Use Azure Application Insights and Azure Monitor for comprehensive monitoring of your functions.

Build in Redundancy: Employ a multi-regional approach for high availability and disaster recovery.
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

import cdktf_cdktf_provider_azurerm.linux_function_app as _cdktf_cdktf_provider_azurerm_linux_function_app_92bbcedf
import cdktf_cdktf_provider_azurerm.resource_group as _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf
import cdktf_cdktf_provider_azurerm.service_plan as _cdktf_cdktf_provider_azurerm_service_plan_92bbcedf
import cdktf_cdktf_provider_azurerm.storage_account as _cdktf_cdktf_provider_azurerm_storage_account_92bbcedf
import constructs as _constructs_77d1e7e8
from ..core_azure import AzureResource as _AzureResource_74eec1c4


class FunctionAppLinux(
    _AzureResource_74eec1c4,
    metaclass=jsii.JSIIMeta,
    jsii_type="@microsoft/terraform-cdk-constructs.azure_functionapp.FunctionAppLinux",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        app_settings: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        auth_settings: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_function_app_92bbcedf.LinuxFunctionAppAuthSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        auth_settings_v2: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_function_app_92bbcedf.LinuxFunctionAppAuthSettingsV2, typing.Dict[builtins.str, typing.Any]]] = None,
        builtin_logging_enabled: typing.Optional[builtins.bool] = None,
        client_certificate_enabled: typing.Optional[builtins.bool] = None,
        client_certificate_exclusion_paths: typing.Optional[builtins.str] = None,
        client_certificate_mode: typing.Optional[builtins.str] = None,
        connection_string: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_azurerm_linux_function_app_92bbcedf.LinuxFunctionAppConnectionString, typing.Dict[builtins.str, typing.Any]]]] = None,
        enabled: typing.Optional[builtins.bool] = None,
        functions_extension_version: typing.Optional[builtins.str] = None,
        https_only: typing.Optional[builtins.bool] = None,
        identity: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_function_app_92bbcedf.LinuxFunctionAppIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
        public_network_access_enabled: typing.Optional[builtins.bool] = None,
        resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
        runtime_version: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_function_app_92bbcedf.LinuxFunctionAppSiteConfigApplicationStack, typing.Dict[builtins.str, typing.Any]]] = None,
        service_plan: typing.Optional[_cdktf_cdktf_provider_azurerm_service_plan_92bbcedf.ServicePlan] = None,
        service_plan_app_service_environment_id: typing.Optional[builtins.str] = None,
        service_plan_maximum_elastic_worker_count: typing.Optional[jsii.Number] = None,
        service_plan_per_site_scaling_enabled: typing.Optional[builtins.bool] = None,
        service_plan_sku: typing.Optional[builtins.str] = None,
        service_plan_worker_count: typing.Optional[jsii.Number] = None,
        service_plan_zone_balancing_enabled: typing.Optional[builtins.bool] = None,
        site_config: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_function_app_92bbcedf.LinuxFunctionAppSiteConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        storage_account: typing.Optional[_cdktf_cdktf_provider_azurerm_storage_account_92bbcedf.StorageAccount] = None,
        storage_account_access_key: typing.Optional[builtins.str] = None,
        storage_uses_managed_identity: typing.Optional[builtins.bool] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        virtual_network_subnet_id: typing.Optional[builtins.str] = None,
        zip_deploy_file: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Constructs a new FunctionAppLinux.

        :param scope: - The scope in which to define this construct.
        :param id: - The ID of this construct.
        :param location: The Azure Region where the Function App will be deployed, e.g., 'East US', 'West Europe'.
        :param name: The name of the Function App. This name must be unique within Azure.
        :param app_settings: Application settings for the Azure Function App.
        :param auth_settings: Optional authentication settings for the Function App.
        :param auth_settings_v2: Optional advanced version of authentication settings for the Function App.
        :param builtin_logging_enabled: Optional flag to enable built-in logging capabilities.
        :param client_certificate_enabled: Optional flag to enable client certificate authentication.
        :param client_certificate_exclusion_paths: Optional paths that are excluded from client certificate authentication.
        :param client_certificate_mode: Optional mode for client certificate requirement (e.g., 'Required', 'Optional').
        :param connection_string: Optional connection string for external services or databases.
        :param enabled: Optional flag to enable or disable the Function App.
        :param functions_extension_version: Optional version setting for the Azure Functions runtime.
        :param https_only: Optional flag to enforce HTTPS only traffic.
        :param identity: Optional identity configuration for the Function App, for use in Managed Service Identity scenarios.
        :param public_network_access_enabled: Optional flag to enable or disable public network access to the Function App.
        :param resource_group: An optional reference to the resource group in which to deploy the Function App. If not provided, the Function App will be deployed in the default resource group.
        :param runtime_version: Optional runtime version specification for the Function App, such as Node.js, .NET, or Java version.
        :param service_plan: Optional ID of an existing App Service Plan to host the Function App. If not provided, a new plan will be created.
        :param service_plan_app_service_environment_id: Optional ID for the App Service Environment to be used by the service plan.
        :param service_plan_maximum_elastic_worker_count: Optional maximum count of elastic workers for the App Service Plan.
        :param service_plan_per_site_scaling_enabled: Optional flag to enable per-site scaling for the App Service Plan.
        :param service_plan_sku: Optional SKU for the App Service Plan, defines the pricing tier and capabilities.
        :param service_plan_worker_count: Optional worker count for the App Service Plan.
        :param service_plan_zone_balancing_enabled: Optional flag to enable zone balancing for the App Service Plan.
        :param site_config: Optional site configuration for additional settings like environment variables, and connection strings.
        :param storage_account: An optional reference to the storage account to be used by the Function App. If not provided, a new storage account will be created.
        :param storage_account_access_key: Optional access key for the storage account.
        :param storage_uses_managed_identity: Optional flag indicating if the storage account uses a Managed Identity.
        :param tags: Optional tags for categorizing and managing the Function App resources within Azure.
        :param virtual_network_subnet_id: Optional ID of a virtual network subnet for the Function App.
        :param zip_deploy_file: Optional path to a ZIP file for deployment to the Function App.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3daa98fefa4d3f3d51500d1006d3a5f777530be3b2749a516c39d1d661eac80e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = FunctionAppLinuxProps(
            location=location,
            name=name,
            app_settings=app_settings,
            auth_settings=auth_settings,
            auth_settings_v2=auth_settings_v2,
            builtin_logging_enabled=builtin_logging_enabled,
            client_certificate_enabled=client_certificate_enabled,
            client_certificate_exclusion_paths=client_certificate_exclusion_paths,
            client_certificate_mode=client_certificate_mode,
            connection_string=connection_string,
            enabled=enabled,
            functions_extension_version=functions_extension_version,
            https_only=https_only,
            identity=identity,
            public_network_access_enabled=public_network_access_enabled,
            resource_group=resource_group,
            runtime_version=runtime_version,
            service_plan=service_plan,
            service_plan_app_service_environment_id=service_plan_app_service_environment_id,
            service_plan_maximum_elastic_worker_count=service_plan_maximum_elastic_worker_count,
            service_plan_per_site_scaling_enabled=service_plan_per_site_scaling_enabled,
            service_plan_sku=service_plan_sku,
            service_plan_worker_count=service_plan_worker_count,
            service_plan_zone_balancing_enabled=service_plan_zone_balancing_enabled,
            site_config=site_config,
            storage_account=storage_account,
            storage_account_access_key=storage_account_access_key,
            storage_uses_managed_identity=storage_uses_managed_identity,
            tags=tags,
            virtual_network_subnet_id=virtual_network_subnet_id,
            zip_deploy_file=zip_deploy_file,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="defaultHostname")
    def default_hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultHostname"))

    @builtins.property
    @jsii.member(jsii_name="kind")
    def kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kind"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="servicePlan")
    def service_plan(
        self,
    ) -> _cdktf_cdktf_provider_azurerm_service_plan_92bbcedf.ServicePlan:
        return typing.cast(_cdktf_cdktf_provider_azurerm_service_plan_92bbcedf.ServicePlan, jsii.get(self, "servicePlan"))

    @builtins.property
    @jsii.member(jsii_name="storageAccount")
    def storage_account(
        self,
    ) -> _cdktf_cdktf_provider_azurerm_storage_account_92bbcedf.StorageAccount:
        return typing.cast(_cdktf_cdktf_provider_azurerm_storage_account_92bbcedf.StorageAccount, jsii.get(self, "storageAccount"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__183c1ef92f1be1b508ac4d390fa0d5cd69de1a6a3c64414c03506a4a56b1052f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8f13951d99b687d3f1b7c44001ed6bb8221bcdd1c348606a23c66e987a0308c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroup", value)


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_functionapp.FunctionAppLinuxProps",
    jsii_struct_bases=[],
    name_mapping={
        "location": "location",
        "name": "name",
        "app_settings": "appSettings",
        "auth_settings": "authSettings",
        "auth_settings_v2": "authSettingsV2",
        "builtin_logging_enabled": "builtinLoggingEnabled",
        "client_certificate_enabled": "clientCertificateEnabled",
        "client_certificate_exclusion_paths": "clientCertificateExclusionPaths",
        "client_certificate_mode": "clientCertificateMode",
        "connection_string": "connectionString",
        "enabled": "enabled",
        "functions_extension_version": "functionsExtensionVersion",
        "https_only": "httpsOnly",
        "identity": "identity",
        "public_network_access_enabled": "publicNetworkAccessEnabled",
        "resource_group": "resourceGroup",
        "runtime_version": "runtimeVersion",
        "service_plan": "servicePlan",
        "service_plan_app_service_environment_id": "servicePlanAppServiceEnvironmentId",
        "service_plan_maximum_elastic_worker_count": "servicePlanMaximumElasticWorkerCount",
        "service_plan_per_site_scaling_enabled": "servicePlanPerSiteScalingEnabled",
        "service_plan_sku": "servicePlanSku",
        "service_plan_worker_count": "servicePlanWorkerCount",
        "service_plan_zone_balancing_enabled": "servicePlanZoneBalancingEnabled",
        "site_config": "siteConfig",
        "storage_account": "storageAccount",
        "storage_account_access_key": "storageAccountAccessKey",
        "storage_uses_managed_identity": "storageUsesManagedIdentity",
        "tags": "tags",
        "virtual_network_subnet_id": "virtualNetworkSubnetId",
        "zip_deploy_file": "zipDeployFile",
    },
)
class FunctionAppLinuxProps:
    def __init__(
        self,
        *,
        location: builtins.str,
        name: builtins.str,
        app_settings: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        auth_settings: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_function_app_92bbcedf.LinuxFunctionAppAuthSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        auth_settings_v2: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_function_app_92bbcedf.LinuxFunctionAppAuthSettingsV2, typing.Dict[builtins.str, typing.Any]]] = None,
        builtin_logging_enabled: typing.Optional[builtins.bool] = None,
        client_certificate_enabled: typing.Optional[builtins.bool] = None,
        client_certificate_exclusion_paths: typing.Optional[builtins.str] = None,
        client_certificate_mode: typing.Optional[builtins.str] = None,
        connection_string: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_azurerm_linux_function_app_92bbcedf.LinuxFunctionAppConnectionString, typing.Dict[builtins.str, typing.Any]]]] = None,
        enabled: typing.Optional[builtins.bool] = None,
        functions_extension_version: typing.Optional[builtins.str] = None,
        https_only: typing.Optional[builtins.bool] = None,
        identity: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_function_app_92bbcedf.LinuxFunctionAppIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
        public_network_access_enabled: typing.Optional[builtins.bool] = None,
        resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
        runtime_version: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_function_app_92bbcedf.LinuxFunctionAppSiteConfigApplicationStack, typing.Dict[builtins.str, typing.Any]]] = None,
        service_plan: typing.Optional[_cdktf_cdktf_provider_azurerm_service_plan_92bbcedf.ServicePlan] = None,
        service_plan_app_service_environment_id: typing.Optional[builtins.str] = None,
        service_plan_maximum_elastic_worker_count: typing.Optional[jsii.Number] = None,
        service_plan_per_site_scaling_enabled: typing.Optional[builtins.bool] = None,
        service_plan_sku: typing.Optional[builtins.str] = None,
        service_plan_worker_count: typing.Optional[jsii.Number] = None,
        service_plan_zone_balancing_enabled: typing.Optional[builtins.bool] = None,
        site_config: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_function_app_92bbcedf.LinuxFunctionAppSiteConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        storage_account: typing.Optional[_cdktf_cdktf_provider_azurerm_storage_account_92bbcedf.StorageAccount] = None,
        storage_account_access_key: typing.Optional[builtins.str] = None,
        storage_uses_managed_identity: typing.Optional[builtins.bool] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        virtual_network_subnet_id: typing.Optional[builtins.str] = None,
        zip_deploy_file: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for the Azure Linux Function App.

        :param location: The Azure Region where the Function App will be deployed, e.g., 'East US', 'West Europe'.
        :param name: The name of the Function App. This name must be unique within Azure.
        :param app_settings: Application settings for the Azure Function App.
        :param auth_settings: Optional authentication settings for the Function App.
        :param auth_settings_v2: Optional advanced version of authentication settings for the Function App.
        :param builtin_logging_enabled: Optional flag to enable built-in logging capabilities.
        :param client_certificate_enabled: Optional flag to enable client certificate authentication.
        :param client_certificate_exclusion_paths: Optional paths that are excluded from client certificate authentication.
        :param client_certificate_mode: Optional mode for client certificate requirement (e.g., 'Required', 'Optional').
        :param connection_string: Optional connection string for external services or databases.
        :param enabled: Optional flag to enable or disable the Function App.
        :param functions_extension_version: Optional version setting for the Azure Functions runtime.
        :param https_only: Optional flag to enforce HTTPS only traffic.
        :param identity: Optional identity configuration for the Function App, for use in Managed Service Identity scenarios.
        :param public_network_access_enabled: Optional flag to enable or disable public network access to the Function App.
        :param resource_group: An optional reference to the resource group in which to deploy the Function App. If not provided, the Function App will be deployed in the default resource group.
        :param runtime_version: Optional runtime version specification for the Function App, such as Node.js, .NET, or Java version.
        :param service_plan: Optional ID of an existing App Service Plan to host the Function App. If not provided, a new plan will be created.
        :param service_plan_app_service_environment_id: Optional ID for the App Service Environment to be used by the service plan.
        :param service_plan_maximum_elastic_worker_count: Optional maximum count of elastic workers for the App Service Plan.
        :param service_plan_per_site_scaling_enabled: Optional flag to enable per-site scaling for the App Service Plan.
        :param service_plan_sku: Optional SKU for the App Service Plan, defines the pricing tier and capabilities.
        :param service_plan_worker_count: Optional worker count for the App Service Plan.
        :param service_plan_zone_balancing_enabled: Optional flag to enable zone balancing for the App Service Plan.
        :param site_config: Optional site configuration for additional settings like environment variables, and connection strings.
        :param storage_account: An optional reference to the storage account to be used by the Function App. If not provided, a new storage account will be created.
        :param storage_account_access_key: Optional access key for the storage account.
        :param storage_uses_managed_identity: Optional flag indicating if the storage account uses a Managed Identity.
        :param tags: Optional tags for categorizing and managing the Function App resources within Azure.
        :param virtual_network_subnet_id: Optional ID of a virtual network subnet for the Function App.
        :param zip_deploy_file: Optional path to a ZIP file for deployment to the Function App.
        '''
        if isinstance(auth_settings, dict):
            auth_settings = _cdktf_cdktf_provider_azurerm_linux_function_app_92bbcedf.LinuxFunctionAppAuthSettings(**auth_settings)
        if isinstance(auth_settings_v2, dict):
            auth_settings_v2 = _cdktf_cdktf_provider_azurerm_linux_function_app_92bbcedf.LinuxFunctionAppAuthSettingsV2(**auth_settings_v2)
        if isinstance(identity, dict):
            identity = _cdktf_cdktf_provider_azurerm_linux_function_app_92bbcedf.LinuxFunctionAppIdentity(**identity)
        if isinstance(runtime_version, dict):
            runtime_version = _cdktf_cdktf_provider_azurerm_linux_function_app_92bbcedf.LinuxFunctionAppSiteConfigApplicationStack(**runtime_version)
        if isinstance(site_config, dict):
            site_config = _cdktf_cdktf_provider_azurerm_linux_function_app_92bbcedf.LinuxFunctionAppSiteConfig(**site_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53587b2bdf36e31f15daa92fc2dde9b6de76acb6a3e642b5678ba48393cc0ee6)
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument app_settings", value=app_settings, expected_type=type_hints["app_settings"])
            check_type(argname="argument auth_settings", value=auth_settings, expected_type=type_hints["auth_settings"])
            check_type(argname="argument auth_settings_v2", value=auth_settings_v2, expected_type=type_hints["auth_settings_v2"])
            check_type(argname="argument builtin_logging_enabled", value=builtin_logging_enabled, expected_type=type_hints["builtin_logging_enabled"])
            check_type(argname="argument client_certificate_enabled", value=client_certificate_enabled, expected_type=type_hints["client_certificate_enabled"])
            check_type(argname="argument client_certificate_exclusion_paths", value=client_certificate_exclusion_paths, expected_type=type_hints["client_certificate_exclusion_paths"])
            check_type(argname="argument client_certificate_mode", value=client_certificate_mode, expected_type=type_hints["client_certificate_mode"])
            check_type(argname="argument connection_string", value=connection_string, expected_type=type_hints["connection_string"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument functions_extension_version", value=functions_extension_version, expected_type=type_hints["functions_extension_version"])
            check_type(argname="argument https_only", value=https_only, expected_type=type_hints["https_only"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument public_network_access_enabled", value=public_network_access_enabled, expected_type=type_hints["public_network_access_enabled"])
            check_type(argname="argument resource_group", value=resource_group, expected_type=type_hints["resource_group"])
            check_type(argname="argument runtime_version", value=runtime_version, expected_type=type_hints["runtime_version"])
            check_type(argname="argument service_plan", value=service_plan, expected_type=type_hints["service_plan"])
            check_type(argname="argument service_plan_app_service_environment_id", value=service_plan_app_service_environment_id, expected_type=type_hints["service_plan_app_service_environment_id"])
            check_type(argname="argument service_plan_maximum_elastic_worker_count", value=service_plan_maximum_elastic_worker_count, expected_type=type_hints["service_plan_maximum_elastic_worker_count"])
            check_type(argname="argument service_plan_per_site_scaling_enabled", value=service_plan_per_site_scaling_enabled, expected_type=type_hints["service_plan_per_site_scaling_enabled"])
            check_type(argname="argument service_plan_sku", value=service_plan_sku, expected_type=type_hints["service_plan_sku"])
            check_type(argname="argument service_plan_worker_count", value=service_plan_worker_count, expected_type=type_hints["service_plan_worker_count"])
            check_type(argname="argument service_plan_zone_balancing_enabled", value=service_plan_zone_balancing_enabled, expected_type=type_hints["service_plan_zone_balancing_enabled"])
            check_type(argname="argument site_config", value=site_config, expected_type=type_hints["site_config"])
            check_type(argname="argument storage_account", value=storage_account, expected_type=type_hints["storage_account"])
            check_type(argname="argument storage_account_access_key", value=storage_account_access_key, expected_type=type_hints["storage_account_access_key"])
            check_type(argname="argument storage_uses_managed_identity", value=storage_uses_managed_identity, expected_type=type_hints["storage_uses_managed_identity"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument virtual_network_subnet_id", value=virtual_network_subnet_id, expected_type=type_hints["virtual_network_subnet_id"])
            check_type(argname="argument zip_deploy_file", value=zip_deploy_file, expected_type=type_hints["zip_deploy_file"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "name": name,
        }
        if app_settings is not None:
            self._values["app_settings"] = app_settings
        if auth_settings is not None:
            self._values["auth_settings"] = auth_settings
        if auth_settings_v2 is not None:
            self._values["auth_settings_v2"] = auth_settings_v2
        if builtin_logging_enabled is not None:
            self._values["builtin_logging_enabled"] = builtin_logging_enabled
        if client_certificate_enabled is not None:
            self._values["client_certificate_enabled"] = client_certificate_enabled
        if client_certificate_exclusion_paths is not None:
            self._values["client_certificate_exclusion_paths"] = client_certificate_exclusion_paths
        if client_certificate_mode is not None:
            self._values["client_certificate_mode"] = client_certificate_mode
        if connection_string is not None:
            self._values["connection_string"] = connection_string
        if enabled is not None:
            self._values["enabled"] = enabled
        if functions_extension_version is not None:
            self._values["functions_extension_version"] = functions_extension_version
        if https_only is not None:
            self._values["https_only"] = https_only
        if identity is not None:
            self._values["identity"] = identity
        if public_network_access_enabled is not None:
            self._values["public_network_access_enabled"] = public_network_access_enabled
        if resource_group is not None:
            self._values["resource_group"] = resource_group
        if runtime_version is not None:
            self._values["runtime_version"] = runtime_version
        if service_plan is not None:
            self._values["service_plan"] = service_plan
        if service_plan_app_service_environment_id is not None:
            self._values["service_plan_app_service_environment_id"] = service_plan_app_service_environment_id
        if service_plan_maximum_elastic_worker_count is not None:
            self._values["service_plan_maximum_elastic_worker_count"] = service_plan_maximum_elastic_worker_count
        if service_plan_per_site_scaling_enabled is not None:
            self._values["service_plan_per_site_scaling_enabled"] = service_plan_per_site_scaling_enabled
        if service_plan_sku is not None:
            self._values["service_plan_sku"] = service_plan_sku
        if service_plan_worker_count is not None:
            self._values["service_plan_worker_count"] = service_plan_worker_count
        if service_plan_zone_balancing_enabled is not None:
            self._values["service_plan_zone_balancing_enabled"] = service_plan_zone_balancing_enabled
        if site_config is not None:
            self._values["site_config"] = site_config
        if storage_account is not None:
            self._values["storage_account"] = storage_account
        if storage_account_access_key is not None:
            self._values["storage_account_access_key"] = storage_account_access_key
        if storage_uses_managed_identity is not None:
            self._values["storage_uses_managed_identity"] = storage_uses_managed_identity
        if tags is not None:
            self._values["tags"] = tags
        if virtual_network_subnet_id is not None:
            self._values["virtual_network_subnet_id"] = virtual_network_subnet_id
        if zip_deploy_file is not None:
            self._values["zip_deploy_file"] = zip_deploy_file

    @builtins.property
    def location(self) -> builtins.str:
        '''The Azure Region where the Function App will be deployed, e.g., 'East US', 'West Europe'.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the Function App.

        This name must be unique within Azure.
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def app_settings(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Application settings for the Azure Function App.

        :property:

        { [key: string]: string } appSettings - A collection of key-value pairs that contain the settings.

        Note on Runtime Settings:

        - 'node_version' in 'site_config' sets the Node.js version.
        Terraform assigns this value to 'WEBSITE_NODE_DEFAULT_VERSION' in app settings.
        - 'functions_extension_version' sets the Azure Functions runtime version.
        Terraform assigns this value to 'FUNCTIONS_EXTENSION_VERSION' in app settings.

        Note on Storage Settings:

        - Properties like 'storage_account_access_key' are used for storage configurations.
        Terraform assigns these values to keys like 'WEBSITE_CONTENTAZUREFILECONNECTIONSTRING',
        'AzureWebJobsStorage' in app settings.

        Note on Application Insights Settings:

        - Use 'application_insights_connection_string' and 'application_insights_key' for Application Insights configurations.
        Terraform assigns these to 'APPINSIGHTS_INSTRUMENTATIONKEY' and 'APPLICATIONINSIGHTS_CONNECTION_STRING' in app settings.

        Note on Health Check Settings:

        - 'health_check_eviction_time_in_min' configures health check settings.
        Terraform assigns this value to 'WEBSITE_HEALTHCHECK_MAXPINGFAILURES' in app settings.

        Note on Storage Account Restriction:

        - To restrict your storage account to a virtual network, set 'WEBSITE_CONTENTOVERVNET' to 1 in app settings.
        Ensure a predefined share is created for this configuration.
        '''
        result = self._values.get("app_settings")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def auth_settings(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_linux_function_app_92bbcedf.LinuxFunctionAppAuthSettings]:
        '''Optional authentication settings for the Function App.'''
        result = self._values.get("auth_settings")
        return typing.cast(typing.Optional[_cdktf_cdktf_provider_azurerm_linux_function_app_92bbcedf.LinuxFunctionAppAuthSettings], result)

    @builtins.property
    def auth_settings_v2(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_linux_function_app_92bbcedf.LinuxFunctionAppAuthSettingsV2]:
        '''Optional advanced version of authentication settings for the Function App.'''
        result = self._values.get("auth_settings_v2")
        return typing.cast(typing.Optional[_cdktf_cdktf_provider_azurerm_linux_function_app_92bbcedf.LinuxFunctionAppAuthSettingsV2], result)

    @builtins.property
    def builtin_logging_enabled(self) -> typing.Optional[builtins.bool]:
        '''Optional flag to enable built-in logging capabilities.'''
        result = self._values.get("builtin_logging_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def client_certificate_enabled(self) -> typing.Optional[builtins.bool]:
        '''Optional flag to enable client certificate authentication.'''
        result = self._values.get("client_certificate_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def client_certificate_exclusion_paths(self) -> typing.Optional[builtins.str]:
        '''Optional paths that are excluded from client certificate authentication.'''
        result = self._values.get("client_certificate_exclusion_paths")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_certificate_mode(self) -> typing.Optional[builtins.str]:
        '''Optional mode for client certificate requirement (e.g., 'Required', 'Optional').'''
        result = self._values.get("client_certificate_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connection_string(
        self,
    ) -> typing.Optional[typing.List[_cdktf_cdktf_provider_azurerm_linux_function_app_92bbcedf.LinuxFunctionAppConnectionString]]:
        '''Optional connection string for external services or databases.'''
        result = self._values.get("connection_string")
        return typing.cast(typing.Optional[typing.List[_cdktf_cdktf_provider_azurerm_linux_function_app_92bbcedf.LinuxFunctionAppConnectionString]], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''Optional flag to enable or disable the Function App.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def functions_extension_version(self) -> typing.Optional[builtins.str]:
        '''Optional version setting for the Azure Functions runtime.'''
        result = self._values.get("functions_extension_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def https_only(self) -> typing.Optional[builtins.bool]:
        '''Optional flag to enforce HTTPS only traffic.'''
        result = self._values.get("https_only")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def identity(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_linux_function_app_92bbcedf.LinuxFunctionAppIdentity]:
        '''Optional identity configuration for the Function App, for use in Managed Service Identity scenarios.'''
        result = self._values.get("identity")
        return typing.cast(typing.Optional[_cdktf_cdktf_provider_azurerm_linux_function_app_92bbcedf.LinuxFunctionAppIdentity], result)

    @builtins.property
    def public_network_access_enabled(self) -> typing.Optional[builtins.bool]:
        '''Optional flag to enable or disable public network access to the Function App.'''
        result = self._values.get("public_network_access_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def resource_group(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup]:
        '''An optional reference to the resource group in which to deploy the Function App.

        If not provided, the Function App will be deployed in the default resource group.
        '''
        result = self._values.get("resource_group")
        return typing.cast(typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup], result)

    @builtins.property
    def runtime_version(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_linux_function_app_92bbcedf.LinuxFunctionAppSiteConfigApplicationStack]:
        '''Optional runtime version specification for the Function App, such as Node.js, .NET, or Java version.'''
        result = self._values.get("runtime_version")
        return typing.cast(typing.Optional[_cdktf_cdktf_provider_azurerm_linux_function_app_92bbcedf.LinuxFunctionAppSiteConfigApplicationStack], result)

    @builtins.property
    def service_plan(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_service_plan_92bbcedf.ServicePlan]:
        '''Optional ID of an existing App Service Plan to host the Function App.

        If not provided, a new plan will be created.
        '''
        result = self._values.get("service_plan")
        return typing.cast(typing.Optional[_cdktf_cdktf_provider_azurerm_service_plan_92bbcedf.ServicePlan], result)

    @builtins.property
    def service_plan_app_service_environment_id(self) -> typing.Optional[builtins.str]:
        '''Optional ID for the App Service Environment to be used by the service plan.'''
        result = self._values.get("service_plan_app_service_environment_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_plan_maximum_elastic_worker_count(self) -> typing.Optional[jsii.Number]:
        '''Optional maximum count of elastic workers for the App Service Plan.'''
        result = self._values.get("service_plan_maximum_elastic_worker_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service_plan_per_site_scaling_enabled(self) -> typing.Optional[builtins.bool]:
        '''Optional flag to enable per-site scaling for the App Service Plan.'''
        result = self._values.get("service_plan_per_site_scaling_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def service_plan_sku(self) -> typing.Optional[builtins.str]:
        '''Optional SKU for the App Service Plan, defines the pricing tier and capabilities.'''
        result = self._values.get("service_plan_sku")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_plan_worker_count(self) -> typing.Optional[jsii.Number]:
        '''Optional worker count for the App Service Plan.'''
        result = self._values.get("service_plan_worker_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service_plan_zone_balancing_enabled(self) -> typing.Optional[builtins.bool]:
        '''Optional flag to enable zone balancing for the App Service Plan.'''
        result = self._values.get("service_plan_zone_balancing_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def site_config(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_linux_function_app_92bbcedf.LinuxFunctionAppSiteConfig]:
        '''Optional site configuration for additional settings like environment variables, and connection strings.'''
        result = self._values.get("site_config")
        return typing.cast(typing.Optional[_cdktf_cdktf_provider_azurerm_linux_function_app_92bbcedf.LinuxFunctionAppSiteConfig], result)

    @builtins.property
    def storage_account(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_storage_account_92bbcedf.StorageAccount]:
        '''An optional reference to the storage account to be used by the Function App.

        If not provided, a new storage account will be created.
        '''
        result = self._values.get("storage_account")
        return typing.cast(typing.Optional[_cdktf_cdktf_provider_azurerm_storage_account_92bbcedf.StorageAccount], result)

    @builtins.property
    def storage_account_access_key(self) -> typing.Optional[builtins.str]:
        '''Optional access key for the storage account.'''
        result = self._values.get("storage_account_access_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_uses_managed_identity(self) -> typing.Optional[builtins.bool]:
        '''Optional flag indicating if the storage account uses a Managed Identity.'''
        result = self._values.get("storage_uses_managed_identity")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional tags for categorizing and managing the Function App resources within Azure.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def virtual_network_subnet_id(self) -> typing.Optional[builtins.str]:
        '''Optional ID of a virtual network subnet for the Function App.'''
        result = self._values.get("virtual_network_subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zip_deploy_file(self) -> typing.Optional[builtins.str]:
        '''Optional path to a ZIP file for deployment to the Function App.'''
        result = self._values.get("zip_deploy_file")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionAppLinuxProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "FunctionAppLinux",
    "FunctionAppLinuxProps",
]

publication.publish()

def _typecheckingstub__3daa98fefa4d3f3d51500d1006d3a5f777530be3b2749a516c39d1d661eac80e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    app_settings: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    auth_settings: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_function_app_92bbcedf.LinuxFunctionAppAuthSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    auth_settings_v2: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_function_app_92bbcedf.LinuxFunctionAppAuthSettingsV2, typing.Dict[builtins.str, typing.Any]]] = None,
    builtin_logging_enabled: typing.Optional[builtins.bool] = None,
    client_certificate_enabled: typing.Optional[builtins.bool] = None,
    client_certificate_exclusion_paths: typing.Optional[builtins.str] = None,
    client_certificate_mode: typing.Optional[builtins.str] = None,
    connection_string: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_azurerm_linux_function_app_92bbcedf.LinuxFunctionAppConnectionString, typing.Dict[builtins.str, typing.Any]]]] = None,
    enabled: typing.Optional[builtins.bool] = None,
    functions_extension_version: typing.Optional[builtins.str] = None,
    https_only: typing.Optional[builtins.bool] = None,
    identity: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_function_app_92bbcedf.LinuxFunctionAppIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    public_network_access_enabled: typing.Optional[builtins.bool] = None,
    resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
    runtime_version: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_function_app_92bbcedf.LinuxFunctionAppSiteConfigApplicationStack, typing.Dict[builtins.str, typing.Any]]] = None,
    service_plan: typing.Optional[_cdktf_cdktf_provider_azurerm_service_plan_92bbcedf.ServicePlan] = None,
    service_plan_app_service_environment_id: typing.Optional[builtins.str] = None,
    service_plan_maximum_elastic_worker_count: typing.Optional[jsii.Number] = None,
    service_plan_per_site_scaling_enabled: typing.Optional[builtins.bool] = None,
    service_plan_sku: typing.Optional[builtins.str] = None,
    service_plan_worker_count: typing.Optional[jsii.Number] = None,
    service_plan_zone_balancing_enabled: typing.Optional[builtins.bool] = None,
    site_config: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_function_app_92bbcedf.LinuxFunctionAppSiteConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_account: typing.Optional[_cdktf_cdktf_provider_azurerm_storage_account_92bbcedf.StorageAccount] = None,
    storage_account_access_key: typing.Optional[builtins.str] = None,
    storage_uses_managed_identity: typing.Optional[builtins.bool] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    virtual_network_subnet_id: typing.Optional[builtins.str] = None,
    zip_deploy_file: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__183c1ef92f1be1b508ac4d390fa0d5cd69de1a6a3c64414c03506a4a56b1052f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8f13951d99b687d3f1b7c44001ed6bb8221bcdd1c348606a23c66e987a0308c(
    value: _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53587b2bdf36e31f15daa92fc2dde9b6de76acb6a3e642b5678ba48393cc0ee6(
    *,
    location: builtins.str,
    name: builtins.str,
    app_settings: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    auth_settings: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_function_app_92bbcedf.LinuxFunctionAppAuthSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    auth_settings_v2: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_function_app_92bbcedf.LinuxFunctionAppAuthSettingsV2, typing.Dict[builtins.str, typing.Any]]] = None,
    builtin_logging_enabled: typing.Optional[builtins.bool] = None,
    client_certificate_enabled: typing.Optional[builtins.bool] = None,
    client_certificate_exclusion_paths: typing.Optional[builtins.str] = None,
    client_certificate_mode: typing.Optional[builtins.str] = None,
    connection_string: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_azurerm_linux_function_app_92bbcedf.LinuxFunctionAppConnectionString, typing.Dict[builtins.str, typing.Any]]]] = None,
    enabled: typing.Optional[builtins.bool] = None,
    functions_extension_version: typing.Optional[builtins.str] = None,
    https_only: typing.Optional[builtins.bool] = None,
    identity: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_function_app_92bbcedf.LinuxFunctionAppIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    public_network_access_enabled: typing.Optional[builtins.bool] = None,
    resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
    runtime_version: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_function_app_92bbcedf.LinuxFunctionAppSiteConfigApplicationStack, typing.Dict[builtins.str, typing.Any]]] = None,
    service_plan: typing.Optional[_cdktf_cdktf_provider_azurerm_service_plan_92bbcedf.ServicePlan] = None,
    service_plan_app_service_environment_id: typing.Optional[builtins.str] = None,
    service_plan_maximum_elastic_worker_count: typing.Optional[jsii.Number] = None,
    service_plan_per_site_scaling_enabled: typing.Optional[builtins.bool] = None,
    service_plan_sku: typing.Optional[builtins.str] = None,
    service_plan_worker_count: typing.Optional[jsii.Number] = None,
    service_plan_zone_balancing_enabled: typing.Optional[builtins.bool] = None,
    site_config: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_function_app_92bbcedf.LinuxFunctionAppSiteConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_account: typing.Optional[_cdktf_cdktf_provider_azurerm_storage_account_92bbcedf.StorageAccount] = None,
    storage_account_access_key: typing.Optional[builtins.str] = None,
    storage_uses_managed_identity: typing.Optional[builtins.bool] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    virtual_network_subnet_id: typing.Optional[builtins.str] = None,
    zip_deploy_file: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
