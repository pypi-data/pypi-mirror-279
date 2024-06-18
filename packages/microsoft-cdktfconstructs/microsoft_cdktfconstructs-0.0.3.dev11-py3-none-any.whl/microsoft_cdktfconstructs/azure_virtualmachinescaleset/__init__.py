'''
# Azure Virtual Machine Scale Set Construct

This construct defines a scalable and managed Virtual Machine Scale Set (VMSS) in Azure, simplifying the deployment and management of multiple VMs that automatically scale in response to demand.

## What is a Virtual Machine Scale Set (VMSS)?

Azure VMSS allows you to deploy and manage a set of autoscaling virtual machines. You can scale the number of VMs in the scale set manually, or automatically based on predefined rules.

Detailed information on Azure VMSS can be found in the [official Azure documentation](https://docs.microsoft.com/en-us/azure/virtual-machine-scale-sets/overview).

## Best Practices

* **Auto-Scaling**: Define rules for automatically scaling the number of VM instances.
* **Updating**: Utilize rolling upgrades for applying patches with minimal downtime.
* **Availability**: Distribute instances across fault domains and update domains.
* **Extensions**: Use VMSS extensions for automatic post-deployment configuration.
* **Load Balancing**: Configure load balancing to distribute traffic among instances.

## Construct Properties

The VMSS construct includes properties for configuration:

* `location`: Region for deployment.
* `resourceGroupName`: Resource group for VMSS.
* `name`: Name of the VMSS.
* `sku`: SKU for VM instances, like `Standard_B2s`.
* `instances`: Number of VM instances.
* `adminUsername`: Admin username.
* `adminPassword`: Admin password.
* `sourceImageReference`: Reference to the OS image.
* `osDisk`: Configuration for OS disk.
* `networkInterface`: Network interface details.
* `publicIPAddress`: Public IP configuration.
* `tags`: Key-value pairs for resource tagging.
* `customData`: Bootstrap script or data.
* `upgradePolicyMode`: Upgrade policy mode setting.
* `overprovision`: Overprovisioning toggle.
* `scaleInPolicy`: Scale-in policy.
* `bootDiagnosticsStorageURI`: URI for boot diagnostics.

## Usage Example

### Linux VMSS

```python
const azureLinuxVMSS = new AzureLinuxVirtualMachineScaleSet(this, 'myLinuxVMSS', {
  resourceGroupName: 'myResourceGroup',
  location: 'West US',
  name: 'myLinuxVMSS',
  adminUsername: 'adminuser',
  sku: 'Standard_B2s',
  instances: 2,
  // ...other configurations
});
```

### Windows VMSS

```python
const azureWindowsVMSS = new AzureWindowsVirtualMachineScaleSet(this, 'myWindowsVMSS', {
  resourceGroupName: 'myResourceGroup',
  location: 'West US',
  name: 'myWindowsVMSS',
  adminUsername: 'adminuser',
  sku: 'Standard_B2s',
  instances: 2,
  // ...other configurations
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
import cdktf_cdktf_provider_azurerm.linux_virtual_machine as _cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf
import cdktf_cdktf_provider_azurerm.linux_virtual_machine_scale_set as _cdktf_cdktf_provider_azurerm_linux_virtual_machine_scale_set_92bbcedf
import cdktf_cdktf_provider_azurerm.resource_group as _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf
import cdktf_cdktf_provider_azurerm.subnet as _cdktf_cdktf_provider_azurerm_subnet_92bbcedf
import cdktf_cdktf_provider_azurerm.windows_virtual_machine as _cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf
import cdktf_cdktf_provider_azurerm.windows_virtual_machine_scale_set as _cdktf_cdktf_provider_azurerm_windows_virtual_machine_scale_set_92bbcedf
import constructs as _constructs_77d1e7e8
from ..core_azure import AzureResource as _AzureResource_74eec1c4


class LinuxCluster(
    _AzureResource_74eec1c4,
    metaclass=jsii.JSIIMeta,
    jsii_type="@microsoft/terraform-cdk-constructs.azure_virtualmachinescaleset.LinuxCluster",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        admin_password: typing.Optional[builtins.str] = None,
        admin_ssh_key: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineAdminSshKey, typing.Dict[builtins.str, typing.Any]]]]] = None,
        admin_username: typing.Optional[builtins.str] = None,
        boot_diagnostics_storage_uri: typing.Optional[builtins.str] = None,
        custom_data: typing.Optional[builtins.str] = None,
        enable_ssh_azure_ad_login: typing.Optional[builtins.bool] = None,
        identity: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
        instances: typing.Optional[jsii.Number] = None,
        location: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        os_disk: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineOsDisk, typing.Dict[builtins.str, typing.Any]]] = None,
        overprovision: typing.Optional[builtins.bool] = None,
        public_ip_address: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_scale_set_92bbcedf.LinuxVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddress, typing.Dict[builtins.str, typing.Any]]]] = None,
        resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
        scale_in_policy: typing.Optional[builtins.str] = None,
        sku: typing.Optional[builtins.str] = None,
        source_image_id: typing.Optional[builtins.str] = None,
        source_image_reference: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineSourceImageReference, typing.Dict[builtins.str, typing.Any]]] = None,
        subnet: typing.Optional[_cdktf_cdktf_provider_azurerm_subnet_92bbcedf.Subnet] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        upgrade_policy_mode: typing.Optional[builtins.str] = None,
        user_data: typing.Optional[builtins.str] = None,
        zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Represents a Linux Virtual Machine Scale Set (VMSS) within Microsoft Azure.

        This class is designed to provision and manage a scale set of Linux virtual machines, providing capabilities such as
        auto-scaling, high availability, and simplified management. It supports detailed configurations like VM size, operating
        system image, network settings, and administrative credentials. Additional functionalities include custom data scripts,
        SSH configurations, and optional features like managed identity and boot diagnostics.

        :param scope: - The scope in which to define this construct, typically representing the Cloud Development Kit (CDK) application.
        :param id: - The unique identifier for this instance of the Linux cluster, used within the scope for reference.
        :param admin_password: The admin password for the virtual machine.
        :param admin_ssh_key: An array of SSH keys for the admin user.
        :param admin_username: The admin username for the virtual machine.
        :param boot_diagnostics_storage_uri: Boot diagnostics settings for the VMSS.
        :param custom_data: Custom data to pass to the virtual machines upon creation.
        :param enable_ssh_azure_ad_login: Enable SSH Azure AD Login, required managed identity to be set. Default: false
        :param identity: Managed identity settings for the VMs.
        :param instances: The number of VM instances in the scale set. Default: 2
        :param location: The Azure location where the virtual machine scale set should be created. Default: "eastus"
        :param name: The name of the virtual machine scale set. Default: - Uses the name derived from the construct path.
        :param os_disk: The OS disk configuration for the virtual machines. Default: - Uses a disk with caching set to "ReadWrite" and storage account type "Standard_LRS".
        :param overprovision: Specifies if the VMSS should be overprovisioned. Default: true
        :param public_ip_address: The allocation method for the public IP.
        :param resource_group: An optional reference to the resource group in which to deploy the Virtual Machine. If not provided, the Virtual Machine will be deployed in the default resource group.
        :param scale_in_policy: Specifies the scale-in policy for the VMSS.
        :param sku: The size of the virtual machines in the scale set. Default: "Standard_B2s"
        :param source_image_id: The ID of the source image for the virtual machines.
        :param source_image_reference: The source image reference for the virtual machines. Default: - Uses a default Ubuntu image.
        :param subnet: The subnet in which the virtual machines will be placed.
        :param tags: Tags to apply to the virtual machine scale set.
        :param upgrade_policy_mode: Specifies the scale set's upgrade policy settings.
        :param user_data: Custom data to pass to the virtual machines upon creation.
        :param zones: The availability zone(s) in which the VMs should be placed.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fc27996012db416df4e609b98d48137396321f694a3108be3d89d25a4942b65)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = LinuxClusterProps(
            admin_password=admin_password,
            admin_ssh_key=admin_ssh_key,
            admin_username=admin_username,
            boot_diagnostics_storage_uri=boot_diagnostics_storage_uri,
            custom_data=custom_data,
            enable_ssh_azure_ad_login=enable_ssh_azure_ad_login,
            identity=identity,
            instances=instances,
            location=location,
            name=name,
            os_disk=os_disk,
            overprovision=overprovision,
            public_ip_address=public_ip_address,
            resource_group=resource_group,
            scale_in_policy=scale_in_policy,
            sku=sku,
            source_image_id=source_image_id,
            source_image_reference=source_image_reference,
            subnet=subnet,
            tags=tags,
            upgrade_policy_mode=upgrade_policy_mode,
            user_data=user_data,
            zones=zones,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="fqn")
    def fqn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fqn"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "LinuxClusterProps":
        return typing.cast("LinuxClusterProps", jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a5bab57b28263fc46a53ddf95de61b6acea41f2c0228a0ed5bcc955aac7f737)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1a4f01c717c28ff4221ab482c74fa4fa8e2ccf900d70156ad3055dac288b58c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroup", value)


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_virtualmachinescaleset.LinuxClusterProps",
    jsii_struct_bases=[],
    name_mapping={
        "admin_password": "adminPassword",
        "admin_ssh_key": "adminSshKey",
        "admin_username": "adminUsername",
        "boot_diagnostics_storage_uri": "bootDiagnosticsStorageURI",
        "custom_data": "customData",
        "enable_ssh_azure_ad_login": "enableSshAzureADLogin",
        "identity": "identity",
        "instances": "instances",
        "location": "location",
        "name": "name",
        "os_disk": "osDisk",
        "overprovision": "overprovision",
        "public_ip_address": "publicIPAddress",
        "resource_group": "resourceGroup",
        "scale_in_policy": "scaleInPolicy",
        "sku": "sku",
        "source_image_id": "sourceImageId",
        "source_image_reference": "sourceImageReference",
        "subnet": "subnet",
        "tags": "tags",
        "upgrade_policy_mode": "upgradePolicyMode",
        "user_data": "userData",
        "zones": "zones",
    },
)
class LinuxClusterProps:
    def __init__(
        self,
        *,
        admin_password: typing.Optional[builtins.str] = None,
        admin_ssh_key: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineAdminSshKey, typing.Dict[builtins.str, typing.Any]]]]] = None,
        admin_username: typing.Optional[builtins.str] = None,
        boot_diagnostics_storage_uri: typing.Optional[builtins.str] = None,
        custom_data: typing.Optional[builtins.str] = None,
        enable_ssh_azure_ad_login: typing.Optional[builtins.bool] = None,
        identity: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
        instances: typing.Optional[jsii.Number] = None,
        location: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        os_disk: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineOsDisk, typing.Dict[builtins.str, typing.Any]]] = None,
        overprovision: typing.Optional[builtins.bool] = None,
        public_ip_address: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_scale_set_92bbcedf.LinuxVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddress, typing.Dict[builtins.str, typing.Any]]]] = None,
        resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
        scale_in_policy: typing.Optional[builtins.str] = None,
        sku: typing.Optional[builtins.str] = None,
        source_image_id: typing.Optional[builtins.str] = None,
        source_image_reference: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineSourceImageReference, typing.Dict[builtins.str, typing.Any]]] = None,
        subnet: typing.Optional[_cdktf_cdktf_provider_azurerm_subnet_92bbcedf.Subnet] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        upgrade_policy_mode: typing.Optional[builtins.str] = None,
        user_data: typing.Optional[builtins.str] = None,
        zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param admin_password: The admin password for the virtual machine.
        :param admin_ssh_key: An array of SSH keys for the admin user.
        :param admin_username: The admin username for the virtual machine.
        :param boot_diagnostics_storage_uri: Boot diagnostics settings for the VMSS.
        :param custom_data: Custom data to pass to the virtual machines upon creation.
        :param enable_ssh_azure_ad_login: Enable SSH Azure AD Login, required managed identity to be set. Default: false
        :param identity: Managed identity settings for the VMs.
        :param instances: The number of VM instances in the scale set. Default: 2
        :param location: The Azure location where the virtual machine scale set should be created. Default: "eastus"
        :param name: The name of the virtual machine scale set. Default: - Uses the name derived from the construct path.
        :param os_disk: The OS disk configuration for the virtual machines. Default: - Uses a disk with caching set to "ReadWrite" and storage account type "Standard_LRS".
        :param overprovision: Specifies if the VMSS should be overprovisioned. Default: true
        :param public_ip_address: The allocation method for the public IP.
        :param resource_group: An optional reference to the resource group in which to deploy the Virtual Machine. If not provided, the Virtual Machine will be deployed in the default resource group.
        :param scale_in_policy: Specifies the scale-in policy for the VMSS.
        :param sku: The size of the virtual machines in the scale set. Default: "Standard_B2s"
        :param source_image_id: The ID of the source image for the virtual machines.
        :param source_image_reference: The source image reference for the virtual machines. Default: - Uses a default Ubuntu image.
        :param subnet: The subnet in which the virtual machines will be placed.
        :param tags: Tags to apply to the virtual machine scale set.
        :param upgrade_policy_mode: Specifies the scale set's upgrade policy settings.
        :param user_data: Custom data to pass to the virtual machines upon creation.
        :param zones: The availability zone(s) in which the VMs should be placed.
        '''
        if isinstance(identity, dict):
            identity = _cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineIdentity(**identity)
        if isinstance(os_disk, dict):
            os_disk = _cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineOsDisk(**os_disk)
        if isinstance(source_image_reference, dict):
            source_image_reference = _cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineSourceImageReference(**source_image_reference)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c770324700497911e54255fe4669fae1f7a3e4b885fcde59827d6d885ecb64be)
            check_type(argname="argument admin_password", value=admin_password, expected_type=type_hints["admin_password"])
            check_type(argname="argument admin_ssh_key", value=admin_ssh_key, expected_type=type_hints["admin_ssh_key"])
            check_type(argname="argument admin_username", value=admin_username, expected_type=type_hints["admin_username"])
            check_type(argname="argument boot_diagnostics_storage_uri", value=boot_diagnostics_storage_uri, expected_type=type_hints["boot_diagnostics_storage_uri"])
            check_type(argname="argument custom_data", value=custom_data, expected_type=type_hints["custom_data"])
            check_type(argname="argument enable_ssh_azure_ad_login", value=enable_ssh_azure_ad_login, expected_type=type_hints["enable_ssh_azure_ad_login"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument instances", value=instances, expected_type=type_hints["instances"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument os_disk", value=os_disk, expected_type=type_hints["os_disk"])
            check_type(argname="argument overprovision", value=overprovision, expected_type=type_hints["overprovision"])
            check_type(argname="argument public_ip_address", value=public_ip_address, expected_type=type_hints["public_ip_address"])
            check_type(argname="argument resource_group", value=resource_group, expected_type=type_hints["resource_group"])
            check_type(argname="argument scale_in_policy", value=scale_in_policy, expected_type=type_hints["scale_in_policy"])
            check_type(argname="argument sku", value=sku, expected_type=type_hints["sku"])
            check_type(argname="argument source_image_id", value=source_image_id, expected_type=type_hints["source_image_id"])
            check_type(argname="argument source_image_reference", value=source_image_reference, expected_type=type_hints["source_image_reference"])
            check_type(argname="argument subnet", value=subnet, expected_type=type_hints["subnet"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument upgrade_policy_mode", value=upgrade_policy_mode, expected_type=type_hints["upgrade_policy_mode"])
            check_type(argname="argument user_data", value=user_data, expected_type=type_hints["user_data"])
            check_type(argname="argument zones", value=zones, expected_type=type_hints["zones"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if admin_password is not None:
            self._values["admin_password"] = admin_password
        if admin_ssh_key is not None:
            self._values["admin_ssh_key"] = admin_ssh_key
        if admin_username is not None:
            self._values["admin_username"] = admin_username
        if boot_diagnostics_storage_uri is not None:
            self._values["boot_diagnostics_storage_uri"] = boot_diagnostics_storage_uri
        if custom_data is not None:
            self._values["custom_data"] = custom_data
        if enable_ssh_azure_ad_login is not None:
            self._values["enable_ssh_azure_ad_login"] = enable_ssh_azure_ad_login
        if identity is not None:
            self._values["identity"] = identity
        if instances is not None:
            self._values["instances"] = instances
        if location is not None:
            self._values["location"] = location
        if name is not None:
            self._values["name"] = name
        if os_disk is not None:
            self._values["os_disk"] = os_disk
        if overprovision is not None:
            self._values["overprovision"] = overprovision
        if public_ip_address is not None:
            self._values["public_ip_address"] = public_ip_address
        if resource_group is not None:
            self._values["resource_group"] = resource_group
        if scale_in_policy is not None:
            self._values["scale_in_policy"] = scale_in_policy
        if sku is not None:
            self._values["sku"] = sku
        if source_image_id is not None:
            self._values["source_image_id"] = source_image_id
        if source_image_reference is not None:
            self._values["source_image_reference"] = source_image_reference
        if subnet is not None:
            self._values["subnet"] = subnet
        if tags is not None:
            self._values["tags"] = tags
        if upgrade_policy_mode is not None:
            self._values["upgrade_policy_mode"] = upgrade_policy_mode
        if user_data is not None:
            self._values["user_data"] = user_data
        if zones is not None:
            self._values["zones"] = zones

    @builtins.property
    def admin_password(self) -> typing.Optional[builtins.str]:
        '''The admin password for the virtual machine.'''
        result = self._values.get("admin_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def admin_ssh_key(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineAdminSshKey]]]:
        '''An array of SSH keys for the admin user.'''
        result = self._values.get("admin_ssh_key")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineAdminSshKey]]], result)

    @builtins.property
    def admin_username(self) -> typing.Optional[builtins.str]:
        '''The admin username for the virtual machine.'''
        result = self._values.get("admin_username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def boot_diagnostics_storage_uri(self) -> typing.Optional[builtins.str]:
        '''Boot diagnostics settings for the VMSS.'''
        result = self._values.get("boot_diagnostics_storage_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_data(self) -> typing.Optional[builtins.str]:
        '''Custom data to pass to the virtual machines upon creation.'''
        result = self._values.get("custom_data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_ssh_azure_ad_login(self) -> typing.Optional[builtins.bool]:
        '''Enable SSH Azure AD Login, required managed identity to be set.

        :default: false
        '''
        result = self._values.get("enable_ssh_azure_ad_login")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def identity(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineIdentity]:
        '''Managed identity settings for the VMs.'''
        result = self._values.get("identity")
        return typing.cast(typing.Optional[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineIdentity], result)

    @builtins.property
    def instances(self) -> typing.Optional[jsii.Number]:
        '''The number of VM instances in the scale set.

        :default: 2
        '''
        result = self._values.get("instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The Azure location where the virtual machine scale set should be created.

        :default: "eastus"
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the virtual machine scale set.

        :default: - Uses the name derived from the construct path.
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def os_disk(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineOsDisk]:
        '''The OS disk configuration for the virtual machines.

        :default: - Uses a disk with caching set to "ReadWrite" and storage account type "Standard_LRS".
        '''
        result = self._values.get("os_disk")
        return typing.cast(typing.Optional[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineOsDisk], result)

    @builtins.property
    def overprovision(self) -> typing.Optional[builtins.bool]:
        '''Specifies if the VMSS should be overprovisioned.

        :default: true
        '''
        result = self._values.get("overprovision")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def public_ip_address(
        self,
    ) -> typing.Optional[typing.List[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_scale_set_92bbcedf.LinuxVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddress]]:
        '''The allocation method for the public IP.'''
        result = self._values.get("public_ip_address")
        return typing.cast(typing.Optional[typing.List[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_scale_set_92bbcedf.LinuxVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddress]], result)

    @builtins.property
    def resource_group(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup]:
        '''An optional reference to the resource group in which to deploy the Virtual Machine.

        If not provided, the Virtual Machine will be deployed in the default resource group.
        '''
        result = self._values.get("resource_group")
        return typing.cast(typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup], result)

    @builtins.property
    def scale_in_policy(self) -> typing.Optional[builtins.str]:
        '''Specifies the scale-in policy for the VMSS.'''
        result = self._values.get("scale_in_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sku(self) -> typing.Optional[builtins.str]:
        '''The size of the virtual machines in the scale set.

        :default: "Standard_B2s"
        '''
        result = self._values.get("sku")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_image_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the source image for the virtual machines.'''
        result = self._values.get("source_image_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_image_reference(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineSourceImageReference]:
        '''The source image reference for the virtual machines.

        :default: - Uses a default Ubuntu image.
        '''
        result = self._values.get("source_image_reference")
        return typing.cast(typing.Optional[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineSourceImageReference], result)

    @builtins.property
    def subnet(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_subnet_92bbcedf.Subnet]:
        '''The subnet in which the virtual machines will be placed.'''
        result = self._values.get("subnet")
        return typing.cast(typing.Optional[_cdktf_cdktf_provider_azurerm_subnet_92bbcedf.Subnet], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Tags to apply to the virtual machine scale set.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def upgrade_policy_mode(self) -> typing.Optional[builtins.str]:
        '''Specifies the scale set's upgrade policy settings.'''
        result = self._values.get("upgrade_policy_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_data(self) -> typing.Optional[builtins.str]:
        '''Custom data to pass to the virtual machines upon creation.'''
        result = self._values.get("user_data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zones(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The availability zone(s) in which the VMs should be placed.'''
        result = self._values.get("zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LinuxClusterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WindowsCluster(
    _AzureResource_74eec1c4,
    metaclass=jsii.JSIIMeta,
    jsii_type="@microsoft/terraform-cdk-constructs.azure_virtualmachinescaleset.WindowsCluster",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        admin_password: builtins.str,
        admin_username: builtins.str,
        boostrap_custom_data: typing.Optional[builtins.str] = None,
        boot_diagnostics_storage_uri: typing.Optional[builtins.str] = None,
        custom_data: typing.Optional[builtins.str] = None,
        instances: typing.Optional[jsii.Number] = None,
        location: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        os_disk: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineOsDisk, typing.Dict[builtins.str, typing.Any]]] = None,
        overprovision: typing.Optional[builtins.bool] = None,
        public_ip_address: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_azurerm_windows_virtual_machine_scale_set_92bbcedf.WindowsVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddress, typing.Dict[builtins.str, typing.Any]]]] = None,
        resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
        scale_in_policy: typing.Optional[builtins.str] = None,
        sku: typing.Optional[builtins.str] = None,
        source_image_id: typing.Optional[builtins.str] = None,
        source_image_reference: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference, typing.Dict[builtins.str, typing.Any]]] = None,
        subnet: typing.Optional[_cdktf_cdktf_provider_azurerm_subnet_92bbcedf.Subnet] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        upgrade_policy_mode: typing.Optional[builtins.str] = None,
        zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Represents a Windows Virtual Machine Scale Set (VMSS) within Microsoft Azure.

        This class provides a way to deploy and manage a scale set of Windows virtual machines, allowing for configurations such as
        auto-scaling, high availability, and simplified patch management. It supports detailed specifications including
        VM size, the operating system image, network settings, and administrative credentials. Additional capabilities include
        custom data scripts, automatic OS updates, and optional features like managed identity and boot diagnostics.

        :param scope: - The scope in which to define this construct, typically representing the Cloud Development Kit (CDK) application.
        :param id: - The unique identifier for this instance of the Windows cluster, used within the scope for reference.
        :param admin_password: The admin password for the virtual machine.
        :param admin_username: The admin username for the virtual machine.
        :param boostrap_custom_data: Custom data to bootstrap the virtual machine. Automatically triggers Azure Custom Script extension to deploy code in custom data.
        :param boot_diagnostics_storage_uri: Bootdiagnostics settings for the VM.
        :param custom_data: Custom data to pass to the virtual machine upon creation.
        :param instances: The number of VM instances in the scale set. Default: 2
        :param location: The Azure location where the virtual machine should be created. Default: "eastus"
        :param name: The name of the virtual machine. Default: - Uses the name derived from the construct path.
        :param os_disk: The OS disk configuration for the virtual machine. Default: - Uses a disk with caching set to "ReadWrite" and storage account type "Standard_LRS".
        :param overprovision: Specifies if the VMSS should be overprovisioned. Default: true
        :param public_ip_address: The allocation method for the public IP.
        :param resource_group: An optional reference to the resource group in which to deploy the Virtual Machine. If not provided, the Virtual Machine will be deployed in the default resource group.
        :param scale_in_policy: Specifies the scale-in policy for the VMSS.
        :param sku: The size of the virtual machine. Default: "Standard_B2s"
        :param source_image_id: The ID of the source image for the virtual machine.
        :param source_image_reference: The source image reference for the virtual machine. Default: - Uses WindowsServer2022DatacenterCore.
        :param subnet: The subnet in which the virtual machine will be placed. Default: - Uses the default subnet from a new virtual network.
        :param tags: Tags to apply to the virtual machine.
        :param upgrade_policy_mode: Specifies the scale set's upgrade policy settings.
        :param zones: The availability zone(s) in which the VMs should be placed.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aac85c808c5d3545e52ee7a89ac8b31f11b381bd3735f4a38c774454b1f45d20)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = WindowsClusterProps(
            admin_password=admin_password,
            admin_username=admin_username,
            boostrap_custom_data=boostrap_custom_data,
            boot_diagnostics_storage_uri=boot_diagnostics_storage_uri,
            custom_data=custom_data,
            instances=instances,
            location=location,
            name=name,
            os_disk=os_disk,
            overprovision=overprovision,
            public_ip_address=public_ip_address,
            resource_group=resource_group,
            scale_in_policy=scale_in_policy,
            sku=sku,
            source_image_id=source_image_id,
            source_image_reference=source_image_reference,
            subnet=subnet,
            tags=tags,
            upgrade_policy_mode=upgrade_policy_mode,
            zones=zones,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "WindowsClusterProps":
        return typing.cast("WindowsClusterProps", jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96215c518fbf8b1f0bbd2b408c969a832a3ea4c0d635c3959d9327a82e188f45)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9af4785819068d3059e7cd42a98719f5e72532df214dd1760024367fe39fbad2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroup", value)


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_virtualmachinescaleset.WindowsClusterProps",
    jsii_struct_bases=[],
    name_mapping={
        "admin_password": "adminPassword",
        "admin_username": "adminUsername",
        "boostrap_custom_data": "boostrapCustomData",
        "boot_diagnostics_storage_uri": "bootDiagnosticsStorageURI",
        "custom_data": "customData",
        "instances": "instances",
        "location": "location",
        "name": "name",
        "os_disk": "osDisk",
        "overprovision": "overprovision",
        "public_ip_address": "publicIPAddress",
        "resource_group": "resourceGroup",
        "scale_in_policy": "scaleInPolicy",
        "sku": "sku",
        "source_image_id": "sourceImageId",
        "source_image_reference": "sourceImageReference",
        "subnet": "subnet",
        "tags": "tags",
        "upgrade_policy_mode": "upgradePolicyMode",
        "zones": "zones",
    },
)
class WindowsClusterProps:
    def __init__(
        self,
        *,
        admin_password: builtins.str,
        admin_username: builtins.str,
        boostrap_custom_data: typing.Optional[builtins.str] = None,
        boot_diagnostics_storage_uri: typing.Optional[builtins.str] = None,
        custom_data: typing.Optional[builtins.str] = None,
        instances: typing.Optional[jsii.Number] = None,
        location: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        os_disk: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineOsDisk, typing.Dict[builtins.str, typing.Any]]] = None,
        overprovision: typing.Optional[builtins.bool] = None,
        public_ip_address: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_azurerm_windows_virtual_machine_scale_set_92bbcedf.WindowsVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddress, typing.Dict[builtins.str, typing.Any]]]] = None,
        resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
        scale_in_policy: typing.Optional[builtins.str] = None,
        sku: typing.Optional[builtins.str] = None,
        source_image_id: typing.Optional[builtins.str] = None,
        source_image_reference: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference, typing.Dict[builtins.str, typing.Any]]] = None,
        subnet: typing.Optional[_cdktf_cdktf_provider_azurerm_subnet_92bbcedf.Subnet] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        upgrade_policy_mode: typing.Optional[builtins.str] = None,
        zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param admin_password: The admin password for the virtual machine.
        :param admin_username: The admin username for the virtual machine.
        :param boostrap_custom_data: Custom data to bootstrap the virtual machine. Automatically triggers Azure Custom Script extension to deploy code in custom data.
        :param boot_diagnostics_storage_uri: Bootdiagnostics settings for the VM.
        :param custom_data: Custom data to pass to the virtual machine upon creation.
        :param instances: The number of VM instances in the scale set. Default: 2
        :param location: The Azure location where the virtual machine should be created. Default: "eastus"
        :param name: The name of the virtual machine. Default: - Uses the name derived from the construct path.
        :param os_disk: The OS disk configuration for the virtual machine. Default: - Uses a disk with caching set to "ReadWrite" and storage account type "Standard_LRS".
        :param overprovision: Specifies if the VMSS should be overprovisioned. Default: true
        :param public_ip_address: The allocation method for the public IP.
        :param resource_group: An optional reference to the resource group in which to deploy the Virtual Machine. If not provided, the Virtual Machine will be deployed in the default resource group.
        :param scale_in_policy: Specifies the scale-in policy for the VMSS.
        :param sku: The size of the virtual machine. Default: "Standard_B2s"
        :param source_image_id: The ID of the source image for the virtual machine.
        :param source_image_reference: The source image reference for the virtual machine. Default: - Uses WindowsServer2022DatacenterCore.
        :param subnet: The subnet in which the virtual machine will be placed. Default: - Uses the default subnet from a new virtual network.
        :param tags: Tags to apply to the virtual machine.
        :param upgrade_policy_mode: Specifies the scale set's upgrade policy settings.
        :param zones: The availability zone(s) in which the VMs should be placed.
        '''
        if isinstance(os_disk, dict):
            os_disk = _cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineOsDisk(**os_disk)
        if isinstance(source_image_reference, dict):
            source_image_reference = _cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference(**source_image_reference)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff3ab4e46dd61cb52691f16a0779d77034548eb470ba3d06e738ca02a9db7391)
            check_type(argname="argument admin_password", value=admin_password, expected_type=type_hints["admin_password"])
            check_type(argname="argument admin_username", value=admin_username, expected_type=type_hints["admin_username"])
            check_type(argname="argument boostrap_custom_data", value=boostrap_custom_data, expected_type=type_hints["boostrap_custom_data"])
            check_type(argname="argument boot_diagnostics_storage_uri", value=boot_diagnostics_storage_uri, expected_type=type_hints["boot_diagnostics_storage_uri"])
            check_type(argname="argument custom_data", value=custom_data, expected_type=type_hints["custom_data"])
            check_type(argname="argument instances", value=instances, expected_type=type_hints["instances"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument os_disk", value=os_disk, expected_type=type_hints["os_disk"])
            check_type(argname="argument overprovision", value=overprovision, expected_type=type_hints["overprovision"])
            check_type(argname="argument public_ip_address", value=public_ip_address, expected_type=type_hints["public_ip_address"])
            check_type(argname="argument resource_group", value=resource_group, expected_type=type_hints["resource_group"])
            check_type(argname="argument scale_in_policy", value=scale_in_policy, expected_type=type_hints["scale_in_policy"])
            check_type(argname="argument sku", value=sku, expected_type=type_hints["sku"])
            check_type(argname="argument source_image_id", value=source_image_id, expected_type=type_hints["source_image_id"])
            check_type(argname="argument source_image_reference", value=source_image_reference, expected_type=type_hints["source_image_reference"])
            check_type(argname="argument subnet", value=subnet, expected_type=type_hints["subnet"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument upgrade_policy_mode", value=upgrade_policy_mode, expected_type=type_hints["upgrade_policy_mode"])
            check_type(argname="argument zones", value=zones, expected_type=type_hints["zones"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "admin_password": admin_password,
            "admin_username": admin_username,
        }
        if boostrap_custom_data is not None:
            self._values["boostrap_custom_data"] = boostrap_custom_data
        if boot_diagnostics_storage_uri is not None:
            self._values["boot_diagnostics_storage_uri"] = boot_diagnostics_storage_uri
        if custom_data is not None:
            self._values["custom_data"] = custom_data
        if instances is not None:
            self._values["instances"] = instances
        if location is not None:
            self._values["location"] = location
        if name is not None:
            self._values["name"] = name
        if os_disk is not None:
            self._values["os_disk"] = os_disk
        if overprovision is not None:
            self._values["overprovision"] = overprovision
        if public_ip_address is not None:
            self._values["public_ip_address"] = public_ip_address
        if resource_group is not None:
            self._values["resource_group"] = resource_group
        if scale_in_policy is not None:
            self._values["scale_in_policy"] = scale_in_policy
        if sku is not None:
            self._values["sku"] = sku
        if source_image_id is not None:
            self._values["source_image_id"] = source_image_id
        if source_image_reference is not None:
            self._values["source_image_reference"] = source_image_reference
        if subnet is not None:
            self._values["subnet"] = subnet
        if tags is not None:
            self._values["tags"] = tags
        if upgrade_policy_mode is not None:
            self._values["upgrade_policy_mode"] = upgrade_policy_mode
        if zones is not None:
            self._values["zones"] = zones

    @builtins.property
    def admin_password(self) -> builtins.str:
        '''The admin password for the virtual machine.'''
        result = self._values.get("admin_password")
        assert result is not None, "Required property 'admin_password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def admin_username(self) -> builtins.str:
        '''The admin username for the virtual machine.'''
        result = self._values.get("admin_username")
        assert result is not None, "Required property 'admin_username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def boostrap_custom_data(self) -> typing.Optional[builtins.str]:
        '''Custom data to bootstrap the virtual machine.

        Automatically triggers Azure Custom Script extension to deploy code in custom data.
        '''
        result = self._values.get("boostrap_custom_data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def boot_diagnostics_storage_uri(self) -> typing.Optional[builtins.str]:
        '''Bootdiagnostics settings for the VM.'''
        result = self._values.get("boot_diagnostics_storage_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_data(self) -> typing.Optional[builtins.str]:
        '''Custom data to pass to the virtual machine upon creation.'''
        result = self._values.get("custom_data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instances(self) -> typing.Optional[jsii.Number]:
        '''The number of VM instances in the scale set.

        :default: 2
        '''
        result = self._values.get("instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The Azure location where the virtual machine should be created.

        :default: "eastus"
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the virtual machine.

        :default: - Uses the name derived from the construct path.
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def os_disk(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineOsDisk]:
        '''The OS disk configuration for the virtual machine.

        :default: - Uses a disk with caching set to "ReadWrite" and storage account type "Standard_LRS".
        '''
        result = self._values.get("os_disk")
        return typing.cast(typing.Optional[_cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineOsDisk], result)

    @builtins.property
    def overprovision(self) -> typing.Optional[builtins.bool]:
        '''Specifies if the VMSS should be overprovisioned.

        :default: true
        '''
        result = self._values.get("overprovision")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def public_ip_address(
        self,
    ) -> typing.Optional[typing.List[_cdktf_cdktf_provider_azurerm_windows_virtual_machine_scale_set_92bbcedf.WindowsVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddress]]:
        '''The allocation method for the public IP.'''
        result = self._values.get("public_ip_address")
        return typing.cast(typing.Optional[typing.List[_cdktf_cdktf_provider_azurerm_windows_virtual_machine_scale_set_92bbcedf.WindowsVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddress]], result)

    @builtins.property
    def resource_group(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup]:
        '''An optional reference to the resource group in which to deploy the Virtual Machine.

        If not provided, the Virtual Machine will be deployed in the default resource group.
        '''
        result = self._values.get("resource_group")
        return typing.cast(typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup], result)

    @builtins.property
    def scale_in_policy(self) -> typing.Optional[builtins.str]:
        '''Specifies the scale-in policy for the VMSS.'''
        result = self._values.get("scale_in_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sku(self) -> typing.Optional[builtins.str]:
        '''The size of the virtual machine.

        :default: "Standard_B2s"
        '''
        result = self._values.get("sku")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_image_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the source image for the virtual machine.'''
        result = self._values.get("source_image_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_image_reference(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference]:
        '''The source image reference for the virtual machine.

        :default: - Uses WindowsServer2022DatacenterCore.
        '''
        result = self._values.get("source_image_reference")
        return typing.cast(typing.Optional[_cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference], result)

    @builtins.property
    def subnet(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_subnet_92bbcedf.Subnet]:
        '''The subnet in which the virtual machine will be placed.

        :default: - Uses the default subnet from a new virtual network.
        '''
        result = self._values.get("subnet")
        return typing.cast(typing.Optional[_cdktf_cdktf_provider_azurerm_subnet_92bbcedf.Subnet], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Tags to apply to the virtual machine.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def upgrade_policy_mode(self) -> typing.Optional[builtins.str]:
        '''Specifies the scale set's upgrade policy settings.'''
        result = self._values.get("upgrade_policy_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zones(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The availability zone(s) in which the VMs should be placed.'''
        result = self._values.get("zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WindowsClusterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "LinuxCluster",
    "LinuxClusterProps",
    "WindowsCluster",
    "WindowsClusterProps",
]

publication.publish()

def _typecheckingstub__7fc27996012db416df4e609b98d48137396321f694a3108be3d89d25a4942b65(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    admin_password: typing.Optional[builtins.str] = None,
    admin_ssh_key: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineAdminSshKey, typing.Dict[builtins.str, typing.Any]]]]] = None,
    admin_username: typing.Optional[builtins.str] = None,
    boot_diagnostics_storage_uri: typing.Optional[builtins.str] = None,
    custom_data: typing.Optional[builtins.str] = None,
    enable_ssh_azure_ad_login: typing.Optional[builtins.bool] = None,
    identity: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    instances: typing.Optional[jsii.Number] = None,
    location: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    os_disk: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineOsDisk, typing.Dict[builtins.str, typing.Any]]] = None,
    overprovision: typing.Optional[builtins.bool] = None,
    public_ip_address: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_scale_set_92bbcedf.LinuxVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddress, typing.Dict[builtins.str, typing.Any]]]] = None,
    resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
    scale_in_policy: typing.Optional[builtins.str] = None,
    sku: typing.Optional[builtins.str] = None,
    source_image_id: typing.Optional[builtins.str] = None,
    source_image_reference: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineSourceImageReference, typing.Dict[builtins.str, typing.Any]]] = None,
    subnet: typing.Optional[_cdktf_cdktf_provider_azurerm_subnet_92bbcedf.Subnet] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    upgrade_policy_mode: typing.Optional[builtins.str] = None,
    user_data: typing.Optional[builtins.str] = None,
    zones: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a5bab57b28263fc46a53ddf95de61b6acea41f2c0228a0ed5bcc955aac7f737(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1a4f01c717c28ff4221ab482c74fa4fa8e2ccf900d70156ad3055dac288b58c(
    value: _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c770324700497911e54255fe4669fae1f7a3e4b885fcde59827d6d885ecb64be(
    *,
    admin_password: typing.Optional[builtins.str] = None,
    admin_ssh_key: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineAdminSshKey, typing.Dict[builtins.str, typing.Any]]]]] = None,
    admin_username: typing.Optional[builtins.str] = None,
    boot_diagnostics_storage_uri: typing.Optional[builtins.str] = None,
    custom_data: typing.Optional[builtins.str] = None,
    enable_ssh_azure_ad_login: typing.Optional[builtins.bool] = None,
    identity: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    instances: typing.Optional[jsii.Number] = None,
    location: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    os_disk: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineOsDisk, typing.Dict[builtins.str, typing.Any]]] = None,
    overprovision: typing.Optional[builtins.bool] = None,
    public_ip_address: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_scale_set_92bbcedf.LinuxVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddress, typing.Dict[builtins.str, typing.Any]]]] = None,
    resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
    scale_in_policy: typing.Optional[builtins.str] = None,
    sku: typing.Optional[builtins.str] = None,
    source_image_id: typing.Optional[builtins.str] = None,
    source_image_reference: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineSourceImageReference, typing.Dict[builtins.str, typing.Any]]] = None,
    subnet: typing.Optional[_cdktf_cdktf_provider_azurerm_subnet_92bbcedf.Subnet] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    upgrade_policy_mode: typing.Optional[builtins.str] = None,
    user_data: typing.Optional[builtins.str] = None,
    zones: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aac85c808c5d3545e52ee7a89ac8b31f11b381bd3735f4a38c774454b1f45d20(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    admin_password: builtins.str,
    admin_username: builtins.str,
    boostrap_custom_data: typing.Optional[builtins.str] = None,
    boot_diagnostics_storage_uri: typing.Optional[builtins.str] = None,
    custom_data: typing.Optional[builtins.str] = None,
    instances: typing.Optional[jsii.Number] = None,
    location: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    os_disk: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineOsDisk, typing.Dict[builtins.str, typing.Any]]] = None,
    overprovision: typing.Optional[builtins.bool] = None,
    public_ip_address: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_azurerm_windows_virtual_machine_scale_set_92bbcedf.WindowsVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddress, typing.Dict[builtins.str, typing.Any]]]] = None,
    resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
    scale_in_policy: typing.Optional[builtins.str] = None,
    sku: typing.Optional[builtins.str] = None,
    source_image_id: typing.Optional[builtins.str] = None,
    source_image_reference: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference, typing.Dict[builtins.str, typing.Any]]] = None,
    subnet: typing.Optional[_cdktf_cdktf_provider_azurerm_subnet_92bbcedf.Subnet] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    upgrade_policy_mode: typing.Optional[builtins.str] = None,
    zones: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96215c518fbf8b1f0bbd2b408c969a832a3ea4c0d635c3959d9327a82e188f45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9af4785819068d3059e7cd42a98719f5e72532df214dd1760024367fe39fbad2(
    value: _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff3ab4e46dd61cb52691f16a0779d77034548eb470ba3d06e738ca02a9db7391(
    *,
    admin_password: builtins.str,
    admin_username: builtins.str,
    boostrap_custom_data: typing.Optional[builtins.str] = None,
    boot_diagnostics_storage_uri: typing.Optional[builtins.str] = None,
    custom_data: typing.Optional[builtins.str] = None,
    instances: typing.Optional[jsii.Number] = None,
    location: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    os_disk: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineOsDisk, typing.Dict[builtins.str, typing.Any]]] = None,
    overprovision: typing.Optional[builtins.bool] = None,
    public_ip_address: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_azurerm_windows_virtual_machine_scale_set_92bbcedf.WindowsVirtualMachineScaleSetNetworkInterfaceIpConfigurationPublicIpAddress, typing.Dict[builtins.str, typing.Any]]]] = None,
    resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
    scale_in_policy: typing.Optional[builtins.str] = None,
    sku: typing.Optional[builtins.str] = None,
    source_image_id: typing.Optional[builtins.str] = None,
    source_image_reference: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference, typing.Dict[builtins.str, typing.Any]]] = None,
    subnet: typing.Optional[_cdktf_cdktf_provider_azurerm_subnet_92bbcedf.Subnet] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    upgrade_policy_mode: typing.Optional[builtins.str] = None,
    zones: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
