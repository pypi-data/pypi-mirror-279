'''
# Azure Log Analytics Workspace Construct

This class represents a Log Analytics Workspace in Azure. It provides a convenient way to manage Azure Log Analytics Workspaces.

## What is a Log Analytics Workspace?

Azure Log Analytics Workspace is a unique environment for Azure Monitor log data. Each workspace has its own data repository and configuration, and data sources and solutions are configured to store their data in that workspace.

You can learn more about Log Analytics Workspace in the [official Azure documentation](https://docs.microsoft.com/en-us/azure/azure-monitor/logs/data-platform-logs).

## Log Analytics Workspace Best Practices

* Consolidate your data in a limited number of workspaces.
* Assign a workspace at the management group level.
* Log minimal data initially, and then increase as necessary.
* Create a data export rule for long-term retention and cold data.
* Assign Azure RBAC roles for Azure Monitor Logs.

## Log Analytics Workspace Class Properties

This class has several properties that control the Log Analytics Workspace's behaviour:

* `location`: The Azure Region where the Log Analytics Workspace will be deployed.
* `name`: The name of the Log Analytics Workspace.
* `resource_group_name`: The name of the Azure Resource Group.
* `sku`: The SKU of the Log Analytics Workspace.
* `retention`: The number of days of retention.
* `tags`: The tags to assign to the Resource Group.
* `rbac`: The RBAC groups to assign to the Resource Group.
* `data_export`: Creates a DataExport for the Log Analytics Workspace.
* `functions`: A collection of Log Analytic functions.
* `queries`: A collection of saved log analytics queries.

## Deploying the Log Analytics Workspace

You can deploy a Log Analytics Workspace using this class like so:

```python
const azureLogAnalytics = new AzureLogAnalytics(this, 'myLogAnalytics', {
  location: 'West US',
  name: 'myLogAnalytics',
  resource_group_name: 'myResourceGroup',
  sku: 'PerGB2018',
  retention: 30,
  tags: {
    'env': 'production',
  },
});
```

This code will create a new Log Analytics Workspace named myLogAnalytics in the West US Azure region with a production environment tag. The workspace belongs to the resource group myResourceGroup and uses the PerGB2018 pricing model. It retains data for 30 days.

## Cost Optimization

In Azure Log Analytics, you are charged for data ingestion and data retention. You pay almost 9x more for data ingested than for data stored. The first 30 days of storage retention are free.

To optimize your costs, consider filtering out what is being ingested. Only log data that will be used. To further reduce costs, consider using a data export rule for long-term retention and cold data.
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
from ..core_azure import AzureResourceWithAlert as _AzureResourceWithAlert_c2e3918b


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_loganalytics.DataExport",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "export_destination_id": "exportDestinationId",
        "name": "name",
        "table_names": "tableNames",
    },
)
class DataExport:
    def __init__(
        self,
        *,
        enabled: builtins.bool,
        export_destination_id: builtins.str,
        name: builtins.str,
        table_names: typing.Sequence[builtins.str],
    ) -> None:
        '''Properties for defining a data export in a Log Analytics Workspace.

        :param enabled: Indicates whether the data export is enabled.
        :param export_destination_id: The ID of the destination resource for the export.
        :param name: The name of the data export.
        :param table_names: An array of table names to be included in the data export.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c10f8d13513051e197c8689ed6dfaed573aa8eb8985cc9af7dbeb58177ee0e27)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument export_destination_id", value=export_destination_id, expected_type=type_hints["export_destination_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument table_names", value=table_names, expected_type=type_hints["table_names"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
            "export_destination_id": export_destination_id,
            "name": name,
            "table_names": table_names,
        }

    @builtins.property
    def enabled(self) -> builtins.bool:
        '''Indicates whether the data export is enabled.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def export_destination_id(self) -> builtins.str:
        '''The ID of the destination resource for the export.'''
        result = self._values.get("export_destination_id")
        assert result is not None, "Required property 'export_destination_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the data export.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_names(self) -> typing.List[builtins.str]:
        '''An array of table names to be included in the data export.'''
        result = self._values.get("table_names")
        assert result is not None, "Required property 'table_names' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataExport(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_loganalytics.LAFunctions",
    jsii_struct_bases=[],
    name_mapping={
        "display_name": "displayName",
        "function_alias": "functionAlias",
        "function_parameters": "functionParameters",
        "name": "name",
        "query": "query",
    },
)
class LAFunctions:
    def __init__(
        self,
        *,
        display_name: builtins.str,
        function_alias: builtins.str,
        function_parameters: typing.Sequence[builtins.str],
        name: builtins.str,
        query: builtins.str,
    ) -> None:
        '''Properties for defining a Log Analytics function.

        :param display_name: The display name for the function.
        :param function_alias: The alias to be used for the function.
        :param function_parameters: A list of parameters for the function.
        :param name: The name of the function.
        :param query: The query that the function will execute.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97f5c9361a176d34e2751d91fbd098eb781392debc703fa70bc94a8b9bd64b35)
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument function_alias", value=function_alias, expected_type=type_hints["function_alias"])
            check_type(argname="argument function_parameters", value=function_parameters, expected_type=type_hints["function_parameters"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "display_name": display_name,
            "function_alias": function_alias,
            "function_parameters": function_parameters,
            "name": name,
            "query": query,
        }

    @builtins.property
    def display_name(self) -> builtins.str:
        '''The display name for the function.'''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def function_alias(self) -> builtins.str:
        '''The alias to be used for the function.'''
        result = self._values.get("function_alias")
        assert result is not None, "Required property 'function_alias' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def function_parameters(self) -> typing.List[builtins.str]:
        '''A list of parameters for the function.'''
        result = self._values.get("function_parameters")
        assert result is not None, "Required property 'function_parameters' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the function.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def query(self) -> builtins.str:
        '''The query that the function will execute.'''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LAFunctions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_loganalytics.Queries",
    jsii_struct_bases=[],
    name_mapping={
        "category": "category",
        "display_name": "displayName",
        "name": "name",
        "query": "query",
    },
)
class Queries:
    def __init__(
        self,
        *,
        category: builtins.str,
        display_name: builtins.str,
        name: builtins.str,
        query: builtins.str,
    ) -> None:
        '''Properties for defining a saved query in a Log Analytics Workspace.

        :param category: The category of the saved query.
        :param display_name: The display name for the saved query.
        :param name: The name of the saved query.
        :param query: The query string.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a622ed3880264b9475e672391c11e0ff37089de0255193901b263bbd511eecc)
            check_type(argname="argument category", value=category, expected_type=type_hints["category"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "category": category,
            "display_name": display_name,
            "name": name,
            "query": query,
        }

    @builtins.property
    def category(self) -> builtins.str:
        '''The category of the saved query.'''
        result = self._values.get("category")
        assert result is not None, "Required property 'category' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''The display name for the saved query.'''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the saved query.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def query(self) -> builtins.str:
        '''The query string.'''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Queries(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Workspace(
    _AzureResourceWithAlert_c2e3918b,
    metaclass=jsii.JSIIMeta,
    jsii_type="@microsoft/terraform-cdk-constructs.azure_loganalytics.Workspace",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        data_export: typing.Optional[typing.Sequence[typing.Union[DataExport, typing.Dict[builtins.str, typing.Any]]]] = None,
        functions: typing.Optional[typing.Sequence[typing.Union[LAFunctions, typing.Dict[builtins.str, typing.Any]]]] = None,
        queries: typing.Optional[typing.Sequence[typing.Union[Queries, typing.Dict[builtins.str, typing.Any]]]] = None,
        resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
        retention: typing.Optional[jsii.Number] = None,
        sku: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Represents an Azure Log Analytics Workspace.

        This class is responsible for the creation and configuration of a Log Analytics Workspace in Azure. A Log Analytics Workspace
        is a unique environment for Azure Monitor data, where data is collected, aggregated, and serves as the administrative boundary.
        Within a workspace, data is collected from various sources and is used for analysis, visualization, and alerting. Configurations
        can include data export rules, saved queries, and custom functions to enhance data analytics capabilities.

        :param scope: - The scope in which to define this construct, typically representing the Cloud Development Kit (CDK) stack.
        :param id: - The unique identifier for this instance of the Log Analytics workspace.
        :param location: The Azure Region to deploy.
        :param name: The name of the Log Analytics Workspace.
        :param data_export: Create a DataExport for the Log Analytics Workspace.
        :param functions: A collection of Log Analytic functions.
        :param queries: A collection of log saved log analytics queries.
        :param resource_group: An optional reference to the resource group in which to deploy the Workspace. If not provided, the Workspace will be deployed in the default resource group.
        :param retention: The number of days of retention. Default is 30.
        :param sku: The SKU of the Log Analytics Workspace.
        :param tags: The tags to assign to the Resource Group.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__519ce91b227d947abed8480d06f8dbdcb94fdf3df467029aece4afb9ac0d4062)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = WorkspaceProps(
            location=location,
            name=name,
            data_export=data_export,
            functions=functions,
            queries=queries,
            resource_group=resource_group,
            retention=retention,
            sku=sku,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "WorkspaceProps":
        return typing.cast("WorkspaceProps", jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa7b3ef950990b4ad74ea33f5b0224eec4f1bd8fb010b54633df1acd9e13c1a7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__00b55aca11d305b98099eb2df158e8fa57cd3e0c3d030b73e6a5747016e428b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroup", value)


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_loganalytics.WorkspaceProps",
    jsii_struct_bases=[],
    name_mapping={
        "location": "location",
        "name": "name",
        "data_export": "dataExport",
        "functions": "functions",
        "queries": "queries",
        "resource_group": "resourceGroup",
        "retention": "retention",
        "sku": "sku",
        "tags": "tags",
    },
)
class WorkspaceProps:
    def __init__(
        self,
        *,
        location: builtins.str,
        name: builtins.str,
        data_export: typing.Optional[typing.Sequence[typing.Union[DataExport, typing.Dict[builtins.str, typing.Any]]]] = None,
        functions: typing.Optional[typing.Sequence[typing.Union[LAFunctions, typing.Dict[builtins.str, typing.Any]]]] = None,
        queries: typing.Optional[typing.Sequence[typing.Union[Queries, typing.Dict[builtins.str, typing.Any]]]] = None,
        resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
        retention: typing.Optional[jsii.Number] = None,
        sku: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param location: The Azure Region to deploy.
        :param name: The name of the Log Analytics Workspace.
        :param data_export: Create a DataExport for the Log Analytics Workspace.
        :param functions: A collection of Log Analytic functions.
        :param queries: A collection of log saved log analytics queries.
        :param resource_group: An optional reference to the resource group in which to deploy the Workspace. If not provided, the Workspace will be deployed in the default resource group.
        :param retention: The number of days of retention. Default is 30.
        :param sku: The SKU of the Log Analytics Workspace.
        :param tags: The tags to assign to the Resource Group.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dcb273b120955caa39f0301e0f14ba6ab0e690d4315705b189838e0fcdfa0ec)
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument data_export", value=data_export, expected_type=type_hints["data_export"])
            check_type(argname="argument functions", value=functions, expected_type=type_hints["functions"])
            check_type(argname="argument queries", value=queries, expected_type=type_hints["queries"])
            check_type(argname="argument resource_group", value=resource_group, expected_type=type_hints["resource_group"])
            check_type(argname="argument retention", value=retention, expected_type=type_hints["retention"])
            check_type(argname="argument sku", value=sku, expected_type=type_hints["sku"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "name": name,
        }
        if data_export is not None:
            self._values["data_export"] = data_export
        if functions is not None:
            self._values["functions"] = functions
        if queries is not None:
            self._values["queries"] = queries
        if resource_group is not None:
            self._values["resource_group"] = resource_group
        if retention is not None:
            self._values["retention"] = retention
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
    def data_export(self) -> typing.Optional[typing.List[DataExport]]:
        '''Create a DataExport for the Log Analytics Workspace.'''
        result = self._values.get("data_export")
        return typing.cast(typing.Optional[typing.List[DataExport]], result)

    @builtins.property
    def functions(self) -> typing.Optional[typing.List[LAFunctions]]:
        '''A collection of Log Analytic functions.'''
        result = self._values.get("functions")
        return typing.cast(typing.Optional[typing.List[LAFunctions]], result)

    @builtins.property
    def queries(self) -> typing.Optional[typing.List[Queries]]:
        '''A collection of log saved log analytics queries.'''
        result = self._values.get("queries")
        return typing.cast(typing.Optional[typing.List[Queries]], result)

    @builtins.property
    def resource_group(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup]:
        '''An optional reference to the resource group in which to deploy the Workspace.

        If not provided, the Workspace will be deployed in the default resource group.
        '''
        result = self._values.get("resource_group")
        return typing.cast(typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup], result)

    @builtins.property
    def retention(self) -> typing.Optional[jsii.Number]:
        '''The number of days of retention.

        Default is 30.
        '''
        result = self._values.get("retention")
        return typing.cast(typing.Optional[jsii.Number], result)

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
        return "WorkspaceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DataExport",
    "LAFunctions",
    "Queries",
    "Workspace",
    "WorkspaceProps",
]

publication.publish()

def _typecheckingstub__c10f8d13513051e197c8689ed6dfaed573aa8eb8985cc9af7dbeb58177ee0e27(
    *,
    enabled: builtins.bool,
    export_destination_id: builtins.str,
    name: builtins.str,
    table_names: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97f5c9361a176d34e2751d91fbd098eb781392debc703fa70bc94a8b9bd64b35(
    *,
    display_name: builtins.str,
    function_alias: builtins.str,
    function_parameters: typing.Sequence[builtins.str],
    name: builtins.str,
    query: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a622ed3880264b9475e672391c11e0ff37089de0255193901b263bbd511eecc(
    *,
    category: builtins.str,
    display_name: builtins.str,
    name: builtins.str,
    query: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__519ce91b227d947abed8480d06f8dbdcb94fdf3df467029aece4afb9ac0d4062(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    data_export: typing.Optional[typing.Sequence[typing.Union[DataExport, typing.Dict[builtins.str, typing.Any]]]] = None,
    functions: typing.Optional[typing.Sequence[typing.Union[LAFunctions, typing.Dict[builtins.str, typing.Any]]]] = None,
    queries: typing.Optional[typing.Sequence[typing.Union[Queries, typing.Dict[builtins.str, typing.Any]]]] = None,
    resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
    retention: typing.Optional[jsii.Number] = None,
    sku: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa7b3ef950990b4ad74ea33f5b0224eec4f1bd8fb010b54633df1acd9e13c1a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00b55aca11d305b98099eb2df158e8fa57cd3e0c3d030b73e6a5747016e428b1(
    value: _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dcb273b120955caa39f0301e0f14ba6ab0e690d4315705b189838e0fcdfa0ec(
    *,
    location: builtins.str,
    name: builtins.str,
    data_export: typing.Optional[typing.Sequence[typing.Union[DataExport, typing.Dict[builtins.str, typing.Any]]]] = None,
    functions: typing.Optional[typing.Sequence[typing.Union[LAFunctions, typing.Dict[builtins.str, typing.Any]]]] = None,
    queries: typing.Optional[typing.Sequence[typing.Union[Queries, typing.Dict[builtins.str, typing.Any]]]] = None,
    resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
    retention: typing.Optional[jsii.Number] = None,
    sku: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
