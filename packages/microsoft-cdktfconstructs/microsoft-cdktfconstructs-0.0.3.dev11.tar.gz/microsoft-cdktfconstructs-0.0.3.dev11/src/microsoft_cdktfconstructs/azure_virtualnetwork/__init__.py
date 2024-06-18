'''
# Azure Virtual Network Construct

This class represents an Azure Virtual Network. It provides a convenient way to manage Azure Virtual Networks and their associated subnets.

## What is an Azure Virtual Network?

Azure Virtual Network (VNet) is the fundamental building block for your private network in Azure. VNet enables many types of Azure resources, such as Azure Virtual Machines (VM), to securely communicate with each other, the internet, and on-premises networks. VNet is similar to a traditional network that you'd operate in your own data center but brings with it additional benefits of Azure's infrastructure.

[Learn more about Azure Virtual Network](https://docs.microsoft.com/en-us/azure/virtual-network/virtual-networks-overview).

## Azure Virtual Network Best Practices

* Design your VNets with multiple subnets for better segmentation.
* Avoid overlapping IP address ranges with your on-premises network space.
* Use Network Security Groups (NSGs) to control inbound and outbound traffic to network interfaces (NIC), VMs, and subnets.
* Implement VNet peering for efficient and secure communication between VNets.
* Regularly audit and monitor network resources using Azure Monitor and Network Watcher.

## Azure Virtual Network Class Properties

This class has several properties that control the Azure Virtual Network's behavior:

* `resourceGroupName`: The name of the Azure Resource Group.
* `name`: The name of the Virtual Network.
* `location`: The Azure Region where the Virtual Network will be deployed.
* `addressSpace`: The IP address ranges for the VNet.
* `subnets`: An array of subnet configurations, each having a `name` and `addressPrefixes`.
* `id`: The unique identifier of the Virtual Network.
* `virtualNetwork`: The underlying Virtual Network resource.

## Deploying the Azure Virtual Network

You can deploy an Azure Virtual Network using this class like so:

```python
const azureVNet = new AzureVirtualNetwork(this, 'myVNet', {
  resourceGroupName: 'myResourceGroup',
  name: 'myVNet',
  location: 'East US',
  addressSpace: ['10.0.0.0/16'],
  subnets: [
    {
      name: 'default',
      addressPrefixes: ['10.0.1.0/24'],
    },
  ],
});
```

This code will create a new Azure Virtual Network named myVNet in the East US Azure region with a specified address space. The VNet belongs to the resource group myResourceGroup and contains a subnet named default.

## VNet Peering

VNet peering allows for a direct network connection between two VNets in the same region. This class provides a method addVnetPeering to establish a peering connection between two VNets.

Example:

```python
Copy code
const remoteVNet = new AzureVirtualNetwork(this, 'remoteVNet', { /* ... */ });
azureVNet.addVnetPeering(remoteVNet);
```

This code establishes a peering connection between `myVNet` and `remoteVNet`.

## Cost Optimization

In Azure Virtual Network, you are primarily charged based on the amount of data transferred out of the VNet. Ensure that you're only allowing necessary traffic and consider using VNet peering instead of VPNs or ExpressRoute for communication between VNets in the same region to reduce costs. Regularly review and clean up unused or unnecessary resources.
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
import cdktf_cdktf_provider_azurerm.subnet as _cdktf_cdktf_provider_azurerm_subnet_92bbcedf
import cdktf_cdktf_provider_azurerm.virtual_network as _cdktf_cdktf_provider_azurerm_virtual_network_92bbcedf
import constructs as _constructs_77d1e7e8
from ..core_azure import AzureResource as _AzureResource_74eec1c4


class Network(
    _AzureResource_74eec1c4,
    metaclass=jsii.JSIIMeta,
    jsii_type="@microsoft/terraform-cdk-constructs.azure_virtualnetwork.Network",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        address_space: typing.Optional[typing.Sequence[builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
        subnets: typing.Optional[typing.Sequence[typing.Union["SubnetConfig", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Represents an Azure Virtual Network (VNet) within Microsoft Azure.

        This class is responsible for the creation and management of a virtual network, which provides an isolated environment
        where Azure resources, such as VMs and databases, can securely communicate with each other, the internet, and on-premises
        networks. It supports configurations such as multiple address spaces and subnets, enabling complex networking scenarios.

        :param scope: - The scope in which to define this construct, typically representing the Cloud Development Kit (CDK) application.
        :param id: - The unique identifier for this instance of the network, used within the scope for reference.
        :param address_space: Optional: A list of address spaces for the virtual network, specified in CIDR notation. For example, ['10.0.0.0/16'] defines a single address space. Multiple address spaces can be provided.
        :param location: Optional: The Azure region in which to create the virtual network, e.g., 'East US', 'West Europe'. If not specified, the region of the resource group will be used.
        :param name: Optional: The name of the virtual network. Must be unique within the resource group. If not provided, a default name will be assigned.
        :param resource_group: An optional reference to the resource group in which to deploy the Virtual Machine. If not provided, the Virtual Machine will be deployed in the default resource group.
        :param subnets: Optional: An array of subnet configurations to be created within the virtual network. Each subnet is defined by its name and address prefix(es).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f12f6d137e512786fc356d6d64f71bd6d13a1ecf2ada88bd3d790a65643b2a85)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = NetworkProps(
            address_space=address_space,
            location=location,
            name=name,
            resource_group=resource_group,
            subnets=subnets,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addVnetPeering")
    def add_vnet_peering(
        self,
        remote_virtual_network: "Network",
        local_peer_settings: typing.Optional[typing.Union["PeerSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        *,
        allow_forwarded_traffic: typing.Optional[builtins.bool] = None,
        allow_gateway_transit: typing.Optional[builtins.bool] = None,
        allow_virtual_network_access: typing.Optional[builtins.bool] = None,
        use_remote_gateways: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Establishes a peering connection between this virtual network and another remote virtual network.

        This method configures a two-way peering connection, allowing resources in both virtual networks to communicate
        seamlessly. It sets up peering settings such as network access, traffic forwarding, and gateway transit based on
        provided configurations.

        :param remote_virtual_network: - The remote virtual network with which to establish a peering connection.
        :param local_peer_settings: - Optional settings applied from this virtual network to the remote virtual network. Controls aspects like virtual network access, traffic forwarding, and use of gateways.
        :param allow_forwarded_traffic: Indicates whether forwarded traffic is allowed. Default: false
        :param allow_gateway_transit: Indicates whether gateway transit is allowed. Default: false
        :param allow_virtual_network_access: Indicates whether virtual network access is allowed. Default: true
        :param use_remote_gateways: Indicates whether to use remote gateways. Default: false
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b7b6ffdbc955084b0c25267f2fea44562735436ef7fae193a495babd8c20ba2)
            check_type(argname="argument remote_virtual_network", value=remote_virtual_network, expected_type=type_hints["remote_virtual_network"])
            check_type(argname="argument local_peer_settings", value=local_peer_settings, expected_type=type_hints["local_peer_settings"])
        remote_peer_settings = PeerSettings(
            allow_forwarded_traffic=allow_forwarded_traffic,
            allow_gateway_transit=allow_gateway_transit,
            allow_virtual_network_access=allow_virtual_network_access,
            use_remote_gateways=use_remote_gateways,
        )

        return typing.cast(None, jsii.invoke(self, "addVnetPeering", [remote_virtual_network, local_peer_settings, remote_peer_settings]))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "NetworkProps":
        return typing.cast("NetworkProps", jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="subnets")
    def subnets(
        self,
    ) -> typing.Mapping[builtins.str, _cdktf_cdktf_provider_azurerm_subnet_92bbcedf.Subnet]:
        return typing.cast(typing.Mapping[builtins.str, _cdktf_cdktf_provider_azurerm_subnet_92bbcedf.Subnet], jsii.get(self, "subnets"))

    @builtins.property
    @jsii.member(jsii_name="virtualNetwork")
    def virtual_network(
        self,
    ) -> _cdktf_cdktf_provider_azurerm_virtual_network_92bbcedf.VirtualNetwork:
        return typing.cast(_cdktf_cdktf_provider_azurerm_virtual_network_92bbcedf.VirtualNetwork, jsii.get(self, "virtualNetwork"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d96a48bce2dbc238b2b7fb010fbca63fe89a92932546b56b0209cadebb00307)
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
            type_hints = typing.get_type_hints(_typecheckingstub__691197cdcd375f4b7dca5e7cfa0b25bc7aaf2a593b9629e029b874c7a8228b36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroup", value)


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_virtualnetwork.NetworkProps",
    jsii_struct_bases=[],
    name_mapping={
        "address_space": "addressSpace",
        "location": "location",
        "name": "name",
        "resource_group": "resourceGroup",
        "subnets": "subnets",
    },
)
class NetworkProps:
    def __init__(
        self,
        *,
        address_space: typing.Optional[typing.Sequence[builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
        subnets: typing.Optional[typing.Sequence[typing.Union["SubnetConfig", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining an Azure Virtual Network.

        :param address_space: Optional: A list of address spaces for the virtual network, specified in CIDR notation. For example, ['10.0.0.0/16'] defines a single address space. Multiple address spaces can be provided.
        :param location: Optional: The Azure region in which to create the virtual network, e.g., 'East US', 'West Europe'. If not specified, the region of the resource group will be used.
        :param name: Optional: The name of the virtual network. Must be unique within the resource group. If not provided, a default name will be assigned.
        :param resource_group: An optional reference to the resource group in which to deploy the Virtual Machine. If not provided, the Virtual Machine will be deployed in the default resource group.
        :param subnets: Optional: An array of subnet configurations to be created within the virtual network. Each subnet is defined by its name and address prefix(es).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b227c2fa6df9f699d5d59f289620a8e4da459aa770f81b9d9df0a384aec9001)
            check_type(argname="argument address_space", value=address_space, expected_type=type_hints["address_space"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group", value=resource_group, expected_type=type_hints["resource_group"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if address_space is not None:
            self._values["address_space"] = address_space
        if location is not None:
            self._values["location"] = location
        if name is not None:
            self._values["name"] = name
        if resource_group is not None:
            self._values["resource_group"] = resource_group
        if subnets is not None:
            self._values["subnets"] = subnets

    @builtins.property
    def address_space(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional: A list of address spaces for the virtual network, specified in CIDR notation.

        For example, ['10.0.0.0/16'] defines a single address space. Multiple address spaces can be provided.
        '''
        result = self._values.get("address_space")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''Optional: The Azure region in which to create the virtual network, e.g., 'East US', 'West Europe'. If not specified, the region of the resource group will be used.'''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Optional: The name of the virtual network.

        Must be unique within the resource group.
        If not provided, a default name will be assigned.
        '''
        result = self._values.get("name")
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
    def subnets(self) -> typing.Optional[typing.List["SubnetConfig"]]:
        '''Optional: An array of subnet configurations to be created within the virtual network.

        Each subnet is defined by its name and address prefix(es).
        '''
        result = self._values.get("subnets")
        return typing.cast(typing.Optional[typing.List["SubnetConfig"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Peer(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@microsoft/terraform-cdk-constructs.azure_virtualnetwork.Peer",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        name: builtins.str,
        *,
        remote_virtual_network: Network,
        virtual_network: Network,
        local_to_remote_settings: typing.Optional[typing.Union["PeerSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        remote_to_local_settings: typing.Optional[typing.Union["PeerSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Represents a Virtual Network Peering within Microsoft Azure.

        This class facilitates the peering between two virtual networks, allowing resources in either network to communicate
        with each other as if they were within the same network. It supports advanced configurations such as traffic forwarding,
        gateway transit, and access settings. This peering does not require a VPN gateway and offers low-latency, high-bandwidth
        connections between resources in different virtual networks.

        :param scope: - The scope in which to define this construct, typically representing the Cloud Development Kit (CDK) application.
        :param name: - The unique name for this instance of the network peering.
        :param remote_virtual_network: ID of the remote virtual network.
        :param virtual_network: ID of the local virtual network.
        :param local_to_remote_settings: Settings applied from the local virtual network to the remote virtual network.
        :param remote_to_local_settings: Settings applied from the remote virtual network to the local virtual network.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3243d18717ecdd159fab2cf0794b605b3b005ba5a198d8a267206e36d1767832)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        props = PeerProps(
            remote_virtual_network=remote_virtual_network,
            virtual_network=virtual_network,
            local_to_remote_settings=local_to_remote_settings,
            remote_to_local_settings=remote_to_local_settings,
        )

        jsii.create(self.__class__, self, [scope, name, props])


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_virtualnetwork.PeerProps",
    jsii_struct_bases=[],
    name_mapping={
        "remote_virtual_network": "remoteVirtualNetwork",
        "virtual_network": "virtualNetwork",
        "local_to_remote_settings": "localToRemoteSettings",
        "remote_to_local_settings": "remoteToLocalSettings",
    },
)
class PeerProps:
    def __init__(
        self,
        *,
        remote_virtual_network: Network,
        virtual_network: Network,
        local_to_remote_settings: typing.Optional[typing.Union["PeerSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        remote_to_local_settings: typing.Optional[typing.Union["PeerSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Interface defining the properties for virtual network peerings.

        :param remote_virtual_network: ID of the remote virtual network.
        :param virtual_network: ID of the local virtual network.
        :param local_to_remote_settings: Settings applied from the local virtual network to the remote virtual network.
        :param remote_to_local_settings: Settings applied from the remote virtual network to the local virtual network.
        '''
        if isinstance(local_to_remote_settings, dict):
            local_to_remote_settings = PeerSettings(**local_to_remote_settings)
        if isinstance(remote_to_local_settings, dict):
            remote_to_local_settings = PeerSettings(**remote_to_local_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__268f114fde1ea8d5558e85dc220bec35ed90da33cc7d10b5b07b4eac897da40d)
            check_type(argname="argument remote_virtual_network", value=remote_virtual_network, expected_type=type_hints["remote_virtual_network"])
            check_type(argname="argument virtual_network", value=virtual_network, expected_type=type_hints["virtual_network"])
            check_type(argname="argument local_to_remote_settings", value=local_to_remote_settings, expected_type=type_hints["local_to_remote_settings"])
            check_type(argname="argument remote_to_local_settings", value=remote_to_local_settings, expected_type=type_hints["remote_to_local_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "remote_virtual_network": remote_virtual_network,
            "virtual_network": virtual_network,
        }
        if local_to_remote_settings is not None:
            self._values["local_to_remote_settings"] = local_to_remote_settings
        if remote_to_local_settings is not None:
            self._values["remote_to_local_settings"] = remote_to_local_settings

    @builtins.property
    def remote_virtual_network(self) -> Network:
        '''ID of the remote virtual network.'''
        result = self._values.get("remote_virtual_network")
        assert result is not None, "Required property 'remote_virtual_network' is missing"
        return typing.cast(Network, result)

    @builtins.property
    def virtual_network(self) -> Network:
        '''ID of the local virtual network.'''
        result = self._values.get("virtual_network")
        assert result is not None, "Required property 'virtual_network' is missing"
        return typing.cast(Network, result)

    @builtins.property
    def local_to_remote_settings(self) -> typing.Optional["PeerSettings"]:
        '''Settings applied from the local virtual network to the remote virtual network.'''
        result = self._values.get("local_to_remote_settings")
        return typing.cast(typing.Optional["PeerSettings"], result)

    @builtins.property
    def remote_to_local_settings(self) -> typing.Optional["PeerSettings"]:
        '''Settings applied from the remote virtual network to the local virtual network.'''
        result = self._values.get("remote_to_local_settings")
        return typing.cast(typing.Optional["PeerSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PeerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_virtualnetwork.PeerSettings",
    jsii_struct_bases=[],
    name_mapping={
        "allow_forwarded_traffic": "allowForwardedTraffic",
        "allow_gateway_transit": "allowGatewayTransit",
        "allow_virtual_network_access": "allowVirtualNetworkAccess",
        "use_remote_gateways": "useRemoteGateways",
    },
)
class PeerSettings:
    def __init__(
        self,
        *,
        allow_forwarded_traffic: typing.Optional[builtins.bool] = None,
        allow_gateway_transit: typing.Optional[builtins.bool] = None,
        allow_virtual_network_access: typing.Optional[builtins.bool] = None,
        use_remote_gateways: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Interface defining the settings for peer connections.

        :param allow_forwarded_traffic: Indicates whether forwarded traffic is allowed. Default: false
        :param allow_gateway_transit: Indicates whether gateway transit is allowed. Default: false
        :param allow_virtual_network_access: Indicates whether virtual network access is allowed. Default: true
        :param use_remote_gateways: Indicates whether to use remote gateways. Default: false
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d66255415e32311b477482b9cc3c147cec3fefee6711ca54bd422c735b625d5)
            check_type(argname="argument allow_forwarded_traffic", value=allow_forwarded_traffic, expected_type=type_hints["allow_forwarded_traffic"])
            check_type(argname="argument allow_gateway_transit", value=allow_gateway_transit, expected_type=type_hints["allow_gateway_transit"])
            check_type(argname="argument allow_virtual_network_access", value=allow_virtual_network_access, expected_type=type_hints["allow_virtual_network_access"])
            check_type(argname="argument use_remote_gateways", value=use_remote_gateways, expected_type=type_hints["use_remote_gateways"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_forwarded_traffic is not None:
            self._values["allow_forwarded_traffic"] = allow_forwarded_traffic
        if allow_gateway_transit is not None:
            self._values["allow_gateway_transit"] = allow_gateway_transit
        if allow_virtual_network_access is not None:
            self._values["allow_virtual_network_access"] = allow_virtual_network_access
        if use_remote_gateways is not None:
            self._values["use_remote_gateways"] = use_remote_gateways

    @builtins.property
    def allow_forwarded_traffic(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether forwarded traffic is allowed.

        :default: false
        '''
        result = self._values.get("allow_forwarded_traffic")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def allow_gateway_transit(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether gateway transit is allowed.

        :default: false
        '''
        result = self._values.get("allow_gateway_transit")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def allow_virtual_network_access(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether virtual network access is allowed.

        :default: true
        '''
        result = self._values.get("allow_virtual_network_access")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def use_remote_gateways(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether to use remote gateways.

        :default: false
        '''
        result = self._values.get("use_remote_gateways")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PeerSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_virtualnetwork.SubnetConfig",
    jsii_struct_bases=[],
    name_mapping={"address_prefixes": "addressPrefixes", "name": "name"},
)
class SubnetConfig:
    def __init__(
        self,
        *,
        address_prefixes: typing.Sequence[builtins.str],
        name: builtins.str,
    ) -> None:
        '''Configuration properties for defining a subnet within an Azure Virtual Network.

        :param address_prefixes: A list of address prefixes for the subnet. These are expressed in CIDR notation. For example, '192.168.1.0/24' to define a subnet with a range of IP addresses.
        :param name: The name of the subnet. This name must be unique within the context of the virtual network.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65e41345078d26347338a20a67caf2c5f80cc72e44fdc171f1455eb58c00fa66)
            check_type(argname="argument address_prefixes", value=address_prefixes, expected_type=type_hints["address_prefixes"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "address_prefixes": address_prefixes,
            "name": name,
        }

    @builtins.property
    def address_prefixes(self) -> typing.List[builtins.str]:
        '''A list of address prefixes for the subnet.

        These are expressed in CIDR notation.
        For example, '192.168.1.0/24' to define a subnet with a range of IP addresses.
        '''
        result = self._values.get("address_prefixes")
        assert result is not None, "Required property 'address_prefixes' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the subnet.

        This name must be unique within the context of the virtual network.
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SubnetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Network",
    "NetworkProps",
    "Peer",
    "PeerProps",
    "PeerSettings",
    "SubnetConfig",
]

publication.publish()

def _typecheckingstub__f12f6d137e512786fc356d6d64f71bd6d13a1ecf2ada88bd3d790a65643b2a85(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    address_space: typing.Optional[typing.Sequence[builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
    subnets: typing.Optional[typing.Sequence[typing.Union[SubnetConfig, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b7b6ffdbc955084b0c25267f2fea44562735436ef7fae193a495babd8c20ba2(
    remote_virtual_network: Network,
    local_peer_settings: typing.Optional[typing.Union[PeerSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    *,
    allow_forwarded_traffic: typing.Optional[builtins.bool] = None,
    allow_gateway_transit: typing.Optional[builtins.bool] = None,
    allow_virtual_network_access: typing.Optional[builtins.bool] = None,
    use_remote_gateways: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d96a48bce2dbc238b2b7fb010fbca63fe89a92932546b56b0209cadebb00307(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__691197cdcd375f4b7dca5e7cfa0b25bc7aaf2a593b9629e029b874c7a8228b36(
    value: _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b227c2fa6df9f699d5d59f289620a8e4da459aa770f81b9d9df0a384aec9001(
    *,
    address_space: typing.Optional[typing.Sequence[builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
    subnets: typing.Optional[typing.Sequence[typing.Union[SubnetConfig, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3243d18717ecdd159fab2cf0794b605b3b005ba5a198d8a267206e36d1767832(
    scope: _constructs_77d1e7e8.Construct,
    name: builtins.str,
    *,
    remote_virtual_network: Network,
    virtual_network: Network,
    local_to_remote_settings: typing.Optional[typing.Union[PeerSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    remote_to_local_settings: typing.Optional[typing.Union[PeerSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__268f114fde1ea8d5558e85dc220bec35ed90da33cc7d10b5b07b4eac897da40d(
    *,
    remote_virtual_network: Network,
    virtual_network: Network,
    local_to_remote_settings: typing.Optional[typing.Union[PeerSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    remote_to_local_settings: typing.Optional[typing.Union[PeerSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d66255415e32311b477482b9cc3c147cec3fefee6711ca54bd422c735b625d5(
    *,
    allow_forwarded_traffic: typing.Optional[builtins.bool] = None,
    allow_gateway_transit: typing.Optional[builtins.bool] = None,
    allow_virtual_network_access: typing.Optional[builtins.bool] = None,
    use_remote_gateways: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65e41345078d26347338a20a67caf2c5f80cc72e44fdc171f1455eb58c00fa66(
    *,
    address_prefixes: typing.Sequence[builtins.str],
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
