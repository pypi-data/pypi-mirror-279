'''
# Azure Kusto (Azure Data Explorer) Construct

This class represents a Kusto (a.k.a Azure Data Explorer) resource in Azure. It provides a convenient way to manage Azure Kusto resources.

## What is Kusto?

Azure Kusto is a powerful and scalable solution for real-time data exploration and analysis, offering a range of features to handle large datasets and diverse data sources.

You can learn more about Azure Kusto in the [official Azure documentation](https://learn.microsoft.com/en-us/azure/data-explorer/data-explorer-overview).

## Kusto Best Practices

Coming soon.

## Kusto Class Properties

This class has several properties that control the Kusto resource's behaviour:

* `azureResourceGroup`: The [Azure Resource Group object](../azure-resourcegroup/) where the Kusto resource will be deployed.
* `name`: The name of the Kusto resource.
* `sku`: (Optional) The SKU of the Kusto resource. Defaults to "dev/test, Dv2/DSv2 Series, Extra small".
* `capacity`: (Optional) The node count for the cluster. Defaults to 2.
* `identityType`: (Optional) The type of Managed Service Identity. Defaults to "SystemAssigned".
* `identityIds`: (Optional) A list of User Assigned Managed Identity IDs to be assigned to this Kusto Cluster.
* `publicNetworkAccessEnabled`: (Optional) Is the public network access enabled? Defaults to true.
* `autoStopEnabled`: (Optional) Specifies if the cluster could be automatically stopped (due to lack of data or no activity for many days). Defaults to true.
* `streamingIngestionEnabled`: (Optional) Specifies if the streaming ingest is enabled. Defaults to true.
* `purgeEnabled`: (Optional) Specifies if the purge operations are enabled. Defaults to false.
* `enableZones`: (Optional) Specifies if the cluster is zone redundant or not. Will check if the sku supports zone redundancy. Defaults to true.
* `minimumInstances`: (Optional) The minimum number of allowed instances. Must between 0 and 1000.
* `maximumInstances`: (Optional) The maximum number of allowed instances. Must between 0 and 1000.
* `tags`: (Optional) A mapping of tags to assign to the Kusto.

## Deploying a Kusto

You can deploy a Kusto resource using this class like so:

```python
  // Create a Resource Group first
  const resourceGroup = new AzureResourceGroup(this, "myResourceGroup", {
    name: 'myResourceGroup',
    location: 'eastus',
  });

  // Create a Kusto Cluster with defult settings
  // import { ComputeSpecification } from '../compute-specification';
  const kustoCluster = new AzureKusto(this, "myKusto", {
    rg: resourceGroup,
    name: 'myKusto',
    sku: ComputeSpecification.devtestExtraSmallEav4,
  });
```

Full example can be found [here](test/ExampleAzureKusto.ts).

## Some convenient methods in the Kusto Class

* Add IAM role to Kusto Cluster

  ```python
  const objectId = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx";
  const role = "Contributor"
  kustoCluster.addAccess(objectId, role);
  ```
* Add Diagnostics Log into LogAnalytics

  ```python
  logAnalyticsWorkspaceId = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx";
  kustoCluster.addDiagSettings({
    name: "diagsettings",
    logAnalyticsWorkspaceId: logAnalyticsWorkspaceId,
  })
  ```
* Create Database into the Kusto

  ```python
  const myKustoDB1 = kustoCluster.addDatabase({
      kusto: kustoCluster,
      name: "myDatabase1",
      hotCachePeriod: "P7D",
      softDeletePeriod: "P1D",
    });
  ```
* Add Permission to the Kusto Database

  ```python
  myKustoDB1.addPermission({
    name: "kustoPermission1",
    tenantId: `${tenantId}`,
    principalId: `${clientId}`,
    principalType: "User",
    role: "Admin",
  });
  ```

  This example will grant the user with `clientId` the `Admin` role to the Kusto Database `myKustoDB1`.
* Add Table to the Kusto Database

  ```python
  myKustoDB1.addTable('myTable', [
    {
      columnName: 'Timestamp',
      columnType: 'datetime',
    },
    {
      columnName: 'User',
      columnType: 'string',
    },
    {
      columnName: 'Value',
      columnType: 'int32',
    },
  ]);
  ```

  This example will create a table named `myTable` with three columns `Timestamp`, `User` and `Value` in the Kusto Database `myKustoDB1`.
* Run script for kusto table operations

  ```python
  const script = '.create table myTable2 ( Timestamp:datetime, User:string, Value:int32 )';
  testDB1.addScript('myScriptName', script);
  ```

  This example will run the script to create a table named `myTable2` with three columns `Timestamp`, `User` and `Value` in the Kusto Database `myKustoDB1`.
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


class Cluster(
    _AzureResource_74eec1c4,
    metaclass=jsii.JSIIMeta,
    jsii_type="@microsoft/terraform-cdk-constructs.azure_kusto.Cluster",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        auto_stop_enabled: typing.Optional[builtins.bool] = None,
        capacity: typing.Optional[jsii.Number] = None,
        enable_zones: typing.Optional[builtins.bool] = None,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        identity_type: typing.Optional[builtins.str] = None,
        maximum_instances: typing.Optional[jsii.Number] = None,
        minimum_instances: typing.Optional[jsii.Number] = None,
        public_network_access_enabled: typing.Optional[builtins.bool] = None,
        purge_enabled: typing.Optional[builtins.bool] = None,
        resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
        sku: typing.Optional["IComputeSpecification"] = None,
        streaming_ingestion_enabled: typing.Optional[builtins.bool] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Represents a Kusto (Azure Data Explorer) cluster in Azure.

        This class is responsible for the creation and management of a Kusto Cluster, which is a highly scalable and secure
        analytics service for ingesting, storing, and analyzing large volumes of data. The cluster supports various configurations
        tailored to the needs of specific data workloads and security requirements.

        :param scope: - The scope in which to define this construct, typically representing the Cloud Development Kit (CDK) stack.
        :param id: - The unique identifier for this instance of the cluster.
        :param name: The name of the Kusto Cluster to create. Only 4-22 lowercase alphanumeric characters allowed, starting with a letter.
        :param auto_stop_enabled: Specifies if the cluster could be automatically stopped. (due to lack of data or no activity for many days). Default: true
        :param capacity: The node count for the cluster. Default: 2
        :param enable_zones: Specifies if the purge operations are enabled. Based on the SKU, the number of zones allowed are different. Default: true
        :param identity_ids: A list of User Assigned Managed Identity IDs to be assigned to this Kusto Cluster.
        :param identity_type: The type of Managed Service Identity. Default: "SystemAssigned"
        :param maximum_instances: The maximum number of allowed instances. Must between 0 and 1000.
        :param minimum_instances: The minimum number of allowed instances. Must between 0 and 1000.
        :param public_network_access_enabled: Is the public network access enabled? Default: true
        :param purge_enabled: Specifies if the purge operations are enabled. Default: false
        :param resource_group: An optional reference to the resource group in which to deploy the Kusto Cluster. If not provided, the Kusto Cluster will be deployed in the default resource group.
        :param sku: The SKU of the Kusto Cluster. All the allowed values are defined in the ComputeSpecification class. Default: devtestExtraSmallDv2
        :param streaming_ingestion_enabled: Specifies if the streaming ingest is enabled. Default: true
        :param tags: A mapping of tags to assign to the Kusto.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9351a5a77b18fe94ed9d59955e81c4877c4006f903bf2ea22d8a9d6cd102e5a3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ClusterProps(
            name=name,
            auto_stop_enabled=auto_stop_enabled,
            capacity=capacity,
            enable_zones=enable_zones,
            identity_ids=identity_ids,
            identity_type=identity_type,
            maximum_instances=maximum_instances,
            minimum_instances=minimum_instances,
            public_network_access_enabled=public_network_access_enabled,
            purge_enabled=purge_enabled,
            resource_group=resource_group,
            sku=sku,
            streaming_ingestion_enabled=streaming_ingestion_enabled,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addDatabase")
    def add_database(
        self,
        *,
        kusto: "Cluster",
        name: builtins.str,
        hot_cache_period: typing.Optional[builtins.str] = None,
        soft_delete_period: typing.Optional[builtins.str] = None,
    ) -> "Database":
        '''Adds a new database to the Azure Kusto Cluster.

        This method creates a database within the Azure Data Explorer (Kusto) cluster, defined by the properties provided.
        A database in Kusto serves as a logical group to manage various tables and store data. It is essential for performing
        data analytics and running queries. The database configuration can include settings like hot cache and soft delete periods,
        which optimize query performance and manage data lifecycle according to specific requirements.

        :param kusto: The Azure Kusto cluster to which this database belongs.
        :param name: The name of the Kusto Database to create.
        :param hot_cache_period: The time the data that should be kept in cache for fast queries as ISO 8601 timespan. Default is unlimited.
        :param soft_delete_period: The time the data should be kept before it stops being accessible to queries as ISO 8601 timespan. Default is unlimited.

        :return:

        A ``Database`` object representing the newly created database within the Kusto cluster.

        Example usage::

        const myDatabase = myCluster.addDatabase({
        kusto: myKustoCluster,
        name: 'OperationalData',
        hotCachePeriod: 'P14D', // 14 days
        softDeletePeriod: 'P365D' // 1 year
        });

        This method facilitates the efficient setup and scaling of databases within an Azure Kusto cluster, allowing
        for complex data analytics operations across large datasets.
        '''
        database_props = DatabaseProps(
            kusto=kusto,
            name=name,
            hot_cache_period=hot_cache_period,
            soft_delete_period=soft_delete_period,
        )

        return typing.cast("Database", jsii.invoke(self, "addDatabase", [database_props]))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "ClusterProps":
        return typing.cast("ClusterProps", jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__016f667b6e3c9557d441729357d8e19f1db29ec4c5fa78c89b941b80e06da1a6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0eafdbeed8d0f571cae144cb65ce6bc8481d686eaa59bee4308fa65c8e66bac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroup", value)


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_kusto.ClusterProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "auto_stop_enabled": "autoStopEnabled",
        "capacity": "capacity",
        "enable_zones": "enableZones",
        "identity_ids": "identityIds",
        "identity_type": "identityType",
        "maximum_instances": "maximumInstances",
        "minimum_instances": "minimumInstances",
        "public_network_access_enabled": "publicNetworkAccessEnabled",
        "purge_enabled": "purgeEnabled",
        "resource_group": "resourceGroup",
        "sku": "sku",
        "streaming_ingestion_enabled": "streamingIngestionEnabled",
        "tags": "tags",
    },
)
class ClusterProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        auto_stop_enabled: typing.Optional[builtins.bool] = None,
        capacity: typing.Optional[jsii.Number] = None,
        enable_zones: typing.Optional[builtins.bool] = None,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        identity_type: typing.Optional[builtins.str] = None,
        maximum_instances: typing.Optional[jsii.Number] = None,
        minimum_instances: typing.Optional[jsii.Number] = None,
        public_network_access_enabled: typing.Optional[builtins.bool] = None,
        purge_enabled: typing.Optional[builtins.bool] = None,
        resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
        sku: typing.Optional["IComputeSpecification"] = None,
        streaming_ingestion_enabled: typing.Optional[builtins.bool] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param name: The name of the Kusto Cluster to create. Only 4-22 lowercase alphanumeric characters allowed, starting with a letter.
        :param auto_stop_enabled: Specifies if the cluster could be automatically stopped. (due to lack of data or no activity for many days). Default: true
        :param capacity: The node count for the cluster. Default: 2
        :param enable_zones: Specifies if the purge operations are enabled. Based on the SKU, the number of zones allowed are different. Default: true
        :param identity_ids: A list of User Assigned Managed Identity IDs to be assigned to this Kusto Cluster.
        :param identity_type: The type of Managed Service Identity. Default: "SystemAssigned"
        :param maximum_instances: The maximum number of allowed instances. Must between 0 and 1000.
        :param minimum_instances: The minimum number of allowed instances. Must between 0 and 1000.
        :param public_network_access_enabled: Is the public network access enabled? Default: true
        :param purge_enabled: Specifies if the purge operations are enabled. Default: false
        :param resource_group: An optional reference to the resource group in which to deploy the Kusto Cluster. If not provided, the Kusto Cluster will be deployed in the default resource group.
        :param sku: The SKU of the Kusto Cluster. All the allowed values are defined in the ComputeSpecification class. Default: devtestExtraSmallDv2
        :param streaming_ingestion_enabled: Specifies if the streaming ingest is enabled. Default: true
        :param tags: A mapping of tags to assign to the Kusto.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2193d533b05f247b87c19b0582d681f927729e68a936477af77a4950358cea65)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument auto_stop_enabled", value=auto_stop_enabled, expected_type=type_hints["auto_stop_enabled"])
            check_type(argname="argument capacity", value=capacity, expected_type=type_hints["capacity"])
            check_type(argname="argument enable_zones", value=enable_zones, expected_type=type_hints["enable_zones"])
            check_type(argname="argument identity_ids", value=identity_ids, expected_type=type_hints["identity_ids"])
            check_type(argname="argument identity_type", value=identity_type, expected_type=type_hints["identity_type"])
            check_type(argname="argument maximum_instances", value=maximum_instances, expected_type=type_hints["maximum_instances"])
            check_type(argname="argument minimum_instances", value=minimum_instances, expected_type=type_hints["minimum_instances"])
            check_type(argname="argument public_network_access_enabled", value=public_network_access_enabled, expected_type=type_hints["public_network_access_enabled"])
            check_type(argname="argument purge_enabled", value=purge_enabled, expected_type=type_hints["purge_enabled"])
            check_type(argname="argument resource_group", value=resource_group, expected_type=type_hints["resource_group"])
            check_type(argname="argument sku", value=sku, expected_type=type_hints["sku"])
            check_type(argname="argument streaming_ingestion_enabled", value=streaming_ingestion_enabled, expected_type=type_hints["streaming_ingestion_enabled"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if auto_stop_enabled is not None:
            self._values["auto_stop_enabled"] = auto_stop_enabled
        if capacity is not None:
            self._values["capacity"] = capacity
        if enable_zones is not None:
            self._values["enable_zones"] = enable_zones
        if identity_ids is not None:
            self._values["identity_ids"] = identity_ids
        if identity_type is not None:
            self._values["identity_type"] = identity_type
        if maximum_instances is not None:
            self._values["maximum_instances"] = maximum_instances
        if minimum_instances is not None:
            self._values["minimum_instances"] = minimum_instances
        if public_network_access_enabled is not None:
            self._values["public_network_access_enabled"] = public_network_access_enabled
        if purge_enabled is not None:
            self._values["purge_enabled"] = purge_enabled
        if resource_group is not None:
            self._values["resource_group"] = resource_group
        if sku is not None:
            self._values["sku"] = sku
        if streaming_ingestion_enabled is not None:
            self._values["streaming_ingestion_enabled"] = streaming_ingestion_enabled
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the Kusto Cluster to create.

        Only 4-22 lowercase alphanumeric characters allowed, starting with a letter.
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auto_stop_enabled(self) -> typing.Optional[builtins.bool]:
        '''Specifies if the cluster could be automatically stopped.

        (due to lack of data or no activity for many days).

        :default: true
        '''
        result = self._values.get("auto_stop_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def capacity(self) -> typing.Optional[jsii.Number]:
        '''The node count for the cluster.

        :default: 2
        '''
        result = self._values.get("capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enable_zones(self) -> typing.Optional[builtins.bool]:
        '''Specifies if the purge operations are enabled.

        Based on the SKU, the number of zones allowed are different.

        :default: true
        '''
        result = self._values.get("enable_zones")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def identity_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of User Assigned Managed Identity IDs to be assigned to this Kusto Cluster.'''
        result = self._values.get("identity_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def identity_type(self) -> typing.Optional[builtins.str]:
        '''The type of Managed Service Identity.

        :default: "SystemAssigned"
        '''
        result = self._values.get("identity_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maximum_instances(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of allowed instances.

        Must between 0 and 1000.
        '''
        result = self._values.get("maximum_instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minimum_instances(self) -> typing.Optional[jsii.Number]:
        '''The minimum number of allowed instances.

        Must between 0 and 1000.
        '''
        result = self._values.get("minimum_instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def public_network_access_enabled(self) -> typing.Optional[builtins.bool]:
        '''Is the public network access enabled?

        :default: true
        '''
        result = self._values.get("public_network_access_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def purge_enabled(self) -> typing.Optional[builtins.bool]:
        '''Specifies if the purge operations are enabled.

        :default: false
        '''
        result = self._values.get("purge_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def resource_group(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup]:
        '''An optional reference to the resource group in which to deploy the Kusto Cluster.

        If not provided, the Kusto Cluster will be deployed in the default resource group.
        '''
        result = self._values.get("resource_group")
        return typing.cast(typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup], result)

    @builtins.property
    def sku(self) -> typing.Optional["IComputeSpecification"]:
        '''The SKU of the Kusto Cluster.

        All the allowed values are defined in the ComputeSpecification class.

        :default: devtestExtraSmallDv2
        '''
        result = self._values.get("sku")
        return typing.cast(typing.Optional["IComputeSpecification"], result)

    @builtins.property
    def streaming_ingestion_enabled(self) -> typing.Optional[builtins.bool]:
        '''Specifies if the streaming ingest is enabled.

        :default: true
        '''
        result = self._values.get("streaming_ingestion_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A mapping of tags to assign to the Kusto.'''
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


class ComputeSpecification(
    metaclass=jsii.JSIIMeta,
    jsii_type="@microsoft/terraform-cdk-constructs.azure_kusto.ComputeSpecification",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.python.classproperty
    @jsii.member(jsii_name="computeOptimizedExtraLargeStandardD32dv4")
    def compute_optimized_extra_large_standard_d32dv4(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "computeOptimizedExtraLargeStandardD32dv4"))

    @compute_optimized_extra_large_standard_d32dv4.setter # type: ignore[no-redef]
    def compute_optimized_extra_large_standard_d32dv4(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d28bc42ddfa7643e7a57dc7b22c3b2fe40540af0fdb9672d6d903a7acbe167a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "computeOptimizedExtraLargeStandardD32dv4", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="computeOptimizedExtraLargeStandardD32dv5")
    def compute_optimized_extra_large_standard_d32dv5(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "computeOptimizedExtraLargeStandardD32dv5"))

    @compute_optimized_extra_large_standard_d32dv5.setter # type: ignore[no-redef]
    def compute_optimized_extra_large_standard_d32dv5(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__491679e1e5d5f66b6ea317330bb6e7336b7f966c7fc90c2ed8eb3234e9ac512e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "computeOptimizedExtraLargeStandardD32dv5", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="computeOptimizedExtraSmallD11v2")
    def compute_optimized_extra_small_d11v2(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "computeOptimizedExtraSmallD11v2"))

    @compute_optimized_extra_small_d11v2.setter # type: ignore[no-redef]
    def compute_optimized_extra_small_d11v2(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77eb537362eec21ba6718412d8c3423662535771156bc61307f441ec0abb2592)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "computeOptimizedExtraSmallD11v2", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="computeOptimizedExtraSmallStandardE2adsv5")
    def compute_optimized_extra_small_standard_e2adsv5(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "computeOptimizedExtraSmallStandardE2adsv5"))

    @compute_optimized_extra_small_standard_e2adsv5.setter # type: ignore[no-redef]
    def compute_optimized_extra_small_standard_e2adsv5(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5603ece543481c136b153a8cb27b7593b6a3f281a3ea3ca2af37dbe8d933678)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "computeOptimizedExtraSmallStandardE2adsv5", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="computeOptimizedExtraSmallStandardE2av4")
    def compute_optimized_extra_small_standard_e2av4(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "computeOptimizedExtraSmallStandardE2av4"))

    @compute_optimized_extra_small_standard_e2av4.setter # type: ignore[no-redef]
    def compute_optimized_extra_small_standard_e2av4(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__500bf6f2650fa0047eb153aa94e146ef9a6aa0ee69e6e7ed46294486885fec4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "computeOptimizedExtraSmallStandardE2av4", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="computeOptimizedExtraSmallStandardE2dv4")
    def compute_optimized_extra_small_standard_e2dv4(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "computeOptimizedExtraSmallStandardE2dv4"))

    @compute_optimized_extra_small_standard_e2dv4.setter # type: ignore[no-redef]
    def compute_optimized_extra_small_standard_e2dv4(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__145ea1ef488b37ce2baa27d5a14a83e0a4331a5a46903710a6f204e50acdfb24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "computeOptimizedExtraSmallStandardE2dv4", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="computeOptimizedExtraSmallStandardE2dv5")
    def compute_optimized_extra_small_standard_e2dv5(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "computeOptimizedExtraSmallStandardE2dv5"))

    @compute_optimized_extra_small_standard_e2dv5.setter # type: ignore[no-redef]
    def compute_optimized_extra_small_standard_e2dv5(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83ed6772a0fedc491b2c2a8783b6bd6f5d802c6a2b6ea2b17977242710844fe1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "computeOptimizedExtraSmallStandardE2dv5", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="computeOptimizedIsolatedStandardE64iv3")
    def compute_optimized_isolated_standard_e64iv3(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "computeOptimizedIsolatedStandardE64iv3"))

    @compute_optimized_isolated_standard_e64iv3.setter # type: ignore[no-redef]
    def compute_optimized_isolated_standard_e64iv3(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cab6dd2c47a3916511b1a080ce66a9afc74db45d5b11fbc945ef2bd489c2ec7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "computeOptimizedIsolatedStandardE64iv3", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="computeOptimizedIsolatedStandardE80idsv4")
    def compute_optimized_isolated_standard_e80idsv4(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "computeOptimizedIsolatedStandardE80idsv4"))

    @compute_optimized_isolated_standard_e80idsv4.setter # type: ignore[no-redef]
    def compute_optimized_isolated_standard_e80idsv4(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3beae95e3a51e99fa82cc09a79cb7896427eea2cb3afc432267560a4606e62d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "computeOptimizedIsolatedStandardE80idsv4", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="computeOptimizedLargeD14v2")
    def compute_optimized_large_d14v2(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "computeOptimizedLargeD14v2"))

    @compute_optimized_large_d14v2.setter # type: ignore[no-redef]
    def compute_optimized_large_d14v2(cls, value: "IComputeSpecification") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f89ed19a43cd5ba674fbc00537182136f66729b1167b29b4ddc20a21cc112c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "computeOptimizedLargeD14v2", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="computeOptimizedLargeD16dv5")
    def compute_optimized_large_d16dv5(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "computeOptimizedLargeD16dv5"))

    @compute_optimized_large_d16dv5.setter # type: ignore[no-redef]
    def compute_optimized_large_d16dv5(cls, value: "IComputeSpecification") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47a147acacc66283572040d97c91a616298f5399fcaaab9b7cb60e0b014b4263)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "computeOptimizedLargeD16dv5", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="computeOptimizedLargeStandardE16adsv5")
    def compute_optimized_large_standard_e16adsv5(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "computeOptimizedLargeStandardE16adsv5"))

    @compute_optimized_large_standard_e16adsv5.setter # type: ignore[no-redef]
    def compute_optimized_large_standard_e16adsv5(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f00c54c46cc8d3c4bb4c3ae023dd28b84f42b0b1dc1cb9bdfd974cbc9d3d4e5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "computeOptimizedLargeStandardE16adsv5", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="computeOptimizedLargeStandardE16av4")
    def compute_optimized_large_standard_e16av4(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "computeOptimizedLargeStandardE16av4"))

    @compute_optimized_large_standard_e16av4.setter # type: ignore[no-redef]
    def compute_optimized_large_standard_e16av4(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49d336bba3f279a727be16e19551ce732a0d1f63411173852559fc8b3af8ca95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "computeOptimizedLargeStandardE16av4", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="computeOptimizedLargeStandardE16dv4")
    def compute_optimized_large_standard_e16dv4(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "computeOptimizedLargeStandardE16dv4"))

    @compute_optimized_large_standard_e16dv4.setter # type: ignore[no-redef]
    def compute_optimized_large_standard_e16dv4(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8ec908d799d81f3d1978c8a6d7a4127d51b62b79da69d4a464fe656cfb43577)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "computeOptimizedLargeStandardE16dv4", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="computeOptimizedLargeStandardE16dv5")
    def compute_optimized_large_standard_e16dv5(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "computeOptimizedLargeStandardE16dv5"))

    @compute_optimized_large_standard_e16dv5.setter # type: ignore[no-redef]
    def compute_optimized_large_standard_e16dv5(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cc0245c04e66c0a1c1610c2e808cb7ba55fc64adf0434fd6fd3ec0d34646bad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "computeOptimizedLargeStandardE16dv5", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="computeOptimizedMediumD13v2")
    def compute_optimized_medium_d13v2(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "computeOptimizedMediumD13v2"))

    @compute_optimized_medium_d13v2.setter # type: ignore[no-redef]
    def compute_optimized_medium_d13v2(cls, value: "IComputeSpecification") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84328743cdc1fd43f3521b372c47364148ce7bee1d58f325ae6c20b305550f24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "computeOptimizedMediumD13v2", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="computeOptimizedMediumStandardE8adsv5")
    def compute_optimized_medium_standard_e8adsv5(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "computeOptimizedMediumStandardE8adsv5"))

    @compute_optimized_medium_standard_e8adsv5.setter # type: ignore[no-redef]
    def compute_optimized_medium_standard_e8adsv5(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62a9488a15813bd82155aefa8ca8ec90103bac9070f8be44814ea00f4b1c4caa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "computeOptimizedMediumStandardE8adsv5", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="computeOptimizedMediumStandardE8av4")
    def compute_optimized_medium_standard_e8av4(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "computeOptimizedMediumStandardE8av4"))

    @compute_optimized_medium_standard_e8av4.setter # type: ignore[no-redef]
    def compute_optimized_medium_standard_e8av4(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0f9c5848183743c4eae1801a1811bacd51f05e81a3fa652c4909862a261f421)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "computeOptimizedMediumStandardE8av4", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="computeOptimizedMediumStandardE8dv4")
    def compute_optimized_medium_standard_e8dv4(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "computeOptimizedMediumStandardE8dv4"))

    @compute_optimized_medium_standard_e8dv4.setter # type: ignore[no-redef]
    def compute_optimized_medium_standard_e8dv4(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33098d3662c412b5f20e8629e47494f7404eb182c1a5e19ea557259bf1c68523)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "computeOptimizedMediumStandardE8dv4", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="computeOptimizedMediumStandardE8dv5")
    def compute_optimized_medium_standard_e8dv5(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "computeOptimizedMediumStandardE8dv5"))

    @compute_optimized_medium_standard_e8dv5.setter # type: ignore[no-redef]
    def compute_optimized_medium_standard_e8dv5(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bbdc7dda046321c937d1b316fe355857857c56591d6720244638772f3220796)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "computeOptimizedMediumStandardE8dv5", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="computeOptimizedSmallD12v2")
    def compute_optimized_small_d12v2(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "computeOptimizedSmallD12v2"))

    @compute_optimized_small_d12v2.setter # type: ignore[no-redef]
    def compute_optimized_small_d12v2(cls, value: "IComputeSpecification") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d753371995aedbeef0609fc7cc491932858c1c265b720b2424448ac3985ba3f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "computeOptimizedSmallD12v2", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="computeOptimizedSmallStandardE4adsv5")
    def compute_optimized_small_standard_e4adsv5(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "computeOptimizedSmallStandardE4adsv5"))

    @compute_optimized_small_standard_e4adsv5.setter # type: ignore[no-redef]
    def compute_optimized_small_standard_e4adsv5(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__554870a2811a35dc1db9ef6f31f48036973e53caf7567005112037252c773d24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "computeOptimizedSmallStandardE4adsv5", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="computeOptimizedSmallStandardE4av4")
    def compute_optimized_small_standard_e4av4(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "computeOptimizedSmallStandardE4av4"))

    @compute_optimized_small_standard_e4av4.setter # type: ignore[no-redef]
    def compute_optimized_small_standard_e4av4(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__571a041fdbe0f711ebdc4c2c1fa60f092cf4cf47c42636604deccf45a06ec475)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "computeOptimizedSmallStandardE4av4", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="computeOptimizedSmallStandardE4dv4")
    def compute_optimized_small_standard_e4dv4(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "computeOptimizedSmallStandardE4dv4"))

    @compute_optimized_small_standard_e4dv4.setter # type: ignore[no-redef]
    def compute_optimized_small_standard_e4dv4(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c53821b5360e6975719bdb3665dd34cbfedee0c16aa2a459fe32f490067ca3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "computeOptimizedSmallStandardE4dv4", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="computeOptimizedSmallStandardE4dv5")
    def compute_optimized_small_standard_e4dv5(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "computeOptimizedSmallStandardE4dv5"))

    @compute_optimized_small_standard_e4dv5.setter # type: ignore[no-redef]
    def compute_optimized_small_standard_e4dv5(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5e9b81f5d5e46f253dcf8e81417a6f2ef2d448bbd12de7b5699f32e0f848522)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "computeOptimizedSmallStandardE4dv5", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="devtestExtraSmallDv2")
    def devtest_extra_small_dv2(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "devtestExtraSmallDv2"))

    @devtest_extra_small_dv2.setter # type: ignore[no-redef]
    def devtest_extra_small_dv2(cls, value: "IComputeSpecification") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87aeefe6880ea065d18a136ef053b6f3ffe4a7234ab7e31cf756fb794b873ede)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "devtestExtraSmallDv2", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="devtestExtraSmallEav4")
    def devtest_extra_small_eav4(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "devtestExtraSmallEav4"))

    @devtest_extra_small_eav4.setter # type: ignore[no-redef]
    def devtest_extra_small_eav4(cls, value: "IComputeSpecification") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b1a7acb1f01bdc158a9f07c2854e5bdca659fcfbaee627fa617dc6f351b6c0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "devtestExtraSmallEav4", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="standardE16asv44TBPS")
    def standard_e16asv44_tbps(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "standardE16asv44TBPS"))

    @standard_e16asv44_tbps.setter # type: ignore[no-redef]
    def standard_e16asv44_tbps(cls, value: "IComputeSpecification") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5981d4cbfc0a70693c4660d945c36f8bed554fe4af0d988befc8ef1c5503e8e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "standardE16asv44TBPS", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="standardE16sv54TBPS")
    def standard_e16sv54_tbps(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "standardE16sv54TBPS"))

    @standard_e16sv54_tbps.setter # type: ignore[no-redef]
    def standard_e16sv54_tbps(cls, value: "IComputeSpecification") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec1839e4a4e2396aa56ecd5e8fd75a2db036c3eb450e652b0d625c977bdc3f7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "standardE16sv54TBPS", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="storageOptimizedExtraLargeStandardL32asv3")
    def storage_optimized_extra_large_standard_l32asv3(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "storageOptimizedExtraLargeStandardL32asv3"))

    @storage_optimized_extra_large_standard_l32asv3.setter # type: ignore[no-redef]
    def storage_optimized_extra_large_standard_l32asv3(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2367e2a40bbb41fdb6f058328ce4a7a16b004feb68f343eee5cccd0c1c82f95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "storageOptimizedExtraLargeStandardL32asv3", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="storageOptimizedExtraLargeStandardL32sv3")
    def storage_optimized_extra_large_standard_l32sv3(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "storageOptimizedExtraLargeStandardL32sv3"))

    @storage_optimized_extra_large_standard_l32sv3.setter # type: ignore[no-redef]
    def storage_optimized_extra_large_standard_l32sv3(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60020ae4d74146b9139e0560bec93d3a5751d3311c70154df24f76e59ce5cff0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "storageOptimizedExtraLargeStandardL32sv3", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="storageOptimizedLargeStandardDS14v24TBPS")
    def storage_optimized_large_standard_ds14v24_tbps(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "storageOptimizedLargeStandardDS14v24TBPS"))

    @storage_optimized_large_standard_ds14v24_tbps.setter # type: ignore[no-redef]
    def storage_optimized_large_standard_ds14v24_tbps(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fe3355c57400165db03f7cff46c3b336ce73cec0811ae3271132adac3a6511c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "storageOptimizedLargeStandardDS14v24TBPS", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="storageOptimizedLargeStandardE16asv43TBPS")
    def storage_optimized_large_standard_e16asv43_tbps(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "storageOptimizedLargeStandardE16asv43TBPS"))

    @storage_optimized_large_standard_e16asv43_tbps.setter # type: ignore[no-redef]
    def storage_optimized_large_standard_e16asv43_tbps(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__605058e16727233c893056961190acce813905a53361f2b424a06e374d0149cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "storageOptimizedLargeStandardE16asv43TBPS", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="storageOptimizedLargeStandardE16asv53TBPS")
    def storage_optimized_large_standard_e16asv53_tbps(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "storageOptimizedLargeStandardE16asv53TBPS"))

    @storage_optimized_large_standard_e16asv53_tbps.setter # type: ignore[no-redef]
    def storage_optimized_large_standard_e16asv53_tbps(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfacb476c4c817150590d0cef83dadd51fd2ae503b2f60bb76b0f3ffc00974ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "storageOptimizedLargeStandardE16asv53TBPS", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="storageOptimizedLargeStandardE16asv54TBPS")
    def storage_optimized_large_standard_e16asv54_tbps(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "storageOptimizedLargeStandardE16asv54TBPS"))

    @storage_optimized_large_standard_e16asv54_tbps.setter # type: ignore[no-redef]
    def storage_optimized_large_standard_e16asv54_tbps(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6804badc2b1b15759763228696b72b565144f2c35dd7d6833f221e129dcc67ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "storageOptimizedLargeStandardE16asv54TBPS", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="storageOptimizedLargeStandardE16sv43TBPS")
    def storage_optimized_large_standard_e16sv43_tbps(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "storageOptimizedLargeStandardE16sv43TBPS"))

    @storage_optimized_large_standard_e16sv43_tbps.setter # type: ignore[no-redef]
    def storage_optimized_large_standard_e16sv43_tbps(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__273fedecc160c301dcd5a4b666175e5994e547fb07231e1a3a6af194be264a9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "storageOptimizedLargeStandardE16sv43TBPS", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="storageOptimizedLargeStandardE16sv44TBPS")
    def storage_optimized_large_standard_e16sv44_tbps(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "storageOptimizedLargeStandardE16sv44TBPS"))

    @storage_optimized_large_standard_e16sv44_tbps.setter # type: ignore[no-redef]
    def storage_optimized_large_standard_e16sv44_tbps(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a5cb7e4bb806ffecd608d3d1fd015be553de0fbe38f487979725d7b982d6492)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "storageOptimizedLargeStandardE16sv44TBPS", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="storageOptimizedLargeStandardEC16adsv5")
    def storage_optimized_large_standard_ec16adsv5(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "storageOptimizedLargeStandardEC16adsv5"))

    @storage_optimized_large_standard_ec16adsv5.setter # type: ignore[no-redef]
    def storage_optimized_large_standard_ec16adsv5(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbc8cfeb76e5a834c6bff4768f7e44f416d5cd1da849976bb9384e3cd0c9b48a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "storageOptimizedLargeStandardEC16adsv5", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="storageOptimizedLargeStandardEC16asv53TBPS")
    def storage_optimized_large_standard_ec16asv53_tbps(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "storageOptimizedLargeStandardEC16asv53TBPS"))

    @storage_optimized_large_standard_ec16asv53_tbps.setter # type: ignore[no-redef]
    def storage_optimized_large_standard_ec16asv53_tbps(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c3b1cf5e578256da17f5e4d172d7cfec965c42b83a293430e0728065b2b5987)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "storageOptimizedLargeStandardEC16asv53TBPS", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="storageOptimizedLargeStandardEC16asv54TBPS")
    def storage_optimized_large_standard_ec16asv54_tbps(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "storageOptimizedLargeStandardEC16asv54TBPS"))

    @storage_optimized_large_standard_ec16asv54_tbps.setter # type: ignore[no-redef]
    def storage_optimized_large_standard_ec16asv54_tbps(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__698f243198e7e4605368bf6e63564011b34b95f5b1cfcb05b7607ab4f5d73db4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "storageOptimizedLargeStandardEC16asv54TBPS", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="storageOptimizedLargeStandardL16asv3")
    def storage_optimized_large_standard_l16asv3(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "storageOptimizedLargeStandardL16asv3"))

    @storage_optimized_large_standard_l16asv3.setter # type: ignore[no-redef]
    def storage_optimized_large_standard_l16asv3(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe3a464457225e9a181eb1b38742358464b14a345665ed233d1b8c92a98e3eb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "storageOptimizedLargeStandardL16asv3", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="storageOptimizedLargeStandardL16sv3")
    def storage_optimized_large_standard_l16sv3(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "storageOptimizedLargeStandardL16sv3"))

    @storage_optimized_large_standard_l16sv3.setter # type: ignore[no-redef]
    def storage_optimized_large_standard_l16sv3(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdec81cb897f3759e538f754b107dfee96a01862fa921b4c6fb67439e3db9bfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "storageOptimizedLargeStandardL16sv3", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="storageOptimizedLargestorageOptimizedLargeStandardE16sv53TBPS")
    def storage_optimized_largestorage_optimized_large_standard_e16sv53_tbps(
        cls,
    ) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "storageOptimizedLargestorageOptimizedLargeStandardE16sv53TBPS"))

    @storage_optimized_largestorage_optimized_large_standard_e16sv53_tbps.setter # type: ignore[no-redef]
    def storage_optimized_largestorage_optimized_large_standard_e16sv53_tbps(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3b43b80db7d343882627adf5d0664dc253a58941c2855927ba16d0dab122bbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "storageOptimizedLargestorageOptimizedLargeStandardE16sv53TBPS", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="storageOptimizedMediumSStandardE8sv41TBPS")
    def storage_optimized_medium_s_standard_e8sv41_tbps(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "storageOptimizedMediumSStandardE8sv41TBPS"))

    @storage_optimized_medium_s_standard_e8sv41_tbps.setter # type: ignore[no-redef]
    def storage_optimized_medium_s_standard_e8sv41_tbps(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bda2ae2cf299e55b4bb97e0b4b451b9f166d5796bff0af08d9fba7ea08b3114)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "storageOptimizedMediumSStandardE8sv41TBPS", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="storageOptimizedMediumStandardDS13v21TBPS")
    def storage_optimized_medium_standard_ds13v21_tbps(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "storageOptimizedMediumStandardDS13v21TBPS"))

    @storage_optimized_medium_standard_ds13v21_tbps.setter # type: ignore[no-redef]
    def storage_optimized_medium_standard_ds13v21_tbps(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__420d1f4d49d5cf46fd19b370aa26ecfaa5614d23fbace9d92fc1ecd4b3c00ac2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "storageOptimizedMediumStandardDS13v21TBPS", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="storageOptimizedMediumStandardDS13v22TBPS")
    def storage_optimized_medium_standard_ds13v22_tbps(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "storageOptimizedMediumStandardDS13v22TBPS"))

    @storage_optimized_medium_standard_ds13v22_tbps.setter # type: ignore[no-redef]
    def storage_optimized_medium_standard_ds13v22_tbps(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__359a79b6f609df14594fd41f433c9701420d5b544ee358d2b594b24855f457a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "storageOptimizedMediumStandardDS13v22TBPS", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="storageOptimizedMediumStandardE8asv41TBPS")
    def storage_optimized_medium_standard_e8asv41_tbps(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "storageOptimizedMediumStandardE8asv41TBPS"))

    @storage_optimized_medium_standard_e8asv41_tbps.setter # type: ignore[no-redef]
    def storage_optimized_medium_standard_e8asv41_tbps(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c62c82459dcdc9fe710371a7d54a2471a21e0ec21a1b1550ada4192d9ecc0969)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "storageOptimizedMediumStandardE8asv41TBPS", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="storageOptimizedMediumStandardE8asv42TBPS")
    def storage_optimized_medium_standard_e8asv42_tbps(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "storageOptimizedMediumStandardE8asv42TBPS"))

    @storage_optimized_medium_standard_e8asv42_tbps.setter # type: ignore[no-redef]
    def storage_optimized_medium_standard_e8asv42_tbps(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44ecd5be5a18a5658ea782612ad64d06b4d60b13f1c430f1cd96c34e9d28f37d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "storageOptimizedMediumStandardE8asv42TBPS", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="storageOptimizedMediumStandardE8asv51TBPS")
    def storage_optimized_medium_standard_e8asv51_tbps(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "storageOptimizedMediumStandardE8asv51TBPS"))

    @storage_optimized_medium_standard_e8asv51_tbps.setter # type: ignore[no-redef]
    def storage_optimized_medium_standard_e8asv51_tbps(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e09b2c675d2077bfce0647633b98e3f3e78c1f775ebc6c6a8799d8f651fdb3dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "storageOptimizedMediumStandardE8asv51TBPS", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="storageOptimizedMediumStandardE8asv52TBPS")
    def storage_optimized_medium_standard_e8asv52_tbps(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "storageOptimizedMediumStandardE8asv52TBPS"))

    @storage_optimized_medium_standard_e8asv52_tbps.setter # type: ignore[no-redef]
    def storage_optimized_medium_standard_e8asv52_tbps(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__661d71792710b5855c4165f31e9f042b74ea64876d2449146e6e21e260a8bbb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "storageOptimizedMediumStandardE8asv52TBPS", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="storageOptimizedMediumStandardE8sv42TBPS")
    def storage_optimized_medium_standard_e8sv42_tbps(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "storageOptimizedMediumStandardE8sv42TBPS"))

    @storage_optimized_medium_standard_e8sv42_tbps.setter # type: ignore[no-redef]
    def storage_optimized_medium_standard_e8sv42_tbps(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79878b4a4ce2a2645dd737112c517c6a16213a899a7c74005ff4c368b59866ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "storageOptimizedMediumStandardE8sv42TBPS", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="storageOptimizedMediumStandardE8sv51TBPS")
    def storage_optimized_medium_standard_e8sv51_tbps(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "storageOptimizedMediumStandardE8sv51TBPS"))

    @storage_optimized_medium_standard_e8sv51_tbps.setter # type: ignore[no-redef]
    def storage_optimized_medium_standard_e8sv51_tbps(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd579726c203b204dfe6348e1de12469592523536ccbcc67c1cd99eaae9a10bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "storageOptimizedMediumStandardE8sv51TBPS", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="storageOptimizedMediumStandardE8sv52TBPS")
    def storage_optimized_medium_standard_e8sv52_tbps(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "storageOptimizedMediumStandardE8sv52TBPS"))

    @storage_optimized_medium_standard_e8sv52_tbps.setter # type: ignore[no-redef]
    def storage_optimized_medium_standard_e8sv52_tbps(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fde24ac4875b4011de2aaee9afbdf2e945d3d754b7299b9a1d480c4389715660)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "storageOptimizedMediumStandardE8sv52TBPS", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="storageOptimizedMediumStandardEC8adsv5")
    def storage_optimized_medium_standard_ec8adsv5(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "storageOptimizedMediumStandardEC8adsv5"))

    @storage_optimized_medium_standard_ec8adsv5.setter # type: ignore[no-redef]
    def storage_optimized_medium_standard_ec8adsv5(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66130241f740346fab5d6d15b4968c0e847f98f8d1aadc0ce857212dbf902ba6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "storageOptimizedMediumStandardEC8adsv5", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="storageOptimizedMediumStandardEC8asv51TBPS")
    def storage_optimized_medium_standard_ec8asv51_tbps(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "storageOptimizedMediumStandardEC8asv51TBPS"))

    @storage_optimized_medium_standard_ec8asv51_tbps.setter # type: ignore[no-redef]
    def storage_optimized_medium_standard_ec8asv51_tbps(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__406614a6d8937c8fd51c5c7344cae3d4034d16619cc829e05579cfc38cc1ffa0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "storageOptimizedMediumStandardEC8asv51TBPS", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="storageOptimizedMediumStandardEC8asv52TBPS")
    def storage_optimized_medium_standard_ec8asv52_tbps(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "storageOptimizedMediumStandardEC8asv52TBPS"))

    @storage_optimized_medium_standard_ec8asv52_tbps.setter # type: ignore[no-redef]
    def storage_optimized_medium_standard_ec8asv52_tbps(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__029897ed5e97b19845a843000c84f1d5ee4db6c27019cf57353cd64297f54b74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "storageOptimizedMediumStandardEC8asv52TBPS", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="storageOptimizedMediumStandardL8asv3")
    def storage_optimized_medium_standard_l8asv3(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "storageOptimizedMediumStandardL8asv3"))

    @storage_optimized_medium_standard_l8asv3.setter # type: ignore[no-redef]
    def storage_optimized_medium_standard_l8asv3(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b67e2923606639ec84c6669011a135485ceb89a98b86dcc9e6b519118dc48cdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "storageOptimizedMediumStandardL8asv3", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="storageOptimizedMediumStandardL8sv3")
    def storage_optimized_medium_standard_l8sv3(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "storageOptimizedMediumStandardL8sv3"))

    @storage_optimized_medium_standard_l8sv3.setter # type: ignore[no-redef]
    def storage_optimized_medium_standard_l8sv3(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0eafa0040198c4d9e61b08dad813396d4af8595389f11675fd02c1765b2c18c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "storageOptimizedMediumStandardL8sv3", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="storageOptimizedStandardDS14v23TBPS")
    def storage_optimized_standard_ds14v23_tbps(cls) -> "IComputeSpecification":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IComputeSpecification", jsii.sget(cls, "storageOptimizedStandardDS14v23TBPS"))

    @storage_optimized_standard_ds14v23_tbps.setter # type: ignore[no-redef]
    def storage_optimized_standard_ds14v23_tbps(
        cls,
        value: "IComputeSpecification",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc7f37736e3c057879f174d1e7466c6e75a9d76fac9b3c656eb782feb110e3cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "storageOptimizedStandardDS14v23TBPS", value)


class Database(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@microsoft/terraform-cdk-constructs.azure_kusto.Database",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        kusto: Cluster,
        name: builtins.str,
        hot_cache_period: typing.Optional[builtins.str] = None,
        soft_delete_period: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Represents a Kusto Database within an Azure Kusto Cluster.

        This class is responsible for the creation and management of a database in Azure Data Explorer (Kusto),
        which stores data tables and provides a query engine. A Kusto database is a logical group of tables
        and is associated with a specific Kusto cluster. The database supports configurations such as
        hot cache period and soft delete period to optimize performance and data retention according to
        specific workload requirements.

        :param scope: - The scope in which to define this construct, typically representing the Cloud Development Kit (CDK) stack.
        :param id: - The unique identifier for this instance of the Kusto database.
        :param kusto: The Azure Kusto cluster to which this database belongs.
        :param name: The name of the Kusto Database to create.
        :param hot_cache_period: The time the data that should be kept in cache for fast queries as ISO 8601 timespan. Default is unlimited.
        :param soft_delete_period: The time the data should be kept before it stops being accessible to queries as ISO 8601 timespan. Default is unlimited.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bb7e049648a84a8e486219349a602116b3098bd3ad3df2bebff015ca0877100)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        kusto_db_props = DatabaseProps(
            kusto=kusto,
            name=name,
            hot_cache_period=hot_cache_period,
            soft_delete_period=soft_delete_period,
        )

        jsii.create(self.__class__, self, [scope, id, kusto_db_props])

    @jsii.member(jsii_name="addPermission")
    def add_permission(
        self,
        *,
        name: builtins.str,
        principal_id: builtins.str,
        principal_type: builtins.str,
        role: builtins.str,
        tenant_id: builtins.str,
    ) -> None:
        '''Adds a database principal assignment in the Kusto cluster, assigning specified access rights to a principal.

        This method is used to grant access permissions to a specific user, group, or service principal within an Azure Active Directory.
        These permissions determine the level of access that the principal has over the Kusto database, such as viewing, ingesting, or managing data.
        The assignment is made by creating a KustoDatabasePrincipalAssignment resource, specifying the principal details and the type of role
        they should assume.

        :param name: The name of the kusto principal assignment.
        :param principal_id: The object id of the principal to assign to Kusto Database.
        :param principal_type: The type of the principal. Valid values include App, Group, User.
        :param role: The database role assigned to the principal. Valid values include Admin, Ingestor, Monitor, UnrestrictedViewer, User and Viewer.
        :param tenant_id: The tenant id in which the principal resides.
        '''
        kusto_database_access_props = DatabaseAccessProps(
            name=name,
            principal_id=principal_id,
            principal_type=principal_type,
            role=role,
            tenant_id=tenant_id,
        )

        return typing.cast(None, jsii.invoke(self, "addPermission", [kusto_database_access_props]))

    @jsii.member(jsii_name="addScript")
    def add_script(
        self,
        script_name: builtins.str,
        script_content: builtins.str,
    ) -> None:
        '''Adds and executes a control command or script within the Kusto database.

        This method facilitates the execution of Kusto Query Language (KQL) scripts or control commands within the specified
        Kusto database. Scripts can perform a variety of functions, from schema modifications, like adding new tables or altering
        existing ones, to data management operations, such as data ingestion or cleanup tasks. Each script is executed as a
        KustoScript resource, which ensures that the script is applied correctly and atomically to the database.

        :param script_name: - A unique name for the script, which helps in identifying the script resource within the deployment.
        :param script_content: - The KQL script or control command to be executed. This should be a valid KQL command string. Example usage:: myDatabase.addScript('InitializeSalesTable', ` .create table SalesData (TransactionId: int, TransactionDate: datetime, Amount: real) .alter-merge table SalesData policy retentionsoftdelete = 365d `); This method will create a ``KustoScript`` resource that encapsulates the command, ensuring it is executed against the database, and is tracked as part of the resource management within Azure.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1fe44cb03828c945451d0676f440fb81bfde50a755b1c3f57f0bb0842fe7c9a)
            check_type(argname="argument script_name", value=script_name, expected_type=type_hints["script_name"])
            check_type(argname="argument script_content", value=script_content, expected_type=type_hints["script_content"])
        return typing.cast(None, jsii.invoke(self, "addScript", [script_name, script_content]))

    @jsii.member(jsii_name="addTable")
    def add_table(
        self,
        table_name: builtins.str,
        table_schema: typing.Sequence[typing.Union["TableSchemaProps", typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''Adds a new table to an existing Azure Kusto database.

        This method creates a table within the specified Kusto database using a given schema. Tables in Kusto store structured data with
        defined columns and types, which are crucial for storing and querying large datasets efficiently. The method constructs a Kusto
        Data Explorer control command to create the table and then executes this command within the context of the database.

        :param table_name: - The name of the table to create, which must be unique within the database.
        :param table_schema: - An array of schema properties defining the columns of the table, including column names and their data types. Example usage:: myDatabase.addTable('SalesData', [ { columnName: 'TransactionId', columnType: 'int' }, { columnName: 'TransactionDate', columnType: 'datetime' }, { columnName: 'Amount', columnType: 'real' } ]); This method constructs the command to create the table and applies it directly within the Kusto database, ensuring the table is ready for data ingestion and querying.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a4e5427243f22a5b893f1d0e1401bbdfc379be8c67e11c64d99fca0794aadcb)
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            check_type(argname="argument table_schema", value=table_schema, expected_type=type_hints["table_schema"])
        return typing.cast(None, jsii.invoke(self, "addTable", [table_name, table_schema]))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="kustoDbProps")
    def kusto_db_props(self) -> "DatabaseProps":
        return typing.cast("DatabaseProps", jsii.get(self, "kustoDbProps"))

    @builtins.property
    @jsii.member(jsii_name="kustoProps")
    def kusto_props(self) -> ClusterProps:
        return typing.cast(ClusterProps, jsii.get(self, "kustoProps"))

    @builtins.property
    @jsii.member(jsii_name="rg")
    def rg(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rg"))


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_kusto.DatabaseAccessProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "principal_id": "principalId",
        "principal_type": "principalType",
        "role": "role",
        "tenant_id": "tenantId",
    },
)
class DatabaseAccessProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        principal_id: builtins.str,
        principal_type: builtins.str,
        role: builtins.str,
        tenant_id: builtins.str,
    ) -> None:
        '''
        :param name: The name of the kusto principal assignment.
        :param principal_id: The object id of the principal to assign to Kusto Database.
        :param principal_type: The type of the principal. Valid values include App, Group, User.
        :param role: The database role assigned to the principal. Valid values include Admin, Ingestor, Monitor, UnrestrictedViewer, User and Viewer.
        :param tenant_id: The tenant id in which the principal resides.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8fae0aa1717ffd90e4aa97235cbcc92728a68e132f7574a341b1ff0026de14b)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument principal_id", value=principal_id, expected_type=type_hints["principal_id"])
            check_type(argname="argument principal_type", value=principal_type, expected_type=type_hints["principal_type"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument tenant_id", value=tenant_id, expected_type=type_hints["tenant_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "principal_id": principal_id,
            "principal_type": principal_type,
            "role": role,
            "tenant_id": tenant_id,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the kusto principal assignment.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def principal_id(self) -> builtins.str:
        '''The object id of the principal to assign to Kusto Database.'''
        result = self._values.get("principal_id")
        assert result is not None, "Required property 'principal_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def principal_type(self) -> builtins.str:
        '''The type of the principal.

        Valid values include App, Group, User.
        '''
        result = self._values.get("principal_type")
        assert result is not None, "Required property 'principal_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role(self) -> builtins.str:
        '''The database role assigned to the principal.

        Valid values include Admin, Ingestor, Monitor, UnrestrictedViewer, User and Viewer.
        '''
        result = self._values.get("role")
        assert result is not None, "Required property 'role' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tenant_id(self) -> builtins.str:
        '''The tenant id in which the principal resides.'''
        result = self._values.get("tenant_id")
        assert result is not None, "Required property 'tenant_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseAccessProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_kusto.DatabaseProps",
    jsii_struct_bases=[],
    name_mapping={
        "kusto": "kusto",
        "name": "name",
        "hot_cache_period": "hotCachePeriod",
        "soft_delete_period": "softDeletePeriod",
    },
)
class DatabaseProps:
    def __init__(
        self,
        *,
        kusto: Cluster,
        name: builtins.str,
        hot_cache_period: typing.Optional[builtins.str] = None,
        soft_delete_period: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kusto: The Azure Kusto cluster to which this database belongs.
        :param name: The name of the Kusto Database to create.
        :param hot_cache_period: The time the data that should be kept in cache for fast queries as ISO 8601 timespan. Default is unlimited.
        :param soft_delete_period: The time the data should be kept before it stops being accessible to queries as ISO 8601 timespan. Default is unlimited.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e3ad0dca05483428a48ef2f19255859d30897ae7656132b3c3fb95e3c87dd41)
            check_type(argname="argument kusto", value=kusto, expected_type=type_hints["kusto"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument hot_cache_period", value=hot_cache_period, expected_type=type_hints["hot_cache_period"])
            check_type(argname="argument soft_delete_period", value=soft_delete_period, expected_type=type_hints["soft_delete_period"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kusto": kusto,
            "name": name,
        }
        if hot_cache_period is not None:
            self._values["hot_cache_period"] = hot_cache_period
        if soft_delete_period is not None:
            self._values["soft_delete_period"] = soft_delete_period

    @builtins.property
    def kusto(self) -> Cluster:
        '''The Azure Kusto cluster to which this database belongs.'''
        result = self._values.get("kusto")
        assert result is not None, "Required property 'kusto' is missing"
        return typing.cast(Cluster, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the Kusto Database to create.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hot_cache_period(self) -> typing.Optional[builtins.str]:
        '''The time the data that should be kept in cache for fast queries as ISO 8601 timespan.

        Default is unlimited.
        '''
        result = self._values.get("hot_cache_period")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def soft_delete_period(self) -> typing.Optional[builtins.str]:
        '''The time the data should be kept before it stops being accessible to queries as ISO 8601 timespan.

        Default is unlimited.
        '''
        result = self._values.get("soft_delete_period")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_kusto.IComputeSpecification"
)
class IComputeSpecification(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="availibleZones")
    def availible_zones(self) -> typing.List[builtins.str]:
        ...

    @availible_zones.setter
    def availible_zones(self, value: typing.List[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="cache")
    def cache(self) -> jsii.Number:
        ...

    @cache.setter
    def cache(self, value: jsii.Number) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> jsii.Number:
        ...

    @memory.setter
    def memory(self, value: jsii.Number) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="series")
    def series(self) -> builtins.str:
        ...

    @series.setter
    def series(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> builtins.str:
        ...

    @size.setter
    def size(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="skuName")
    def sku_name(self) -> builtins.str:
        ...

    @sku_name.setter
    def sku_name(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="vCPU")
    def v_cpu(self) -> jsii.Number:
        ...

    @v_cpu.setter
    def v_cpu(self, value: jsii.Number) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="workload")
    def workload(self) -> builtins.str:
        ...

    @workload.setter
    def workload(self, value: builtins.str) -> None:
        ...


class _IComputeSpecificationProxy:
    __jsii_type__: typing.ClassVar[str] = "@microsoft/terraform-cdk-constructs.azure_kusto.IComputeSpecification"

    @builtins.property
    @jsii.member(jsii_name="availibleZones")
    def availible_zones(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "availibleZones"))

    @availible_zones.setter
    def availible_zones(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf20655e0f3d40d5c219517f9507557eaa70b00ab9919bff768660954f6e2ae1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availibleZones", value)

    @builtins.property
    @jsii.member(jsii_name="cache")
    def cache(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cache"))

    @cache.setter
    def cache(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bf1f1e0843d32a20bce66dc3629e8a9fd69f4fd30e3070ed552aa0760654467)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cache", value)

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memory"))

    @memory.setter
    def memory(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__017d858f2cf926f6300507ca699a8609c2bcc97e5e7d44ea50213ce407ec3890)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memory", value)

    @builtins.property
    @jsii.member(jsii_name="series")
    def series(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "series"))

    @series.setter
    def series(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b224dde02d6c5cfa49fb834e7f30ef7f7ff54c0afc3e517e31a0c794517feb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "series", value)

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "size"))

    @size.setter
    def size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__335585384a26e9e79a5c33addbf17852d441dfd58c28b9ed908d8e651cd4ba13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "size", value)

    @builtins.property
    @jsii.member(jsii_name="skuName")
    def sku_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "skuName"))

    @sku_name.setter
    def sku_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__387ff60bca1335cddf1da1fad8ae4def36bec0958a7a55986a470d95d447e9f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skuName", value)

    @builtins.property
    @jsii.member(jsii_name="vCPU")
    def v_cpu(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "vCPU"))

    @v_cpu.setter
    def v_cpu(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdd09233c30506d55c1c74b15a204b3cd7eb5fb8e6eca5fc153dbde49b2ebe2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vCPU", value)

    @builtins.property
    @jsii.member(jsii_name="workload")
    def workload(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workload"))

    @workload.setter
    def workload(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58b64a477ad62fd004941b5dcc092a7f760389aee7470d74059427704881068c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workload", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IComputeSpecification).__jsii_proxy_class__ = lambda : _IComputeSpecificationProxy


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_kusto.TableSchemaProps",
    jsii_struct_bases=[],
    name_mapping={"column_name": "columnName", "column_type": "columnType"},
)
class TableSchemaProps:
    def __init__(self, *, column_name: builtins.str, column_type: builtins.str) -> None:
        '''
        :param column_name: 
        :param column_type: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4a9184b4b9face27efb8668fd03e05ae3fe22c501aa89b961de19b223e20e6f)
            check_type(argname="argument column_name", value=column_name, expected_type=type_hints["column_name"])
            check_type(argname="argument column_type", value=column_type, expected_type=type_hints["column_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "column_name": column_name,
            "column_type": column_type,
        }

    @builtins.property
    def column_name(self) -> builtins.str:
        result = self._values.get("column_name")
        assert result is not None, "Required property 'column_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def column_type(self) -> builtins.str:
        result = self._values.get("column_type")
        assert result is not None, "Required property 'column_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TableSchemaProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Cluster",
    "ClusterProps",
    "ComputeSpecification",
    "Database",
    "DatabaseAccessProps",
    "DatabaseProps",
    "IComputeSpecification",
    "TableSchemaProps",
]

publication.publish()

def _typecheckingstub__9351a5a77b18fe94ed9d59955e81c4877c4006f903bf2ea22d8a9d6cd102e5a3(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    auto_stop_enabled: typing.Optional[builtins.bool] = None,
    capacity: typing.Optional[jsii.Number] = None,
    enable_zones: typing.Optional[builtins.bool] = None,
    identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    identity_type: typing.Optional[builtins.str] = None,
    maximum_instances: typing.Optional[jsii.Number] = None,
    minimum_instances: typing.Optional[jsii.Number] = None,
    public_network_access_enabled: typing.Optional[builtins.bool] = None,
    purge_enabled: typing.Optional[builtins.bool] = None,
    resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
    sku: typing.Optional[IComputeSpecification] = None,
    streaming_ingestion_enabled: typing.Optional[builtins.bool] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__016f667b6e3c9557d441729357d8e19f1db29ec4c5fa78c89b941b80e06da1a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0eafdbeed8d0f571cae144cb65ce6bc8481d686eaa59bee4308fa65c8e66bac(
    value: _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2193d533b05f247b87c19b0582d681f927729e68a936477af77a4950358cea65(
    *,
    name: builtins.str,
    auto_stop_enabled: typing.Optional[builtins.bool] = None,
    capacity: typing.Optional[jsii.Number] = None,
    enable_zones: typing.Optional[builtins.bool] = None,
    identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    identity_type: typing.Optional[builtins.str] = None,
    maximum_instances: typing.Optional[jsii.Number] = None,
    minimum_instances: typing.Optional[jsii.Number] = None,
    public_network_access_enabled: typing.Optional[builtins.bool] = None,
    purge_enabled: typing.Optional[builtins.bool] = None,
    resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
    sku: typing.Optional[IComputeSpecification] = None,
    streaming_ingestion_enabled: typing.Optional[builtins.bool] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d28bc42ddfa7643e7a57dc7b22c3b2fe40540af0fdb9672d6d903a7acbe167a(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__491679e1e5d5f66b6ea317330bb6e7336b7f966c7fc90c2ed8eb3234e9ac512e(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77eb537362eec21ba6718412d8c3423662535771156bc61307f441ec0abb2592(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5603ece543481c136b153a8cb27b7593b6a3f281a3ea3ca2af37dbe8d933678(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__500bf6f2650fa0047eb153aa94e146ef9a6aa0ee69e6e7ed46294486885fec4b(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__145ea1ef488b37ce2baa27d5a14a83e0a4331a5a46903710a6f204e50acdfb24(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83ed6772a0fedc491b2c2a8783b6bd6f5d802c6a2b6ea2b17977242710844fe1(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cab6dd2c47a3916511b1a080ce66a9afc74db45d5b11fbc945ef2bd489c2ec7e(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3beae95e3a51e99fa82cc09a79cb7896427eea2cb3afc432267560a4606e62d2(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f89ed19a43cd5ba674fbc00537182136f66729b1167b29b4ddc20a21cc112c6(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47a147acacc66283572040d97c91a616298f5399fcaaab9b7cb60e0b014b4263(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f00c54c46cc8d3c4bb4c3ae023dd28b84f42b0b1dc1cb9bdfd974cbc9d3d4e5c(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49d336bba3f279a727be16e19551ce732a0d1f63411173852559fc8b3af8ca95(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8ec908d799d81f3d1978c8a6d7a4127d51b62b79da69d4a464fe656cfb43577(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cc0245c04e66c0a1c1610c2e808cb7ba55fc64adf0434fd6fd3ec0d34646bad(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84328743cdc1fd43f3521b372c47364148ce7bee1d58f325ae6c20b305550f24(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62a9488a15813bd82155aefa8ca8ec90103bac9070f8be44814ea00f4b1c4caa(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0f9c5848183743c4eae1801a1811bacd51f05e81a3fa652c4909862a261f421(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33098d3662c412b5f20e8629e47494f7404eb182c1a5e19ea557259bf1c68523(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bbdc7dda046321c937d1b316fe355857857c56591d6720244638772f3220796(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d753371995aedbeef0609fc7cc491932858c1c265b720b2424448ac3985ba3f8(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__554870a2811a35dc1db9ef6f31f48036973e53caf7567005112037252c773d24(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__571a041fdbe0f711ebdc4c2c1fa60f092cf4cf47c42636604deccf45a06ec475(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c53821b5360e6975719bdb3665dd34cbfedee0c16aa2a459fe32f490067ca3b(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5e9b81f5d5e46f253dcf8e81417a6f2ef2d448bbd12de7b5699f32e0f848522(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87aeefe6880ea065d18a136ef053b6f3ffe4a7234ab7e31cf756fb794b873ede(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b1a7acb1f01bdc158a9f07c2854e5bdca659fcfbaee627fa617dc6f351b6c0d(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5981d4cbfc0a70693c4660d945c36f8bed554fe4af0d988befc8ef1c5503e8e7(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec1839e4a4e2396aa56ecd5e8fd75a2db036c3eb450e652b0d625c977bdc3f7d(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2367e2a40bbb41fdb6f058328ce4a7a16b004feb68f343eee5cccd0c1c82f95(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60020ae4d74146b9139e0560bec93d3a5751d3311c70154df24f76e59ce5cff0(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fe3355c57400165db03f7cff46c3b336ce73cec0811ae3271132adac3a6511c(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__605058e16727233c893056961190acce813905a53361f2b424a06e374d0149cc(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfacb476c4c817150590d0cef83dadd51fd2ae503b2f60bb76b0f3ffc00974ba(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6804badc2b1b15759763228696b72b565144f2c35dd7d6833f221e129dcc67ef(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__273fedecc160c301dcd5a4b666175e5994e547fb07231e1a3a6af194be264a9b(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a5cb7e4bb806ffecd608d3d1fd015be553de0fbe38f487979725d7b982d6492(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbc8cfeb76e5a834c6bff4768f7e44f416d5cd1da849976bb9384e3cd0c9b48a(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c3b1cf5e578256da17f5e4d172d7cfec965c42b83a293430e0728065b2b5987(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__698f243198e7e4605368bf6e63564011b34b95f5b1cfcb05b7607ab4f5d73db4(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe3a464457225e9a181eb1b38742358464b14a345665ed233d1b8c92a98e3eb4(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdec81cb897f3759e538f754b107dfee96a01862fa921b4c6fb67439e3db9bfd(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3b43b80db7d343882627adf5d0664dc253a58941c2855927ba16d0dab122bbe(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bda2ae2cf299e55b4bb97e0b4b451b9f166d5796bff0af08d9fba7ea08b3114(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__420d1f4d49d5cf46fd19b370aa26ecfaa5614d23fbace9d92fc1ecd4b3c00ac2(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__359a79b6f609df14594fd41f433c9701420d5b544ee358d2b594b24855f457a3(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c62c82459dcdc9fe710371a7d54a2471a21e0ec21a1b1550ada4192d9ecc0969(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44ecd5be5a18a5658ea782612ad64d06b4d60b13f1c430f1cd96c34e9d28f37d(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e09b2c675d2077bfce0647633b98e3f3e78c1f775ebc6c6a8799d8f651fdb3dc(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__661d71792710b5855c4165f31e9f042b74ea64876d2449146e6e21e260a8bbb3(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79878b4a4ce2a2645dd737112c517c6a16213a899a7c74005ff4c368b59866ff(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd579726c203b204dfe6348e1de12469592523536ccbcc67c1cd99eaae9a10bf(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fde24ac4875b4011de2aaee9afbdf2e945d3d754b7299b9a1d480c4389715660(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66130241f740346fab5d6d15b4968c0e847f98f8d1aadc0ce857212dbf902ba6(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__406614a6d8937c8fd51c5c7344cae3d4034d16619cc829e05579cfc38cc1ffa0(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__029897ed5e97b19845a843000c84f1d5ee4db6c27019cf57353cd64297f54b74(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b67e2923606639ec84c6669011a135485ceb89a98b86dcc9e6b519118dc48cdf(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0eafa0040198c4d9e61b08dad813396d4af8595389f11675fd02c1765b2c18c(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc7f37736e3c057879f174d1e7466c6e75a9d76fac9b3c656eb782feb110e3cd(
    value: IComputeSpecification,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bb7e049648a84a8e486219349a602116b3098bd3ad3df2bebff015ca0877100(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    kusto: Cluster,
    name: builtins.str,
    hot_cache_period: typing.Optional[builtins.str] = None,
    soft_delete_period: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1fe44cb03828c945451d0676f440fb81bfde50a755b1c3f57f0bb0842fe7c9a(
    script_name: builtins.str,
    script_content: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a4e5427243f22a5b893f1d0e1401bbdfc379be8c67e11c64d99fca0794aadcb(
    table_name: builtins.str,
    table_schema: typing.Sequence[typing.Union[TableSchemaProps, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8fae0aa1717ffd90e4aa97235cbcc92728a68e132f7574a341b1ff0026de14b(
    *,
    name: builtins.str,
    principal_id: builtins.str,
    principal_type: builtins.str,
    role: builtins.str,
    tenant_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e3ad0dca05483428a48ef2f19255859d30897ae7656132b3c3fb95e3c87dd41(
    *,
    kusto: Cluster,
    name: builtins.str,
    hot_cache_period: typing.Optional[builtins.str] = None,
    soft_delete_period: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf20655e0f3d40d5c219517f9507557eaa70b00ab9919bff768660954f6e2ae1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bf1f1e0843d32a20bce66dc3629e8a9fd69f4fd30e3070ed552aa0760654467(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__017d858f2cf926f6300507ca699a8609c2bcc97e5e7d44ea50213ce407ec3890(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b224dde02d6c5cfa49fb834e7f30ef7f7ff54c0afc3e517e31a0c794517feb9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__335585384a26e9e79a5c33addbf17852d441dfd58c28b9ed908d8e651cd4ba13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__387ff60bca1335cddf1da1fad8ae4def36bec0958a7a55986a470d95d447e9f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdd09233c30506d55c1c74b15a204b3cd7eb5fb8e6eca5fc153dbde49b2ebe2f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58b64a477ad62fd004941b5dcc092a7f760389aee7470d74059427704881068c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4a9184b4b9face27efb8668fd03e05ae3fe22c501aa89b961de19b223e20e6f(
    *,
    column_name: builtins.str,
    column_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
