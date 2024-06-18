'''
# Azure Network Security Group Construct

This class represents an Azure Network Security Group. It provides a convenient way to manage Azure Network Security Groups and their associated rules and associations.

## What is an Azure Network Security Group?

Azure Network Security Group (NSG) is a feature in Azure that allows you to filter network traffic to and from Azure resources in an Azure virtual network. NSGs can be associated with subnets or individual network interfaces attached to virtual machines.

You can learn more about Azure Network Security Groups in the [official Azure documentation](https://docs.microsoft.com/en-us/azure/virtual-network/security-overview).

## Azure Network Security Group Best Practices

* Use NSGs to restrict traffic to the minimal required for your application.
* Avoid overlapping security rules that can cause confusion.
* Use named security rules for clarity.
* Regularly review and update your NSG rules.
* Use Application Security Groups (ASGs) to group virtual machines and define network security policies based on those groups.

## Azure Network Security Group Class Properties

This class has several properties that control the Azure Network Security Group's behaviour:

* `props`: Properties of the Azure Network Security Group.
* `id`: Unique identifier of the Network Security Group.
* `name`: Name of the Network Security Group.

## Deploying the Azure Network Security Group

You can deploy an Azure Network Security Group using this class like so:

```python
const azureNSG = new AzureNetworkSecurityGroup(this, 'myNSG', {
  resourceGroupName: 'myResourceGroup',
  location: 'West US',
  name: 'myNSG',
  rules: [...], // Define your rules here
});
```

This code will create a new Azure Network Security Group named myNSG in the West US Azure region. The NSG belongs to the resource group myResourceGroup and contains the specified security rules.

## Security Considerations

In Azure Network Security Groups, it's essential to ensure that you're not inadvertently allowing unwanted traffic. Always follow the principle of least privilege – only allow traffic that is explicitly required. Regularly review and audit your NSG rules to ensure they remain relevant and secure.
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

import cdktf_cdktf_provider_azurerm.network_interface as _cdktf_cdktf_provider_azurerm_network_interface_92bbcedf
import cdktf_cdktf_provider_azurerm.resource_group as _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf
import cdktf_cdktf_provider_azurerm.subnet as _cdktf_cdktf_provider_azurerm_subnet_92bbcedf
import constructs as _constructs_77d1e7e8
from ..core_azure import AzureResource as _AzureResource_74eec1c4


class PreconfiguredRules(
    metaclass=jsii.JSIIMeta,
    jsii_type="@microsoft/terraform-cdk-constructs.azure_networksecuritygroup.PreconfiguredRules",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="addDestinationAddress")
    @builtins.classmethod
    def add_destination_address(
        cls,
        rule: typing.Union["RuleConfig", typing.Dict[builtins.str, typing.Any]],
        destination_address_prefix: builtins.str,
    ) -> "RuleConfig":
        '''
        :param rule: -
        :param destination_address_prefix: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36828755c5b4c1e8159d75a5791196dbe984738537aa216471a1af45feecc05d)
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
            check_type(argname="argument destination_address_prefix", value=destination_address_prefix, expected_type=type_hints["destination_address_prefix"])
        return typing.cast("RuleConfig", jsii.sinvoke(cls, "addDestinationAddress", [rule, destination_address_prefix]))

    @jsii.member(jsii_name="addPriority")
    @builtins.classmethod
    def add_priority(
        cls,
        rule: typing.Union["RuleConfig", typing.Dict[builtins.str, typing.Any]],
        priority: jsii.Number,
    ) -> "RuleConfig":
        '''
        :param rule: -
        :param priority: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5047f03b32af36e495107644a1cca8ef3f5685f6440fb5594b8c4e9da8fac527)
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
        return typing.cast("RuleConfig", jsii.sinvoke(cls, "addPriority", [rule, priority]))

    @jsii.member(jsii_name="addSourceAddress")
    @builtins.classmethod
    def add_source_address(
        cls,
        rule: typing.Union["RuleConfig", typing.Dict[builtins.str, typing.Any]],
        source_address_prefix: builtins.str,
    ) -> "RuleConfig":
        '''
        :param rule: -
        :param source_address_prefix: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__380230cfd2bf19b7b486337feed1a961cec154d093a50410318ae6f069c3c07d)
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
            check_type(argname="argument source_address_prefix", value=source_address_prefix, expected_type=type_hints["source_address_prefix"])
        return typing.cast("RuleConfig", jsii.sinvoke(cls, "addSourceAddress", [rule, source_address_prefix]))

    @jsii.member(jsii_name="applyRuleOverrides")
    @builtins.classmethod
    def apply_rule_overrides(
        cls,
        base_rule: typing.Union["RuleConfig", typing.Dict[builtins.str, typing.Any]],
        *,
        destination_address_prefix: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        source_address_prefix: typing.Optional[builtins.str] = None,
    ) -> "RuleConfig":
        '''
        :param base_rule: -
        :param destination_address_prefix: Optional destination address prefix to be matched for the rule. Similar to the source address prefix, this can be a specific IP address or a range. If not provided, it defaults to matching any destination address.
        :param priority: Optional priority for the rule. Rules are processed in the order of their priority, with lower numbers processed before higher numbers. If not provided, a default priority will be assigned.
        :param source_address_prefix: Optional source address prefix to be matched for the rule. This can be an IP address or a range of IP addresses. If not specified, the default behavior is to match any source address.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f7fa8ff8e816697bfed79efeb582a0a3d5959f3568e35df3423eb7a9afd975e)
            check_type(argname="argument base_rule", value=base_rule, expected_type=type_hints["base_rule"])
        overrides = RuleOverrides(
            destination_address_prefix=destination_address_prefix,
            priority=priority,
            source_address_prefix=source_address_prefix,
        )

        return typing.cast("RuleConfig", jsii.sinvoke(cls, "applyRuleOverrides", [base_rule, overrides]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="activeDirectoryAllowADDSWebServices")
    def active_directory_allow_adds_web_services(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "activeDirectoryAllowADDSWebServices"))

    @active_directory_allow_adds_web_services.setter # type: ignore[no-redef]
    def active_directory_allow_adds_web_services(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__428dbd0c13493fc0e286f68339632262ddbbce1720cc3e20f23fde221976c2ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "activeDirectoryAllowADDSWebServices", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="activeDirectoryAllowADGCReplication")
    def active_directory_allow_adgc_replication(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "activeDirectoryAllowADGCReplication"))

    @active_directory_allow_adgc_replication.setter # type: ignore[no-redef]
    def active_directory_allow_adgc_replication(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5abd3e7641c842e5e9a5a14e677aa271ce51d2e2ee02a0b9f1eda7c7a932993)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "activeDirectoryAllowADGCReplication", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="activeDirectoryAllowADGCReplicationSSL")
    def active_directory_allow_adgc_replication_ssl(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "activeDirectoryAllowADGCReplicationSSL"))

    @active_directory_allow_adgc_replication_ssl.setter # type: ignore[no-redef]
    def active_directory_allow_adgc_replication_ssl(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d8f1ccf57bc1e925a8d384f8ffdc24be8d843c10da95b29ada00685a8906004)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "activeDirectoryAllowADGCReplicationSSL", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="activeDirectoryAllowADReplication")
    def active_directory_allow_ad_replication(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "activeDirectoryAllowADReplication"))

    @active_directory_allow_ad_replication.setter # type: ignore[no-redef]
    def active_directory_allow_ad_replication(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7274ca46989376e017367f8eea4daf57323cbfc5b5dd4fde03064dcf182866fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "activeDirectoryAllowADReplication", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="activeDirectoryAllowADReplicationSSL")
    def active_directory_allow_ad_replication_ssl(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "activeDirectoryAllowADReplicationSSL"))

    @active_directory_allow_ad_replication_ssl.setter # type: ignore[no-redef]
    def active_directory_allow_ad_replication_ssl(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a576f2d388842b9d27aba4477ce3b42e1f5dddf49e3e3c9e9bcafb6ebc72235)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "activeDirectoryAllowADReplicationSSL", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="activeDirectoryAllowADReplicationTrust")
    def active_directory_allow_ad_replication_trust(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "activeDirectoryAllowADReplicationTrust"))

    @active_directory_allow_ad_replication_trust.setter # type: ignore[no-redef]
    def active_directory_allow_ad_replication_trust(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0bc577ddca27fe23efab210d6e0a9e0650c7eaeb5611b2acd8c793c5701a753)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "activeDirectoryAllowADReplicationTrust", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="activeDirectoryAllowDFSGroupPolicy")
    def active_directory_allow_dfs_group_policy(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "activeDirectoryAllowDFSGroupPolicy"))

    @active_directory_allow_dfs_group_policy.setter # type: ignore[no-redef]
    def active_directory_allow_dfs_group_policy(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d09b9850fb411ed4831ffca866e06c4331fb796968850a0acacb5442ec49469)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "activeDirectoryAllowDFSGroupPolicy", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="activeDirectoryAllowDNS")
    def active_directory_allow_dns(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "activeDirectoryAllowDNS"))

    @active_directory_allow_dns.setter # type: ignore[no-redef]
    def active_directory_allow_dns(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5af60cd8933cc2c05423257643cdcf293dd3757574d3043c20cd31a472f5620)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "activeDirectoryAllowDNS", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="activeDirectoryAllowFileReplication")
    def active_directory_allow_file_replication(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "activeDirectoryAllowFileReplication"))

    @active_directory_allow_file_replication.setter # type: ignore[no-redef]
    def active_directory_allow_file_replication(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b171e6d47709b8132a24a97da7d017b8d1751629bb9e51863a89461f53b3d4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "activeDirectoryAllowFileReplication", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="activeDirectoryAllowKerberosAuthentication")
    def active_directory_allow_kerberos_authentication(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "activeDirectoryAllowKerberosAuthentication"))

    @active_directory_allow_kerberos_authentication.setter # type: ignore[no-redef]
    def active_directory_allow_kerberos_authentication(
        cls,
        value: "RuleConfig",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e8794392c6432472a6b30efd2e4b5779aa5c3aa94a4ffaefc35fa6a434df62d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "activeDirectoryAllowKerberosAuthentication", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="activeDirectoryAllowNETBIOSAuthentication")
    def active_directory_allow_netbios_authentication(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "activeDirectoryAllowNETBIOSAuthentication"))

    @active_directory_allow_netbios_authentication.setter # type: ignore[no-redef]
    def active_directory_allow_netbios_authentication(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__931d4418249ac4993f526a0f267e88e8b9117cbc8a1eb53dc22d13f6f9dcf30b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "activeDirectoryAllowNETBIOSAuthentication", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="activeDirectoryAllowNETBIOSReplication")
    def active_directory_allow_netbios_replication(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "activeDirectoryAllowNETBIOSReplication"))

    @active_directory_allow_netbios_replication.setter # type: ignore[no-redef]
    def active_directory_allow_netbios_replication(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b4a15df9f07baaeec11fa5e27f6363014b619931162d24d3c06da60d3bd791a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "activeDirectoryAllowNETBIOSReplication", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="activeDirectoryAllowPasswordChangeKerberes")
    def active_directory_allow_password_change_kerberes(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "activeDirectoryAllowPasswordChangeKerberes"))

    @active_directory_allow_password_change_kerberes.setter # type: ignore[no-redef]
    def active_directory_allow_password_change_kerberes(
        cls,
        value: "RuleConfig",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d4106eaa46732da846afdc98b2dac21fdd385660c8090177e8252c48e8d839b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "activeDirectoryAllowPasswordChangeKerberes", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="activeDirectoryAllowRPCReplication")
    def active_directory_allow_rpc_replication(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "activeDirectoryAllowRPCReplication"))

    @active_directory_allow_rpc_replication.setter # type: ignore[no-redef]
    def active_directory_allow_rpc_replication(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__799bd466f4976406d080d7d848270f33f8f35833d2783953465125a108780a00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "activeDirectoryAllowRPCReplication", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="activeDirectoryAllowSMTPReplication")
    def active_directory_allow_smtp_replication(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "activeDirectoryAllowSMTPReplication"))

    @active_directory_allow_smtp_replication.setter # type: ignore[no-redef]
    def active_directory_allow_smtp_replication(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__286a9dbad6ec5bbf7414e63969dec5cb59ca47b52197452b70b51fafa181d08f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "activeDirectoryAllowSMTPReplication", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="activeDirectoryAllowWindowsTime")
    def active_directory_allow_windows_time(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "activeDirectoryAllowWindowsTime"))

    @active_directory_allow_windows_time.setter # type: ignore[no-redef]
    def active_directory_allow_windows_time(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66bff9971afcefaf5f92d772e054e0149616b70bc27bc93692a95e13a570a998)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "activeDirectoryAllowWindowsTime", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="cassandra")
    def cassandra(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "cassandra"))

    @cassandra.setter # type: ignore[no-redef]
    def cassandra(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8506559ba4cf5d3e3d387692f33e7ec9bf02e3b064e2a5ccb33db5745849e6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "cassandra", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="cassandraJmx")
    def cassandra_jmx(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "cassandraJmx"))

    @cassandra_jmx.setter # type: ignore[no-redef]
    def cassandra_jmx(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ce0a5c999b498f7a6fb7e853fe1f904c2b3bf8862be5ede1625c27242145473)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "cassandraJmx", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="cassandraThrift")
    def cassandra_thrift(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "cassandraThrift"))

    @cassandra_thrift.setter # type: ignore[no-redef]
    def cassandra_thrift(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cedddad1428ac3deb46d7311e21c459c6cd3b46ff7ab1a2d09934a78eba5703)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "cassandraThrift", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="couchDb")
    def couch_db(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "couchDb"))

    @couch_db.setter # type: ignore[no-redef]
    def couch_db(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48852d8760d119fcbfa2b860fd109b554979a7652fb5e6573f98cee5945832c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "couchDb", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="couchDbHttps")
    def couch_db_https(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "couchDbHttps"))

    @couch_db_https.setter # type: ignore[no-redef]
    def couch_db_https(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d29164b53f6202e703e04ca59eac03fd47c8e35674a6f672839c83df86431d5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "couchDbHttps", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="dnsTcp")
    def dns_tcp(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "dnsTcp"))

    @dns_tcp.setter # type: ignore[no-redef]
    def dns_tcp(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffdb020f25d7d1f372c71e8af761870b07343746191e11bd44de87b2dff322fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "dnsTcp", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="dnsUdp")
    def dns_udp(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "dnsUdp"))

    @dns_udp.setter # type: ignore[no-redef]
    def dns_udp(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c7f03cd304680af8ab3f4ba907a113d43c53453541b1fc99feaddeb099ccf3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "dnsUdp", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="dynamicPorts")
    def dynamic_ports(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "dynamicPorts"))

    @dynamic_ports.setter # type: ignore[no-redef]
    def dynamic_ports(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec1b148591455a614356cd34bad511f12e54608ceed1c6f9a1461e07ab27342e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "dynamicPorts", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="elasticSearch")
    def elastic_search(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "elasticSearch"))

    @elastic_search.setter # type: ignore[no-redef]
    def elastic_search(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54410fe55d2997976ee966e459623a740e9f84c4adce2a8d51ab26be9d7f0628)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "elasticSearch", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="ftp")
    def ftp(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "ftp"))

    @ftp.setter # type: ignore[no-redef]
    def ftp(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adb934347cc434d0e3677a0e47529fa36c57f65ce84e41e1dfe3f60cbcfa8968)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "ftp", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="https")
    def https(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "https"))

    @https.setter # type: ignore[no-redef]
    def https(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f290022d5480ff24483f9d2ad46943dfd2b4748a77879e75f56d4e1c34bbfa4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "https", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="httpTcp")
    def http_tcp(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "httpTcp"))

    @http_tcp.setter # type: ignore[no-redef]
    def http_tcp(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fff096289e22ceac25c3bbf80dd71a972b07629d656bd3e3944119e79f5941f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "httpTcp", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="httpUdp")
    def http_udp(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "httpUdp"))

    @http_udp.setter # type: ignore[no-redef]
    def http_udp(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c4046f07fac26ea6893f576569d324557542559aec9ecc5255680c51ff71265)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "httpUdp", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="imap")
    def imap(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "imap"))

    @imap.setter # type: ignore[no-redef]
    def imap(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b46638380c8f6029b6a9d9ef048441def6bf355d71a288b50972a97eb7674198)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "imap", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="imaps")
    def imaps(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "imaps"))

    @imaps.setter # type: ignore[no-redef]
    def imaps(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4f675e3a430889a6f228c843aba118114a919ba6e758a028c4506db7712d4ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "imaps", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="kestrel")
    def kestrel(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "kestrel"))

    @kestrel.setter # type: ignore[no-redef]
    def kestrel(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b194b6fee033ff03617c32a20dd338fe4ea21485c8020dba303f1eba1e54024d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "kestrel", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="ldap")
    def ldap(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "ldap"))

    @ldap.setter # type: ignore[no-redef]
    def ldap(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f4f075495519a2ded6add6124312cb4922a6dcd004a2f45e4ceaca138cede30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "ldap", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="memcached")
    def memcached(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "memcached"))

    @memcached.setter # type: ignore[no-redef]
    def memcached(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3af61fd076a850e44f55148f4961fc6bf5ab13ed828d9d442d8c365736c9d3cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "memcached", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="mongoDB")
    def mongo_db(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "mongoDB"))

    @mongo_db.setter # type: ignore[no-redef]
    def mongo_db(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f720f7075628d4674b53bdc2ba92196b48132d79f5854c8f3be1322a4edca655)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "mongoDB", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="mssql")
    def mssql(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "mssql"))

    @mssql.setter # type: ignore[no-redef]
    def mssql(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c4ab80763d6a0e866559b76c804c1299012f8b2c54d744bd12b5c7360234e8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "mssql", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="mySQL")
    def my_sql(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "mySQL"))

    @my_sql.setter # type: ignore[no-redef]
    def my_sql(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b52ee43f2b122e438aa6de1db7d6089d2bb85d4ced823b9d956e07a1f1e4363a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "mySQL", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="neo4J")
    def neo4_j(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "neo4J"))

    @neo4_j.setter # type: ignore[no-redef]
    def neo4_j(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6eb8b6aff1ddde58f600085a8382b928d2b34b187d37a983b764b3462642a6a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "neo4J", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="pop3")
    def pop3(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "pop3"))

    @pop3.setter # type: ignore[no-redef]
    def pop3(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8dc18c7d81c1a523b059b4f9d774dd14d52db1a6e76cdacd546ef48bd0e0327)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "pop3", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="pop3s")
    def pop3s(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "pop3s"))

    @pop3s.setter # type: ignore[no-redef]
    def pop3s(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cb0ee61bcdb0821166eab5a777a7191ee2590f7ded8fe36fda3145c4220054c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "pop3s", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="postgreSQL")
    def postgre_sql(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "postgreSQL"))

    @postgre_sql.setter # type: ignore[no-redef]
    def postgre_sql(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8afcb92b737eddf80dae97e4fa5ef4288070711c4efa1d09e67a8c6a1282479)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "postgreSQL", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="rabbitMQ")
    def rabbit_mq(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "rabbitMQ"))

    @rabbit_mq.setter # type: ignore[no-redef]
    def rabbit_mq(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f8e402ea9052c619a30f98a9f8106c116773962c7843e9c505dbb3b3849e0f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "rabbitMQ", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="rdp")
    def rdp(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "rdp"))

    @rdp.setter # type: ignore[no-redef]
    def rdp(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d74ff2280fd53db436d9053cbf0ee58158899ab12a4355be85bb9b26b0b8746)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "rdp", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="redis")
    def redis(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "redis"))

    @redis.setter # type: ignore[no-redef]
    def redis(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1644617b606d0b3f41a767f22fa6824eab1b9763906e94622a0fb0406b374e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "redis", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="riak")
    def riak(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "riak"))

    @riak.setter # type: ignore[no-redef]
    def riak(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e9b8e0482d42615228dc6f7bc12651f727309a2e7f4ccb202b434a1dadd6e8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "riak", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="riakJMX")
    def riak_jmx(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "riakJMX"))

    @riak_jmx.setter # type: ignore[no-redef]
    def riak_jmx(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c31226f6cc08d856fa6fd8d25a3ae32ffd1d79e06ba62dfc35321ae6c800e58d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "riakJMX", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="smtp")
    def smtp(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "smtp"))

    @smtp.setter # type: ignore[no-redef]
    def smtp(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf112adc9f030cc1968f5f18f721ebf04512547c31fe8694b70985b223f90882)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "smtp", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="smtps")
    def smtps(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "smtps"))

    @smtps.setter # type: ignore[no-redef]
    def smtps(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20ec9ca8d52857f5348c2e3d90288f9e90a23e991f7d8b9aca38c25eb1175c95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "smtps", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="ssh")
    def ssh(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "ssh"))

    @ssh.setter # type: ignore[no-redef]
    def ssh(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee6b9440b83c9e576328c0aff089b45ab02542468a21d873ca9bbcac74caad04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "ssh", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="winRM")
    def win_rm(cls) -> "RuleConfig":  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("RuleConfig", jsii.sget(cls, "winRM"))

    @win_rm.setter # type: ignore[no-redef]
    def win_rm(cls, value: "RuleConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa4c8632ac5b1a4c99029db980e5d8040476957230a6e2955cd946c07885b166)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "winRM", value)


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_networksecuritygroup.RuleConfig",
    jsii_struct_bases=[],
    name_mapping={
        "access": "access",
        "destination_address_prefix": "destinationAddressPrefix",
        "destination_port_range": "destinationPortRange",
        "direction": "direction",
        "name": "name",
        "priority": "priority",
        "protocol": "protocol",
        "source_address_prefix": "sourceAddressPrefix",
        "source_port_range": "sourcePortRange",
    },
)
class RuleConfig:
    def __init__(
        self,
        *,
        access: builtins.str,
        destination_address_prefix: builtins.str,
        destination_port_range: builtins.str,
        direction: builtins.str,
        name: builtins.str,
        priority: jsii.Number,
        protocol: builtins.str,
        source_address_prefix: builtins.str,
        source_port_range: builtins.str,
    ) -> None:
        '''Configuration properties for defining a rule within an Azure Network Security Group.

        :param access: The access type of the rule, which determines whether the rule permits or denies traffic. Common values are 'Allow' or 'Deny'.
        :param destination_address_prefix: The CIDR or destination IP range or '*' to match any IP. This specifies the range of destination IPs for which the rule is applicable.
        :param destination_port_range: The range of destination ports to which the rule applies. Can also be a single port or a range.
        :param direction: The direction of the rule, which can be 'Inbound' or 'Outbound'.
        :param name: The name of the security rule.
        :param priority: The priority of the rule. Lower numbers have higher priority. Allowed values are from 100 to 4096.
        :param protocol: The protocol to which the rule applies, such as 'Tcp', 'Udp', or '*' (for all protocols).
        :param source_address_prefix: The CIDR or source IP range or '*' to match any IP. This is the range of source IPs for which the rule applies.
        :param source_port_range: The range of source ports to which the rule applies. Can be a single port or a range like '1024-2048'.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48a76cf5c5861de94a0266a502c4961f68a6396179e4dd0b8cbadb2094d45e15)
            check_type(argname="argument access", value=access, expected_type=type_hints["access"])
            check_type(argname="argument destination_address_prefix", value=destination_address_prefix, expected_type=type_hints["destination_address_prefix"])
            check_type(argname="argument destination_port_range", value=destination_port_range, expected_type=type_hints["destination_port_range"])
            check_type(argname="argument direction", value=direction, expected_type=type_hints["direction"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument source_address_prefix", value=source_address_prefix, expected_type=type_hints["source_address_prefix"])
            check_type(argname="argument source_port_range", value=source_port_range, expected_type=type_hints["source_port_range"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access": access,
            "destination_address_prefix": destination_address_prefix,
            "destination_port_range": destination_port_range,
            "direction": direction,
            "name": name,
            "priority": priority,
            "protocol": protocol,
            "source_address_prefix": source_address_prefix,
            "source_port_range": source_port_range,
        }

    @builtins.property
    def access(self) -> builtins.str:
        '''The access type of the rule, which determines whether the rule permits or denies traffic.

        Common values are 'Allow' or 'Deny'.
        '''
        result = self._values.get("access")
        assert result is not None, "Required property 'access' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination_address_prefix(self) -> builtins.str:
        '''The CIDR or destination IP range or '*' to match any IP.

        This specifies the range of destination IPs for which the rule is applicable.
        '''
        result = self._values.get("destination_address_prefix")
        assert result is not None, "Required property 'destination_address_prefix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination_port_range(self) -> builtins.str:
        '''The range of destination ports to which the rule applies.

        Can also be a single port or a range.
        '''
        result = self._values.get("destination_port_range")
        assert result is not None, "Required property 'destination_port_range' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def direction(self) -> builtins.str:
        '''The direction of the rule, which can be 'Inbound' or 'Outbound'.'''
        result = self._values.get("direction")
        assert result is not None, "Required property 'direction' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the security rule.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def priority(self) -> jsii.Number:
        '''The priority of the rule.

        Lower numbers have higher priority. Allowed values are from 100 to 4096.
        '''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def protocol(self) -> builtins.str:
        '''The protocol to which the rule applies, such as 'Tcp', 'Udp', or '*' (for all protocols).'''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_address_prefix(self) -> builtins.str:
        '''The CIDR or source IP range or '*' to match any IP.

        This is the range of source IPs for which the rule applies.
        '''
        result = self._values.get("source_address_prefix")
        assert result is not None, "Required property 'source_address_prefix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_port_range(self) -> builtins.str:
        '''The range of source ports to which the rule applies.

        Can be a single port or a range like '1024-2048'.
        '''
        result = self._values.get("source_port_range")
        assert result is not None, "Required property 'source_port_range' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_networksecuritygroup.RuleOverrides",
    jsii_struct_bases=[],
    name_mapping={
        "destination_address_prefix": "destinationAddressPrefix",
        "priority": "priority",
        "source_address_prefix": "sourceAddressPrefix",
    },
)
class RuleOverrides:
    def __init__(
        self,
        *,
        destination_address_prefix: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        source_address_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining overrides for a rule in an Azure Network Security Group.

        :param destination_address_prefix: Optional destination address prefix to be matched for the rule. Similar to the source address prefix, this can be a specific IP address or a range. If not provided, it defaults to matching any destination address.
        :param priority: Optional priority for the rule. Rules are processed in the order of their priority, with lower numbers processed before higher numbers. If not provided, a default priority will be assigned.
        :param source_address_prefix: Optional source address prefix to be matched for the rule. This can be an IP address or a range of IP addresses. If not specified, the default behavior is to match any source address.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee09b7b2522a444a73becebd30a013761b548942c7e5be345565bd4de7e54221)
            check_type(argname="argument destination_address_prefix", value=destination_address_prefix, expected_type=type_hints["destination_address_prefix"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument source_address_prefix", value=source_address_prefix, expected_type=type_hints["source_address_prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if destination_address_prefix is not None:
            self._values["destination_address_prefix"] = destination_address_prefix
        if priority is not None:
            self._values["priority"] = priority
        if source_address_prefix is not None:
            self._values["source_address_prefix"] = source_address_prefix

    @builtins.property
    def destination_address_prefix(self) -> typing.Optional[builtins.str]:
        '''Optional destination address prefix to be matched for the rule.

        Similar to the source address prefix,
        this can be a specific IP address or a range. If not provided, it defaults to matching any destination address.
        '''
        result = self._values.get("destination_address_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''Optional priority for the rule.

        Rules are processed in the order of their priority,
        with lower numbers processed before higher numbers. If not provided, a default priority will be assigned.
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def source_address_prefix(self) -> typing.Optional[builtins.str]:
        '''Optional source address prefix to be matched for the rule.

        This can be an IP address or a range of IP addresses.
        If not specified, the default behavior is to match any source address.
        '''
        result = self._values.get("source_address_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RuleOverrides(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityGroup(
    _AzureResource_74eec1c4,
    metaclass=jsii.JSIIMeta,
    jsii_type="@microsoft/terraform-cdk-constructs.azure_networksecuritygroup.SecurityGroup",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        rules: typing.Sequence[typing.Union[RuleConfig, typing.Dict[builtins.str, typing.Any]]],
        resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
    ) -> None:
        '''Represents an Azure Network Security Group (NSG).

        This class is responsible for the creation and management of an Azure Network Security Group, which acts as a virtual firewall
        for virtual network resources. A Network Security Group contains a list of security rules that allow or deny network traffic
        to resources connected to Azure Virtual Networks (VNet). Each rule specifies a combination of source and destination, port,
        and protocol, and an action (allow or deny) based on those combinations. This class allows for detailed configuration of these
        rules to enforce security policies for inbound and outbound network traffic.

        :param scope: - The scope in which to define this construct, typically representing the Cloud Development Kit (CDK) stack.
        :param id: - The unique identifier for this instance of the security group.
        :param location: The Azure region in which to create the network security group, e.g., 'East US', 'West Europe'.
        :param name: The name of the network security group. Must be unique within the resource group.
        :param rules: An array of rule configurations to be applied to the network security group.
        :param resource_group: An optional reference to the resource group in which to deploy the Workspace. If not provided, the Workspace will be deployed in the default resource group.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aa95efe68d21a63b93f1eb87166793543fbfb2ea39d8f2d1225583762f0b0e1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SecurityGroupProps(
            location=location, name=name, rules=rules, resource_group=resource_group
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="associateToNetworkInterface")
    def associate_to_network_interface(
        self,
        network_interface: _cdktf_cdktf_provider_azurerm_network_interface_92bbcedf.NetworkInterface,
    ) -> None:
        '''Associates this Network Security Group with a specified network interface.

        This method attaches the security group to a network interface, applying the security group's rules to the network interface.
        This allows for fine-grained control of network traffic to and from the specific network interface.

        :param network_interface: - The network interface object to which this network security group will be associated. Example usage:: const myNetworkInterface = { id: 'nic-456', name: 'NetworkInterfaceA' }; mySecurityGroup.associateToNetworkInterface(myNetworkInterface); This operation ensures that the security rules defined in the network security group are applied directly to the specified network interface, controlling access in a more targeted manner.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92f9e57b285151d8483831ce14f03602abbadf56db0aa9a80406366244656236)
            check_type(argname="argument network_interface", value=network_interface, expected_type=type_hints["network_interface"])
        return typing.cast(None, jsii.invoke(self, "associateToNetworkInterface", [network_interface]))

    @jsii.member(jsii_name="associateToSubnet")
    def associate_to_subnet(
        self,
        subnet: _cdktf_cdktf_provider_azurerm_subnet_92bbcedf.Subnet,
    ) -> None:
        '''Associates this Network Security Group with a specified subnet.

        This method facilitates the attachment of the security group to a subnet, applying the security group's rules to all
        resources within the subnet. This is crucial for managing network access and security policies at the subnet level.

        :param subnet: - The subnet object to which this network security group will be associated. Example usage:: const mySubnet = { id: 'subnet-123', name: 'SubnetA' }; mySecurityGroup.associateToSubnet(mySubnet); This operation ensures that the security rules defined in the network security group are enforced on all network interfaces attached to the specified subnet.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92d195c7b2cb05cc143e838bb2bddfd966d519129c8774ccd521e71e42a3df4d)
            check_type(argname="argument subnet", value=subnet, expected_type=type_hints["subnet"])
        return typing.cast(None, jsii.invoke(self, "associateToSubnet", [subnet]))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "SecurityGroupProps":
        return typing.cast("SecurityGroupProps", jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f94efb4824688e9def6cff58a3a46fbc4323e3e38fd48ba2ee21ca0dafc2fd69)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e02e03a0aeef8c43217e2127b1a030ffb36700d6088e6eb32e1504060a01fa4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroup", value)


class SecurityGroupAssociations(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@microsoft/terraform-cdk-constructs.azure_networksecuritygroup.SecurityGroupAssociations",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        network_security_group_id: builtins.str,
        network_interface_id: typing.Optional[builtins.str] = None,
        subnet_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Manages the associations of Azure Network Security Groups with subnets and network interfaces.

        This class provides the functionality to associate a network security group with either subnets or network interfaces
        within the Azure environment. By managing these associations, it helps enforce security rules at both the subnet level
        and the network interface level, enhancing security configurations and compliance.

        :param scope: - The scope in which to define this construct, typically representing the Cloud Development Kit (CDK) stack.
        :param id: - The unique identifier for the association instance.
        :param network_security_group_id: The ID of the network security group to be associated.
        :param network_interface_id: Optional network interface ID to associate with the network security group. If provided, the security group will be associated with this network interface.
        :param subnet_id: Optional subnet ID to associate with the network security group. If provided, the security group will be associated with this subnet.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da46013d569817cde3759230947d3e9f0fef81e401220cfc79c8c5d7f47566da)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SecurityGroupAssociationsProps(
            network_security_group_id=network_security_group_id,
            network_interface_id=network_interface_id,
            subnet_id=subnet_id,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_networksecuritygroup.SecurityGroupAssociationsProps",
    jsii_struct_bases=[],
    name_mapping={
        "network_security_group_id": "networkSecurityGroupId",
        "network_interface_id": "networkInterfaceId",
        "subnet_id": "subnetId",
    },
)
class SecurityGroupAssociationsProps:
    def __init__(
        self,
        *,
        network_security_group_id: builtins.str,
        network_interface_id: typing.Optional[builtins.str] = None,
        subnet_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for associating Azure Network Security Groups with subnets and network interfaces.

        :param network_security_group_id: The ID of the network security group to be associated.
        :param network_interface_id: Optional network interface ID to associate with the network security group. If provided, the security group will be associated with this network interface.
        :param subnet_id: Optional subnet ID to associate with the network security group. If provided, the security group will be associated with this subnet.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__805aa3371592a232ef6988236e010bd394175732a6fbe69206859074c589eed1)
            check_type(argname="argument network_security_group_id", value=network_security_group_id, expected_type=type_hints["network_security_group_id"])
            check_type(argname="argument network_interface_id", value=network_interface_id, expected_type=type_hints["network_interface_id"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "network_security_group_id": network_security_group_id,
        }
        if network_interface_id is not None:
            self._values["network_interface_id"] = network_interface_id
        if subnet_id is not None:
            self._values["subnet_id"] = subnet_id

    @builtins.property
    def network_security_group_id(self) -> builtins.str:
        '''The ID of the network security group to be associated.'''
        result = self._values.get("network_security_group_id")
        assert result is not None, "Required property 'network_security_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_interface_id(self) -> typing.Optional[builtins.str]:
        '''Optional network interface ID to associate with the network security group.

        If provided, the security group will be associated with this network interface.
        '''
        result = self._values.get("network_interface_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''Optional subnet ID to associate with the network security group.

        If provided, the security group will be associated with this subnet.
        '''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityGroupAssociationsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_networksecuritygroup.SecurityGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "location": "location",
        "name": "name",
        "rules": "rules",
        "resource_group": "resourceGroup",
    },
)
class SecurityGroupProps:
    def __init__(
        self,
        *,
        location: builtins.str,
        name: builtins.str,
        rules: typing.Sequence[typing.Union[RuleConfig, typing.Dict[builtins.str, typing.Any]]],
        resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
    ) -> None:
        '''Properties for defining an Azure Network Security Group.

        :param location: The Azure region in which to create the network security group, e.g., 'East US', 'West Europe'.
        :param name: The name of the network security group. Must be unique within the resource group.
        :param rules: An array of rule configurations to be applied to the network security group.
        :param resource_group: An optional reference to the resource group in which to deploy the Workspace. If not provided, the Workspace will be deployed in the default resource group.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cd7a0de161a25d6de85e71efdf1a6c2c1f32a58488a0ab5198a64378a79a326)
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            check_type(argname="argument resource_group", value=resource_group, expected_type=type_hints["resource_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "name": name,
            "rules": rules,
        }
        if resource_group is not None:
            self._values["resource_group"] = resource_group

    @builtins.property
    def location(self) -> builtins.str:
        '''The Azure region in which to create the network security group, e.g., 'East US', 'West Europe'.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the network security group.

        Must be unique within the resource group.
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rules(self) -> typing.List[RuleConfig]:
        '''An array of rule configurations to be applied to the network security group.'''
        result = self._values.get("rules")
        assert result is not None, "Required property 'rules' is missing"
        return typing.cast(typing.List[RuleConfig], result)

    @builtins.property
    def resource_group(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup]:
        '''An optional reference to the resource group in which to deploy the Workspace.

        If not provided, the Workspace will be deployed in the default resource group.
        '''
        result = self._values.get("resource_group")
        return typing.cast(typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "PreconfiguredRules",
    "RuleConfig",
    "RuleOverrides",
    "SecurityGroup",
    "SecurityGroupAssociations",
    "SecurityGroupAssociationsProps",
    "SecurityGroupProps",
]

publication.publish()

def _typecheckingstub__36828755c5b4c1e8159d75a5791196dbe984738537aa216471a1af45feecc05d(
    rule: typing.Union[RuleConfig, typing.Dict[builtins.str, typing.Any]],
    destination_address_prefix: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5047f03b32af36e495107644a1cca8ef3f5685f6440fb5594b8c4e9da8fac527(
    rule: typing.Union[RuleConfig, typing.Dict[builtins.str, typing.Any]],
    priority: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__380230cfd2bf19b7b486337feed1a961cec154d093a50410318ae6f069c3c07d(
    rule: typing.Union[RuleConfig, typing.Dict[builtins.str, typing.Any]],
    source_address_prefix: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f7fa8ff8e816697bfed79efeb582a0a3d5959f3568e35df3423eb7a9afd975e(
    base_rule: typing.Union[RuleConfig, typing.Dict[builtins.str, typing.Any]],
    *,
    destination_address_prefix: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    source_address_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__428dbd0c13493fc0e286f68339632262ddbbce1720cc3e20f23fde221976c2ce(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5abd3e7641c842e5e9a5a14e677aa271ce51d2e2ee02a0b9f1eda7c7a932993(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d8f1ccf57bc1e925a8d384f8ffdc24be8d843c10da95b29ada00685a8906004(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7274ca46989376e017367f8eea4daf57323cbfc5b5dd4fde03064dcf182866fd(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a576f2d388842b9d27aba4477ce3b42e1f5dddf49e3e3c9e9bcafb6ebc72235(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0bc577ddca27fe23efab210d6e0a9e0650c7eaeb5611b2acd8c793c5701a753(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d09b9850fb411ed4831ffca866e06c4331fb796968850a0acacb5442ec49469(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5af60cd8933cc2c05423257643cdcf293dd3757574d3043c20cd31a472f5620(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b171e6d47709b8132a24a97da7d017b8d1751629bb9e51863a89461f53b3d4c(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e8794392c6432472a6b30efd2e4b5779aa5c3aa94a4ffaefc35fa6a434df62d(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__931d4418249ac4993f526a0f267e88e8b9117cbc8a1eb53dc22d13f6f9dcf30b(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b4a15df9f07baaeec11fa5e27f6363014b619931162d24d3c06da60d3bd791a(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d4106eaa46732da846afdc98b2dac21fdd385660c8090177e8252c48e8d839b(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__799bd466f4976406d080d7d848270f33f8f35833d2783953465125a108780a00(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__286a9dbad6ec5bbf7414e63969dec5cb59ca47b52197452b70b51fafa181d08f(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66bff9971afcefaf5f92d772e054e0149616b70bc27bc93692a95e13a570a998(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8506559ba4cf5d3e3d387692f33e7ec9bf02e3b064e2a5ccb33db5745849e6e(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ce0a5c999b498f7a6fb7e853fe1f904c2b3bf8862be5ede1625c27242145473(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cedddad1428ac3deb46d7311e21c459c6cd3b46ff7ab1a2d09934a78eba5703(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48852d8760d119fcbfa2b860fd109b554979a7652fb5e6573f98cee5945832c7(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d29164b53f6202e703e04ca59eac03fd47c8e35674a6f672839c83df86431d5d(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffdb020f25d7d1f372c71e8af761870b07343746191e11bd44de87b2dff322fd(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c7f03cd304680af8ab3f4ba907a113d43c53453541b1fc99feaddeb099ccf3b(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec1b148591455a614356cd34bad511f12e54608ceed1c6f9a1461e07ab27342e(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54410fe55d2997976ee966e459623a740e9f84c4adce2a8d51ab26be9d7f0628(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adb934347cc434d0e3677a0e47529fa36c57f65ce84e41e1dfe3f60cbcfa8968(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f290022d5480ff24483f9d2ad46943dfd2b4748a77879e75f56d4e1c34bbfa4(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fff096289e22ceac25c3bbf80dd71a972b07629d656bd3e3944119e79f5941f7(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c4046f07fac26ea6893f576569d324557542559aec9ecc5255680c51ff71265(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b46638380c8f6029b6a9d9ef048441def6bf355d71a288b50972a97eb7674198(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4f675e3a430889a6f228c843aba118114a919ba6e758a028c4506db7712d4ef(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b194b6fee033ff03617c32a20dd338fe4ea21485c8020dba303f1eba1e54024d(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f4f075495519a2ded6add6124312cb4922a6dcd004a2f45e4ceaca138cede30(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3af61fd076a850e44f55148f4961fc6bf5ab13ed828d9d442d8c365736c9d3cf(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f720f7075628d4674b53bdc2ba92196b48132d79f5854c8f3be1322a4edca655(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c4ab80763d6a0e866559b76c804c1299012f8b2c54d744bd12b5c7360234e8d(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b52ee43f2b122e438aa6de1db7d6089d2bb85d4ced823b9d956e07a1f1e4363a(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eb8b6aff1ddde58f600085a8382b928d2b34b187d37a983b764b3462642a6a1(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8dc18c7d81c1a523b059b4f9d774dd14d52db1a6e76cdacd546ef48bd0e0327(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cb0ee61bcdb0821166eab5a777a7191ee2590f7ded8fe36fda3145c4220054c(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8afcb92b737eddf80dae97e4fa5ef4288070711c4efa1d09e67a8c6a1282479(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f8e402ea9052c619a30f98a9f8106c116773962c7843e9c505dbb3b3849e0f9(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d74ff2280fd53db436d9053cbf0ee58158899ab12a4355be85bb9b26b0b8746(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1644617b606d0b3f41a767f22fa6824eab1b9763906e94622a0fb0406b374e5(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e9b8e0482d42615228dc6f7bc12651f727309a2e7f4ccb202b434a1dadd6e8c(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c31226f6cc08d856fa6fd8d25a3ae32ffd1d79e06ba62dfc35321ae6c800e58d(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf112adc9f030cc1968f5f18f721ebf04512547c31fe8694b70985b223f90882(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20ec9ca8d52857f5348c2e3d90288f9e90a23e991f7d8b9aca38c25eb1175c95(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee6b9440b83c9e576328c0aff089b45ab02542468a21d873ca9bbcac74caad04(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa4c8632ac5b1a4c99029db980e5d8040476957230a6e2955cd946c07885b166(
    value: RuleConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48a76cf5c5861de94a0266a502c4961f68a6396179e4dd0b8cbadb2094d45e15(
    *,
    access: builtins.str,
    destination_address_prefix: builtins.str,
    destination_port_range: builtins.str,
    direction: builtins.str,
    name: builtins.str,
    priority: jsii.Number,
    protocol: builtins.str,
    source_address_prefix: builtins.str,
    source_port_range: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee09b7b2522a444a73becebd30a013761b548942c7e5be345565bd4de7e54221(
    *,
    destination_address_prefix: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    source_address_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aa95efe68d21a63b93f1eb87166793543fbfb2ea39d8f2d1225583762f0b0e1(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    rules: typing.Sequence[typing.Union[RuleConfig, typing.Dict[builtins.str, typing.Any]]],
    resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92f9e57b285151d8483831ce14f03602abbadf56db0aa9a80406366244656236(
    network_interface: _cdktf_cdktf_provider_azurerm_network_interface_92bbcedf.NetworkInterface,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92d195c7b2cb05cc143e838bb2bddfd966d519129c8774ccd521e71e42a3df4d(
    subnet: _cdktf_cdktf_provider_azurerm_subnet_92bbcedf.Subnet,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f94efb4824688e9def6cff58a3a46fbc4323e3e38fd48ba2ee21ca0dafc2fd69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e02e03a0aeef8c43217e2127b1a030ffb36700d6088e6eb32e1504060a01fa4e(
    value: _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da46013d569817cde3759230947d3e9f0fef81e401220cfc79c8c5d7f47566da(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    network_security_group_id: builtins.str,
    network_interface_id: typing.Optional[builtins.str] = None,
    subnet_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__805aa3371592a232ef6988236e010bd394175732a6fbe69206859074c589eed1(
    *,
    network_security_group_id: builtins.str,
    network_interface_id: typing.Optional[builtins.str] = None,
    subnet_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cd7a0de161a25d6de85e71efdf1a6c2c1f32a58488a0ab5198a64378a79a326(
    *,
    location: builtins.str,
    name: builtins.str,
    rules: typing.Sequence[typing.Union[RuleConfig, typing.Dict[builtins.str, typing.Any]]],
    resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
) -> None:
    """Type checking stubs"""
    pass
