'''
# Azure Storage Account Construct

This documentation covers the Azure Storage Account Construct, a comprehensive class for managing various storage solutions within Azure. It provides a convenient and efficient way to deploy and manage Azure Storage resources, including Containers, File Shares, Tables, Queues, and Network Rules.

## What is Azure Storage Account?

Azure Storage Account offers a scalable and secure place for storing data in the cloud. It supports a variety of data objects such as blobs, files, queues, and tables, making it ideal for a wide range of storage scenarios.

Learn more about Azure Storage Account in the official Azure documentation.

## Best Practices for Azure Storage Account

Use different storage accounts for different types of data to optimize performance.
Enable secure transfer to ensure data is encrypted during transit.
Implement access policies and use Azure Active Directory (AAD) for authentication.
Regularly monitor and audit your storage account activity.
Azure Storage Account Class Properties
The class has several properties to customize the behavior of the Storage Account:

* **name**: Unique name of the Storage Account.
* **location**: Azure Region for the Storage Account deployment.
* **resourceGroup**: Azure Resource Group to which the Storage Account belongs.
* **tags**: Key-value pairs for resource categorization.
* **accountReplicationType**: Type of data replication (e.g., LRS, GRS).
* **accountTier**: Performance tier (Standard, Premium).

Additional properties like enableHttpsTrafficOnly, accessTier, isHnsEnabled, etc.

## Deploying the Azure Storage Account

```python
const storageAccount = new AzureStorageAccount(this, 'storageaccount', {
  name: 'myStorageAccount',
  location: 'East US',
  resourceGroup: myResourceGroup,
  accountReplicationType: 'LRS',
  accountTier: 'Standard',
  // Other properties
});
```

This code snippet creates a new Storage Account with specified properties.

### Creating a Storage Container

Containers in Azure Blob Storage are used to store blobs. Here's how to deploy a Container:

```python
const storageAccount = new AzureStorageAccount(this, 'storageaccount', {
  name: 'myStorageAccount',
  location: 'East US',
});

const storageContainer = storageAccount.addContainer("myContainer");
// Upload a local file to blob storage
storageContainer.addBlob("testblob.txt", "../../../test.txt")
```

This will create a new container named myContainer in the Storage Account and upload a local file to the Container as blob storage.

### Deploying a File Share

Azure File Share provides managed file shares for cloud or on-premises deployments. To deploy a File Share:

```python
const storageAccount = new AzureStorageAccount(this, 'storageaccount', {
  name: 'myStorageAccount',
  location: 'East US',
});

const storageFileShare = storageAccount.addFileShare("testshare")
// Upload a local file to the share
storageFileShare.addFile("testfile.txt", "../../../test.txt")
```

### Creating a Storage Table

Azure Table Storage offers NoSQL data storage for large-scale applications. Here's how to create a Table:

```python
const storageAccount = new AzureStorageAccount(this, 'storageaccount', {
  name: 'myStorageAccount',
  location: 'East US',
});

const storageTable = storageAccount.addTable("myTable")
```

### Adding a Queue

Azure Queue Storage enables storing large numbers of messages. To create a Queue:

```python
const queue = storageAccount.addQueue("myQueue")
```

### Configuring Network Rules

Network rules add an additional layer of security. Here's how to set them up:

```python
const storageAccount = new AzureStorageAccount(this, 'storageaccount', {
  name: 'myStorageAccount',
  location: 'East US',
});

storageAccount.addNetworkRules({
  bypass: ["AzureServices"],
  defaultAction: "Deny",
  ipRules: ["1.2.3.4/32"],
});
```

This will configure network rules for your Storage Account according to the specified properties.
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
import cdktf_cdktf_provider_azurerm.storage_account_network_rules as _cdktf_cdktf_provider_azurerm_storage_account_network_rules_92bbcedf
import cdktf_cdktf_provider_azurerm.storage_blob as _cdktf_cdktf_provider_azurerm_storage_blob_92bbcedf
import cdktf_cdktf_provider_azurerm.storage_container as _cdktf_cdktf_provider_azurerm_storage_container_92bbcedf
import cdktf_cdktf_provider_azurerm.storage_queue as _cdktf_cdktf_provider_azurerm_storage_queue_92bbcedf
import cdktf_cdktf_provider_azurerm.storage_share as _cdktf_cdktf_provider_azurerm_storage_share_92bbcedf
import cdktf_cdktf_provider_azurerm.storage_share_file as _cdktf_cdktf_provider_azurerm_storage_share_file_92bbcedf
import cdktf_cdktf_provider_azurerm.storage_table as _cdktf_cdktf_provider_azurerm_storage_table_92bbcedf
import constructs as _constructs_77d1e7e8
from ..core_azure import AzureResourceWithAlert as _AzureResourceWithAlert_c2e3918b


class Account(
    _AzureResourceWithAlert_c2e3918b,
    metaclass=jsii.JSIIMeta,
    jsii_type="@microsoft/terraform-cdk-constructs.azure_storageaccount.Account",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        access_tier: typing.Optional[builtins.str] = None,
        account_kind: typing.Optional[builtins.str] = None,
        account_replication_type: typing.Optional[builtins.str] = None,
        account_tier: typing.Optional[builtins.str] = None,
        enable_https_traffic_only: typing.Optional[builtins.bool] = None,
        identity: typing.Any = None,
        is_hns_enabled: typing.Optional[builtins.bool] = None,
        min_tls_version: typing.Optional[builtins.str] = None,
        public_network_access_enabled: typing.Optional[builtins.bool] = None,
        resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Represents an Azure Storage Account within a Terraform deployment.

        This class is responsible for the creation and management of an Azure Storage Account, which is a scalable and secure service
        for storing large amounts of unstructured data that can be accessed from anywhere in the world over HTTP or HTTPS. Common uses
        of the Azure Storage Account include storing of blobs (objects), file shares, tables, and queues. This class provides methods
        to manage storage resources, configure network rules, and integrate with Azure Active Directory for secure access management.

        :param scope: - The scope in which to define this construct, typically representing the Cloud Development Kit (CDK) stack.
        :param id: - The unique identifier for this instance of the storage account.
        :param location: The Azure region in which to create the storage account.
        :param name: The name of the storage account. Must be unique across Azure.
        :param access_tier: The data access tier of the storage account, which impacts storage costs and data retrieval speeds. Example values: Hot, Cool.
        :param account_kind: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.92.0/docs/resources/storage_account#account_kind StorageAccount#account_kind}.
        :param account_replication_type: The type of replication to use for the storage account. This determines how your data is replicated across Azure's infrastructure. Example values: LRS (Locally Redundant Storage), GRS (Geo-Redundant Storage), RAGRS (Read Access Geo-Redundant Storage).
        :param account_tier: The performance tier of the storage account. Determines the type of hardware and performance level. Example values: Standard, Premium.
        :param enable_https_traffic_only: A boolean flag indicating whether to enforce HTTPS for data transfer to the storage account.
        :param identity: Managed Service Identity (MSI) details. Used for enabling and managing Azure Active Directory (AAD) authentication.
        :param is_hns_enabled: A flag indicating whether the Hierarchical Namespace (HNS) is enabled, which is required for Azure Data Lake Storage Gen2 features.
        :param min_tls_version: The minimum TLS version to be used for securing connections to the storage account. Example values: TLS1_0, TLS1_1, TLS1_2.
        :param public_network_access_enabled: A boolean flag indicating whether public network access to the storage account is allowed.
        :param resource_group: The name of the Azure resource group in which to create the storage account.
        :param tags: Tags to apply to the storage account, used for categorization and billing purposes. Format: { [key: string]: string }
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cf8d651224015dd5f566f70fa4f6451c4aa70245e080717f03189f597288cda)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AccountProps(
            location=location,
            name=name,
            access_tier=access_tier,
            account_kind=account_kind,
            account_replication_type=account_replication_type,
            account_tier=account_tier,
            enable_https_traffic_only=enable_https_traffic_only,
            identity=identity,
            is_hns_enabled=is_hns_enabled,
            min_tls_version=min_tls_version,
            public_network_access_enabled=public_network_access_enabled,
            resource_group=resource_group,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addContainer")
    def add_container(
        self,
        name: builtins.str,
        container_access_type: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> "Container":
        '''Adds a new container to the storage account.

        :param name: The name of the container. It must be unique within the storage account.
        :param container_access_type: The level of public access to the container. Defaults to 'private'.
        :param metadata: Optional metadata for the container as key-value pairs.

        :return: The created Container instance.

        :throws:

        Error if a container with the same name already exists within the storage account.

        This method creates a new container within the Azure storage account, allowing for the specification of access
        level and metadata. If the container already exists, it throws an error to prevent duplication.

        Example usage::

        const container = storageAccount.addContainer('myContainer', 'private', { owner: 'IT' });
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1507cad6d96c6bff9c8948d2fc2dc3b492f45668b2d27256eeeb72784ce61712)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument container_access_type", value=container_access_type, expected_type=type_hints["container_access_type"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
        return typing.cast("Container", jsii.invoke(self, "addContainer", [name, container_access_type, metadata]))

    @jsii.member(jsii_name="addFileShare")
    def add_file_share(
        self,
        name: builtins.str,
        *,
        access_tier: typing.Optional[builtins.str] = None,
        acl: typing.Any = None,
        enabled_protocol: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        quota: typing.Optional[jsii.Number] = None,
    ) -> "FileShare":
        '''Adds a new file share to the storage account.

        :param name: The name of the file share. Must be unique within the storage account.
        :param access_tier: The access tier of the storage share. This property is only applicable to storage shares with a premium account type. Example values: Hot, Cool.
        :param acl: A list of access control rules for the storage share.
        :param enabled_protocol: The protocol to use when accessing the storage share. Example values: SMB, NFS.
        :param metadata: A mapping of tags to assign to the storage share. Format: { [key: string]: string }
        :param quota: The maximum size of the storage share, in gigabytes.

        :return: The created FileShare instance.

        :throws:

        Error if a file share with the same name already exists.

        This method facilitates the addition of a file share to the storage account, with optional settings for
        capacity (quota) and data access frequency (access tier). If a file share with the same name exists, an error is thrown.

        Example usage::

        const fileShare = storageAccount.addFileShare('myFileShare', { quota: 1024, accessTier: 'Hot' });
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__417198ca18a6617286bb83e6a9fd18479dae6f9437b3f86bfed5be54795acc23)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        props = FileShareProps(
            access_tier=access_tier,
            acl=acl,
            enabled_protocol=enabled_protocol,
            metadata=metadata,
            quota=quota,
        )

        return typing.cast("FileShare", jsii.invoke(self, "addFileShare", [name, props]))

    @jsii.member(jsii_name="addNetworkRules")
    def add_network_rules(
        self,
        *,
        default_action: builtins.str,
        bypass: typing.Optional[typing.Sequence[builtins.str]] = None,
        ip_rules: typing.Optional[typing.Sequence[builtins.str]] = None,
        private_link_access: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_azurerm_storage_account_network_rules_92bbcedf.StorageAccountNetworkRulesPrivateLinkAccessA, typing.Dict[builtins.str, typing.Any]]]] = None,
        virtual_network_subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _cdktf_cdktf_provider_azurerm_storage_account_network_rules_92bbcedf.StorageAccountNetworkRulesA:
        '''Adds network rules to the storage account to control access based on IP and virtual network settings.

        :param default_action: The default action of the network rule set. Options are 'Allow' or 'Deny'. Set to 'Deny' to enable network rules and restrict access to the storage account. 'Allow' permits access by default.
        :param bypass: Specifies which traffic to bypass from the network rules. The possible values are 'AzureServices', 'Logging', 'Metrics', and 'None'. Bypassing 'AzureServices' enables Azure's internal services to access the storage account.
        :param ip_rules: An array of IP rules to allow access to the storage account. These are specified as CIDR ranges. Example: ['1.2.3.4/32', '5.6.7.0/24'] to allow specific IPs/subnets.
        :param private_link_access: An array of objects representing the private link access settings. Each object in the array defines the sub-resource name (e.g., 'blob', 'file') and its respective private endpoint connections for the storage account.
        :param virtual_network_subnet_ids: An array of virtual network subnet IDs that are allowed to access the storage account. This enables you to secure the storage account to a specific virtual network and subnet within Azure.

        :return:

        The configured network rules.

        This method configures network rules for the storage account, specifying which IPs and virtual networks can access
        the storage resources. It allows detailed control over data security and access management.

        Example usage::

        storageAccount.addNetworkRules({
        bypass: ['AzureServices'],
        defaultAction: 'Deny',
        ipRules: ['1.2.3.4/32'],
        virtualNetworkSubnetIds: ['subnetId'],
        });
        '''
        props = NetworkRulesProps(
            default_action=default_action,
            bypass=bypass,
            ip_rules=ip_rules,
            private_link_access=private_link_access,
            virtual_network_subnet_ids=virtual_network_subnet_ids,
        )

        return typing.cast(_cdktf_cdktf_provider_azurerm_storage_account_network_rules_92bbcedf.StorageAccountNetworkRulesA, jsii.invoke(self, "addNetworkRules", [props]))

    @jsii.member(jsii_name="addQueue")
    def add_queue(
        self,
        name: builtins.str,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> "Queue":
        '''Adds a new queue to the storage account.

        :param name: The name of the queue. Must be unique within the storage account.
        :param metadata: Optional metadata for the queue as key-value pairs.

        :return:

        The created Queue instance.

        This method creates a new queue in the storage account, with optional metadata. It is useful for message queuing
        in applications, enabling asynchronous task processing and inter-service communication.

        Example usage::

        const queue = storageAccount.addQueue('myQueue', { priority: 'high' });
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01ff1359fcff7f63e01967486b6eab1309a5a0499600d0f9996baaece4d468bd)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
        return typing.cast("Queue", jsii.invoke(self, "addQueue", [name, metadata]))

    @jsii.member(jsii_name="addTable")
    def add_table(
        self,
        name: builtins.str,
        acl: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_azurerm_storage_table_92bbcedf.StorageTableAcl, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> "Table":
        '''Adds a new table to the storage account.

        :param name: The name of the table. Must be unique within the storage account.
        :param acl: Optional access control list for the table, specifying permissions.

        :return: The created Table instance.

        :throws:

        Error if a table with the same name already exists.

        This method creates a new table within the storage account, optionally allowing for access control configurations.
        It throws an error if a table with the same name already exists, ensuring uniqueness within the account.

        Example usage::

        const table = storageAccount.addTable('myTable', [{ id: 'policy1', type: 'read' }]);
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa42f736eee4b505889af078f894ef6cb9dfdc60488ee3b76d0ece3d794f5ff6)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument acl", value=acl, expected_type=type_hints["acl"])
        return typing.cast("Table", jsii.invoke(self, "addTable", [name, acl]))

    @builtins.property
    @jsii.member(jsii_name="accountKind")
    def account_kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountKind"))

    @builtins.property
    @jsii.member(jsii_name="accountTier")
    def account_tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountTier"))

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
    def props(self) -> "AccountProps":
        return typing.cast("AccountProps", jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5024b09e7cb3af550bee25059decceb2e25cbec13a7b5afe4b3170d8e7c13ab0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__98ede1f7c205554b760d9e374dba3482370df0f4a4e133b3ca6dd38d5cb2a801)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroup", value)


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_storageaccount.AccountProps",
    jsii_struct_bases=[],
    name_mapping={
        "location": "location",
        "name": "name",
        "access_tier": "accessTier",
        "account_kind": "accountKind",
        "account_replication_type": "accountReplicationType",
        "account_tier": "accountTier",
        "enable_https_traffic_only": "enableHttpsTrafficOnly",
        "identity": "identity",
        "is_hns_enabled": "isHnsEnabled",
        "min_tls_version": "minTlsVersion",
        "public_network_access_enabled": "publicNetworkAccessEnabled",
        "resource_group": "resourceGroup",
        "tags": "tags",
    },
)
class AccountProps:
    def __init__(
        self,
        *,
        location: builtins.str,
        name: builtins.str,
        access_tier: typing.Optional[builtins.str] = None,
        account_kind: typing.Optional[builtins.str] = None,
        account_replication_type: typing.Optional[builtins.str] = None,
        account_tier: typing.Optional[builtins.str] = None,
        enable_https_traffic_only: typing.Optional[builtins.bool] = None,
        identity: typing.Any = None,
        is_hns_enabled: typing.Optional[builtins.bool] = None,
        min_tls_version: typing.Optional[builtins.str] = None,
        public_network_access_enabled: typing.Optional[builtins.bool] = None,
        resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param location: The Azure region in which to create the storage account.
        :param name: The name of the storage account. Must be unique across Azure.
        :param access_tier: The data access tier of the storage account, which impacts storage costs and data retrieval speeds. Example values: Hot, Cool.
        :param account_kind: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.92.0/docs/resources/storage_account#account_kind StorageAccount#account_kind}.
        :param account_replication_type: The type of replication to use for the storage account. This determines how your data is replicated across Azure's infrastructure. Example values: LRS (Locally Redundant Storage), GRS (Geo-Redundant Storage), RAGRS (Read Access Geo-Redundant Storage).
        :param account_tier: The performance tier of the storage account. Determines the type of hardware and performance level. Example values: Standard, Premium.
        :param enable_https_traffic_only: A boolean flag indicating whether to enforce HTTPS for data transfer to the storage account.
        :param identity: Managed Service Identity (MSI) details. Used for enabling and managing Azure Active Directory (AAD) authentication.
        :param is_hns_enabled: A flag indicating whether the Hierarchical Namespace (HNS) is enabled, which is required for Azure Data Lake Storage Gen2 features.
        :param min_tls_version: The minimum TLS version to be used for securing connections to the storage account. Example values: TLS1_0, TLS1_1, TLS1_2.
        :param public_network_access_enabled: A boolean flag indicating whether public network access to the storage account is allowed.
        :param resource_group: The name of the Azure resource group in which to create the storage account.
        :param tags: Tags to apply to the storage account, used for categorization and billing purposes. Format: { [key: string]: string }
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0072c193a9790f4f261e3f6c7c6cad7d13e9d662dc060adff5d380ad9854013)
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument access_tier", value=access_tier, expected_type=type_hints["access_tier"])
            check_type(argname="argument account_kind", value=account_kind, expected_type=type_hints["account_kind"])
            check_type(argname="argument account_replication_type", value=account_replication_type, expected_type=type_hints["account_replication_type"])
            check_type(argname="argument account_tier", value=account_tier, expected_type=type_hints["account_tier"])
            check_type(argname="argument enable_https_traffic_only", value=enable_https_traffic_only, expected_type=type_hints["enable_https_traffic_only"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument is_hns_enabled", value=is_hns_enabled, expected_type=type_hints["is_hns_enabled"])
            check_type(argname="argument min_tls_version", value=min_tls_version, expected_type=type_hints["min_tls_version"])
            check_type(argname="argument public_network_access_enabled", value=public_network_access_enabled, expected_type=type_hints["public_network_access_enabled"])
            check_type(argname="argument resource_group", value=resource_group, expected_type=type_hints["resource_group"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "name": name,
        }
        if access_tier is not None:
            self._values["access_tier"] = access_tier
        if account_kind is not None:
            self._values["account_kind"] = account_kind
        if account_replication_type is not None:
            self._values["account_replication_type"] = account_replication_type
        if account_tier is not None:
            self._values["account_tier"] = account_tier
        if enable_https_traffic_only is not None:
            self._values["enable_https_traffic_only"] = enable_https_traffic_only
        if identity is not None:
            self._values["identity"] = identity
        if is_hns_enabled is not None:
            self._values["is_hns_enabled"] = is_hns_enabled
        if min_tls_version is not None:
            self._values["min_tls_version"] = min_tls_version
        if public_network_access_enabled is not None:
            self._values["public_network_access_enabled"] = public_network_access_enabled
        if resource_group is not None:
            self._values["resource_group"] = resource_group
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def location(self) -> builtins.str:
        '''The Azure region in which to create the storage account.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the storage account.

        Must be unique across Azure.
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_tier(self) -> typing.Optional[builtins.str]:
        '''The data access tier of the storage account, which impacts storage costs and data retrieval speeds.

        Example values: Hot, Cool.
        '''
        result = self._values.get("access_tier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def account_kind(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.92.0/docs/resources/storage_account#account_kind StorageAccount#account_kind}.'''
        result = self._values.get("account_kind")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def account_replication_type(self) -> typing.Optional[builtins.str]:
        '''The type of replication to use for the storage account.

        This determines how your data is replicated across Azure's infrastructure.
        Example values: LRS (Locally Redundant Storage), GRS (Geo-Redundant Storage), RAGRS (Read Access Geo-Redundant Storage).
        '''
        result = self._values.get("account_replication_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def account_tier(self) -> typing.Optional[builtins.str]:
        '''The performance tier of the storage account.

        Determines the type of hardware and performance level.
        Example values: Standard, Premium.
        '''
        result = self._values.get("account_tier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_https_traffic_only(self) -> typing.Optional[builtins.bool]:
        '''A boolean flag indicating whether to enforce HTTPS for data transfer to the storage account.'''
        result = self._values.get("enable_https_traffic_only")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def identity(self) -> typing.Any:
        '''Managed Service Identity (MSI) details.

        Used for enabling and managing Azure Active Directory (AAD) authentication.
        '''
        result = self._values.get("identity")
        return typing.cast(typing.Any, result)

    @builtins.property
    def is_hns_enabled(self) -> typing.Optional[builtins.bool]:
        '''A flag indicating whether the Hierarchical Namespace (HNS) is enabled, which is required for Azure Data Lake Storage Gen2 features.'''
        result = self._values.get("is_hns_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def min_tls_version(self) -> typing.Optional[builtins.str]:
        '''The minimum TLS version to be used for securing connections to the storage account.

        Example values: TLS1_0, TLS1_1, TLS1_2.
        '''
        result = self._values.get("min_tls_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_network_access_enabled(self) -> typing.Optional[builtins.bool]:
        '''A boolean flag indicating whether public network access to the storage account is allowed.'''
        result = self._values.get("public_network_access_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def resource_group(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup]:
        '''The name of the Azure resource group in which to create the storage account.'''
        result = self._values.get("resource_group")
        return typing.cast(typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Tags to apply to the storage account, used for categorization and billing purposes.

        Format: { [key: string]: string }
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccountProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Blob(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@microsoft/terraform-cdk-constructs.azure_storageaccount.Blob",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        storage_account_name: builtins.str,
        storage_container_name: builtins.str,
        type: builtins.str,
        access_tier: typing.Optional[builtins.str] = None,
        cache_control: typing.Optional[builtins.str] = None,
        content_md5: typing.Optional[builtins.str] = None,
        content_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        parallelism: typing.Optional[jsii.Number] = None,
        size: typing.Optional[jsii.Number] = None,
        source: typing.Optional[builtins.str] = None,
        source_content: typing.Optional[builtins.str] = None,
        source_uri: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_storage_blob_92bbcedf.StorageBlobTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Represents a blob within an Azure Storage Container.

        This class is responsible for the creation and management of a blob in an Azure Storage Container. Blobs are unstructured
        data objects, which can include files like images, documents, videos, or any other file type. The Blob class provides a way
        to manage these files in the cloud, allowing for scalable, durable, and accessible data storage. This class supports various
        blob types such as block blobs for text and binary data, append blobs for log files, and page blobs for large volumes of
        random access data.

        :param scope: - The scope in which to define this construct, typically representing the Cloud Development Kit (CDK) stack.
        :param id_: - The unique identifier for this instance of the blob.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_blob#name StorageBlob#name}.
        :param storage_account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_blob#storage_account_name StorageBlob#storage_account_name}.
        :param storage_container_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_blob#storage_container_name StorageBlob#storage_container_name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_blob#type StorageBlob#type}.
        :param access_tier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_blob#access_tier StorageBlob#access_tier}.
        :param cache_control: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_blob#cache_control StorageBlob#cache_control}.
        :param content_md5: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_blob#content_md5 StorageBlob#content_md5}.
        :param content_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_blob#content_type StorageBlob#content_type}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_blob#id StorageBlob#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param metadata: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_blob#metadata StorageBlob#metadata}.
        :param parallelism: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_blob#parallelism StorageBlob#parallelism}.
        :param size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_blob#size StorageBlob#size}.
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_blob#source StorageBlob#source}.
        :param source_content: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_blob#source_content StorageBlob#source_content}.
        :param source_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_blob#source_uri StorageBlob#source_uri}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_blob#timeouts StorageBlob#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd765c1dee5ff09470496fc284b6bb6ae1ffdd7b67b7650dc411b5d15ca54a1f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        props = _cdktf_cdktf_provider_azurerm_storage_blob_92bbcedf.StorageBlobConfig(
            name=name,
            storage_account_name=storage_account_name,
            storage_container_name=storage_container_name,
            type=type,
            access_tier=access_tier,
            cache_control=cache_control,
            content_md5=content_md5,
            content_type=content_type,
            id=id,
            metadata=metadata,
            parallelism=parallelism,
            size=size,
            source=source,
            source_content=source_content,
            source_uri=source_uri,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, props])

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))


class Container(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@microsoft/terraform-cdk-constructs.azure_storageaccount.Container",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        storage_account_name: builtins.str,
        container_access_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_storage_container_92bbcedf.StorageContainerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Represents an Azure Storage Container within a specific Azure Storage Account.

        This class is designed for the creation and management of an Azure Storage Container, which serves as a unit of storage
        that houses data objects, known as blobs. Containers are analogous to directories in a file system, and are used to organize
        sets of blobs within a storage account. This class allows for granular control over blob storage, providing functionalities
        such as setting access levels, managing metadata, and implementing security measures like encryption scopes.

        :param scope: - The scope in which to define this construct, typically a reference to the Cloud Development Kit (CDK) stack.
        :param id_: - The unique identifier for this instance of the container.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_container#name StorageContainer#name}.
        :param storage_account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_container#storage_account_name StorageContainer#storage_account_name}.
        :param container_access_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_container#container_access_type StorageContainer#container_access_type}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_container#id StorageContainer#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param metadata: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_container#metadata StorageContainer#metadata}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_container#timeouts StorageContainer#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf8aea438662ddf74e870f852aeb8ae5faa1ebd51d3d093feed528ac9ce497cc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        props = _cdktf_cdktf_provider_azurerm_storage_container_92bbcedf.StorageContainerConfig(
            name=name,
            storage_account_name=storage_account_name,
            container_access_type=container_access_type,
            id=id,
            metadata=metadata,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, props])

    @jsii.member(jsii_name="addBlob")
    def add_blob(
        self,
        blob_name: builtins.str,
        file_path: builtins.str,
        *,
        name: builtins.str,
        storage_account_name: builtins.str,
        storage_container_name: builtins.str,
        type: builtins.str,
        access_tier: typing.Optional[builtins.str] = None,
        cache_control: typing.Optional[builtins.str] = None,
        content_md5: typing.Optional[builtins.str] = None,
        content_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        parallelism: typing.Optional[jsii.Number] = None,
        size: typing.Optional[jsii.Number] = None,
        source: typing.Optional[builtins.str] = None,
        source_content: typing.Optional[builtins.str] = None,
        source_uri: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_storage_blob_92bbcedf.StorageBlobTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> Blob:
        '''Adds a blob to this Azure Storage Container.

        This method facilitates the addition of a blob to an Azure Storage Container managed by this class. It handles the creation and
        configuration of the blob, including setting its type, source content, and metadata. This is useful for uploading various types
        of unstructured data, such as images, videos, documents, or other binary files, into a cloud-based storage solution.

        :param blob_name: - The name of the blob to be added, which will be used as the blob's unique identifier within the container.
        :param file_path: - The file path or URL for the source of the blob's content. This specifies the location of the file to be uploaded.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_blob#name StorageBlob#name}.
        :param storage_account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_blob#storage_account_name StorageBlob#storage_account_name}.
        :param storage_container_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_blob#storage_container_name StorageBlob#storage_container_name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_blob#type StorageBlob#type}.
        :param access_tier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_blob#access_tier StorageBlob#access_tier}.
        :param cache_control: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_blob#cache_control StorageBlob#cache_control}.
        :param content_md5: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_blob#content_md5 StorageBlob#content_md5}.
        :param content_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_blob#content_type StorageBlob#content_type}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_blob#id StorageBlob#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param metadata: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_blob#metadata StorageBlob#metadata}.
        :param parallelism: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_blob#parallelism StorageBlob#parallelism}.
        :param size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_blob#size StorageBlob#size}.
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_blob#source StorageBlob#source}.
        :param source_content: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_blob#source_content StorageBlob#source_content}.
        :param source_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_blob#source_uri StorageBlob#source_uri}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_blob#timeouts StorageBlob#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 

        :return:

        The newly created Blob object, which represents the blob added to the storage container.

        Example usage::

        const storageBlob = storageContainer.addBlob('exampleBlob', './path/to/local/file.txt', {
        type: 'Block',
        contentType: 'text/plain',
        metadata: { customKey: 'customValue' }
        });

        In this example, a new blob named 'exampleBlob' is added to the storage container. The content of the blob is sourced
        from a local file specified by ``filePath``. The blob is configured as a 'Block' type with 'text/plain' content type and
        custom metadata. The method returns the blob instance for further use or reference.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e4f23a53fd58239dea6b2f497da13f1dda1d394a4b6fb1b2969ed0792b18e32)
            check_type(argname="argument blob_name", value=blob_name, expected_type=type_hints["blob_name"])
            check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
        props = _cdktf_cdktf_provider_azurerm_storage_blob_92bbcedf.StorageBlobConfig(
            name=name,
            storage_account_name=storage_account_name,
            storage_container_name=storage_container_name,
            type=type,
            access_tier=access_tier,
            cache_control=cache_control,
            content_md5=content_md5,
            content_type=content_type,
            id=id,
            metadata=metadata,
            parallelism=parallelism,
            size=size,
            source=source,
            source_content=source_content,
            source_uri=source_uri,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        return typing.cast(Blob, jsii.invoke(self, "addBlob", [blob_name, file_path, props]))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))


class File(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@microsoft/terraform-cdk-constructs.azure_storageaccount.File",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        storage_share_id: builtins.str,
        content_disposition: typing.Optional[builtins.str] = None,
        content_encoding: typing.Optional[builtins.str] = None,
        content_md5: typing.Optional[builtins.str] = None,
        content_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        path: typing.Optional[builtins.str] = None,
        source: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_storage_share_file_92bbcedf.StorageShareFileTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Represents a file within an Azure Storage Share.

        This class is responsible for the creation and management of a file in an Azure Storage Share, which allows for cloud file storage
        that can be accessed and managed like a file system. The File class enables detailed configuration of file properties including
        content type, encoding, and metadata, making it suitable for storing and accessing various types of data.

        :param scope: - The scope in which to define this construct, typically representing the Cloud Development Kit (CDK) stack.
        :param id_: - The unique identifier for this instance of the file.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_share_file#name StorageShareFile#name}.
        :param storage_share_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_share_file#storage_share_id StorageShareFile#storage_share_id}.
        :param content_disposition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_share_file#content_disposition StorageShareFile#content_disposition}.
        :param content_encoding: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_share_file#content_encoding StorageShareFile#content_encoding}.
        :param content_md5: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_share_file#content_md5 StorageShareFile#content_md5}.
        :param content_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_share_file#content_type StorageShareFile#content_type}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_share_file#id StorageShareFile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param metadata: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_share_file#metadata StorageShareFile#metadata}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_share_file#path StorageShareFile#path}.
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_share_file#source StorageShareFile#source}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_share_file#timeouts StorageShareFile#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16432b46cc40fbd4a478574b1a6c92923d92075753e76f794a3cf23bb719bfd3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        props = _cdktf_cdktf_provider_azurerm_storage_share_file_92bbcedf.StorageShareFileConfig(
            name=name,
            storage_share_id=storage_share_id,
            content_disposition=content_disposition,
            content_encoding=content_encoding,
            content_md5=content_md5,
            content_type=content_type,
            id=id,
            metadata=metadata,
            path=path,
            source=source,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, props])

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))


class FileShare(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@microsoft/terraform-cdk-constructs.azure_storageaccount.FileShare",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        quota: jsii.Number,
        storage_account_name: builtins.str,
        access_tier: typing.Optional[builtins.str] = None,
        acl: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[_cdktf_cdktf_provider_azurerm_storage_share_92bbcedf.StorageShareAcl, typing.Dict[builtins.str, typing.Any]]]]] = None,
        enabled_protocol: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_storage_share_92bbcedf.StorageShareTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id_: -
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_share#name StorageShare#name}.
        :param quota: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_share#quota StorageShare#quota}.
        :param storage_account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_share#storage_account_name StorageShare#storage_account_name}.
        :param access_tier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_share#access_tier StorageShare#access_tier}.
        :param acl: acl block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_share#acl StorageShare#acl}
        :param enabled_protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_share#enabled_protocol StorageShare#enabled_protocol}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_share#id StorageShare#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param metadata: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_share#metadata StorageShare#metadata}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_share#timeouts StorageShare#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9812954a73f8817b9eec05619517134fd846a8514a3d411d0e1345b83ef9e96e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        props = _cdktf_cdktf_provider_azurerm_storage_share_92bbcedf.StorageShareConfig(
            name=name,
            quota=quota,
            storage_account_name=storage_account_name,
            access_tier=access_tier,
            acl=acl,
            enabled_protocol=enabled_protocol,
            id=id,
            metadata=metadata,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, props])

    @jsii.member(jsii_name="addFile")
    def add_file(
        self,
        file_name: builtins.str,
        file_source: typing.Optional[builtins.str] = None,
        *,
        name: builtins.str,
        storage_share_id: builtins.str,
        content_disposition: typing.Optional[builtins.str] = None,
        content_encoding: typing.Optional[builtins.str] = None,
        content_md5: typing.Optional[builtins.str] = None,
        content_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        path: typing.Optional[builtins.str] = None,
        source: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_storage_share_file_92bbcedf.StorageShareFileTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> File:
        '''Adds a file to the Azure Storage File Share.

        :param file_name: The name of the file to be added.
        :param file_source: Optional path or URL to the source of the file's content.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_share_file#name StorageShareFile#name}.
        :param storage_share_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_share_file#storage_share_id StorageShareFile#storage_share_id}.
        :param content_disposition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_share_file#content_disposition StorageShareFile#content_disposition}.
        :param content_encoding: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_share_file#content_encoding StorageShareFile#content_encoding}.
        :param content_md5: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_share_file#content_md5 StorageShareFile#content_md5}.
        :param content_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_share_file#content_type StorageShareFile#content_type}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_share_file#id StorageShareFile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param metadata: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_share_file#metadata StorageShareFile#metadata}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_share_file#path StorageShareFile#path}.
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_share_file#source StorageShareFile#source}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_share_file#timeouts StorageShareFile#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 

        :return:

        The created AzureStorageShareFile instance.

        This method allows you to add a file to your Azure Storage File Share, optionally specifying
        the file's content source and other properties like content type, encoding, and metadata.
        If ``fileSource`` is provided, the content of the file is sourced from this location.
        The ``props`` parameter allows for further customization of the file, such as setting the content type
        (default is 'application/octet-stream') and adding metadata.

        Example usage::

        const storageShareFile = storageShare.addFile('example.txt', './path/to/local/file.txt', {
        contentType: 'text/plain',
        metadata: { customKey: 'customValue' }
        });

        In this example, a text file named 'example.txt' is added to the storage share. The content of the file
        is sourced from a local file, and the content type is specified as 'text/plain' with custom metadata.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b02aa2198fb33f4138369b7551b1be9e8267855ea44d93c99d6416dd8986c0ed)
            check_type(argname="argument file_name", value=file_name, expected_type=type_hints["file_name"])
            check_type(argname="argument file_source", value=file_source, expected_type=type_hints["file_source"])
        props = _cdktf_cdktf_provider_azurerm_storage_share_file_92bbcedf.StorageShareFileConfig(
            name=name,
            storage_share_id=storage_share_id,
            content_disposition=content_disposition,
            content_encoding=content_encoding,
            content_md5=content_md5,
            content_type=content_type,
            id=id,
            metadata=metadata,
            path=path,
            source=source,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        return typing.cast(File, jsii.invoke(self, "addFile", [file_name, file_source, props]))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountName")
    def storage_account_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountName"))

    @builtins.property
    @jsii.member(jsii_name="storageShareName")
    def storage_share_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageShareName"))


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_storageaccount.FileShareProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_tier": "accessTier",
        "acl": "acl",
        "enabled_protocol": "enabledProtocol",
        "metadata": "metadata",
        "quota": "quota",
    },
)
class FileShareProps:
    def __init__(
        self,
        *,
        access_tier: typing.Optional[builtins.str] = None,
        acl: typing.Any = None,
        enabled_protocol: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        quota: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param access_tier: The access tier of the storage share. This property is only applicable to storage shares with a premium account type. Example values: Hot, Cool.
        :param acl: A list of access control rules for the storage share.
        :param enabled_protocol: The protocol to use when accessing the storage share. Example values: SMB, NFS.
        :param metadata: A mapping of tags to assign to the storage share. Format: { [key: string]: string }
        :param quota: The maximum size of the storage share, in gigabytes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e56cbf4116d87b4124bd3e753ede685265ef315d32554e49ee0bb07935943a5d)
            check_type(argname="argument access_tier", value=access_tier, expected_type=type_hints["access_tier"])
            check_type(argname="argument acl", value=acl, expected_type=type_hints["acl"])
            check_type(argname="argument enabled_protocol", value=enabled_protocol, expected_type=type_hints["enabled_protocol"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument quota", value=quota, expected_type=type_hints["quota"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_tier is not None:
            self._values["access_tier"] = access_tier
        if acl is not None:
            self._values["acl"] = acl
        if enabled_protocol is not None:
            self._values["enabled_protocol"] = enabled_protocol
        if metadata is not None:
            self._values["metadata"] = metadata
        if quota is not None:
            self._values["quota"] = quota

    @builtins.property
    def access_tier(self) -> typing.Optional[builtins.str]:
        '''The access tier of the storage share.

        This property is only applicable to storage shares with a premium account type.
        Example values: Hot, Cool.
        '''
        result = self._values.get("access_tier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def acl(self) -> typing.Any:
        '''A list of access control rules for the storage share.'''
        result = self._values.get("acl")
        return typing.cast(typing.Any, result)

    @builtins.property
    def enabled_protocol(self) -> typing.Optional[builtins.str]:
        '''The protocol to use when accessing the storage share.

        Example values: SMB, NFS.
        '''
        result = self._values.get("enabled_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metadata(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A mapping of tags to assign to the storage share.

        Format: { [key: string]: string }
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def quota(self) -> typing.Optional[jsii.Number]:
        '''The maximum size of the storage share, in gigabytes.'''
        result = self._values.get("quota")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FileShareProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_storageaccount.NetworkRulesProps",
    jsii_struct_bases=[],
    name_mapping={
        "default_action": "defaultAction",
        "bypass": "bypass",
        "ip_rules": "ipRules",
        "private_link_access": "privateLinkAccess",
        "virtual_network_subnet_ids": "virtualNetworkSubnetIds",
    },
)
class NetworkRulesProps:
    def __init__(
        self,
        *,
        default_action: builtins.str,
        bypass: typing.Optional[typing.Sequence[builtins.str]] = None,
        ip_rules: typing.Optional[typing.Sequence[builtins.str]] = None,
        private_link_access: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_azurerm_storage_account_network_rules_92bbcedf.StorageAccountNetworkRulesPrivateLinkAccessA, typing.Dict[builtins.str, typing.Any]]]] = None,
        virtual_network_subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param default_action: The default action of the network rule set. Options are 'Allow' or 'Deny'. Set to 'Deny' to enable network rules and restrict access to the storage account. 'Allow' permits access by default.
        :param bypass: Specifies which traffic to bypass from the network rules. The possible values are 'AzureServices', 'Logging', 'Metrics', and 'None'. Bypassing 'AzureServices' enables Azure's internal services to access the storage account.
        :param ip_rules: An array of IP rules to allow access to the storage account. These are specified as CIDR ranges. Example: ['1.2.3.4/32', '5.6.7.0/24'] to allow specific IPs/subnets.
        :param private_link_access: An array of objects representing the private link access settings. Each object in the array defines the sub-resource name (e.g., 'blob', 'file') and its respective private endpoint connections for the storage account.
        :param virtual_network_subnet_ids: An array of virtual network subnet IDs that are allowed to access the storage account. This enables you to secure the storage account to a specific virtual network and subnet within Azure.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dc2b426ec7348bba58ba58cf71d391e8683562f457bf2b3988d535d597d554f)
            check_type(argname="argument default_action", value=default_action, expected_type=type_hints["default_action"])
            check_type(argname="argument bypass", value=bypass, expected_type=type_hints["bypass"])
            check_type(argname="argument ip_rules", value=ip_rules, expected_type=type_hints["ip_rules"])
            check_type(argname="argument private_link_access", value=private_link_access, expected_type=type_hints["private_link_access"])
            check_type(argname="argument virtual_network_subnet_ids", value=virtual_network_subnet_ids, expected_type=type_hints["virtual_network_subnet_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_action": default_action,
        }
        if bypass is not None:
            self._values["bypass"] = bypass
        if ip_rules is not None:
            self._values["ip_rules"] = ip_rules
        if private_link_access is not None:
            self._values["private_link_access"] = private_link_access
        if virtual_network_subnet_ids is not None:
            self._values["virtual_network_subnet_ids"] = virtual_network_subnet_ids

    @builtins.property
    def default_action(self) -> builtins.str:
        '''The default action of the network rule set.

        Options are 'Allow' or 'Deny'. Set to 'Deny' to enable network rules and restrict
        access to the storage account. 'Allow' permits access by default.
        '''
        result = self._values.get("default_action")
        assert result is not None, "Required property 'default_action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bypass(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies which traffic to bypass from the network rules.

        The possible values are 'AzureServices', 'Logging', 'Metrics',
        and 'None'. Bypassing 'AzureServices' enables Azure's internal services to access the storage account.
        '''
        result = self._values.get("bypass")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ip_rules(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of IP rules to allow access to the storage account.

        These are specified as CIDR ranges.
        Example: ['1.2.3.4/32', '5.6.7.0/24'] to allow specific IPs/subnets.
        '''
        result = self._values.get("ip_rules")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def private_link_access(
        self,
    ) -> typing.Optional[typing.List[_cdktf_cdktf_provider_azurerm_storage_account_network_rules_92bbcedf.StorageAccountNetworkRulesPrivateLinkAccessA]]:
        '''An array of objects representing the private link access settings.

        Each object in the array defines the sub-resource name
        (e.g., 'blob', 'file') and its respective private endpoint connections for the storage account.
        '''
        result = self._values.get("private_link_access")
        return typing.cast(typing.Optional[typing.List[_cdktf_cdktf_provider_azurerm_storage_account_network_rules_92bbcedf.StorageAccountNetworkRulesPrivateLinkAccessA]], result)

    @builtins.property
    def virtual_network_subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of virtual network subnet IDs that are allowed to access the storage account.

        This enables you to secure the storage
        account to a specific virtual network and subnet within Azure.
        '''
        result = self._values.get("virtual_network_subnet_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkRulesProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Queue(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@microsoft/terraform-cdk-constructs.azure_storageaccount.Queue",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        storage_account_name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_storage_queue_92bbcedf.StorageQueueTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Represents an Azure Storage Queue within a specific Azure Storage Account.

        This class is responsible for the creation and management of an Azure Storage Queue, which is a service for storing large numbers
        of messages that can be accessed from anywhere in the world via authenticated calls using HTTP or HTTPS. A single queue message
        can be up to 64 KB in size, and a queue can contain millions of messages, up to the total capacity limit of a storage account.
        This class provides a way to manage messages in a scalable and secure manner.

        :param scope: - The scope in which to define this construct, typically representing the Cloud Development Kit (CDK) stack.
        :param id_: - The unique identifier for this instance of the queue.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_queue#name StorageQueue#name}.
        :param storage_account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_queue#storage_account_name StorageQueue#storage_account_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_queue#id StorageQueue#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param metadata: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_queue#metadata StorageQueue#metadata}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_queue#timeouts StorageQueue#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d244330190615564ee6dbe2d543b2a4184c79a1bb46ad618ca56cf5001b92f56)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        props = _cdktf_cdktf_provider_azurerm_storage_queue_92bbcedf.StorageQueueConfig(
            name=name,
            storage_account_name=storage_account_name,
            id=id,
            metadata=metadata,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, props])

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))


class Table(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@microsoft/terraform-cdk-constructs.azure_storageaccount.Table",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        storage_account_name: builtins.str,
        acl: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[_cdktf_cdktf_provider_azurerm_storage_table_92bbcedf.StorageTableAcl, typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_storage_table_92bbcedf.StorageTableTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Represents an Azure Storage Table within a specific Azure Storage Account.

        This class is responsible for the creation and management of an Azure Storage Table, which provides a NoSQL key-attribute data store
        that can massively scale. It is suitable for storing structured, non-relational data, allowing rapid development and fast access to large
        quantities of data. The class facilitates creating and configuring storage tables including setting up access control lists (ACLs).

        :param scope: - The scope in which to define this construct, typically representing the Cloud Development Kit (CDK) stack.
        :param id_: - The unique identifier for this instance of the table.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_table#name StorageTable#name}.
        :param storage_account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_table#storage_account_name StorageTable#storage_account_name}.
        :param acl: acl block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_table#acl StorageTable#acl}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_table#id StorageTable#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.70.0/docs/resources/storage_table#timeouts StorageTable#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b18eeca647cce1092403c4ab1b5a3e6352b1a2110148b703c2e7fd47748618a6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        props = _cdktf_cdktf_provider_azurerm_storage_table_92bbcedf.StorageTableConfig(
            name=name,
            storage_account_name=storage_account_name,
            acl=acl,
            id=id,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, props])

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))


__all__ = [
    "Account",
    "AccountProps",
    "Blob",
    "Container",
    "File",
    "FileShare",
    "FileShareProps",
    "NetworkRulesProps",
    "Queue",
    "Table",
]

publication.publish()

def _typecheckingstub__6cf8d651224015dd5f566f70fa4f6451c4aa70245e080717f03189f597288cda(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    access_tier: typing.Optional[builtins.str] = None,
    account_kind: typing.Optional[builtins.str] = None,
    account_replication_type: typing.Optional[builtins.str] = None,
    account_tier: typing.Optional[builtins.str] = None,
    enable_https_traffic_only: typing.Optional[builtins.bool] = None,
    identity: typing.Any = None,
    is_hns_enabled: typing.Optional[builtins.bool] = None,
    min_tls_version: typing.Optional[builtins.str] = None,
    public_network_access_enabled: typing.Optional[builtins.bool] = None,
    resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1507cad6d96c6bff9c8948d2fc2dc3b492f45668b2d27256eeeb72784ce61712(
    name: builtins.str,
    container_access_type: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__417198ca18a6617286bb83e6a9fd18479dae6f9437b3f86bfed5be54795acc23(
    name: builtins.str,
    *,
    access_tier: typing.Optional[builtins.str] = None,
    acl: typing.Any = None,
    enabled_protocol: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    quota: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01ff1359fcff7f63e01967486b6eab1309a5a0499600d0f9996baaece4d468bd(
    name: builtins.str,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa42f736eee4b505889af078f894ef6cb9dfdc60488ee3b76d0ece3d794f5ff6(
    name: builtins.str,
    acl: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_azurerm_storage_table_92bbcedf.StorageTableAcl, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5024b09e7cb3af550bee25059decceb2e25cbec13a7b5afe4b3170d8e7c13ab0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98ede1f7c205554b760d9e374dba3482370df0f4a4e133b3ca6dd38d5cb2a801(
    value: _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0072c193a9790f4f261e3f6c7c6cad7d13e9d662dc060adff5d380ad9854013(
    *,
    location: builtins.str,
    name: builtins.str,
    access_tier: typing.Optional[builtins.str] = None,
    account_kind: typing.Optional[builtins.str] = None,
    account_replication_type: typing.Optional[builtins.str] = None,
    account_tier: typing.Optional[builtins.str] = None,
    enable_https_traffic_only: typing.Optional[builtins.bool] = None,
    identity: typing.Any = None,
    is_hns_enabled: typing.Optional[builtins.bool] = None,
    min_tls_version: typing.Optional[builtins.str] = None,
    public_network_access_enabled: typing.Optional[builtins.bool] = None,
    resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd765c1dee5ff09470496fc284b6bb6ae1ffdd7b67b7650dc411b5d15ca54a1f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    storage_account_name: builtins.str,
    storage_container_name: builtins.str,
    type: builtins.str,
    access_tier: typing.Optional[builtins.str] = None,
    cache_control: typing.Optional[builtins.str] = None,
    content_md5: typing.Optional[builtins.str] = None,
    content_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    parallelism: typing.Optional[jsii.Number] = None,
    size: typing.Optional[jsii.Number] = None,
    source: typing.Optional[builtins.str] = None,
    source_content: typing.Optional[builtins.str] = None,
    source_uri: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_storage_blob_92bbcedf.StorageBlobTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__cf8aea438662ddf74e870f852aeb8ae5faa1ebd51d3d093feed528ac9ce497cc(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    storage_account_name: builtins.str,
    container_access_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_storage_container_92bbcedf.StorageContainerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__8e4f23a53fd58239dea6b2f497da13f1dda1d394a4b6fb1b2969ed0792b18e32(
    blob_name: builtins.str,
    file_path: builtins.str,
    *,
    name: builtins.str,
    storage_account_name: builtins.str,
    storage_container_name: builtins.str,
    type: builtins.str,
    access_tier: typing.Optional[builtins.str] = None,
    cache_control: typing.Optional[builtins.str] = None,
    content_md5: typing.Optional[builtins.str] = None,
    content_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    parallelism: typing.Optional[jsii.Number] = None,
    size: typing.Optional[jsii.Number] = None,
    source: typing.Optional[builtins.str] = None,
    source_content: typing.Optional[builtins.str] = None,
    source_uri: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_storage_blob_92bbcedf.StorageBlobTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__16432b46cc40fbd4a478574b1a6c92923d92075753e76f794a3cf23bb719bfd3(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    storage_share_id: builtins.str,
    content_disposition: typing.Optional[builtins.str] = None,
    content_encoding: typing.Optional[builtins.str] = None,
    content_md5: typing.Optional[builtins.str] = None,
    content_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    path: typing.Optional[builtins.str] = None,
    source: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_storage_share_file_92bbcedf.StorageShareFileTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__9812954a73f8817b9eec05619517134fd846a8514a3d411d0e1345b83ef9e96e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    quota: jsii.Number,
    storage_account_name: builtins.str,
    access_tier: typing.Optional[builtins.str] = None,
    acl: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[_cdktf_cdktf_provider_azurerm_storage_share_92bbcedf.StorageShareAcl, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enabled_protocol: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_storage_share_92bbcedf.StorageShareTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__b02aa2198fb33f4138369b7551b1be9e8267855ea44d93c99d6416dd8986c0ed(
    file_name: builtins.str,
    file_source: typing.Optional[builtins.str] = None,
    *,
    name: builtins.str,
    storage_share_id: builtins.str,
    content_disposition: typing.Optional[builtins.str] = None,
    content_encoding: typing.Optional[builtins.str] = None,
    content_md5: typing.Optional[builtins.str] = None,
    content_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    path: typing.Optional[builtins.str] = None,
    source: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_storage_share_file_92bbcedf.StorageShareFileTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__e56cbf4116d87b4124bd3e753ede685265ef315d32554e49ee0bb07935943a5d(
    *,
    access_tier: typing.Optional[builtins.str] = None,
    acl: typing.Any = None,
    enabled_protocol: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    quota: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dc2b426ec7348bba58ba58cf71d391e8683562f457bf2b3988d535d597d554f(
    *,
    default_action: builtins.str,
    bypass: typing.Optional[typing.Sequence[builtins.str]] = None,
    ip_rules: typing.Optional[typing.Sequence[builtins.str]] = None,
    private_link_access: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_azurerm_storage_account_network_rules_92bbcedf.StorageAccountNetworkRulesPrivateLinkAccessA, typing.Dict[builtins.str, typing.Any]]]] = None,
    virtual_network_subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d244330190615564ee6dbe2d543b2a4184c79a1bb46ad618ca56cf5001b92f56(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    storage_account_name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_storage_queue_92bbcedf.StorageQueueTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__b18eeca647cce1092403c4ab1b5a3e6352b1a2110148b703c2e7fd47748618a6(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    storage_account_name: builtins.str,
    acl: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[_cdktf_cdktf_provider_azurerm_storage_table_92bbcedf.StorageTableAcl, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_storage_table_92bbcedf.StorageTableTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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
