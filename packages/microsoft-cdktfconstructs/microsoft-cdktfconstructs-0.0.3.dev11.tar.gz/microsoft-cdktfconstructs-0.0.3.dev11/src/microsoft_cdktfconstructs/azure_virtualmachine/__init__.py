'''
# Azure Virtual Machine Construct

This construct provides a simplified way to deploy and manage an Azure Virtual Machine (VM), suitable for both Windows and Linux configurations.

## Overview

Azure Virtual Machines give you the flexibility of virtualization without buying and maintaining the physical hardware. They are ideal for a variety of computing solutions like development and testing, running applications, and extending your datacenter.

For detailed information on Azure VMs, visit the [Azure Virtual Machines documentation](https://docs.microsoft.com/en-us/azure/virtual-machines/).

## Best Practices for Virtual Machines

* **Size Appropriately**: Choose a VM size that fits your workload requirements.
* **Keep Updated**: Regularly apply updates and patches to your VMs.
* **Network Security**: Secure your VMs with network security groups and firewall rules.
* **Use Managed Disks**: Leverage managed disks for better management and security of your VM storage.
* **Backup and Recovery**: Implement a backup strategy and disaster recovery plan.

## Construct Properties

Configure your VM with the following properties:

* `location`: The deployment region for the VM.
* `resourceGroupName`: The name of the resource group.
* `name`: The name of the VM.
* `size`: The VM size (e.g., `Standard_B2s`).
* `adminUsername`: Administrator username for the VM.
* `adminPassword`: Administrator password for the VM.
* `sourceImageReference`: Reference to the source image for the VM's operating system.
* `osDisk`: Configuration for the operating system disk.
* `networkInterface`: Network interface details for the VM.
* `publicIPAllocationMethod`: Allocation method for the VM's public IP address.
* `tags`: A dictionary of tags to apply to the VM.
* `customData`: Custom data for bootstrapping the VM.

## Deployment Example

### Windows Virtual Machine

```python
const azureWindowsVM = new AzureWindowsVirtualMachine(this, 'myWindowsVM', {
  resourceGroupName: 'myResourceGroup',
  location: 'West US',
  name: 'myWindowsVM',
  adminUsername: 'adminuser',
  adminPassword: 'SecurePassword123',
  size: 'Standard_B2s',
  tags: {
    'env': 'production',
  },
  // Additional configurations...
});
```

### Linux Virtual Machine

```python
const azureLinuxVM = new AzureLinuxVirtualMachine(this, 'myLinuxVM', {
  resourceGroupName: 'myResourceGroup',
  location: 'West US',
  name: 'myLinuxVM',
  adminUsername: 'adminuser',
  size: 'Standard_B2s',
  tags: {
    'env': 'development',
  },
  // Additional configurations...
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
import cdktf_cdktf_provider_azurerm.resource_group as _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf
import cdktf_cdktf_provider_azurerm.subnet as _cdktf_cdktf_provider_azurerm_subnet_92bbcedf
import cdktf_cdktf_provider_azurerm.windows_virtual_machine as _cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf
import constructs as _constructs_77d1e7e8
from ..core_azure import AzureResource as _AzureResource_74eec1c4


class LinuxImageReferences(
    metaclass=jsii.JSIIMeta,
    jsii_type="@microsoft/terraform-cdk-constructs.azure_virtualmachine.LinuxImageReferences",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.python.classproperty
    @jsii.member(jsii_name="centOS75")
    def cent_os75(
        cls,
    ) -> _cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineSourceImageReference:  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineSourceImageReference, jsii.sget(cls, "centOS75"))

    @cent_os75.setter # type: ignore[no-redef]
    def cent_os75(
        cls,
        value: _cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineSourceImageReference,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29a7c8d8f4ade05e5e41d2ccd39372d86d2fa2224109c485bf2f79e84b4836ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "centOS75", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="centOS85Gen2")
    def cent_os85_gen2(
        cls,
    ) -> _cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineSourceImageReference:  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineSourceImageReference, jsii.sget(cls, "centOS85Gen2"))

    @cent_os85_gen2.setter # type: ignore[no-redef]
    def cent_os85_gen2(
        cls,
        value: _cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineSourceImageReference,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5930d1184f218f5a271e84427012d2dbc17809f7422ecce05bf2b3ac575715e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "centOS85Gen2", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="debian10")
    def debian10(
        cls,
    ) -> _cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineSourceImageReference:  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineSourceImageReference, jsii.sget(cls, "debian10"))

    @debian10.setter # type: ignore[no-redef]
    def debian10(
        cls,
        value: _cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineSourceImageReference,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__332d98f3e6e5e53589f78bddd78e5ca9dcf43ecf7932ce6bf073b7dfc11ee209)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "debian10", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="debian11BackportsGen2")
    def debian11_backports_gen2(
        cls,
    ) -> _cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineSourceImageReference:  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineSourceImageReference, jsii.sget(cls, "debian11BackportsGen2"))

    @debian11_backports_gen2.setter # type: ignore[no-redef]
    def debian11_backports_gen2(
        cls,
        value: _cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineSourceImageReference,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf30a5745843a5ebe2e5fdf88ed967b6ea615a6c1cf691bc07b3711445edb237)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "debian11BackportsGen2", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="ubuntuServer1804LTS")
    def ubuntu_server1804_lts(
        cls,
    ) -> _cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineSourceImageReference:  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineSourceImageReference, jsii.sget(cls, "ubuntuServer1804LTS"))

    @ubuntu_server1804_lts.setter # type: ignore[no-redef]
    def ubuntu_server1804_lts(
        cls,
        value: _cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineSourceImageReference,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c977d4d4456b47218802aab7d3dd741e65a3c5b0c2772fb3b495a2733bc5209)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "ubuntuServer1804LTS", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="ubuntuServer2204LTS")
    def ubuntu_server2204_lts(
        cls,
    ) -> _cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineSourceImageReference:  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineSourceImageReference, jsii.sget(cls, "ubuntuServer2204LTS"))

    @ubuntu_server2204_lts.setter # type: ignore[no-redef]
    def ubuntu_server2204_lts(
        cls,
        value: _cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineSourceImageReference,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55ae29f90b43e9254f55fda36fb112dacb0a667d26f0ab3e6a15f145f8a2e180)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "ubuntuServer2204LTS", value)


class LinuxVM(
    _AzureResource_74eec1c4,
    metaclass=jsii.JSIIMeta,
    jsii_type="@microsoft/terraform-cdk-constructs.azure_virtualmachine.LinuxVM",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        additional_capabilities: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineAdditionalCapabilities, typing.Dict[builtins.str, typing.Any]]] = None,
        admin_password: typing.Optional[builtins.str] = None,
        admin_ssh_key: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineAdminSshKey, typing.Dict[builtins.str, typing.Any]]]]] = None,
        admin_username: typing.Optional[builtins.str] = None,
        availability_set_id: typing.Optional[builtins.str] = None,
        boot_diagnostics_storage_uri: typing.Optional[builtins.str] = None,
        custom_data: typing.Optional[builtins.str] = None,
        enable_ssh_azure_ad_login: typing.Optional[builtins.bool] = None,
        identity: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
        location: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        os_disk: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineOsDisk, typing.Dict[builtins.str, typing.Any]]] = None,
        public_ip_allocation_method: typing.Optional[builtins.str] = None,
        resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
        secret: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineSecret, typing.Dict[builtins.str, typing.Any]]]] = None,
        size: typing.Optional[builtins.str] = None,
        source_image_id: typing.Optional[builtins.str] = None,
        source_image_reference: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineSourceImageReference, typing.Dict[builtins.str, typing.Any]]] = None,
        subnet: typing.Optional[_cdktf_cdktf_provider_azurerm_subnet_92bbcedf.Subnet] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        user_data: typing.Optional[builtins.str] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Represents a Linux-based Virtual Machine (VM) within Microsoft Azure.

        This class is designed to provision and manage a Linux VM in Azure, facilitating detailed configuration including
        VM size, the operating system image, network settings, and administrative credentials. It supports custom data scripts,
        SSH configurations, and optional features like managed identity and boot diagnostics.

        :param scope: - The scope in which to define this construct, typically representing the Cloud Development Kit (CDK) application.
        :param id: - The unique identifier for this instance of the Linux VM, used within the scope for reference.
        :param additional_capabilities: Additional capabilities like Ultra Disk compatibility.
        :param admin_password: The admin password for the virtual machine.
        :param admin_ssh_key: An array of SSH keys for the admin user.
        :param admin_username: The admin username for the virtual machine.
        :param availability_set_id: The ID of the availability set in which the VM should be placed.
        :param boot_diagnostics_storage_uri: Bootdiagnostics settings for the VM.
        :param custom_data: Custom data to pass to the virtual machine upon creation.
        :param enable_ssh_azure_ad_login: Enable SSH Azure AD Login, required managed identity to be set.
        :param identity: Managed identity settings for the VM.
        :param location: The Azure location where the virtual machine should be created. Default: "eastus"
        :param name: The name of the virtual machine. Default: - Uses the name derived from the construct path.
        :param os_disk: The OS disk configuration for the virtual machine. Default: - Uses a disk with caching set to "ReadWrite" and storage account type "Standard_LRS".
        :param public_ip_allocation_method: The allocation method for the public IP.
        :param resource_group: An optional reference to the resource group in which to deploy the Virtual Machine. If not provided, the Virtual Machine will be deployed in the default resource group.
        :param secret: An array of secrets to be passed to the VM.
        :param size: The size of the virtual machine. Default: "Standard_B2s"
        :param source_image_id: The ID of the source image for the virtual machine.
        :param source_image_reference: The source image reference for the virtual machine. Default: - Uses WindowsServer2022DatacenterCore.
        :param subnet: The subnet in which the virtual machine will be placed. Default: - Uses the default subnet from a new virtual network.
        :param tags: Tags to apply to the virtual machine.
        :param user_data: Custom data to pass to the virtual machine upon creation.
        :param zone: The availability zone in which the VM should be placed.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4503c856086be09ccd03fad9fec5fa5a06773c3e3cfd91a62ac778582a4b3ada)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = LinuxVMProps(
            additional_capabilities=additional_capabilities,
            admin_password=admin_password,
            admin_ssh_key=admin_ssh_key,
            admin_username=admin_username,
            availability_set_id=availability_set_id,
            boot_diagnostics_storage_uri=boot_diagnostics_storage_uri,
            custom_data=custom_data,
            enable_ssh_azure_ad_login=enable_ssh_azure_ad_login,
            identity=identity,
            location=location,
            name=name,
            os_disk=os_disk,
            public_ip_allocation_method=public_ip_allocation_method,
            resource_group=resource_group,
            secret=secret,
            size=size,
            source_image_id=source_image_id,
            source_image_reference=source_image_reference,
            subnet=subnet,
            tags=tags,
            user_data=user_data,
            zone=zone,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "LinuxVMProps":
        return typing.cast("LinuxVMProps", jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="publicIp")
    def public_ip(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicIp"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c5f0ee7ea05450a854f9fbb748ea8d4d20d5af57db5caff9ee90994b7c45755)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a57b7d59a91a7d43ceef299ac7a55a7e1c678e52058ec6f6fa9c402e61271919)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroup", value)


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_virtualmachine.LinuxVMProps",
    jsii_struct_bases=[],
    name_mapping={
        "additional_capabilities": "additionalCapabilities",
        "admin_password": "adminPassword",
        "admin_ssh_key": "adminSshKey",
        "admin_username": "adminUsername",
        "availability_set_id": "availabilitySetId",
        "boot_diagnostics_storage_uri": "bootDiagnosticsStorageURI",
        "custom_data": "customData",
        "enable_ssh_azure_ad_login": "enableSshAzureADLogin",
        "identity": "identity",
        "location": "location",
        "name": "name",
        "os_disk": "osDisk",
        "public_ip_allocation_method": "publicIPAllocationMethod",
        "resource_group": "resourceGroup",
        "secret": "secret",
        "size": "size",
        "source_image_id": "sourceImageId",
        "source_image_reference": "sourceImageReference",
        "subnet": "subnet",
        "tags": "tags",
        "user_data": "userData",
        "zone": "zone",
    },
)
class LinuxVMProps:
    def __init__(
        self,
        *,
        additional_capabilities: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineAdditionalCapabilities, typing.Dict[builtins.str, typing.Any]]] = None,
        admin_password: typing.Optional[builtins.str] = None,
        admin_ssh_key: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineAdminSshKey, typing.Dict[builtins.str, typing.Any]]]]] = None,
        admin_username: typing.Optional[builtins.str] = None,
        availability_set_id: typing.Optional[builtins.str] = None,
        boot_diagnostics_storage_uri: typing.Optional[builtins.str] = None,
        custom_data: typing.Optional[builtins.str] = None,
        enable_ssh_azure_ad_login: typing.Optional[builtins.bool] = None,
        identity: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
        location: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        os_disk: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineOsDisk, typing.Dict[builtins.str, typing.Any]]] = None,
        public_ip_allocation_method: typing.Optional[builtins.str] = None,
        resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
        secret: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineSecret, typing.Dict[builtins.str, typing.Any]]]] = None,
        size: typing.Optional[builtins.str] = None,
        source_image_id: typing.Optional[builtins.str] = None,
        source_image_reference: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineSourceImageReference, typing.Dict[builtins.str, typing.Any]]] = None,
        subnet: typing.Optional[_cdktf_cdktf_provider_azurerm_subnet_92bbcedf.Subnet] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        user_data: typing.Optional[builtins.str] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param additional_capabilities: Additional capabilities like Ultra Disk compatibility.
        :param admin_password: The admin password for the virtual machine.
        :param admin_ssh_key: An array of SSH keys for the admin user.
        :param admin_username: The admin username for the virtual machine.
        :param availability_set_id: The ID of the availability set in which the VM should be placed.
        :param boot_diagnostics_storage_uri: Bootdiagnostics settings for the VM.
        :param custom_data: Custom data to pass to the virtual machine upon creation.
        :param enable_ssh_azure_ad_login: Enable SSH Azure AD Login, required managed identity to be set.
        :param identity: Managed identity settings for the VM.
        :param location: The Azure location where the virtual machine should be created. Default: "eastus"
        :param name: The name of the virtual machine. Default: - Uses the name derived from the construct path.
        :param os_disk: The OS disk configuration for the virtual machine. Default: - Uses a disk with caching set to "ReadWrite" and storage account type "Standard_LRS".
        :param public_ip_allocation_method: The allocation method for the public IP.
        :param resource_group: An optional reference to the resource group in which to deploy the Virtual Machine. If not provided, the Virtual Machine will be deployed in the default resource group.
        :param secret: An array of secrets to be passed to the VM.
        :param size: The size of the virtual machine. Default: "Standard_B2s"
        :param source_image_id: The ID of the source image for the virtual machine.
        :param source_image_reference: The source image reference for the virtual machine. Default: - Uses WindowsServer2022DatacenterCore.
        :param subnet: The subnet in which the virtual machine will be placed. Default: - Uses the default subnet from a new virtual network.
        :param tags: Tags to apply to the virtual machine.
        :param user_data: Custom data to pass to the virtual machine upon creation.
        :param zone: The availability zone in which the VM should be placed.
        '''
        if isinstance(additional_capabilities, dict):
            additional_capabilities = _cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineAdditionalCapabilities(**additional_capabilities)
        if isinstance(identity, dict):
            identity = _cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineIdentity(**identity)
        if isinstance(os_disk, dict):
            os_disk = _cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineOsDisk(**os_disk)
        if isinstance(source_image_reference, dict):
            source_image_reference = _cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineSourceImageReference(**source_image_reference)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53d88c32a57de5faac8a76fe382df39f974f727204f91f8ebede45487727829e)
            check_type(argname="argument additional_capabilities", value=additional_capabilities, expected_type=type_hints["additional_capabilities"])
            check_type(argname="argument admin_password", value=admin_password, expected_type=type_hints["admin_password"])
            check_type(argname="argument admin_ssh_key", value=admin_ssh_key, expected_type=type_hints["admin_ssh_key"])
            check_type(argname="argument admin_username", value=admin_username, expected_type=type_hints["admin_username"])
            check_type(argname="argument availability_set_id", value=availability_set_id, expected_type=type_hints["availability_set_id"])
            check_type(argname="argument boot_diagnostics_storage_uri", value=boot_diagnostics_storage_uri, expected_type=type_hints["boot_diagnostics_storage_uri"])
            check_type(argname="argument custom_data", value=custom_data, expected_type=type_hints["custom_data"])
            check_type(argname="argument enable_ssh_azure_ad_login", value=enable_ssh_azure_ad_login, expected_type=type_hints["enable_ssh_azure_ad_login"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument os_disk", value=os_disk, expected_type=type_hints["os_disk"])
            check_type(argname="argument public_ip_allocation_method", value=public_ip_allocation_method, expected_type=type_hints["public_ip_allocation_method"])
            check_type(argname="argument resource_group", value=resource_group, expected_type=type_hints["resource_group"])
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
            check_type(argname="argument source_image_id", value=source_image_id, expected_type=type_hints["source_image_id"])
            check_type(argname="argument source_image_reference", value=source_image_reference, expected_type=type_hints["source_image_reference"])
            check_type(argname="argument subnet", value=subnet, expected_type=type_hints["subnet"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument user_data", value=user_data, expected_type=type_hints["user_data"])
            check_type(argname="argument zone", value=zone, expected_type=type_hints["zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if additional_capabilities is not None:
            self._values["additional_capabilities"] = additional_capabilities
        if admin_password is not None:
            self._values["admin_password"] = admin_password
        if admin_ssh_key is not None:
            self._values["admin_ssh_key"] = admin_ssh_key
        if admin_username is not None:
            self._values["admin_username"] = admin_username
        if availability_set_id is not None:
            self._values["availability_set_id"] = availability_set_id
        if boot_diagnostics_storage_uri is not None:
            self._values["boot_diagnostics_storage_uri"] = boot_diagnostics_storage_uri
        if custom_data is not None:
            self._values["custom_data"] = custom_data
        if enable_ssh_azure_ad_login is not None:
            self._values["enable_ssh_azure_ad_login"] = enable_ssh_azure_ad_login
        if identity is not None:
            self._values["identity"] = identity
        if location is not None:
            self._values["location"] = location
        if name is not None:
            self._values["name"] = name
        if os_disk is not None:
            self._values["os_disk"] = os_disk
        if public_ip_allocation_method is not None:
            self._values["public_ip_allocation_method"] = public_ip_allocation_method
        if resource_group is not None:
            self._values["resource_group"] = resource_group
        if secret is not None:
            self._values["secret"] = secret
        if size is not None:
            self._values["size"] = size
        if source_image_id is not None:
            self._values["source_image_id"] = source_image_id
        if source_image_reference is not None:
            self._values["source_image_reference"] = source_image_reference
        if subnet is not None:
            self._values["subnet"] = subnet
        if tags is not None:
            self._values["tags"] = tags
        if user_data is not None:
            self._values["user_data"] = user_data
        if zone is not None:
            self._values["zone"] = zone

    @builtins.property
    def additional_capabilities(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineAdditionalCapabilities]:
        '''Additional capabilities like Ultra Disk compatibility.'''
        result = self._values.get("additional_capabilities")
        return typing.cast(typing.Optional[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineAdditionalCapabilities], result)

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
    def availability_set_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the availability set in which the VM should be placed.'''
        result = self._values.get("availability_set_id")
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
    def enable_ssh_azure_ad_login(self) -> typing.Optional[builtins.bool]:
        '''Enable SSH Azure AD Login, required managed identity to be set.'''
        result = self._values.get("enable_ssh_azure_ad_login")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def identity(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineIdentity]:
        '''Managed identity settings for the VM.'''
        result = self._values.get("identity")
        return typing.cast(typing.Optional[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineIdentity], result)

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
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineOsDisk]:
        '''The OS disk configuration for the virtual machine.

        :default: - Uses a disk with caching set to "ReadWrite" and storage account type "Standard_LRS".
        '''
        result = self._values.get("os_disk")
        return typing.cast(typing.Optional[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineOsDisk], result)

    @builtins.property
    def public_ip_allocation_method(self) -> typing.Optional[builtins.str]:
        '''The allocation method for the public IP.'''
        result = self._values.get("public_ip_allocation_method")
        return typing.cast(typing.Optional[builtins.str], result)

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
    def secret(
        self,
    ) -> typing.Optional[typing.List[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineSecret]]:
        '''An array of secrets to be passed to the VM.'''
        result = self._values.get("secret")
        return typing.cast(typing.Optional[typing.List[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineSecret]], result)

    @builtins.property
    def size(self) -> typing.Optional[builtins.str]:
        '''The size of the virtual machine.

        :default: "Standard_B2s"
        '''
        result = self._values.get("size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_image_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the source image for the virtual machine.'''
        result = self._values.get("source_image_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_image_reference(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineSourceImageReference]:
        '''The source image reference for the virtual machine.

        :default: - Uses WindowsServer2022DatacenterCore.
        '''
        result = self._values.get("source_image_reference")
        return typing.cast(typing.Optional[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineSourceImageReference], result)

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
    def user_data(self) -> typing.Optional[builtins.str]:
        '''Custom data to pass to the virtual machine upon creation.'''
        result = self._values.get("user_data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zone(self) -> typing.Optional[builtins.str]:
        '''The availability zone in which the VM should be placed.'''
        result = self._values.get("zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LinuxVMProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WindowsImageReferences(
    metaclass=jsii.JSIIMeta,
    jsii_type="@microsoft/terraform-cdk-constructs.azure_virtualmachine.WindowsImageReferences",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.python.classproperty
    @jsii.member(jsii_name="windows10Enterprise")
    def windows10_enterprise(
        cls,
    ) -> _cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference:  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference, jsii.sget(cls, "windows10Enterprise"))

    @windows10_enterprise.setter # type: ignore[no-redef]
    def windows10_enterprise(
        cls,
        value: _cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf40c34d0166c0f6bee833b7b61bb742f4f48b90d3e4b3e5eeef1a04db5c4606)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "windows10Enterprise", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="windows10Pro")
    def windows10_pro(
        cls,
    ) -> _cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference:  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference, jsii.sget(cls, "windows10Pro"))

    @windows10_pro.setter # type: ignore[no-redef]
    def windows10_pro(
        cls,
        value: _cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9aff3b10fb9bc184f52cf14764691d0c805719c00ccd9637a645f259045085d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "windows10Pro", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="windowsServer2012R2Datacenter")
    def windows_server2012_r2_datacenter(
        cls,
    ) -> _cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference:  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference, jsii.sget(cls, "windowsServer2012R2Datacenter"))

    @windows_server2012_r2_datacenter.setter # type: ignore[no-redef]
    def windows_server2012_r2_datacenter(
        cls,
        value: _cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5ebfee79d399fb0e9a7b8f50006a53381a91211129c2124c0f1ae78ee3dd172)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "windowsServer2012R2Datacenter", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="windowsServer2012R2DatacenterCore")
    def windows_server2012_r2_datacenter_core(
        cls,
    ) -> _cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference:  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference, jsii.sget(cls, "windowsServer2012R2DatacenterCore"))

    @windows_server2012_r2_datacenter_core.setter # type: ignore[no-redef]
    def windows_server2012_r2_datacenter_core(
        cls,
        value: _cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fb3ea6e310f913788b2dcc3f2798ad0ac7f3162bec92b92c2e0d06399e7c0d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "windowsServer2012R2DatacenterCore", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="windowsServer2016Datacenter")
    def windows_server2016_datacenter(
        cls,
    ) -> _cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference:  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference, jsii.sget(cls, "windowsServer2016Datacenter"))

    @windows_server2016_datacenter.setter # type: ignore[no-redef]
    def windows_server2016_datacenter(
        cls,
        value: _cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab632c1332e6eb149f8379dd60672373b62743d1a44f42fcf20f220c5190cf9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "windowsServer2016Datacenter", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="windowsServer2016DatacenterCore")
    def windows_server2016_datacenter_core(
        cls,
    ) -> _cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference:  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference, jsii.sget(cls, "windowsServer2016DatacenterCore"))

    @windows_server2016_datacenter_core.setter # type: ignore[no-redef]
    def windows_server2016_datacenter_core(
        cls,
        value: _cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cce5ebd44c0d1eb2ecf32b2c12611fe3c6fca269e4b37341c6bb8615d8dd0e3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "windowsServer2016DatacenterCore", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="windowsServer2019Datacenter")
    def windows_server2019_datacenter(
        cls,
    ) -> _cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference:  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference, jsii.sget(cls, "windowsServer2019Datacenter"))

    @windows_server2019_datacenter.setter # type: ignore[no-redef]
    def windows_server2019_datacenter(
        cls,
        value: _cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca4185605ed0a1f2183d40eaa7ba6d4284c7431d629b2e82ffb3c7f6822189ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "windowsServer2019Datacenter", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="windowsServer2019DatacenterCore")
    def windows_server2019_datacenter_core(
        cls,
    ) -> _cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference:  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference, jsii.sget(cls, "windowsServer2019DatacenterCore"))

    @windows_server2019_datacenter_core.setter # type: ignore[no-redef]
    def windows_server2019_datacenter_core(
        cls,
        value: _cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f57c5d44eee3ebbd882a61df6189449ceea10f7dd5141cf63bbb84bfa77850d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "windowsServer2019DatacenterCore", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="windowsServer2022Datacenter")
    def windows_server2022_datacenter(
        cls,
    ) -> _cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference:  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference, jsii.sget(cls, "windowsServer2022Datacenter"))

    @windows_server2022_datacenter.setter # type: ignore[no-redef]
    def windows_server2022_datacenter(
        cls,
        value: _cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47ebd4045041171630b40321487b500a7da9806e4f60bdfe7b79957dd3a12e64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "windowsServer2022Datacenter", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="windowsServer2022DatacenterCore")
    def windows_server2022_datacenter_core(
        cls,
    ) -> _cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference:  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference, jsii.sget(cls, "windowsServer2022DatacenterCore"))

    @windows_server2022_datacenter_core.setter # type: ignore[no-redef]
    def windows_server2022_datacenter_core(
        cls,
        value: _cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e56057d4d440886628ab2559209f143dd2c88e7da105be6d2a71911f212b8e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "windowsServer2022DatacenterCore", value)


class WindowsVM(
    _AzureResource_74eec1c4,
    metaclass=jsii.JSIIMeta,
    jsii_type="@microsoft/terraform-cdk-constructs.azure_virtualmachine.WindowsVM",
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
        location: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        os_disk: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineOsDisk, typing.Dict[builtins.str, typing.Any]]] = None,
        public_ip_allocation_method: typing.Optional[builtins.str] = None,
        resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
        size: typing.Optional[builtins.str] = None,
        source_image_id: typing.Optional[builtins.str] = None,
        source_image_reference: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference, typing.Dict[builtins.str, typing.Any]]] = None,
        subnet: typing.Optional[_cdktf_cdktf_provider_azurerm_subnet_92bbcedf.Subnet] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Represents a Windows-based Virtual Machine (VM) within Microsoft Azure.

        This class is designed to provision and manage a Windows VM in Azure, allowing for detailed configuration including
        the VM's size, the operating system image, network settings, and administrative credentials. It supports customization
        of the OS disk, networking setup, and optional features like custom data scripts and boot diagnostics.

        :param scope: - The scope in which to define this construct, typically representing the Cloud Development Kit (CDK) application.
        :param id: - The unique identifier for this instance of the Windows VM, used within the scope for reference.
        :param admin_password: The admin password for the virtual machine.
        :param admin_username: The admin username for the virtual machine.
        :param boostrap_custom_data: Custom data to bootstrap the virtual machine. Automatically triggers Azure Custom Script extension to deploy code in custom data.
        :param boot_diagnostics_storage_uri: Bootdiagnostics settings for the VM.
        :param custom_data: Custom data to pass to the virtual machine upon creation.
        :param location: The Azure location where the virtual machine should be created. Default: "eastus"
        :param name: The name of the virtual machine. Default: - Uses the name derived from the construct path.
        :param os_disk: The OS disk configuration for the virtual machine. Default: - Uses a disk with caching set to "ReadWrite" and storage account type "Standard_LRS".
        :param public_ip_allocation_method: The allocation method for the public IP.
        :param resource_group: An optional reference to the resource group in which to deploy the Virtual Machine. If not provided, the Virtual Machine will be deployed in the default resource group.
        :param size: The size of the virtual machine. Default: "Standard_B2s"
        :param source_image_id: The ID of the source image for the virtual machine.
        :param source_image_reference: The source image reference for the virtual machine. Default: - Uses WindowsServer2022DatacenterCore.
        :param subnet: The subnet in which the virtual machine will be placed. Default: - Uses the default subnet from a new virtual network.
        :param tags: Tags to apply to the virtual machine.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc4ad31f1b205600bc2a349d409b5768c7caa371a75834fb6702709fa88f3494)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = WindowsVMProps(
            admin_password=admin_password,
            admin_username=admin_username,
            boostrap_custom_data=boostrap_custom_data,
            boot_diagnostics_storage_uri=boot_diagnostics_storage_uri,
            custom_data=custom_data,
            location=location,
            name=name,
            os_disk=os_disk,
            public_ip_allocation_method=public_ip_allocation_method,
            resource_group=resource_group,
            size=size,
            source_image_id=source_image_id,
            source_image_reference=source_image_reference,
            subnet=subnet,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "WindowsVMProps":
        return typing.cast("WindowsVMProps", jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="publicIp")
    def public_ip(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicIp"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b47a207b1765a3aa336ec4612e50b423d4eb44694227971bffbfca74437aa9de)
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
            type_hints = typing.get_type_hints(_typecheckingstub__33f6db9075a6d9a44f420490ba2399cd34e8e67d1c6f6ae522059159ec0d794e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroup", value)


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_virtualmachine.WindowsVMProps",
    jsii_struct_bases=[],
    name_mapping={
        "admin_password": "adminPassword",
        "admin_username": "adminUsername",
        "boostrap_custom_data": "boostrapCustomData",
        "boot_diagnostics_storage_uri": "bootDiagnosticsStorageURI",
        "custom_data": "customData",
        "location": "location",
        "name": "name",
        "os_disk": "osDisk",
        "public_ip_allocation_method": "publicIPAllocationMethod",
        "resource_group": "resourceGroup",
        "size": "size",
        "source_image_id": "sourceImageId",
        "source_image_reference": "sourceImageReference",
        "subnet": "subnet",
        "tags": "tags",
    },
)
class WindowsVMProps:
    def __init__(
        self,
        *,
        admin_password: builtins.str,
        admin_username: builtins.str,
        boostrap_custom_data: typing.Optional[builtins.str] = None,
        boot_diagnostics_storage_uri: typing.Optional[builtins.str] = None,
        custom_data: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        os_disk: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineOsDisk, typing.Dict[builtins.str, typing.Any]]] = None,
        public_ip_allocation_method: typing.Optional[builtins.str] = None,
        resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
        size: typing.Optional[builtins.str] = None,
        source_image_id: typing.Optional[builtins.str] = None,
        source_image_reference: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference, typing.Dict[builtins.str, typing.Any]]] = None,
        subnet: typing.Optional[_cdktf_cdktf_provider_azurerm_subnet_92bbcedf.Subnet] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param admin_password: The admin password for the virtual machine.
        :param admin_username: The admin username for the virtual machine.
        :param boostrap_custom_data: Custom data to bootstrap the virtual machine. Automatically triggers Azure Custom Script extension to deploy code in custom data.
        :param boot_diagnostics_storage_uri: Bootdiagnostics settings for the VM.
        :param custom_data: Custom data to pass to the virtual machine upon creation.
        :param location: The Azure location where the virtual machine should be created. Default: "eastus"
        :param name: The name of the virtual machine. Default: - Uses the name derived from the construct path.
        :param os_disk: The OS disk configuration for the virtual machine. Default: - Uses a disk with caching set to "ReadWrite" and storage account type "Standard_LRS".
        :param public_ip_allocation_method: The allocation method for the public IP.
        :param resource_group: An optional reference to the resource group in which to deploy the Virtual Machine. If not provided, the Virtual Machine will be deployed in the default resource group.
        :param size: The size of the virtual machine. Default: "Standard_B2s"
        :param source_image_id: The ID of the source image for the virtual machine.
        :param source_image_reference: The source image reference for the virtual machine. Default: - Uses WindowsServer2022DatacenterCore.
        :param subnet: The subnet in which the virtual machine will be placed. Default: - Uses the default subnet from a new virtual network.
        :param tags: Tags to apply to the virtual machine.
        '''
        if isinstance(os_disk, dict):
            os_disk = _cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineOsDisk(**os_disk)
        if isinstance(source_image_reference, dict):
            source_image_reference = _cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference(**source_image_reference)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c829d260403fdd4cef500aeb0808fafc9d26c9425d70d31f1740bccd18470681)
            check_type(argname="argument admin_password", value=admin_password, expected_type=type_hints["admin_password"])
            check_type(argname="argument admin_username", value=admin_username, expected_type=type_hints["admin_username"])
            check_type(argname="argument boostrap_custom_data", value=boostrap_custom_data, expected_type=type_hints["boostrap_custom_data"])
            check_type(argname="argument boot_diagnostics_storage_uri", value=boot_diagnostics_storage_uri, expected_type=type_hints["boot_diagnostics_storage_uri"])
            check_type(argname="argument custom_data", value=custom_data, expected_type=type_hints["custom_data"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument os_disk", value=os_disk, expected_type=type_hints["os_disk"])
            check_type(argname="argument public_ip_allocation_method", value=public_ip_allocation_method, expected_type=type_hints["public_ip_allocation_method"])
            check_type(argname="argument resource_group", value=resource_group, expected_type=type_hints["resource_group"])
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
            check_type(argname="argument source_image_id", value=source_image_id, expected_type=type_hints["source_image_id"])
            check_type(argname="argument source_image_reference", value=source_image_reference, expected_type=type_hints["source_image_reference"])
            check_type(argname="argument subnet", value=subnet, expected_type=type_hints["subnet"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
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
        if location is not None:
            self._values["location"] = location
        if name is not None:
            self._values["name"] = name
        if os_disk is not None:
            self._values["os_disk"] = os_disk
        if public_ip_allocation_method is not None:
            self._values["public_ip_allocation_method"] = public_ip_allocation_method
        if resource_group is not None:
            self._values["resource_group"] = resource_group
        if size is not None:
            self._values["size"] = size
        if source_image_id is not None:
            self._values["source_image_id"] = source_image_id
        if source_image_reference is not None:
            self._values["source_image_reference"] = source_image_reference
        if subnet is not None:
            self._values["subnet"] = subnet
        if tags is not None:
            self._values["tags"] = tags

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
    def public_ip_allocation_method(self) -> typing.Optional[builtins.str]:
        '''The allocation method for the public IP.'''
        result = self._values.get("public_ip_allocation_method")
        return typing.cast(typing.Optional[builtins.str], result)

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
    def size(self) -> typing.Optional[builtins.str]:
        '''The size of the virtual machine.

        :default: "Standard_B2s"
        '''
        result = self._values.get("size")
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

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WindowsVMProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "LinuxImageReferences",
    "LinuxVM",
    "LinuxVMProps",
    "WindowsImageReferences",
    "WindowsVM",
    "WindowsVMProps",
]

publication.publish()

def _typecheckingstub__29a7c8d8f4ade05e5e41d2ccd39372d86d2fa2224109c485bf2f79e84b4836ae(
    value: _cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineSourceImageReference,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5930d1184f218f5a271e84427012d2dbc17809f7422ecce05bf2b3ac575715e(
    value: _cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineSourceImageReference,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__332d98f3e6e5e53589f78bddd78e5ca9dcf43ecf7932ce6bf073b7dfc11ee209(
    value: _cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineSourceImageReference,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf30a5745843a5ebe2e5fdf88ed967b6ea615a6c1cf691bc07b3711445edb237(
    value: _cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineSourceImageReference,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c977d4d4456b47218802aab7d3dd741e65a3c5b0c2772fb3b495a2733bc5209(
    value: _cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineSourceImageReference,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55ae29f90b43e9254f55fda36fb112dacb0a667d26f0ab3e6a15f145f8a2e180(
    value: _cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineSourceImageReference,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4503c856086be09ccd03fad9fec5fa5a06773c3e3cfd91a62ac778582a4b3ada(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    additional_capabilities: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineAdditionalCapabilities, typing.Dict[builtins.str, typing.Any]]] = None,
    admin_password: typing.Optional[builtins.str] = None,
    admin_ssh_key: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineAdminSshKey, typing.Dict[builtins.str, typing.Any]]]]] = None,
    admin_username: typing.Optional[builtins.str] = None,
    availability_set_id: typing.Optional[builtins.str] = None,
    boot_diagnostics_storage_uri: typing.Optional[builtins.str] = None,
    custom_data: typing.Optional[builtins.str] = None,
    enable_ssh_azure_ad_login: typing.Optional[builtins.bool] = None,
    identity: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    location: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    os_disk: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineOsDisk, typing.Dict[builtins.str, typing.Any]]] = None,
    public_ip_allocation_method: typing.Optional[builtins.str] = None,
    resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
    secret: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineSecret, typing.Dict[builtins.str, typing.Any]]]] = None,
    size: typing.Optional[builtins.str] = None,
    source_image_id: typing.Optional[builtins.str] = None,
    source_image_reference: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineSourceImageReference, typing.Dict[builtins.str, typing.Any]]] = None,
    subnet: typing.Optional[_cdktf_cdktf_provider_azurerm_subnet_92bbcedf.Subnet] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    user_data: typing.Optional[builtins.str] = None,
    zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c5f0ee7ea05450a854f9fbb748ea8d4d20d5af57db5caff9ee90994b7c45755(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a57b7d59a91a7d43ceef299ac7a55a7e1c678e52058ec6f6fa9c402e61271919(
    value: _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53d88c32a57de5faac8a76fe382df39f974f727204f91f8ebede45487727829e(
    *,
    additional_capabilities: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineAdditionalCapabilities, typing.Dict[builtins.str, typing.Any]]] = None,
    admin_password: typing.Optional[builtins.str] = None,
    admin_ssh_key: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineAdminSshKey, typing.Dict[builtins.str, typing.Any]]]]] = None,
    admin_username: typing.Optional[builtins.str] = None,
    availability_set_id: typing.Optional[builtins.str] = None,
    boot_diagnostics_storage_uri: typing.Optional[builtins.str] = None,
    custom_data: typing.Optional[builtins.str] = None,
    enable_ssh_azure_ad_login: typing.Optional[builtins.bool] = None,
    identity: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    location: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    os_disk: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineOsDisk, typing.Dict[builtins.str, typing.Any]]] = None,
    public_ip_allocation_method: typing.Optional[builtins.str] = None,
    resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
    secret: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineSecret, typing.Dict[builtins.str, typing.Any]]]] = None,
    size: typing.Optional[builtins.str] = None,
    source_image_id: typing.Optional[builtins.str] = None,
    source_image_reference: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_linux_virtual_machine_92bbcedf.LinuxVirtualMachineSourceImageReference, typing.Dict[builtins.str, typing.Any]]] = None,
    subnet: typing.Optional[_cdktf_cdktf_provider_azurerm_subnet_92bbcedf.Subnet] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    user_data: typing.Optional[builtins.str] = None,
    zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf40c34d0166c0f6bee833b7b61bb742f4f48b90d3e4b3e5eeef1a04db5c4606(
    value: _cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aff3b10fb9bc184f52cf14764691d0c805719c00ccd9637a645f259045085d9(
    value: _cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5ebfee79d399fb0e9a7b8f50006a53381a91211129c2124c0f1ae78ee3dd172(
    value: _cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fb3ea6e310f913788b2dcc3f2798ad0ac7f3162bec92b92c2e0d06399e7c0d0(
    value: _cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab632c1332e6eb149f8379dd60672373b62743d1a44f42fcf20f220c5190cf9b(
    value: _cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cce5ebd44c0d1eb2ecf32b2c12611fe3c6fca269e4b37341c6bb8615d8dd0e3f(
    value: _cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca4185605ed0a1f2183d40eaa7ba6d4284c7431d629b2e82ffb3c7f6822189ef(
    value: _cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f57c5d44eee3ebbd882a61df6189449ceea10f7dd5141cf63bbb84bfa77850d4(
    value: _cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47ebd4045041171630b40321487b500a7da9806e4f60bdfe7b79957dd3a12e64(
    value: _cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e56057d4d440886628ab2559209f143dd2c88e7da105be6d2a71911f212b8e6(
    value: _cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc4ad31f1b205600bc2a349d409b5768c7caa371a75834fb6702709fa88f3494(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    admin_password: builtins.str,
    admin_username: builtins.str,
    boostrap_custom_data: typing.Optional[builtins.str] = None,
    boot_diagnostics_storage_uri: typing.Optional[builtins.str] = None,
    custom_data: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    os_disk: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineOsDisk, typing.Dict[builtins.str, typing.Any]]] = None,
    public_ip_allocation_method: typing.Optional[builtins.str] = None,
    resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
    size: typing.Optional[builtins.str] = None,
    source_image_id: typing.Optional[builtins.str] = None,
    source_image_reference: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference, typing.Dict[builtins.str, typing.Any]]] = None,
    subnet: typing.Optional[_cdktf_cdktf_provider_azurerm_subnet_92bbcedf.Subnet] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b47a207b1765a3aa336ec4612e50b423d4eb44694227971bffbfca74437aa9de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33f6db9075a6d9a44f420490ba2399cd34e8e67d1c6f6ae522059159ec0d794e(
    value: _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c829d260403fdd4cef500aeb0808fafc9d26c9425d70d31f1740bccd18470681(
    *,
    admin_password: builtins.str,
    admin_username: builtins.str,
    boostrap_custom_data: typing.Optional[builtins.str] = None,
    boot_diagnostics_storage_uri: typing.Optional[builtins.str] = None,
    custom_data: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    os_disk: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineOsDisk, typing.Dict[builtins.str, typing.Any]]] = None,
    public_ip_allocation_method: typing.Optional[builtins.str] = None,
    resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
    size: typing.Optional[builtins.str] = None,
    source_image_id: typing.Optional[builtins.str] = None,
    source_image_reference: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_windows_virtual_machine_92bbcedf.WindowsVirtualMachineSourceImageReference, typing.Dict[builtins.str, typing.Any]]] = None,
    subnet: typing.Optional[_cdktf_cdktf_provider_azurerm_subnet_92bbcedf.Subnet] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
