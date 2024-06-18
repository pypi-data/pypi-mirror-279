'''
# Azure Application Gateway Construct

This class represents an Azure Application Gateway resource. It provides a convenient way to manage Azure Application Gateway resources.

## What is Azure Application Gateway?

Azure Application Gateway is a web traffic load balancer that enables you to manage traffic to your web applications. It offers various features like URL-based routing, session affinity, secure sockets layer (SSL) termination, Web Application Firewall (WAF), and more. This makes it an ideal choice for optimizing web app performance and reliability.

For more information, refer to the [official Azure documentation on Application Gateway](https://docs.microsoft.com/en-us/azure/application-gateway/).

## Application Gateway Best Practices

* Use separate instances for production and non-production environments.
* Implement WAF to protect your web applications from common web vulnerabilities.
* Use URL-based routing for better control of the traffic distribution.
* Enable diagnostics and logging for better monitoring and troubleshooting.

## Application Gateway Class Properties

This class encapsulates several properties to configure and manage the Application Gateway:

* `name`: The name of the Application Gateway resource.
* `location`: The Azure region where the Application Gateway will be deployed.
* `resourceGroup`: The Azure Resource Group to which the Application Gateway belongs.
* `skuTier`: The pricing tier (e.g., Standard, WAF).
* `skuSize`: The size of the Application Gateway instance.
* `capacity`: The number of instances for the Application Gateway.
* `backendAddressPools`: Backend address pools for routing traffic.
* `backendHttpSettings`: HTTP settings for the backend address pool.
* `httpListeners`: HTTP listeners for processing incoming traffic.
* `requestRoutingRules`: Routing rules for directing traffic.
* `frontendPorts`: Frontend ports configuration.
* `subnet`: Subnet details for the Application Gateway.
* `tags`: Tags for identifying and categorizing the Application Gateway.
* Additional properties for advanced configurations (SSL certificates, WAF configuration, etc.).

## Deploying the Application Gateway

Here's an example of how to deploy an Application Gateway resource using this class:

```python
const appGateway = new Gateway(this, 'myAppGateway', {
  name: 'myAppGateway',
  location: 'East US',
  resourceGroup: myResourceGroup,
  skuTier: 'Standard_v2',
  skuSize: 'Standard_Small',
  capacity: 2,
  backendAddressPools: [...],
  backendHttpSettings: [...],
  httpListeners: [...],
  requestRoutingRules: [...],
  frontendPorts: [...],
  // Additional configurations
  tags: {
    'env': 'production',
  },
});

This code will create a new Application Gateway named myAppGateway in the East US Azure region within the specified resource group. It will be configured with the Standard v2 pricing tier, small SKU size, and essential settings for backend pools, HTTP settings, listeners, and routing rules. Tags are used for easy identification.
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

import cdktf_cdktf_provider_azurerm.application_gateway as _cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf
import cdktf_cdktf_provider_azurerm.key_vault as _cdktf_cdktf_provider_azurerm_key_vault_92bbcedf
import cdktf_cdktf_provider_azurerm.public_ip as _cdktf_cdktf_provider_azurerm_public_ip_92bbcedf
import cdktf_cdktf_provider_azurerm.resource_group as _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf
import cdktf_cdktf_provider_azurerm.subnet as _cdktf_cdktf_provider_azurerm_subnet_92bbcedf
import constructs as _constructs_77d1e7e8
from ..core_azure import AzureResource as _AzureResource_74eec1c4


class Gateway(
    _AzureResource_74eec1c4,
    metaclass=jsii.JSIIMeta,
    jsii_type="@microsoft/terraform-cdk-constructs.azure_applicationgateway.Gateway",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        props: "IGatewayProps",
    ) -> None:
        '''Constructs a new Azure Application Gateway.

        :param scope: - The scope in which to define this construct.
        :param id: - The ID of this construct.
        :param props: - The properties for configuring the Azure Application Gateway. The properties include: - ``name``: Required. Unique name for the Application Gateway within Azure. - ``location``: Required. Azure Region for deployment. - ``resourceGroup``: Optional. Reference to the resource group for deployment. - ``skuTier``: Required. SKU tier of the Application Gateway (e.g., Standard, WAF). - ``skuSize``: Required. Size of the SKU for the Application Gateway. - ``capacity``: Required. Capacity (instance count) of the Application Gateway. - ``backendAddressPools``: Required. Backend address pools for the Application Gateway. - ``backendHttpSettings``: Required. Backend HTTP settings for the Application Gateway. - ``httpListeners``: Required. HTTP listeners for the Application Gateway. - ``requestRoutingRules``: Required. Request routing rules for the Application Gateway. - ``publicIpAddress``: Optional. Public IP address for the frontend. - ``privateIpAddress``: Optional. Private IP address for the frontend. - ``privateIpAddressAllocation``: Optional. Allocation method for the private IP (Static, Dynamic). - ``frontendPorts``: Optional. Frontend ports for the Application Gateway. - ``subnet``: Optional. Subnet for the Application Gateway. - ``enableHttp2``: Optional. Flag to enable HTTP2. - ``fipsEnabled``: Optional. Flag to enable FIPS-compliant algorithms. - ``firewallPolicyId``: Optional. ID of the firewall policy. - ``forceFirewallPolicyAssociation``: Optional. Flag to enforce association of the firewall policy. - ``tags``: Optional. Tags for resource management. - Additional optional properties as described in ``IGatewayProps`` interface. Example usage:: new Gateway(this, 'appGateway1', { name: 'gatewayEast', resourceGroup: resourceGroup, location: "eastus", skuTier: "Standard_v2", skuSize: "Standard_v2", capacity: 2, publicIpAddress: publicIp, subnet: subnet, backendAddressPools: [ { name: "backend-address-pool-1" }, { name: "backend-address-pool-2", ipAddresses: ["10.1.0.4", "10.1.0.5", "10.1.0.6"], }, ], httpListeners: [ { name: "http-listener", frontendPortName: "80", frontendIpConfigurationName: "Public-frontend-ip-configuration", protocol: "Http", }, ], backendHttpSettings: [ { name: "backend-http-setting", port: 80, protocol: "Http", requestTimeout: 20, cookieBasedAffinity: "Disabled", }, ], requestRoutingRules: [ { name: "request-routing-rule-1", httpListenerName: "http-listener", priority: 1, backendAddressPoolName: "backend-address-pool-1", backendHttpSettingsName: "backend-http-setting", ruleType: "Basic", }, ], });
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70268ba9e307d3454870ee0057f05b3b009f0dd65bf5374e1cbc7bcc7fbf8c15)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "IGatewayProps":
        return typing.cast("IGatewayProps", jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b61d2d601d949705a9855d8c64b55d0bffb323d9b834e4cee097484d2df53178)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6551808057430f5a4eed594f7a9df507a653f2aa7d6d3dabb9cf55796fc6ebd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroup", value)


@jsii.interface(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_applicationgateway.IGatewayProps"
)
class IGatewayProps(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="backendAddressPools")
    def backend_address_pools(
        self,
    ) -> typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayBackendAddressPool]:
        '''The backend address pools for the Application Gateway.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="backendHttpSettings")
    def backend_http_settings(
        self,
    ) -> typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayBackendHttpSettings]:
        '''The backend HTTP settings for the Application Gateway.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="capacity")
    def capacity(self) -> jsii.Number:
        '''The capacity (instance count) of the Application Gateway.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="httpListeners")
    def http_listeners(
        self,
    ) -> typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayHttpListener]:
        '''The HTTP listeners for the Application Gateway.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        '''The location where the Application Gateway will be deployed (e.g., region).'''
        ...

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the Application Gateway.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="requestRoutingRules")
    def request_routing_rules(
        self,
    ) -> typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayRequestRoutingRule]:
        '''The request routing rules for the Application Gateway.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="skuSize")
    def sku_size(self) -> builtins.str:
        '''The size of the SKU for the Application Gateway.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="skuTier")
    def sku_tier(self) -> builtins.str:
        '''The SKU tier of the Application Gateway (e.g., Standard, WAF).'''
        ...

    @builtins.property
    @jsii.member(jsii_name="authenticationCertificate")
    def authentication_certificate(
        self,
    ) -> typing.Optional[typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayAuthenticationCertificate]]:
        '''Optional authentication certificates for mutual authentication.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="autoscaleConfiguration")
    def autoscale_configuration(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayAutoscaleConfiguration]:
        '''Optional autoscale configuration for dynamically adjusting the capacity of the Application Gateway.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="customErrorConfiguration")
    def custom_error_configuration(
        self,
    ) -> typing.Optional[typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayCustomErrorConfiguration]]:
        '''Optional custom error configurations to specify custom error pages.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="enableHttp2")
    def enable_http2(self) -> typing.Optional[builtins.bool]:
        '''Flag to enable HTTP2.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="fipsEnabled")
    def fips_enabled(self) -> typing.Optional[builtins.bool]:
        '''Flag to enable FIPS-compliant algorithms.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="firewallPolicyId")
    def firewall_policy_id(self) -> typing.Optional[builtins.str]:
        '''Optional ID of the firewall policy.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="forceFirewallPolicyAssociation")
    def force_firewall_policy_association(self) -> typing.Optional[builtins.bool]:
        '''Flag to enforce association of the firewall policy.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="frontendPorts")
    def frontend_ports(
        self,
    ) -> typing.Optional[typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayFrontendPort]]:
        '''Optional frontend ports for the Application Gateway.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayIdentity]:
        '''Optional identity for the Application Gateway, used for accessing other Azure resources.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="keyVault")
    def key_vault(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_key_vault_92bbcedf.KeyVault]:
        '''Optional Key Vault resource for storing SSL certificates.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="privateLinkConfiguration")
    def private_link_configuration(
        self,
    ) -> typing.Optional[typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayPrivateLinkConfiguration]]:
        '''Optional configurations for enabling Private Link on the Application Gateway.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="probe")
    def probe(
        self,
    ) -> typing.Optional[typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayProbe]]:
        '''Optional probes for health checks of the backend HTTP settings.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="redirectConfiguration")
    def redirect_configuration(
        self,
    ) -> typing.Optional[typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayRedirectConfiguration]]:
        '''Optional configurations for redirect rules.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="resourceGroup")
    def resource_group(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup]:
        '''An optional reference to the resource group in which to deploy the Application Gateway.

        If not provided, the Application Gateway will be deployed in the default resource group.
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="rewriteRuleSet")
    def rewrite_rule_set(
        self,
    ) -> typing.Optional[typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayRewriteRuleSet]]:
        '''Optional rewrite rule sets for modifying HTTP request and response headers and bodies.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="sslCertificate")
    def ssl_certificate(
        self,
    ) -> typing.Optional[typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewaySslCertificate]]:
        '''Optional SSL certificates for enabling HTTPS on the Application Gateway.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="sslPolicy")
    def ssl_policy(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewaySslPolicy]:
        '''Optional SSL policy configurations, defining the protocol and cipher suites used.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="sslProfile")
    def ssl_profile(
        self,
    ) -> typing.Optional[typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewaySslProfile]]:
        '''Optional SSL profiles for managing SSL termination and policy settings.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="subnet")
    def subnet(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_subnet_92bbcedf.Subnet]:
        '''Optional subnet for the Application Gateway.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional tags for the Application Gateway resource.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> typing.Optional[builtins.str]:
        '''Optional tenant ID for use with Key Vault, if applicable.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayTimeouts]:
        '''Optional timeout settings for the Application Gateway resources.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="trustedClientCertificate")
    def trusted_client_certificate(
        self,
    ) -> typing.Optional[typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayTrustedClientCertificate]]:
        '''Optional trusted client certificates for mutual authentication.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="trustedRootCertificate")
    def trusted_root_certificate(
        self,
    ) -> typing.Optional[typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayTrustedRootCertificate]]:
        '''Optional trusted root certificates for backend authentication.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="urlPathMap")
    def url_path_map(
        self,
    ) -> typing.Optional[typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayUrlPathMap]]:
        '''Optional URL path map for routing based on URL paths.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="wafConfiguration")
    def waf_configuration(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayWafConfiguration]:
        '''Optional Web Application Firewall (WAF) configuration to provide enhanced security.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="zones")
    def zones(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional availability zones for the Application Gateway.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="privateIpAddress")
    def private_ip_address(self) -> typing.Optional[builtins.str]:
        '''Optional private IP address for the frontend of the Application Gateway.'''
        ...

    @private_ip_address.setter
    def private_ip_address(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="privateIpAddressAllocation")
    def private_ip_address_allocation(self) -> typing.Optional[builtins.str]:
        '''Allocation method for the private IP address (e.g., Static, Dynamic).'''
        ...

    @private_ip_address_allocation.setter
    def private_ip_address_allocation(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="publicIpAddress")
    def public_ip_address(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_public_ip_92bbcedf.PublicIp]:
        '''Optional public IP address for the frontend of the Application Gateway.'''
        ...

    @public_ip_address.setter
    def public_ip_address(
        self,
        value: typing.Optional[_cdktf_cdktf_provider_azurerm_public_ip_92bbcedf.PublicIp],
    ) -> None:
        ...


class _IGatewayPropsProxy:
    __jsii_type__: typing.ClassVar[str] = "@microsoft/terraform-cdk-constructs.azure_applicationgateway.IGatewayProps"

    @builtins.property
    @jsii.member(jsii_name="backendAddressPools")
    def backend_address_pools(
        self,
    ) -> typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayBackendAddressPool]:
        '''The backend address pools for the Application Gateway.'''
        return typing.cast(typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayBackendAddressPool], jsii.get(self, "backendAddressPools"))

    @builtins.property
    @jsii.member(jsii_name="backendHttpSettings")
    def backend_http_settings(
        self,
    ) -> typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayBackendHttpSettings]:
        '''The backend HTTP settings for the Application Gateway.'''
        return typing.cast(typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayBackendHttpSettings], jsii.get(self, "backendHttpSettings"))

    @builtins.property
    @jsii.member(jsii_name="capacity")
    def capacity(self) -> jsii.Number:
        '''The capacity (instance count) of the Application Gateway.'''
        return typing.cast(jsii.Number, jsii.get(self, "capacity"))

    @builtins.property
    @jsii.member(jsii_name="httpListeners")
    def http_listeners(
        self,
    ) -> typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayHttpListener]:
        '''The HTTP listeners for the Application Gateway.'''
        return typing.cast(typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayHttpListener], jsii.get(self, "httpListeners"))

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        '''The location where the Application Gateway will be deployed (e.g., region).'''
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the Application Gateway.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="requestRoutingRules")
    def request_routing_rules(
        self,
    ) -> typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayRequestRoutingRule]:
        '''The request routing rules for the Application Gateway.'''
        return typing.cast(typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayRequestRoutingRule], jsii.get(self, "requestRoutingRules"))

    @builtins.property
    @jsii.member(jsii_name="skuSize")
    def sku_size(self) -> builtins.str:
        '''The size of the SKU for the Application Gateway.'''
        return typing.cast(builtins.str, jsii.get(self, "skuSize"))

    @builtins.property
    @jsii.member(jsii_name="skuTier")
    def sku_tier(self) -> builtins.str:
        '''The SKU tier of the Application Gateway (e.g., Standard, WAF).'''
        return typing.cast(builtins.str, jsii.get(self, "skuTier"))

    @builtins.property
    @jsii.member(jsii_name="authenticationCertificate")
    def authentication_certificate(
        self,
    ) -> typing.Optional[typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayAuthenticationCertificate]]:
        '''Optional authentication certificates for mutual authentication.'''
        return typing.cast(typing.Optional[typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayAuthenticationCertificate]], jsii.get(self, "authenticationCertificate"))

    @builtins.property
    @jsii.member(jsii_name="autoscaleConfiguration")
    def autoscale_configuration(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayAutoscaleConfiguration]:
        '''Optional autoscale configuration for dynamically adjusting the capacity of the Application Gateway.'''
        return typing.cast(typing.Optional[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayAutoscaleConfiguration], jsii.get(self, "autoscaleConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="customErrorConfiguration")
    def custom_error_configuration(
        self,
    ) -> typing.Optional[typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayCustomErrorConfiguration]]:
        '''Optional custom error configurations to specify custom error pages.'''
        return typing.cast(typing.Optional[typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayCustomErrorConfiguration]], jsii.get(self, "customErrorConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="enableHttp2")
    def enable_http2(self) -> typing.Optional[builtins.bool]:
        '''Flag to enable HTTP2.'''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enableHttp2"))

    @builtins.property
    @jsii.member(jsii_name="fipsEnabled")
    def fips_enabled(self) -> typing.Optional[builtins.bool]:
        '''Flag to enable FIPS-compliant algorithms.'''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "fipsEnabled"))

    @builtins.property
    @jsii.member(jsii_name="firewallPolicyId")
    def firewall_policy_id(self) -> typing.Optional[builtins.str]:
        '''Optional ID of the firewall policy.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firewallPolicyId"))

    @builtins.property
    @jsii.member(jsii_name="forceFirewallPolicyAssociation")
    def force_firewall_policy_association(self) -> typing.Optional[builtins.bool]:
        '''Flag to enforce association of the firewall policy.'''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "forceFirewallPolicyAssociation"))

    @builtins.property
    @jsii.member(jsii_name="frontendPorts")
    def frontend_ports(
        self,
    ) -> typing.Optional[typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayFrontendPort]]:
        '''Optional frontend ports for the Application Gateway.'''
        return typing.cast(typing.Optional[typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayFrontendPort]], jsii.get(self, "frontendPorts"))

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayIdentity]:
        '''Optional identity for the Application Gateway, used for accessing other Azure resources.'''
        return typing.cast(typing.Optional[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayIdentity], jsii.get(self, "identity"))

    @builtins.property
    @jsii.member(jsii_name="keyVault")
    def key_vault(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_key_vault_92bbcedf.KeyVault]:
        '''Optional Key Vault resource for storing SSL certificates.'''
        return typing.cast(typing.Optional[_cdktf_cdktf_provider_azurerm_key_vault_92bbcedf.KeyVault], jsii.get(self, "keyVault"))

    @builtins.property
    @jsii.member(jsii_name="privateLinkConfiguration")
    def private_link_configuration(
        self,
    ) -> typing.Optional[typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayPrivateLinkConfiguration]]:
        '''Optional configurations for enabling Private Link on the Application Gateway.'''
        return typing.cast(typing.Optional[typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayPrivateLinkConfiguration]], jsii.get(self, "privateLinkConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="probe")
    def probe(
        self,
    ) -> typing.Optional[typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayProbe]]:
        '''Optional probes for health checks of the backend HTTP settings.'''
        return typing.cast(typing.Optional[typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayProbe]], jsii.get(self, "probe"))

    @builtins.property
    @jsii.member(jsii_name="redirectConfiguration")
    def redirect_configuration(
        self,
    ) -> typing.Optional[typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayRedirectConfiguration]]:
        '''Optional configurations for redirect rules.'''
        return typing.cast(typing.Optional[typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayRedirectConfiguration]], jsii.get(self, "redirectConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroup")
    def resource_group(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup]:
        '''An optional reference to the resource group in which to deploy the Application Gateway.

        If not provided, the Application Gateway will be deployed in the default resource group.
        '''
        return typing.cast(typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup], jsii.get(self, "resourceGroup"))

    @builtins.property
    @jsii.member(jsii_name="rewriteRuleSet")
    def rewrite_rule_set(
        self,
    ) -> typing.Optional[typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayRewriteRuleSet]]:
        '''Optional rewrite rule sets for modifying HTTP request and response headers and bodies.'''
        return typing.cast(typing.Optional[typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayRewriteRuleSet]], jsii.get(self, "rewriteRuleSet"))

    @builtins.property
    @jsii.member(jsii_name="sslCertificate")
    def ssl_certificate(
        self,
    ) -> typing.Optional[typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewaySslCertificate]]:
        '''Optional SSL certificates for enabling HTTPS on the Application Gateway.'''
        return typing.cast(typing.Optional[typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewaySslCertificate]], jsii.get(self, "sslCertificate"))

    @builtins.property
    @jsii.member(jsii_name="sslPolicy")
    def ssl_policy(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewaySslPolicy]:
        '''Optional SSL policy configurations, defining the protocol and cipher suites used.'''
        return typing.cast(typing.Optional[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewaySslPolicy], jsii.get(self, "sslPolicy"))

    @builtins.property
    @jsii.member(jsii_name="sslProfile")
    def ssl_profile(
        self,
    ) -> typing.Optional[typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewaySslProfile]]:
        '''Optional SSL profiles for managing SSL termination and policy settings.'''
        return typing.cast(typing.Optional[typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewaySslProfile]], jsii.get(self, "sslProfile"))

    @builtins.property
    @jsii.member(jsii_name="subnet")
    def subnet(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_subnet_92bbcedf.Subnet]:
        '''Optional subnet for the Application Gateway.'''
        return typing.cast(typing.Optional[_cdktf_cdktf_provider_azurerm_subnet_92bbcedf.Subnet], jsii.get(self, "subnet"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional tags for the Application Gateway resource.'''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> typing.Optional[builtins.str]:
        '''Optional tenant ID for use with Key Vault, if applicable.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantId"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayTimeouts]:
        '''Optional timeout settings for the Application Gateway resources.'''
        return typing.cast(typing.Optional[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayTimeouts], jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="trustedClientCertificate")
    def trusted_client_certificate(
        self,
    ) -> typing.Optional[typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayTrustedClientCertificate]]:
        '''Optional trusted client certificates for mutual authentication.'''
        return typing.cast(typing.Optional[typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayTrustedClientCertificate]], jsii.get(self, "trustedClientCertificate"))

    @builtins.property
    @jsii.member(jsii_name="trustedRootCertificate")
    def trusted_root_certificate(
        self,
    ) -> typing.Optional[typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayTrustedRootCertificate]]:
        '''Optional trusted root certificates for backend authentication.'''
        return typing.cast(typing.Optional[typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayTrustedRootCertificate]], jsii.get(self, "trustedRootCertificate"))

    @builtins.property
    @jsii.member(jsii_name="urlPathMap")
    def url_path_map(
        self,
    ) -> typing.Optional[typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayUrlPathMap]]:
        '''Optional URL path map for routing based on URL paths.'''
        return typing.cast(typing.Optional[typing.List[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayUrlPathMap]], jsii.get(self, "urlPathMap"))

    @builtins.property
    @jsii.member(jsii_name="wafConfiguration")
    def waf_configuration(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayWafConfiguration]:
        '''Optional Web Application Firewall (WAF) configuration to provide enhanced security.'''
        return typing.cast(typing.Optional[_cdktf_cdktf_provider_azurerm_application_gateway_92bbcedf.ApplicationGatewayWafConfiguration], jsii.get(self, "wafConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="zones")
    def zones(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional availability zones for the Application Gateway.'''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "zones"))

    @builtins.property
    @jsii.member(jsii_name="privateIpAddress")
    def private_ip_address(self) -> typing.Optional[builtins.str]:
        '''Optional private IP address for the frontend of the Application Gateway.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateIpAddress"))

    @private_ip_address.setter
    def private_ip_address(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbaf5601517121ecf3e6c5bfbad398d6fc66732abcefaee3fc48616ef5b33f11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateIpAddress", value)

    @builtins.property
    @jsii.member(jsii_name="privateIpAddressAllocation")
    def private_ip_address_allocation(self) -> typing.Optional[builtins.str]:
        '''Allocation method for the private IP address (e.g., Static, Dynamic).'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateIpAddressAllocation"))

    @private_ip_address_allocation.setter
    def private_ip_address_allocation(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29ab46a33a4233e4bfcca45f824126ded626c5f17eddf67d7aa1ba5b8c01b307)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateIpAddressAllocation", value)

    @builtins.property
    @jsii.member(jsii_name="publicIpAddress")
    def public_ip_address(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_public_ip_92bbcedf.PublicIp]:
        '''Optional public IP address for the frontend of the Application Gateway.'''
        return typing.cast(typing.Optional[_cdktf_cdktf_provider_azurerm_public_ip_92bbcedf.PublicIp], jsii.get(self, "publicIpAddress"))

    @public_ip_address.setter
    def public_ip_address(
        self,
        value: typing.Optional[_cdktf_cdktf_provider_azurerm_public_ip_92bbcedf.PublicIp],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3f2be42b8d8580dbbe0e634eca503316a293e223d4118caac90eb4c45772d46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicIpAddress", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGatewayProps).__jsii_proxy_class__ = lambda : _IGatewayPropsProxy


__all__ = [
    "Gateway",
    "IGatewayProps",
]

publication.publish()

def _typecheckingstub__70268ba9e307d3454870ee0057f05b3b009f0dd65bf5374e1cbc7bcc7fbf8c15(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    props: IGatewayProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b61d2d601d949705a9855d8c64b55d0bffb323d9b834e4cee097484d2df53178(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6551808057430f5a4eed594f7a9df507a653f2aa7d6d3dabb9cf55796fc6ebd2(
    value: _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbaf5601517121ecf3e6c5bfbad398d6fc66732abcefaee3fc48616ef5b33f11(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29ab46a33a4233e4bfcca45f824126ded626c5f17eddf67d7aa1ba5b8c01b307(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3f2be42b8d8580dbbe0e634eca503316a293e223d4118caac90eb4c45772d46(
    value: typing.Optional[_cdktf_cdktf_provider_azurerm_public_ip_92bbcedf.PublicIp],
) -> None:
    """Type checking stubs"""
    pass
