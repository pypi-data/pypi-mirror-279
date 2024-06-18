'''
# Azure Eventhub Construct

This class represents an Eventhub resource in Azure. It provides a convenient way to manage Azure Eventhub resources.

# What is Eventhub?

See [officail document](https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-features).

# Eventhub Best Practices

Coming soon...

# Create an Eventhub Namespace and Eventhub Instance

This class has several properties that control the Eventhub resource's behaviour:

* `rg`: The [Azure Resource Group object](../azure-resourcegroup/) in which to create the Eventhub Namespace.
* `name`: The name of the Eventhub Namespace to create.
* `sku`: (Optional) Defines which tier to use. Valid options are Basic, Standard, and Premium.
* `capacity`: (Optional) Specifies the Capacity / Throughput Units for a Standard SKU namespace. Default is 2.
* `autoInflateEnabled`: (Optional) Specifies if the EventHub Namespace should be Auto Inflate enabled. Default is false.
* `maximumThroughputUnits`: (Optional) Specifies the maximum number of throughput units when Auto Inflate is Enabled. Valid values range from 1 - 20. Default is 2.
* `zoneRedundant`: (Optional) Specifies if the EventHub Namespace should be Zone Redundant (created across Availability Zones). Default is true.
* `tags`: (Optional) The tags to assign to the Key Vault.
* `minimumTlsVersion`: (Optional) The minimum supported TLS version for this EventHub Namespace. Valid values are: 1.0, 1.1 and 1.2. Default is 1.2.
* `publicNetworkAccessEnabled`: (Optional) Is public network access enabled for the EventHub Namespace? Default is true.
* `localAuthenticationEnabled`: (Optional) Is SAS authentication enabled for the EventHub Namespace? North Central US Not supported. Default is false.
* `identityType`: (Optional) Specifies the type of Managed Service Identity that should be configured on this Event Hub Namespace. Possible values are SystemAssigned or UserAssigned. Default is SystemAssigned.
* `identityIds`: (Optional) Specifies a list of User Assigned Managed Identity IDs to be assigned to this EventHub namespace.

You can deploy a Eventhub Namespace using this class like:

```python
// Create a Resource Group first
const resourceGroup = new AzureResourceGroup(this, "rg", {
  name: 'myResourceGroup',
  location: 'eastus',
});

// Create Eventhub Namespace
const eventhubNamespace = new AzureEventhubNamespace(this, "eventhub", {
  rg: resourceGroup,
  name: 'myEventhubNamespace',
  sku: "Basic",
});

// Add IAM role to Eventhub Namespace
const objectId = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx";
const role = "Contributor";
eventhubNamespace.addAccess(objectId, role);
```

Then, you can deploy several Eventhub Instances in the Eventhub Namespace using this class like:

```python
// Create Eventhub Instance
const eventhubInstance = eventhubNamespace.addEventhubInstance({
  name: `myEventhubInstance1`,
  partitionCount: 2,
  messageRetention: 1,
  status: "Active",
});
```

And, there are several methods in the Eventhub Instance class to setup Authorization rule, Consumer Group, Kusto data connection, etc.

* Add Authorization Rule to Eventhub Instance

  ```python
  eventhubInstance.addAuthorizationRule({
    name: `test-rule`,
    listen: true,
    send: true,
    manage: false,
  });
  ```
* Add Consumer Group to Eventhub Instance

  ```python
  eventhubInstance.addConsumerGroup({
    name: `test-consumer-group`,
  });
  ```
* Add data connection between Eventhub Instance and Kusto database

  ```python
  // Add Kusto data connection
  eventhubInstance.addKustoDataConnection({
    name: `kustoDataConnection1`,
    location: 'eastus',
    resourceGroupName: 'myKustoRg',    // Kusto resource group
    clusterName: 'myKustoCluster',     // Kusto cluster name
    databaseName: "myKustoDatabase1",  // Kusto database name
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
import cdktf_cdktf_provider_azurerm.eventhub_authorization_rule as _cdktf_cdktf_provider_azurerm_eventhub_authorization_rule_92bbcedf
import cdktf_cdktf_provider_azurerm.resource_group as _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf
import constructs as _constructs_77d1e7e8
from ..azure_keyvault import Vault as _Vault_3dbe0187
from ..core_azure import (
    AzureResource as _AzureResource_74eec1c4,
    AzureResourceWithAlert as _AzureResourceWithAlert_c2e3918b,
)


class AuthorizationRule(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@microsoft/terraform-cdk-constructs.azure_eventhub.AuthorizationRule",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        name_: builtins.str,
        *,
        eventhub_name: builtins.str,
        name: builtins.str,
        namespace_name: builtins.str,
        resource_group_name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        listen: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        manage: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        send: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_eventhub_authorization_rule_92bbcedf.EventhubAuthorizationRuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Constructs a new Authorization Rule for an Azure Event Hub.

        This class creates an authorization rule which defines the permissions granted to users and applications
        for accessing and managing the Event Hub. An Authorization Rule can grant listening, sending, and full manage
        permissions based on the properties specified.

        :param scope: - The scope in which to define this construct, typically used for managing lifecycles and creation order.
        :param name_: - The unique name for this instance of the Authorization Rule.
        :param eventhub_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/eventhub_authorization_rule#eventhub_name EventhubAuthorizationRule#eventhub_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/eventhub_authorization_rule#name EventhubAuthorizationRule#name}.
        :param namespace_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/eventhub_authorization_rule#namespace_name EventhubAuthorizationRule#namespace_name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/eventhub_authorization_rule#resource_group_name EventhubAuthorizationRule#resource_group_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/eventhub_authorization_rule#id EventhubAuthorizationRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param listen: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/eventhub_authorization_rule#listen EventhubAuthorizationRule#listen}.
        :param manage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/eventhub_authorization_rule#manage EventhubAuthorizationRule#manage}.
        :param send: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/eventhub_authorization_rule#send EventhubAuthorizationRule#send}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/eventhub_authorization_rule#timeouts EventhubAuthorizationRule#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 

        :remarks:

        The primary connection string and primary key are accessible after the instance creation,
        allowing for integration with other Azure services or client applications.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c1c6f293e6acf5436c72813818813598afbd2a83ba004aa4ccf61ed33758436)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument name_", value=name_, expected_type=type_hints["name_"])
        eh_instance_auth_props = _cdktf_cdktf_provider_azurerm_eventhub_authorization_rule_92bbcedf.EventhubAuthorizationRuleConfig(
            eventhub_name=eventhub_name,
            name=name,
            namespace_name=namespace_name,
            resource_group_name=resource_group_name,
            id=id,
            listen=listen,
            manage=manage,
            send=send,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, name_, eh_instance_auth_props])

    @jsii.member(jsii_name="addPrimaryConnectionStringToVault")
    def add_primary_connection_string_to_vault(
        self,
        vault: _Vault_3dbe0187,
        name: builtins.str,
        expiration_date: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param vault: -
        :param name: -
        :param expiration_date: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0214ac5924c3dc5c9e3f26b91a6c9b1d3dfe07ad2ea89e13535ffd8ec5a4ba0b)
            check_type(argname="argument vault", value=vault, expected_type=type_hints["vault"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument expiration_date", value=expiration_date, expected_type=type_hints["expiration_date"])
        return typing.cast(None, jsii.invoke(self, "addPrimaryConnectionStringToVault", [vault, name, expiration_date]))

    @jsii.member(jsii_name="addPrimaryKeyToVault")
    def add_primary_key_to_vault(
        self,
        vault: _Vault_3dbe0187,
        name: builtins.str,
        expiration_date: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param vault: -
        :param name: -
        :param expiration_date: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99de90f20bfe2eb69b5f50c097faa58d627eaca216cadc2732f88dadb737107d)
            check_type(argname="argument vault", value=vault, expected_type=type_hints["vault"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument expiration_date", value=expiration_date, expected_type=type_hints["expiration_date"])
        return typing.cast(None, jsii.invoke(self, "addPrimaryKeyToVault", [vault, name, expiration_date]))

    @builtins.property
    @jsii.member(jsii_name="ehInstanceAuthProps")
    def eh_instance_auth_props(
        self,
    ) -> _cdktf_cdktf_provider_azurerm_eventhub_authorization_rule_92bbcedf.EventhubAuthorizationRuleConfig:
        return typing.cast(_cdktf_cdktf_provider_azurerm_eventhub_authorization_rule_92bbcedf.EventhubAuthorizationRuleConfig, jsii.get(self, "ehInstanceAuthProps"))


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_eventhub.AuthorizationRuleProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "listen": "listen",
        "manage": "manage",
        "send": "send",
    },
)
class AuthorizationRuleProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        listen: typing.Optional[builtins.bool] = None,
        manage: typing.Optional[builtins.bool] = None,
        send: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param name: 
        :param listen: The name of the resource group in which the EventHub's parent Namespace exists.
        :param manage: Does this Authorization Rule have permissions to Manage to the Event Hub? When this property is true - both listen and send must be too. Default: false
        :param send: Does this Authorization Rule have permissions to Send to the Event Hub? Default: false
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d14b7ca345031d7d76fdb93aa3a21bdc290a32f9bb5730d9e9ebd608e85a2737)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument listen", value=listen, expected_type=type_hints["listen"])
            check_type(argname="argument manage", value=manage, expected_type=type_hints["manage"])
            check_type(argname="argument send", value=send, expected_type=type_hints["send"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if listen is not None:
            self._values["listen"] = listen
        if manage is not None:
            self._values["manage"] = manage
        if send is not None:
            self._values["send"] = send

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def listen(self) -> typing.Optional[builtins.bool]:
        '''The name of the resource group in which the EventHub's parent Namespace exists.'''
        result = self._values.get("listen")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def manage(self) -> typing.Optional[builtins.bool]:
        '''Does this Authorization Rule have permissions to Manage to the Event Hub?

        When this property is true - both listen and send must be too.

        :default: false
        '''
        result = self._values.get("manage")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def send(self) -> typing.Optional[builtins.bool]:
        '''Does this Authorization Rule have permissions to Send to the Event Hub?

        :default: false
        '''
        result = self._values.get("send")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AuthorizationRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_eventhub.BaseInstanceProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "message_retention": "messageRetention",
        "partition_count": "partitionCount",
        "status": "status",
    },
)
class BaseInstanceProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        message_retention: typing.Optional[jsii.Number] = None,
        partition_count: typing.Optional[jsii.Number] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Specifies the name of the EventHub resource.
        :param message_retention: Specifies the number of days to retain the events for this Event Hub. Default: 1
        :param partition_count: Specifies the current number of shards on the Event Hub. When using a shared parent EventHub Namespace, maximum value is 32. Default: 2
        :param status: Specifies the status of the Event Hub resource. Possible values are Active, Disabled and SendDisabled. Default: "Active"
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31739a1c075beeaa002d3eefcd272a71ba46aacd5a741e6e66345de650d9a9e7)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument message_retention", value=message_retention, expected_type=type_hints["message_retention"])
            check_type(argname="argument partition_count", value=partition_count, expected_type=type_hints["partition_count"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if message_retention is not None:
            self._values["message_retention"] = message_retention
        if partition_count is not None:
            self._values["partition_count"] = partition_count
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def name(self) -> builtins.str:
        '''Specifies the name of the EventHub resource.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def message_retention(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of days to retain the events for this Event Hub.

        :default: 1
        '''
        result = self._values.get("message_retention")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def partition_count(self) -> typing.Optional[jsii.Number]:
        '''Specifies the current number of shards on the Event Hub.

        When using a shared parent EventHub Namespace, maximum value is 32.

        :default: 2
        '''
        result = self._values.get("partition_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Specifies the status of the Event Hub resource.

        Possible values are Active, Disabled and SendDisabled.

        :default: "Active"
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BaseInstanceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_eventhub.BaseKustoDataConnectionProps",
    jsii_struct_bases=[],
    name_mapping={
        "kusto_cluster_name": "kustoClusterName",
        "kusto_database_name": "kustoDatabaseName",
        "kusto_resource_group": "kustoResourceGroup",
        "location": "location",
        "name": "name",
        "compression": "compression",
        "consumer_group": "consumerGroup",
        "database_routing_type": "databaseRoutingType",
        "data_format": "dataFormat",
        "identity_id": "identityId",
        "mapping_rule_name": "mappingRuleName",
        "table_name": "tableName",
    },
)
class BaseKustoDataConnectionProps:
    def __init__(
        self,
        *,
        kusto_cluster_name: builtins.str,
        kusto_database_name: builtins.str,
        kusto_resource_group: _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup,
        location: builtins.str,
        name: builtins.str,
        compression: typing.Optional[builtins.str] = None,
        consumer_group: typing.Optional[builtins.str] = None,
        database_routing_type: typing.Optional[builtins.str] = None,
        data_format: typing.Optional[builtins.str] = None,
        identity_id: typing.Optional[builtins.str] = None,
        mapping_rule_name: typing.Optional[builtins.str] = None,
        table_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kusto_cluster_name: Specifies the name of the Kusto Cluster this data connection will be added to.
        :param kusto_database_name: Specifies the name of the Kusto Database this data connection will be added to.
        :param kusto_resource_group: Specifies the Resource Group where the Kusto Database should exist.
        :param location: The location where the Kusto EventHub Data Connection should be created.
        :param name: The name of the Kusto EventHub Data Connection to create.
        :param compression: Specifies compression type for the connection. Allowed values: GZip and None. Default: "None"
        :param consumer_group: Specifies the EventHub consumer group this data connection will use for ingestion. Default: "$Default"
        :param database_routing_type: Indication for database routing information from the data connection, by default only database routing information is allowed. Allowed values: Single, Multi. Default: "Single"
        :param data_format: Specifies the data format of the EventHub messages. Allowed values: APACHEAVRO, AVRO, CSV, JSON, MULTIJSON, ORC, PARQUET, PSV, RAW, SCSV, SINGLEJSON, SOHSV, TSVE, TSV, TXT, and W3CLOGFILE. Default: "JSON"
        :param identity_id: The resource ID of a managed identity (system or user assigned) to be used to authenticate with event hub.
        :param mapping_rule_name: Specifies the mapping rule used for the message ingestion. Mapping rule must exist before resource is created.
        :param table_name: Specifies the target table name used for the message ingestion. Table must exist before resource is created.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0689b3cc5855245f78be80a1a26107af28531e4f6e7c45d9451dd6180b8316d)
            check_type(argname="argument kusto_cluster_name", value=kusto_cluster_name, expected_type=type_hints["kusto_cluster_name"])
            check_type(argname="argument kusto_database_name", value=kusto_database_name, expected_type=type_hints["kusto_database_name"])
            check_type(argname="argument kusto_resource_group", value=kusto_resource_group, expected_type=type_hints["kusto_resource_group"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument compression", value=compression, expected_type=type_hints["compression"])
            check_type(argname="argument consumer_group", value=consumer_group, expected_type=type_hints["consumer_group"])
            check_type(argname="argument database_routing_type", value=database_routing_type, expected_type=type_hints["database_routing_type"])
            check_type(argname="argument data_format", value=data_format, expected_type=type_hints["data_format"])
            check_type(argname="argument identity_id", value=identity_id, expected_type=type_hints["identity_id"])
            check_type(argname="argument mapping_rule_name", value=mapping_rule_name, expected_type=type_hints["mapping_rule_name"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kusto_cluster_name": kusto_cluster_name,
            "kusto_database_name": kusto_database_name,
            "kusto_resource_group": kusto_resource_group,
            "location": location,
            "name": name,
        }
        if compression is not None:
            self._values["compression"] = compression
        if consumer_group is not None:
            self._values["consumer_group"] = consumer_group
        if database_routing_type is not None:
            self._values["database_routing_type"] = database_routing_type
        if data_format is not None:
            self._values["data_format"] = data_format
        if identity_id is not None:
            self._values["identity_id"] = identity_id
        if mapping_rule_name is not None:
            self._values["mapping_rule_name"] = mapping_rule_name
        if table_name is not None:
            self._values["table_name"] = table_name

    @builtins.property
    def kusto_cluster_name(self) -> builtins.str:
        '''Specifies the name of the Kusto Cluster this data connection will be added to.'''
        result = self._values.get("kusto_cluster_name")
        assert result is not None, "Required property 'kusto_cluster_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kusto_database_name(self) -> builtins.str:
        '''Specifies the name of the Kusto Database this data connection will be added to.'''
        result = self._values.get("kusto_database_name")
        assert result is not None, "Required property 'kusto_database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kusto_resource_group(
        self,
    ) -> _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup:
        '''Specifies the Resource Group where the Kusto Database should exist.'''
        result = self._values.get("kusto_resource_group")
        assert result is not None, "Required property 'kusto_resource_group' is missing"
        return typing.cast(_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location where the Kusto EventHub Data Connection should be created.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the Kusto EventHub Data Connection to create.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def compression(self) -> typing.Optional[builtins.str]:
        '''Specifies compression type for the connection.

        Allowed values: GZip and None.

        :default: "None"
        '''
        result = self._values.get("compression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def consumer_group(self) -> typing.Optional[builtins.str]:
        '''Specifies the EventHub consumer group this data connection will use for ingestion.

        :default: "$Default"
        '''
        result = self._values.get("consumer_group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def database_routing_type(self) -> typing.Optional[builtins.str]:
        '''Indication for database routing information from the data connection, by default only database routing information is allowed.

        Allowed values: Single, Multi.

        :default: "Single"
        '''
        result = self._values.get("database_routing_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the data format of the EventHub messages.

        Allowed values: APACHEAVRO, AVRO, CSV, JSON, MULTIJSON, ORC, PARQUET, PSV, RAW, SCSV, SINGLEJSON, SOHSV, TSVE, TSV, TXT, and W3CLOGFILE.

        :default: "JSON"
        '''
        result = self._values.get("data_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_id(self) -> typing.Optional[builtins.str]:
        '''The resource ID of a managed identity (system or user assigned) to be used to authenticate with event hub.'''
        result = self._values.get("identity_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mapping_rule_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the mapping rule used for the message ingestion.

        Mapping rule must exist before resource is created.
        '''
        result = self._values.get("mapping_rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def table_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the target table name used for the message ingestion.

        Table must exist before resource is created.
        '''
        result = self._values.get("table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BaseKustoDataConnectionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Cluster(
    _AzureResource_74eec1c4,
    metaclass=jsii.JSIIMeta,
    jsii_type="@microsoft/terraform-cdk-constructs.azure_eventhub.Cluster",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        name_: builtins.str,
        *,
        name: builtins.str,
        resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
        sku_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Constructs a new Event Hub Cluster.

        This class creates an Azure Event Hub Cluster which is a dedicated capacity resource for handling
        high-throughput, low-latency event ingestion and streaming. It is used in scenarios where you need
        predictable performance and cost regardless of the volume of data ingress or number of downstream
        event consumers.

        :param scope: - The scope in which to define this construct, usually representing the Cloud Development Kit (CDK) stack.
        :param name_: - The unique name for this instance of the Event Hub Cluster.
        :param name: The name of the EventHub Cluster.
        :param resource_group: An optional reference to the resource group in which to deploy the Event Hub Cluster. If not provided, the Event Hub Cluster will be deployed in the default resource group.
        :param sku_name: The SKU name of the EventHub Cluster. The only supported value at this time is Dedicated_1. Default: "Dedicated_1"
        :param tags: The tags to assign to the Application Insights resource.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9325412d61ac035504e7b062fbc0964eb65b9626d0007084dde7186a87bed5fa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument name_", value=name_, expected_type=type_hints["name_"])
        props = EventHubClusterProps(
            name=name, resource_group=resource_group, sku_name=sku_name, tags=tags
        )

        jsii.create(self.__class__, self, [scope, name_, props])

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "EventHubClusterProps":
        return typing.cast("EventHubClusterProps", jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2005aa8f57434f9765546b33a3fd9c29a44e344e4c145aeca1155fbc2c755cf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__66a33608fc271b155bfcb128a658452996ea2776e99607f1cc49ee62c541b1e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroup", value)


class ConsumerGroup(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@microsoft/terraform-cdk-constructs.azure_eventhub.ConsumerGroup",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        name_: builtins.str,
        *,
        eventhub_name: builtins.str,
        name: builtins.str,
        namespace_name: builtins.str,
        resource_group: _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup,
        user_metadata: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Constructs a new Event Hub Consumer Group.

        An Event Hub Consumer Group is a view of an entire Event Hub that enables consumer applications to each have
        a separate view of the event stream. They read the stream independently at their own pace and with their own
        offsets. This class creates a consumer group for a specified Event Hub, allowing for decentralized and
        scalable event processing.

        :param scope: - The scope in which to define this construct, typically representing the Cloud Development Kit (CDK) stack.
        :param name_: - The unique name for this instance of the Consumer Group.
        :param eventhub_name: Specifies the name of the EventHub.
        :param name: 
        :param namespace_name: Specifies the name of the grandparent EventHub Namespace.
        :param resource_group: The name of the resource group in which the EventHub Consumer Group's grandparent Namespace exists.
        :param user_metadata: Specifies the user metadata.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a8139279750b65048fa5110a327c0d601a1554c23b92e2c2cba7f8e89ff87cd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument name_", value=name_, expected_type=type_hints["name_"])
        eh_consumer_group_props = ConsumerGroupProps(
            eventhub_name=eventhub_name,
            name=name,
            namespace_name=namespace_name,
            resource_group=resource_group,
            user_metadata=user_metadata,
        )

        jsii.create(self.__class__, self, [scope, name_, eh_consumer_group_props])

    @builtins.property
    @jsii.member(jsii_name="ehConsumerGroupProps")
    def eh_consumer_group_props(self) -> "ConsumerGroupProps":
        return typing.cast("ConsumerGroupProps", jsii.get(self, "ehConsumerGroupProps"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_eventhub.ConsumerGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "eventhub_name": "eventhubName",
        "name": "name",
        "namespace_name": "namespaceName",
        "resource_group": "resourceGroup",
        "user_metadata": "userMetadata",
    },
)
class ConsumerGroupProps:
    def __init__(
        self,
        *,
        eventhub_name: builtins.str,
        name: builtins.str,
        namespace_name: builtins.str,
        resource_group: _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup,
        user_metadata: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param eventhub_name: Specifies the name of the EventHub.
        :param name: 
        :param namespace_name: Specifies the name of the grandparent EventHub Namespace.
        :param resource_group: The name of the resource group in which the EventHub Consumer Group's grandparent Namespace exists.
        :param user_metadata: Specifies the user metadata.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e8f89b463fc90e79558f1493e210f98c407f279a95929c357a6fb5c9ed2e142)
            check_type(argname="argument eventhub_name", value=eventhub_name, expected_type=type_hints["eventhub_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument namespace_name", value=namespace_name, expected_type=type_hints["namespace_name"])
            check_type(argname="argument resource_group", value=resource_group, expected_type=type_hints["resource_group"])
            check_type(argname="argument user_metadata", value=user_metadata, expected_type=type_hints["user_metadata"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "eventhub_name": eventhub_name,
            "name": name,
            "namespace_name": namespace_name,
            "resource_group": resource_group,
        }
        if user_metadata is not None:
            self._values["user_metadata"] = user_metadata

    @builtins.property
    def eventhub_name(self) -> builtins.str:
        '''Specifies the name of the EventHub.'''
        result = self._values.get("eventhub_name")
        assert result is not None, "Required property 'eventhub_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def namespace_name(self) -> builtins.str:
        '''Specifies the name of the grandparent EventHub Namespace.'''
        result = self._values.get("namespace_name")
        assert result is not None, "Required property 'namespace_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group(
        self,
    ) -> _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup:
        '''The name of the resource group in which the EventHub Consumer Group's grandparent Namespace exists.'''
        result = self._values.get("resource_group")
        assert result is not None, "Required property 'resource_group' is missing"
        return typing.cast(_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup, result)

    @builtins.property
    def user_metadata(self) -> typing.Optional[builtins.str]:
        '''Specifies the user metadata.'''
        result = self._values.get("user_metadata")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConsumerGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_eventhub.EventHubClusterProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "resource_group": "resourceGroup",
        "sku_name": "skuName",
        "tags": "tags",
    },
)
class EventHubClusterProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
        sku_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param name: The name of the EventHub Cluster.
        :param resource_group: An optional reference to the resource group in which to deploy the Event Hub Cluster. If not provided, the Event Hub Cluster will be deployed in the default resource group.
        :param sku_name: The SKU name of the EventHub Cluster. The only supported value at this time is Dedicated_1. Default: "Dedicated_1"
        :param tags: The tags to assign to the Application Insights resource.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a18ded3b6e021459ebd10c2faa67178f8c192d6b057a954ba0b9c9703a6aa48)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group", value=resource_group, expected_type=type_hints["resource_group"])
            check_type(argname="argument sku_name", value=sku_name, expected_type=type_hints["sku_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if resource_group is not None:
            self._values["resource_group"] = resource_group
        if sku_name is not None:
            self._values["sku_name"] = sku_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the EventHub Cluster.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup]:
        '''An optional reference to the resource group in which to deploy the Event Hub Cluster.

        If not provided, the Event Hub Cluster will be deployed in the default resource group.
        '''
        result = self._values.get("resource_group")
        return typing.cast(typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup], result)

    @builtins.property
    def sku_name(self) -> typing.Optional[builtins.str]:
        '''The SKU name of the EventHub Cluster.

        The only supported value at this time is Dedicated_1.

        :default: "Dedicated_1"
        '''
        result = self._values.get("sku_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The tags to assign to the Application Insights resource.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventHubClusterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Instance(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@microsoft/terraform-cdk-constructs.azure_eventhub.Instance",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        name: builtins.str,
        *,
        namespace_name: builtins.str,
        resource_group: _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup,
        name: builtins.str,
        message_retention: typing.Optional[jsii.Number] = None,
        partition_count: typing.Optional[jsii.Number] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Constructs a new Event Hub instance.

        This class creates an Azure Event Hub instance within a specified namespace. Event Hubs is a highly scalable
        data streaming platform and event ingestion service, capable of receiving and processing millions of events per second.
        Event Hubs can process and store events, data, or telemetry produced by distributed software and devices.

        :param scope: - The scope in which to define this construct, typically used for managing lifecycles and creation order.
        :param name: - The unique name for this instance of the Event Hub.
        :param namespace_name: Specifies the name of the EventHub Namespace.
        :param resource_group: The name of the resource group in which the EventHub's parent Namespace exists.
        :param name: Specifies the name of the EventHub resource.
        :param message_retention: Specifies the number of days to retain the events for this Event Hub. Default: 1
        :param partition_count: Specifies the current number of shards on the Event Hub. When using a shared parent EventHub Namespace, maximum value is 32. Default: 2
        :param status: Specifies the status of the Event Hub resource. Possible values are Active, Disabled and SendDisabled. Default: "Active"
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4948905e1978b1095ac0f766fdab18a145e3616c5ab54b06f33b4b2184c4a2b5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        eh_instance_props = InstanceProps(
            namespace_name=namespace_name,
            resource_group=resource_group,
            name=name,
            message_retention=message_retention,
            partition_count=partition_count,
            status=status,
        )

        jsii.create(self.__class__, self, [scope, name, eh_instance_props])

    @jsii.member(jsii_name="addAuthorizationRule")
    def add_authorization_rule(
        self,
        *,
        name: builtins.str,
        listen: typing.Optional[builtins.bool] = None,
        manage: typing.Optional[builtins.bool] = None,
        send: typing.Optional[builtins.bool] = None,
    ) -> AuthorizationRule:
        '''Adds an Authorization Rule to an Event Hub instance.

        This method creates a new Authorization Rule associated with the specified Event Hub,
        granting specified permissions such as 'listen', 'send', and 'manage' based on the properties provided.
        The rule determines the access level granted to users and applications for the Event Hub.

        :param name: 
        :param listen: The name of the resource group in which the EventHub's parent Namespace exists.
        :param manage: Does this Authorization Rule have permissions to Manage to the Event Hub? When this property is true - both listen and send must be too. Default: false
        :param send: Does this Authorization Rule have permissions to Send to the Event Hub? Default: false

        :return:

        An instance of the AuthorizationRule class, configured with the specified permissions and associated
        with the Event Hub specified in the enclosing construct's properties.

        Example usage::

        const eventHubAuthRule = eventHubInstance.addAuthorizationRule({
        name: 'myCustomAuthRule',
        listen: true,
        send: true,
        manage: false // Only listening and sending permissions are granted.
        });
        '''
        props = AuthorizationRuleProps(
            name=name, listen=listen, manage=manage, send=send
        )

        return typing.cast(AuthorizationRule, jsii.invoke(self, "addAuthorizationRule", [props]))

    @jsii.member(jsii_name="addConsumerGroup")
    def add_consumer_group(
        self,
        name: builtins.str,
        user_metadata: typing.Optional[builtins.str] = None,
    ) -> ConsumerGroup:
        '''Adds a Consumer Group to an existing Event Hub instance.

        This method creates a new Consumer Group for the specified Event Hub. Consumer groups represent a view of the entire Event Hub,
        allowing consumer applications to have separate, independent views of the event stream. They read the stream at their own pace
        and maintain their own sequence point or offset. This enables a single Event Hub to support multiple consumer applications.

        :param name: - The name of the Consumer Group to be added. This name must be unique within the Event Hub namespace.
        :param user_metadata: - Optional. User-defined metadata for the Consumer Group. This metadata is useful for storing additional information about the consumer group, such as its purpose or operational details.

        :return:

        An instance of the ConsumerGroup class, configured with the specified properties and associated with the Event Hub
        specified in the enclosing construct's properties.

        Example usage::

        const myConsumerGroup = eventHubInstance.addConsumerGroup('myConsumerGroupName', 'Metadata about this consumer group');

        :remarks:

        Each consumer group can have multiple concurrent readers, but each partition in the Event Hub can only have one active consumer
        from a specific consumer group at a time. Multiple consumer groups enable multiple consuming applications to each have a separate
        view of the event stream, and to read the stream independently at their own pace and with their own offsets.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe8193289e2151a2d124ddd011eace10bee17e5b578d6b819df127f9d4b2e382)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument user_metadata", value=user_metadata, expected_type=type_hints["user_metadata"])
        return typing.cast(ConsumerGroup, jsii.invoke(self, "addConsumerGroup", [name, user_metadata]))

    @jsii.member(jsii_name="addKustoDataConnection")
    def add_kusto_data_connection(
        self,
        *,
        kusto_cluster_name: builtins.str,
        kusto_database_name: builtins.str,
        kusto_resource_group: _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup,
        location: builtins.str,
        name: builtins.str,
        compression: typing.Optional[builtins.str] = None,
        consumer_group: typing.Optional[builtins.str] = None,
        database_routing_type: typing.Optional[builtins.str] = None,
        data_format: typing.Optional[builtins.str] = None,
        identity_id: typing.Optional[builtins.str] = None,
        mapping_rule_name: typing.Optional[builtins.str] = None,
        table_name: typing.Optional[builtins.str] = None,
    ) -> "KustoDataConnection":
        '''Adds a Kusto Data Connection to an existing Kusto Cluster and Database for ingesting data from an EventHub.

        This method configures a new Kusto Data Connection linked to the specified EventHub. It facilitates the ingestion of streaming data
        into the Kusto database, allowing for real-time analytics on streamed data. This connection specifies how data from EventHub
        is to be ingested into tables within the Kusto Database.

        :param kusto_cluster_name: Specifies the name of the Kusto Cluster this data connection will be added to.
        :param kusto_database_name: Specifies the name of the Kusto Database this data connection will be added to.
        :param kusto_resource_group: Specifies the Resource Group where the Kusto Database should exist.
        :param location: The location where the Kusto EventHub Data Connection should be created.
        :param name: The name of the Kusto EventHub Data Connection to create.
        :param compression: Specifies compression type for the connection. Allowed values: GZip and None. Default: "None"
        :param consumer_group: Specifies the EventHub consumer group this data connection will use for ingestion. Default: "$Default"
        :param database_routing_type: Indication for database routing information from the data connection, by default only database routing information is allowed. Allowed values: Single, Multi. Default: "Single"
        :param data_format: Specifies the data format of the EventHub messages. Allowed values: APACHEAVRO, AVRO, CSV, JSON, MULTIJSON, ORC, PARQUET, PSV, RAW, SCSV, SINGLEJSON, SOHSV, TSVE, TSV, TXT, and W3CLOGFILE. Default: "JSON"
        :param identity_id: The resource ID of a managed identity (system or user assigned) to be used to authenticate with event hub.
        :param mapping_rule_name: Specifies the mapping rule used for the message ingestion. Mapping rule must exist before resource is created.
        :param table_name: Specifies the target table name used for the message ingestion. Table must exist before resource is created.

        :return:

        An instance of the KustoDataConnection class, configured with the specified properties and linked to the EventHub
        specified in the enclosing construct's properties.

        Example usage::

        const kustoConnection = kustoInstance.addKustoDataConnection({
        name: 'myKustoDataConnection',
        location: 'West US',
        kustoResourceGroup: resourceGroup,
        kustoClusterName: 'myCluster',
        kustoDatabaseName: 'myDatabase',
        tableName: 'IngestionTable',
        consumerGroup: '$Default',
        dataFormat: 'JSON'
        });
        '''
        props = BaseKustoDataConnectionProps(
            kusto_cluster_name=kusto_cluster_name,
            kusto_database_name=kusto_database_name,
            kusto_resource_group=kusto_resource_group,
            location=location,
            name=name,
            compression=compression,
            consumer_group=consumer_group,
            database_routing_type=database_routing_type,
            data_format=data_format,
            identity_id=identity_id,
            mapping_rule_name=mapping_rule_name,
            table_name=table_name,
        )

        return typing.cast("KustoDataConnection", jsii.invoke(self, "addKustoDataConnection", [props]))

    @builtins.property
    @jsii.member(jsii_name="ehInstanceProps")
    def eh_instance_props(self) -> "InstanceProps":
        return typing.cast("InstanceProps", jsii.get(self, "ehInstanceProps"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="partitionIds")
    def partition_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "partitionIds"))


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_eventhub.InstanceProps",
    jsii_struct_bases=[BaseInstanceProps],
    name_mapping={
        "name": "name",
        "message_retention": "messageRetention",
        "partition_count": "partitionCount",
        "status": "status",
        "namespace_name": "namespaceName",
        "resource_group": "resourceGroup",
    },
)
class InstanceProps(BaseInstanceProps):
    def __init__(
        self,
        *,
        name: builtins.str,
        message_retention: typing.Optional[jsii.Number] = None,
        partition_count: typing.Optional[jsii.Number] = None,
        status: typing.Optional[builtins.str] = None,
        namespace_name: builtins.str,
        resource_group: _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup,
    ) -> None:
        '''
        :param name: Specifies the name of the EventHub resource.
        :param message_retention: Specifies the number of days to retain the events for this Event Hub. Default: 1
        :param partition_count: Specifies the current number of shards on the Event Hub. When using a shared parent EventHub Namespace, maximum value is 32. Default: 2
        :param status: Specifies the status of the Event Hub resource. Possible values are Active, Disabled and SendDisabled. Default: "Active"
        :param namespace_name: Specifies the name of the EventHub Namespace.
        :param resource_group: The name of the resource group in which the EventHub's parent Namespace exists.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f05ad2cf1dc9e1093643ee5300849f817d2f1fd487f8bf5b767b31e1ce3f414)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument message_retention", value=message_retention, expected_type=type_hints["message_retention"])
            check_type(argname="argument partition_count", value=partition_count, expected_type=type_hints["partition_count"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument namespace_name", value=namespace_name, expected_type=type_hints["namespace_name"])
            check_type(argname="argument resource_group", value=resource_group, expected_type=type_hints["resource_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "namespace_name": namespace_name,
            "resource_group": resource_group,
        }
        if message_retention is not None:
            self._values["message_retention"] = message_retention
        if partition_count is not None:
            self._values["partition_count"] = partition_count
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def name(self) -> builtins.str:
        '''Specifies the name of the EventHub resource.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def message_retention(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of days to retain the events for this Event Hub.

        :default: 1
        '''
        result = self._values.get("message_retention")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def partition_count(self) -> typing.Optional[jsii.Number]:
        '''Specifies the current number of shards on the Event Hub.

        When using a shared parent EventHub Namespace, maximum value is 32.

        :default: 2
        '''
        result = self._values.get("partition_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Specifies the status of the Event Hub resource.

        Possible values are Active, Disabled and SendDisabled.

        :default: "Active"
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace_name(self) -> builtins.str:
        '''Specifies the name of the EventHub Namespace.'''
        result = self._values.get("namespace_name")
        assert result is not None, "Required property 'namespace_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group(
        self,
    ) -> _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup:
        '''The name of the resource group in which the EventHub's parent Namespace exists.'''
        result = self._values.get("resource_group")
        assert result is not None, "Required property 'resource_group' is missing"
        return typing.cast(_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InstanceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KustoDataConnection(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@microsoft/terraform-cdk-constructs.azure_eventhub.KustoDataConnection",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        eventhub_id: builtins.str,
        kusto_cluster_name: builtins.str,
        kusto_database_name: builtins.str,
        kusto_resource_group: _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup,
        location: builtins.str,
        name: builtins.str,
        compression: typing.Optional[builtins.str] = None,
        consumer_group: typing.Optional[builtins.str] = None,
        database_routing_type: typing.Optional[builtins.str] = None,
        data_format: typing.Optional[builtins.str] = None,
        identity_id: typing.Optional[builtins.str] = None,
        mapping_rule_name: typing.Optional[builtins.str] = None,
        table_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Constructs a new Azure Kusto Data Connection for ingesting data from an EventHub.

        This class creates a data connection within a specified Kusto (Azure Data Explorer) database that connects
        to an Azure EventHub. This setup enables seamless data ingestion from EventHub into the Kusto database,
        allowing for real-time analytics on streamed data.

        :param scope: - The scope in which to define this construct, typically representing the Cloud Development Kit (CDK) stack.
        :param id: - The unique identifier for this instance of the data connection.
        :param eventhub_id: Specifies the resource id of the EventHub this data connection will use for ingestion.
        :param kusto_cluster_name: Specifies the name of the Kusto Cluster this data connection will be added to.
        :param kusto_database_name: Specifies the name of the Kusto Database this data connection will be added to.
        :param kusto_resource_group: Specifies the Resource Group where the Kusto Database should exist.
        :param location: The location where the Kusto EventHub Data Connection should be created.
        :param name: The name of the Kusto EventHub Data Connection to create.
        :param compression: Specifies compression type for the connection. Allowed values: GZip and None. Default: "None"
        :param consumer_group: Specifies the EventHub consumer group this data connection will use for ingestion. Default: "$Default"
        :param database_routing_type: Indication for database routing information from the data connection, by default only database routing information is allowed. Allowed values: Single, Multi. Default: "Single"
        :param data_format: Specifies the data format of the EventHub messages. Allowed values: APACHEAVRO, AVRO, CSV, JSON, MULTIJSON, ORC, PARQUET, PSV, RAW, SCSV, SINGLEJSON, SOHSV, TSVE, TSV, TXT, and W3CLOGFILE. Default: "JSON"
        :param identity_id: The resource ID of a managed identity (system or user assigned) to be used to authenticate with event hub.
        :param mapping_rule_name: Specifies the mapping rule used for the message ingestion. Mapping rule must exist before resource is created.
        :param table_name: Specifies the target table name used for the message ingestion. Table must exist before resource is created.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62b3da48c45f3f6e9b8c2e99377ece2ac8ca75b941ca3990d7da9809fe5c2849)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        kusto_data_connection_props = KustoDataConnectionProps(
            eventhub_id=eventhub_id,
            kusto_cluster_name=kusto_cluster_name,
            kusto_database_name=kusto_database_name,
            kusto_resource_group=kusto_resource_group,
            location=location,
            name=name,
            compression=compression,
            consumer_group=consumer_group,
            database_routing_type=database_routing_type,
            data_format=data_format,
            identity_id=identity_id,
            mapping_rule_name=mapping_rule_name,
            table_name=table_name,
        )

        jsii.create(self.__class__, self, [scope, id, kusto_data_connection_props])

    @builtins.property
    @jsii.member(jsii_name="eventhubKustoDataConnectionProps")
    def eventhub_kusto_data_connection_props(self) -> "KustoDataConnectionProps":
        return typing.cast("KustoDataConnectionProps", jsii.get(self, "eventhubKustoDataConnectionProps"))


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_eventhub.KustoDataConnectionProps",
    jsii_struct_bases=[BaseKustoDataConnectionProps],
    name_mapping={
        "kusto_cluster_name": "kustoClusterName",
        "kusto_database_name": "kustoDatabaseName",
        "kusto_resource_group": "kustoResourceGroup",
        "location": "location",
        "name": "name",
        "compression": "compression",
        "consumer_group": "consumerGroup",
        "database_routing_type": "databaseRoutingType",
        "data_format": "dataFormat",
        "identity_id": "identityId",
        "mapping_rule_name": "mappingRuleName",
        "table_name": "tableName",
        "eventhub_id": "eventhubId",
    },
)
class KustoDataConnectionProps(BaseKustoDataConnectionProps):
    def __init__(
        self,
        *,
        kusto_cluster_name: builtins.str,
        kusto_database_name: builtins.str,
        kusto_resource_group: _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup,
        location: builtins.str,
        name: builtins.str,
        compression: typing.Optional[builtins.str] = None,
        consumer_group: typing.Optional[builtins.str] = None,
        database_routing_type: typing.Optional[builtins.str] = None,
        data_format: typing.Optional[builtins.str] = None,
        identity_id: typing.Optional[builtins.str] = None,
        mapping_rule_name: typing.Optional[builtins.str] = None,
        table_name: typing.Optional[builtins.str] = None,
        eventhub_id: builtins.str,
    ) -> None:
        '''
        :param kusto_cluster_name: Specifies the name of the Kusto Cluster this data connection will be added to.
        :param kusto_database_name: Specifies the name of the Kusto Database this data connection will be added to.
        :param kusto_resource_group: Specifies the Resource Group where the Kusto Database should exist.
        :param location: The location where the Kusto EventHub Data Connection should be created.
        :param name: The name of the Kusto EventHub Data Connection to create.
        :param compression: Specifies compression type for the connection. Allowed values: GZip and None. Default: "None"
        :param consumer_group: Specifies the EventHub consumer group this data connection will use for ingestion. Default: "$Default"
        :param database_routing_type: Indication for database routing information from the data connection, by default only database routing information is allowed. Allowed values: Single, Multi. Default: "Single"
        :param data_format: Specifies the data format of the EventHub messages. Allowed values: APACHEAVRO, AVRO, CSV, JSON, MULTIJSON, ORC, PARQUET, PSV, RAW, SCSV, SINGLEJSON, SOHSV, TSVE, TSV, TXT, and W3CLOGFILE. Default: "JSON"
        :param identity_id: The resource ID of a managed identity (system or user assigned) to be used to authenticate with event hub.
        :param mapping_rule_name: Specifies the mapping rule used for the message ingestion. Mapping rule must exist before resource is created.
        :param table_name: Specifies the target table name used for the message ingestion. Table must exist before resource is created.
        :param eventhub_id: Specifies the resource id of the EventHub this data connection will use for ingestion.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bfa41b399d7b3d24221998820347cbea3233009963ae993b32aba3bed46a284)
            check_type(argname="argument kusto_cluster_name", value=kusto_cluster_name, expected_type=type_hints["kusto_cluster_name"])
            check_type(argname="argument kusto_database_name", value=kusto_database_name, expected_type=type_hints["kusto_database_name"])
            check_type(argname="argument kusto_resource_group", value=kusto_resource_group, expected_type=type_hints["kusto_resource_group"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument compression", value=compression, expected_type=type_hints["compression"])
            check_type(argname="argument consumer_group", value=consumer_group, expected_type=type_hints["consumer_group"])
            check_type(argname="argument database_routing_type", value=database_routing_type, expected_type=type_hints["database_routing_type"])
            check_type(argname="argument data_format", value=data_format, expected_type=type_hints["data_format"])
            check_type(argname="argument identity_id", value=identity_id, expected_type=type_hints["identity_id"])
            check_type(argname="argument mapping_rule_name", value=mapping_rule_name, expected_type=type_hints["mapping_rule_name"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            check_type(argname="argument eventhub_id", value=eventhub_id, expected_type=type_hints["eventhub_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kusto_cluster_name": kusto_cluster_name,
            "kusto_database_name": kusto_database_name,
            "kusto_resource_group": kusto_resource_group,
            "location": location,
            "name": name,
            "eventhub_id": eventhub_id,
        }
        if compression is not None:
            self._values["compression"] = compression
        if consumer_group is not None:
            self._values["consumer_group"] = consumer_group
        if database_routing_type is not None:
            self._values["database_routing_type"] = database_routing_type
        if data_format is not None:
            self._values["data_format"] = data_format
        if identity_id is not None:
            self._values["identity_id"] = identity_id
        if mapping_rule_name is not None:
            self._values["mapping_rule_name"] = mapping_rule_name
        if table_name is not None:
            self._values["table_name"] = table_name

    @builtins.property
    def kusto_cluster_name(self) -> builtins.str:
        '''Specifies the name of the Kusto Cluster this data connection will be added to.'''
        result = self._values.get("kusto_cluster_name")
        assert result is not None, "Required property 'kusto_cluster_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kusto_database_name(self) -> builtins.str:
        '''Specifies the name of the Kusto Database this data connection will be added to.'''
        result = self._values.get("kusto_database_name")
        assert result is not None, "Required property 'kusto_database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kusto_resource_group(
        self,
    ) -> _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup:
        '''Specifies the Resource Group where the Kusto Database should exist.'''
        result = self._values.get("kusto_resource_group")
        assert result is not None, "Required property 'kusto_resource_group' is missing"
        return typing.cast(_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location where the Kusto EventHub Data Connection should be created.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the Kusto EventHub Data Connection to create.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def compression(self) -> typing.Optional[builtins.str]:
        '''Specifies compression type for the connection.

        Allowed values: GZip and None.

        :default: "None"
        '''
        result = self._values.get("compression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def consumer_group(self) -> typing.Optional[builtins.str]:
        '''Specifies the EventHub consumer group this data connection will use for ingestion.

        :default: "$Default"
        '''
        result = self._values.get("consumer_group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def database_routing_type(self) -> typing.Optional[builtins.str]:
        '''Indication for database routing information from the data connection, by default only database routing information is allowed.

        Allowed values: Single, Multi.

        :default: "Single"
        '''
        result = self._values.get("database_routing_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the data format of the EventHub messages.

        Allowed values: APACHEAVRO, AVRO, CSV, JSON, MULTIJSON, ORC, PARQUET, PSV, RAW, SCSV, SINGLEJSON, SOHSV, TSVE, TSV, TXT, and W3CLOGFILE.

        :default: "JSON"
        '''
        result = self._values.get("data_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_id(self) -> typing.Optional[builtins.str]:
        '''The resource ID of a managed identity (system or user assigned) to be used to authenticate with event hub.'''
        result = self._values.get("identity_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mapping_rule_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the mapping rule used for the message ingestion.

        Mapping rule must exist before resource is created.
        '''
        result = self._values.get("mapping_rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def table_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the target table name used for the message ingestion.

        Table must exist before resource is created.
        '''
        result = self._values.get("table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def eventhub_id(self) -> builtins.str:
        '''Specifies the resource id of the EventHub this data connection will use for ingestion.'''
        result = self._values.get("eventhub_id")
        assert result is not None, "Required property 'eventhub_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KustoDataConnectionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Namespace(
    _AzureResourceWithAlert_c2e3918b,
    metaclass=jsii.JSIIMeta,
    jsii_type="@microsoft/terraform-cdk-constructs.azure_eventhub.Namespace",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        name_: builtins.str,
        *,
        name: builtins.str,
        auto_inflate_enabled: typing.Optional[builtins.bool] = None,
        capacity: typing.Optional[jsii.Number] = None,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        identity_type: typing.Optional[builtins.str] = None,
        local_authentication_enabled: typing.Optional[builtins.bool] = None,
        maximum_throughput_units: typing.Optional[jsii.Number] = None,
        minimum_tls_version: typing.Optional[builtins.str] = None,
        public_network_access_enabled: typing.Optional[builtins.bool] = None,
        resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
        sku: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        zone_redundant: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Constructs a new Event Hub Namespace.

        This class creates an Azure Event Hub Namespace, which serves as a container for all messaging components.
        Namespaces provide a scoping container for Event Hub resources within a specific region, which can be further
        controlled and managed using the provided settings.

        :param scope: - The scope in which to define this construct, typically representing the Cloud Development Kit (CDK) stack.
        :param name_: - The unique name for this instance of the Event Hub Namespace.
        :param name: The name of the EventHub Namespace to create.
        :param auto_inflate_enabled: Specifies if the EventHub Namespace should be Auto Inflate enabled. Default: false
        :param capacity: Specifies the Capacity / Throughput Units for a Standard SKU namespace. Default: 2
        :param identity_ids: Specifies a list of User Assigned Managed Identity IDs to be assigned to this EventHub namespace.
        :param identity_type: Specifies the type of Managed Service Identity that should be configured on this Event Hub Namespace. Possible values are SystemAssigned or UserAssigned. Default: "SystemAssigned"
        :param local_authentication_enabled: Is SAS authentication enabled for the EventHub Namespace? North Central US Not supported. Default: false
        :param maximum_throughput_units: Specifies the maximum number of throughput units when Auto Inflate is Enabled. Valid values range from 1 - 20. Default: 2
        :param minimum_tls_version: The minimum supported TLS version for this EventHub Namespace. Valid values are: 1.0, 1.1 and 1.2. Default: "1.2"
        :param public_network_access_enabled: Is public network access enabled for the EventHub Namespace? Default: true
        :param resource_group: An optional reference to the resource group in which to deploy the Event Hub Cluster. If not provided, the Event Hub Cluster will be deployed in the default resource group.
        :param sku: Defines which tier to use. Valid options are Basic, Standard, and Premium. Default: "Basic"
        :param tags: The tags to assign to the Key Vault.
        :param zone_redundant: Specifies if the EventHub Namespace should be Zone Redundant (created across Availability Zones). Default: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd10fe3a28646307e69b67ab941cf10ec21cbb8b7a0c307eb340fb37a0ccbdba)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument name_", value=name_, expected_type=type_hints["name_"])
        props = NamespaceProps(
            name=name,
            auto_inflate_enabled=auto_inflate_enabled,
            capacity=capacity,
            identity_ids=identity_ids,
            identity_type=identity_type,
            local_authentication_enabled=local_authentication_enabled,
            maximum_throughput_units=maximum_throughput_units,
            minimum_tls_version=minimum_tls_version,
            public_network_access_enabled=public_network_access_enabled,
            resource_group=resource_group,
            sku=sku,
            tags=tags,
            zone_redundant=zone_redundant,
        )

        jsii.create(self.__class__, self, [scope, name_, props])

    @jsii.member(jsii_name="addEventhubInstance")
    def add_eventhub_instance(
        self,
        *,
        name: builtins.str,
        message_retention: typing.Optional[jsii.Number] = None,
        partition_count: typing.Optional[jsii.Number] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> Instance:
        '''Creates and adds an Event Hub instance to the current namespace.

        This method sets up a new Event Hub instance within the namespace defined by this class. An Event Hub instance
        serves as a container that processes and stores events. This method facilitates the setup of multiple Event Hubs
        within a single namespace, each configured according to the specified properties.

        :param name: Specifies the name of the EventHub resource.
        :param message_retention: Specifies the number of days to retain the events for this Event Hub. Default: 1
        :param partition_count: Specifies the current number of shards on the Event Hub. When using a shared parent EventHub Namespace, maximum value is 32. Default: 2
        :param status: Specifies the status of the Event Hub resource. Possible values are Active, Disabled and SendDisabled. Default: "Active"

        :return:

        An instance of the Event Hub (``Instance`` class), configured with the specified properties.

        Example usage::

        const eventHub = namespace.addEventhubInstance({
        name: 'myEventHub',
        partitionCount: 4,
        messageRetention: 7,
        status: 'Active'
        });

        :remarks:

        Ensure that the namespace has sufficient capacity and configuration to support the properties of the Event Hub being created,
        especially in terms of partition count and throughput units if applicable.
        '''
        props = BaseInstanceProps(
            name=name,
            message_retention=message_retention,
            partition_count=partition_count,
            status=status,
        )

        return typing.cast(Instance, jsii.invoke(self, "addEventhubInstance", [props]))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "NamespaceProps":
        return typing.cast("NamespaceProps", jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68df9e05dd29b48311fc4d90dc9e00ac6c3f48740bd59c500eba8ca385ce3632)
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
            type_hints = typing.get_type_hints(_typecheckingstub__222713931f6bd804ed9f1b9fbec9d4632ff68b9c592ba7f00657688fbc697c93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroup", value)


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_eventhub.NamespaceProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "auto_inflate_enabled": "autoInflateEnabled",
        "capacity": "capacity",
        "identity_ids": "identityIds",
        "identity_type": "identityType",
        "local_authentication_enabled": "localAuthenticationEnabled",
        "maximum_throughput_units": "maximumThroughputUnits",
        "minimum_tls_version": "minimumTlsVersion",
        "public_network_access_enabled": "publicNetworkAccessEnabled",
        "resource_group": "resourceGroup",
        "sku": "sku",
        "tags": "tags",
        "zone_redundant": "zoneRedundant",
    },
)
class NamespaceProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        auto_inflate_enabled: typing.Optional[builtins.bool] = None,
        capacity: typing.Optional[jsii.Number] = None,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        identity_type: typing.Optional[builtins.str] = None,
        local_authentication_enabled: typing.Optional[builtins.bool] = None,
        maximum_throughput_units: typing.Optional[jsii.Number] = None,
        minimum_tls_version: typing.Optional[builtins.str] = None,
        public_network_access_enabled: typing.Optional[builtins.bool] = None,
        resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
        sku: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        zone_redundant: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param name: The name of the EventHub Namespace to create.
        :param auto_inflate_enabled: Specifies if the EventHub Namespace should be Auto Inflate enabled. Default: false
        :param capacity: Specifies the Capacity / Throughput Units for a Standard SKU namespace. Default: 2
        :param identity_ids: Specifies a list of User Assigned Managed Identity IDs to be assigned to this EventHub namespace.
        :param identity_type: Specifies the type of Managed Service Identity that should be configured on this Event Hub Namespace. Possible values are SystemAssigned or UserAssigned. Default: "SystemAssigned"
        :param local_authentication_enabled: Is SAS authentication enabled for the EventHub Namespace? North Central US Not supported. Default: false
        :param maximum_throughput_units: Specifies the maximum number of throughput units when Auto Inflate is Enabled. Valid values range from 1 - 20. Default: 2
        :param minimum_tls_version: The minimum supported TLS version for this EventHub Namespace. Valid values are: 1.0, 1.1 and 1.2. Default: "1.2"
        :param public_network_access_enabled: Is public network access enabled for the EventHub Namespace? Default: true
        :param resource_group: An optional reference to the resource group in which to deploy the Event Hub Cluster. If not provided, the Event Hub Cluster will be deployed in the default resource group.
        :param sku: Defines which tier to use. Valid options are Basic, Standard, and Premium. Default: "Basic"
        :param tags: The tags to assign to the Key Vault.
        :param zone_redundant: Specifies if the EventHub Namespace should be Zone Redundant (created across Availability Zones). Default: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__519836849fa3453a694ed144010f5350fb88e448353ce28e09e57559ef5020eb)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument auto_inflate_enabled", value=auto_inflate_enabled, expected_type=type_hints["auto_inflate_enabled"])
            check_type(argname="argument capacity", value=capacity, expected_type=type_hints["capacity"])
            check_type(argname="argument identity_ids", value=identity_ids, expected_type=type_hints["identity_ids"])
            check_type(argname="argument identity_type", value=identity_type, expected_type=type_hints["identity_type"])
            check_type(argname="argument local_authentication_enabled", value=local_authentication_enabled, expected_type=type_hints["local_authentication_enabled"])
            check_type(argname="argument maximum_throughput_units", value=maximum_throughput_units, expected_type=type_hints["maximum_throughput_units"])
            check_type(argname="argument minimum_tls_version", value=minimum_tls_version, expected_type=type_hints["minimum_tls_version"])
            check_type(argname="argument public_network_access_enabled", value=public_network_access_enabled, expected_type=type_hints["public_network_access_enabled"])
            check_type(argname="argument resource_group", value=resource_group, expected_type=type_hints["resource_group"])
            check_type(argname="argument sku", value=sku, expected_type=type_hints["sku"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument zone_redundant", value=zone_redundant, expected_type=type_hints["zone_redundant"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if auto_inflate_enabled is not None:
            self._values["auto_inflate_enabled"] = auto_inflate_enabled
        if capacity is not None:
            self._values["capacity"] = capacity
        if identity_ids is not None:
            self._values["identity_ids"] = identity_ids
        if identity_type is not None:
            self._values["identity_type"] = identity_type
        if local_authentication_enabled is not None:
            self._values["local_authentication_enabled"] = local_authentication_enabled
        if maximum_throughput_units is not None:
            self._values["maximum_throughput_units"] = maximum_throughput_units
        if minimum_tls_version is not None:
            self._values["minimum_tls_version"] = minimum_tls_version
        if public_network_access_enabled is not None:
            self._values["public_network_access_enabled"] = public_network_access_enabled
        if resource_group is not None:
            self._values["resource_group"] = resource_group
        if sku is not None:
            self._values["sku"] = sku
        if tags is not None:
            self._values["tags"] = tags
        if zone_redundant is not None:
            self._values["zone_redundant"] = zone_redundant

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the EventHub Namespace to create.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auto_inflate_enabled(self) -> typing.Optional[builtins.bool]:
        '''Specifies if the EventHub Namespace should be Auto Inflate enabled.

        :default: false
        '''
        result = self._values.get("auto_inflate_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def capacity(self) -> typing.Optional[jsii.Number]:
        '''Specifies the Capacity / Throughput Units for a Standard SKU namespace.

        :default: 2
        '''
        result = self._values.get("capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def identity_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of User Assigned Managed Identity IDs to be assigned to this EventHub namespace.'''
        result = self._values.get("identity_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def identity_type(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of Managed Service Identity that should be configured on this Event Hub Namespace.

        Possible values are SystemAssigned or UserAssigned.

        :default: "SystemAssigned"
        '''
        result = self._values.get("identity_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_authentication_enabled(self) -> typing.Optional[builtins.bool]:
        '''Is SAS authentication enabled for the EventHub Namespace?

        North Central US Not supported.

        :default: false
        '''
        result = self._values.get("local_authentication_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def maximum_throughput_units(self) -> typing.Optional[jsii.Number]:
        '''Specifies the maximum number of throughput units when Auto Inflate is Enabled.

        Valid values range from 1 - 20.

        :default: 2
        '''
        result = self._values.get("maximum_throughput_units")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minimum_tls_version(self) -> typing.Optional[builtins.str]:
        '''The minimum supported TLS version for this EventHub Namespace.

        Valid values are: 1.0, 1.1 and 1.2.

        :default: "1.2"
        '''
        result = self._values.get("minimum_tls_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_network_access_enabled(self) -> typing.Optional[builtins.bool]:
        '''Is public network access enabled for the EventHub Namespace?

        :default: true
        '''
        result = self._values.get("public_network_access_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def resource_group(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup]:
        '''An optional reference to the resource group in which to deploy the Event Hub Cluster.

        If not provided, the Event Hub Cluster will be deployed in the default resource group.
        '''
        result = self._values.get("resource_group")
        return typing.cast(typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup], result)

    @builtins.property
    def sku(self) -> typing.Optional[builtins.str]:
        '''Defines which tier to use.

        Valid options are Basic, Standard, and Premium.

        :default: "Basic"
        '''
        result = self._values.get("sku")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The tags to assign to the Key Vault.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def zone_redundant(self) -> typing.Optional[builtins.bool]:
        '''Specifies if the EventHub Namespace should be Zone Redundant (created across Availability Zones).

        :default: true
        '''
        result = self._values.get("zone_redundant")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NamespaceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AuthorizationRule",
    "AuthorizationRuleProps",
    "BaseInstanceProps",
    "BaseKustoDataConnectionProps",
    "Cluster",
    "ConsumerGroup",
    "ConsumerGroupProps",
    "EventHubClusterProps",
    "Instance",
    "InstanceProps",
    "KustoDataConnection",
    "KustoDataConnectionProps",
    "Namespace",
    "NamespaceProps",
]

publication.publish()

def _typecheckingstub__7c1c6f293e6acf5436c72813818813598afbd2a83ba004aa4ccf61ed33758436(
    scope: _constructs_77d1e7e8.Construct,
    name_: builtins.str,
    *,
    eventhub_name: builtins.str,
    name: builtins.str,
    namespace_name: builtins.str,
    resource_group_name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    listen: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    manage: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    send: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_eventhub_authorization_rule_92bbcedf.EventhubAuthorizationRuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0214ac5924c3dc5c9e3f26b91a6c9b1d3dfe07ad2ea89e13535ffd8ec5a4ba0b(
    vault: _Vault_3dbe0187,
    name: builtins.str,
    expiration_date: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99de90f20bfe2eb69b5f50c097faa58d627eaca216cadc2732f88dadb737107d(
    vault: _Vault_3dbe0187,
    name: builtins.str,
    expiration_date: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d14b7ca345031d7d76fdb93aa3a21bdc290a32f9bb5730d9e9ebd608e85a2737(
    *,
    name: builtins.str,
    listen: typing.Optional[builtins.bool] = None,
    manage: typing.Optional[builtins.bool] = None,
    send: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31739a1c075beeaa002d3eefcd272a71ba46aacd5a741e6e66345de650d9a9e7(
    *,
    name: builtins.str,
    message_retention: typing.Optional[jsii.Number] = None,
    partition_count: typing.Optional[jsii.Number] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0689b3cc5855245f78be80a1a26107af28531e4f6e7c45d9451dd6180b8316d(
    *,
    kusto_cluster_name: builtins.str,
    kusto_database_name: builtins.str,
    kusto_resource_group: _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup,
    location: builtins.str,
    name: builtins.str,
    compression: typing.Optional[builtins.str] = None,
    consumer_group: typing.Optional[builtins.str] = None,
    database_routing_type: typing.Optional[builtins.str] = None,
    data_format: typing.Optional[builtins.str] = None,
    identity_id: typing.Optional[builtins.str] = None,
    mapping_rule_name: typing.Optional[builtins.str] = None,
    table_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9325412d61ac035504e7b062fbc0964eb65b9626d0007084dde7186a87bed5fa(
    scope: _constructs_77d1e7e8.Construct,
    name_: builtins.str,
    *,
    name: builtins.str,
    resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
    sku_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2005aa8f57434f9765546b33a3fd9c29a44e344e4c145aeca1155fbc2c755cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66a33608fc271b155bfcb128a658452996ea2776e99607f1cc49ee62c541b1e2(
    value: _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a8139279750b65048fa5110a327c0d601a1554c23b92e2c2cba7f8e89ff87cd(
    scope: _constructs_77d1e7e8.Construct,
    name_: builtins.str,
    *,
    eventhub_name: builtins.str,
    name: builtins.str,
    namespace_name: builtins.str,
    resource_group: _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup,
    user_metadata: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e8f89b463fc90e79558f1493e210f98c407f279a95929c357a6fb5c9ed2e142(
    *,
    eventhub_name: builtins.str,
    name: builtins.str,
    namespace_name: builtins.str,
    resource_group: _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup,
    user_metadata: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a18ded3b6e021459ebd10c2faa67178f8c192d6b057a954ba0b9c9703a6aa48(
    *,
    name: builtins.str,
    resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
    sku_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4948905e1978b1095ac0f766fdab18a145e3616c5ab54b06f33b4b2184c4a2b5(
    scope: _constructs_77d1e7e8.Construct,
    name: builtins.str,
    *,
    namespace_name: builtins.str,
    resource_group: _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup,
    name: builtins.str,
    message_retention: typing.Optional[jsii.Number] = None,
    partition_count: typing.Optional[jsii.Number] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe8193289e2151a2d124ddd011eace10bee17e5b578d6b819df127f9d4b2e382(
    name: builtins.str,
    user_metadata: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f05ad2cf1dc9e1093643ee5300849f817d2f1fd487f8bf5b767b31e1ce3f414(
    *,
    name: builtins.str,
    message_retention: typing.Optional[jsii.Number] = None,
    partition_count: typing.Optional[jsii.Number] = None,
    status: typing.Optional[builtins.str] = None,
    namespace_name: builtins.str,
    resource_group: _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62b3da48c45f3f6e9b8c2e99377ece2ac8ca75b941ca3990d7da9809fe5c2849(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    eventhub_id: builtins.str,
    kusto_cluster_name: builtins.str,
    kusto_database_name: builtins.str,
    kusto_resource_group: _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup,
    location: builtins.str,
    name: builtins.str,
    compression: typing.Optional[builtins.str] = None,
    consumer_group: typing.Optional[builtins.str] = None,
    database_routing_type: typing.Optional[builtins.str] = None,
    data_format: typing.Optional[builtins.str] = None,
    identity_id: typing.Optional[builtins.str] = None,
    mapping_rule_name: typing.Optional[builtins.str] = None,
    table_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bfa41b399d7b3d24221998820347cbea3233009963ae993b32aba3bed46a284(
    *,
    kusto_cluster_name: builtins.str,
    kusto_database_name: builtins.str,
    kusto_resource_group: _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup,
    location: builtins.str,
    name: builtins.str,
    compression: typing.Optional[builtins.str] = None,
    consumer_group: typing.Optional[builtins.str] = None,
    database_routing_type: typing.Optional[builtins.str] = None,
    data_format: typing.Optional[builtins.str] = None,
    identity_id: typing.Optional[builtins.str] = None,
    mapping_rule_name: typing.Optional[builtins.str] = None,
    table_name: typing.Optional[builtins.str] = None,
    eventhub_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd10fe3a28646307e69b67ab941cf10ec21cbb8b7a0c307eb340fb37a0ccbdba(
    scope: _constructs_77d1e7e8.Construct,
    name_: builtins.str,
    *,
    name: builtins.str,
    auto_inflate_enabled: typing.Optional[builtins.bool] = None,
    capacity: typing.Optional[jsii.Number] = None,
    identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    identity_type: typing.Optional[builtins.str] = None,
    local_authentication_enabled: typing.Optional[builtins.bool] = None,
    maximum_throughput_units: typing.Optional[jsii.Number] = None,
    minimum_tls_version: typing.Optional[builtins.str] = None,
    public_network_access_enabled: typing.Optional[builtins.bool] = None,
    resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
    sku: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    zone_redundant: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68df9e05dd29b48311fc4d90dc9e00ac6c3f48740bd59c500eba8ca385ce3632(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__222713931f6bd804ed9f1b9fbec9d4632ff68b9c592ba7f00657688fbc697c93(
    value: _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__519836849fa3453a694ed144010f5350fb88e448353ce28e09e57559ef5020eb(
    *,
    name: builtins.str,
    auto_inflate_enabled: typing.Optional[builtins.bool] = None,
    capacity: typing.Optional[jsii.Number] = None,
    identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    identity_type: typing.Optional[builtins.str] = None,
    local_authentication_enabled: typing.Optional[builtins.bool] = None,
    maximum_throughput_units: typing.Optional[jsii.Number] = None,
    minimum_tls_version: typing.Optional[builtins.str] = None,
    public_network_access_enabled: typing.Optional[builtins.bool] = None,
    resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
    sku: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    zone_redundant: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass
