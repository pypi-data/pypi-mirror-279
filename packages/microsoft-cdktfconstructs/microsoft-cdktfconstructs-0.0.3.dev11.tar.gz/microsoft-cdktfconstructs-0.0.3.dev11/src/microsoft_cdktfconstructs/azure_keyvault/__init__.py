'''
# Azure Key Vault Construct

This class represents a Key Vault in Azure. It provides a convenient way to manage Azure Key Vault resources.

## What is Azure Key Vault?

Azure Key Vault is a service for securely storing and accessing secrets. A secret is anything that you want to tightly control access to, such as API keys, passwords, certificates, or cryptographic keys.

You can learn more about Azure Key Vault in the [official Azure documentation](https://docs.microsoft.com/en-us/azure/key-vault/general/overview).

## Key Vault Best Practices

* Consolidate your secrets, keys, and certificates into as few key vaults as possible.
* Use Azure RBAC roles for Key Vault for fine-grained access control.
* Enable soft delete and purge protection to prevent accidental deletion of secrets.
* Use Managed identities with Key Vault where possible.

## Key Vault Class Properties

This class has several properties that control the Key Vault's behaviour:

* `name`: The name of the Key Vault.
* `location`: The Azure Region where the Key Vault will be deployed.
* `resource_group_name`: The name of the Azure Resource Group.
* `tags`: The tags to assign to the Key Vault.
* `sku`: The Name of the SKU used for this Key Vault. Possible values are `standard` and `premium`.
* `tenant_id`: The Azure Active Directory tenant ID that should be used for authenticating requests to the key vault.

## Deploying the Key Vault

You can deploy a Key Vault using this class like so:

```python
const azureKeyVault = new AzureKeyVault(this, 'myKeyVault', {
  name: 'myKeyVault',
  location: 'West US',
  resource_group_name: 'myResourceGroup',
  sku: 'standard',
  tenant_id: 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx',
  tags: {
    'env': 'production',
  },
});
```

This code will create a new Key Vault named myKeyVault in the West US Azure region with a production environment tag. The vault belongs to the resource group myResourceGroup, uses the standard pricing model, and will authenticate requests using the provided tenant ID.
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

import cdktf_cdktf_provider_azurerm.key_vault as _cdktf_cdktf_provider_azurerm_key_vault_92bbcedf
import cdktf_cdktf_provider_azurerm.key_vault_certificate as _cdktf_cdktf_provider_azurerm_key_vault_certificate_92bbcedf
import cdktf_cdktf_provider_azurerm.key_vault_key as _cdktf_cdktf_provider_azurerm_key_vault_key_92bbcedf
import cdktf_cdktf_provider_azurerm.resource_group as _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf
import constructs as _constructs_77d1e7e8
from ..core_azure import AzureResource as _AzureResource_74eec1c4


class AccessPolicy(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@microsoft/terraform-cdk-constructs.azure_keyvault.AccessPolicy",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        key_vault_id: "Vault",
        object_id: builtins.str,
        tenant_id: builtins.str,
        certificate_permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
        key_permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
        secret_permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
        storage_permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Constructs a new Access Policy for Azure Key Vault.

        This class is responsible for setting up access policies that define what operations an Azure AD identity
        can perform on the keys, secrets, certificates, and storage accounts within a specified Azure Key Vault.

        :param scope: - The scope in which to define this construct, usually representing the Cloud Development Kit (CDK) stack.
        :param id: - The unique identifier for this instance of the access policy.
        :param key_vault_id: The Azure Key Vault instance or its identifier.
        :param object_id: The Azure Active Directory object ID for which the policy will be applied. This can be a user, group, or service principal.
        :param tenant_id: The Azure Active Directory tenant ID where the Key Vault is hosted. This is typically the directory ID of your Azure AD.
        :param certificate_permissions: The permissions to certificates stored in the Key Vault. Possible values might include: 'get', 'list', 'create', 'update', etc. If not provided, no certificate permissions are set.
        :param key_permissions: The permissions to keys stored in the Key Vault. Possible values might include: 'get', 'list', 'create', 'sign', etc. If not provided, no key permissions are set.
        :param secret_permissions: The permissions to secrets stored in the Key Vault. Possible values might include: 'get', 'list', 'set', 'delete', etc. If not provided, no secret permissions are set.
        :param storage_permissions: The permissions to storage accounts linked to the Key Vault. Possible values might include: 'get', 'list', 'delete', 'set', etc. If not provided, no storage permissions are set.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd7fc0b79a19acf1e5e94e93e6997a8d5f2b15e90adea376529cae5a756db705)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AccessPolicyProps(
            key_vault_id=key_vault_id,
            object_id=object_id,
            tenant_id=tenant_id,
            certificate_permissions=certificate_permissions,
            key_permissions=key_permissions,
            secret_permissions=secret_permissions,
            storage_permissions=storage_permissions,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="fqdn")
    def fqdn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fqdn"))


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_keyvault.AccessPolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "key_vault_id": "keyVaultId",
        "object_id": "objectId",
        "tenant_id": "tenantId",
        "certificate_permissions": "certificatePermissions",
        "key_permissions": "keyPermissions",
        "secret_permissions": "secretPermissions",
        "storage_permissions": "storagePermissions",
    },
)
class AccessPolicyProps:
    def __init__(
        self,
        *,
        key_vault_id: "Vault",
        object_id: builtins.str,
        tenant_id: builtins.str,
        certificate_permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
        key_permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
        secret_permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
        storage_permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param key_vault_id: The Azure Key Vault instance or its identifier.
        :param object_id: The Azure Active Directory object ID for which the policy will be applied. This can be a user, group, or service principal.
        :param tenant_id: The Azure Active Directory tenant ID where the Key Vault is hosted. This is typically the directory ID of your Azure AD.
        :param certificate_permissions: The permissions to certificates stored in the Key Vault. Possible values might include: 'get', 'list', 'create', 'update', etc. If not provided, no certificate permissions are set.
        :param key_permissions: The permissions to keys stored in the Key Vault. Possible values might include: 'get', 'list', 'create', 'sign', etc. If not provided, no key permissions are set.
        :param secret_permissions: The permissions to secrets stored in the Key Vault. Possible values might include: 'get', 'list', 'set', 'delete', etc. If not provided, no secret permissions are set.
        :param storage_permissions: The permissions to storage accounts linked to the Key Vault. Possible values might include: 'get', 'list', 'delete', 'set', etc. If not provided, no storage permissions are set.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cfe410d8def41b97bf697999052e8eae3ba4691c72f03f9db1d7275baf6ed07)
            check_type(argname="argument key_vault_id", value=key_vault_id, expected_type=type_hints["key_vault_id"])
            check_type(argname="argument object_id", value=object_id, expected_type=type_hints["object_id"])
            check_type(argname="argument tenant_id", value=tenant_id, expected_type=type_hints["tenant_id"])
            check_type(argname="argument certificate_permissions", value=certificate_permissions, expected_type=type_hints["certificate_permissions"])
            check_type(argname="argument key_permissions", value=key_permissions, expected_type=type_hints["key_permissions"])
            check_type(argname="argument secret_permissions", value=secret_permissions, expected_type=type_hints["secret_permissions"])
            check_type(argname="argument storage_permissions", value=storage_permissions, expected_type=type_hints["storage_permissions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key_vault_id": key_vault_id,
            "object_id": object_id,
            "tenant_id": tenant_id,
        }
        if certificate_permissions is not None:
            self._values["certificate_permissions"] = certificate_permissions
        if key_permissions is not None:
            self._values["key_permissions"] = key_permissions
        if secret_permissions is not None:
            self._values["secret_permissions"] = secret_permissions
        if storage_permissions is not None:
            self._values["storage_permissions"] = storage_permissions

    @builtins.property
    def key_vault_id(self) -> "Vault":
        '''The Azure Key Vault instance or its identifier.'''
        result = self._values.get("key_vault_id")
        assert result is not None, "Required property 'key_vault_id' is missing"
        return typing.cast("Vault", result)

    @builtins.property
    def object_id(self) -> builtins.str:
        '''The Azure Active Directory object ID for which the policy will be applied.

        This can be a user, group, or service principal.
        '''
        result = self._values.get("object_id")
        assert result is not None, "Required property 'object_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tenant_id(self) -> builtins.str:
        '''The Azure Active Directory tenant ID where the Key Vault is hosted.

        This is typically the directory ID of your Azure AD.
        '''
        result = self._values.get("tenant_id")
        assert result is not None, "Required property 'tenant_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def certificate_permissions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The permissions to certificates stored in the Key Vault.

        Possible values might include: 'get', 'list', 'create', 'update', etc.
        If not provided, no certificate permissions are set.
        '''
        result = self._values.get("certificate_permissions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def key_permissions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The permissions to keys stored in the Key Vault.

        Possible values might include: 'get', 'list', 'create', 'sign', etc.
        If not provided, no key permissions are set.
        '''
        result = self._values.get("key_permissions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def secret_permissions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The permissions to secrets stored in the Key Vault.

        Possible values might include: 'get', 'list', 'set', 'delete', etc.
        If not provided, no secret permissions are set.
        '''
        result = self._values.get("secret_permissions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def storage_permissions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The permissions to storage accounts linked to the Key Vault.

        Possible values might include: 'get', 'list', 'delete', 'set', etc.
        If not provided, no storage permissions are set.
        '''
        result = self._values.get("storage_permissions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CertificateIssuer(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@microsoft/terraform-cdk-constructs.azure_keyvault.CertificateIssuer",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        access_policies: typing.Sequence[AccessPolicy],
        key_vault_id: "Vault",
        name: builtins.str,
        provider_name: builtins.str,
        password: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Constructs a new Certificate Issuer within an Azure Key Vault.

        This class is responsible for setting up a certificate issuer in Azure Key Vault. A certificate issuer is an entity
        that issues digital certificates for use in SSL/TLS and other cryptographic security contexts. By configuring an issuer,
        you can manage certificate lifecycle (issue, renew, revoke) through Azure Key Vault in conjunction with external certificate
        authorities (CAs).

        :param scope: - The scope in which to define this construct, usually representing the Cloud Development Kit (CDK) stack.
        :param id: - The unique identifier for this instance of the certificate issuer.
        :param access_policies: Access policies defining who can manage this issuer and the certificates it issues within the Key Vault.
        :param key_vault_id: The ID of the Azure Key Vault where the issuer will be configured.
        :param name: The name of the certificate issuer as it will appear in Azure Key Vault.
        :param provider_name: The name of the provider that will issue the certificate, such as 'DigiCert' or 'GlobalSign'.
        :param password: The password required to authenticate with the certificate provider (if applicable).
        :param username: The username required to authenticate with the certificate provider (if applicable).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fd1d912631fc8dde1a769566e3ea99baf2954d0af16be561aae29ad55ace25b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CertificateIssuerProps(
            access_policies=access_policies,
            key_vault_id=key_vault_id,
            name=name,
            provider_name=provider_name,
            password=password,
            username=username,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_keyvault.CertificateIssuerProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_policies": "accessPolicies",
        "key_vault_id": "keyVaultId",
        "name": "name",
        "provider_name": "providerName",
        "password": "password",
        "username": "username",
    },
)
class CertificateIssuerProps:
    def __init__(
        self,
        *,
        access_policies: typing.Sequence[AccessPolicy],
        key_vault_id: "Vault",
        name: builtins.str,
        provider_name: builtins.str,
        password: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties required to configure a certificate issuer within Azure Key Vault.

        :param access_policies: Access policies defining who can manage this issuer and the certificates it issues within the Key Vault.
        :param key_vault_id: The ID of the Azure Key Vault where the issuer will be configured.
        :param name: The name of the certificate issuer as it will appear in Azure Key Vault.
        :param provider_name: The name of the provider that will issue the certificate, such as 'DigiCert' or 'GlobalSign'.
        :param password: The password required to authenticate with the certificate provider (if applicable).
        :param username: The username required to authenticate with the certificate provider (if applicable).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5040b69059943a548e408c33cf899a9e5cd1230fcfac175e830c76b10642f504)
            check_type(argname="argument access_policies", value=access_policies, expected_type=type_hints["access_policies"])
            check_type(argname="argument key_vault_id", value=key_vault_id, expected_type=type_hints["key_vault_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument provider_name", value=provider_name, expected_type=type_hints["provider_name"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_policies": access_policies,
            "key_vault_id": key_vault_id,
            "name": name,
            "provider_name": provider_name,
        }
        if password is not None:
            self._values["password"] = password
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def access_policies(self) -> typing.List[AccessPolicy]:
        '''Access policies defining who can manage this issuer and the certificates it issues within the Key Vault.'''
        result = self._values.get("access_policies")
        assert result is not None, "Required property 'access_policies' is missing"
        return typing.cast(typing.List[AccessPolicy], result)

    @builtins.property
    def key_vault_id(self) -> "Vault":
        '''The ID of the Azure Key Vault where the issuer will be configured.'''
        result = self._values.get("key_vault_id")
        assert result is not None, "Required property 'key_vault_id' is missing"
        return typing.cast("Vault", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the certificate issuer as it will appear in Azure Key Vault.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def provider_name(self) -> builtins.str:
        '''The name of the provider that will issue the certificate, such as 'DigiCert' or 'GlobalSign'.'''
        result = self._values.get("provider_name")
        assert result is not None, "Required property 'provider_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''The password required to authenticate with the certificate provider (if applicable).'''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''The username required to authenticate with the certificate provider (if applicable).'''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CertificateIssuerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_keyvault.GrantCustomAccessOptions",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_permissions": "certificatePermissions",
        "key_permissions": "keyPermissions",
        "secret_permissions": "secretPermissions",
        "storage_permissions": "storagePermissions",
    },
)
class GrantCustomAccessOptions:
    def __init__(
        self,
        *,
        certificate_permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
        key_permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
        secret_permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
        storage_permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Options for granting custom access permissions in Azure Key Vault.

        :param certificate_permissions: Optional: A list of permissions to grant for certificates in the Key Vault. Example permissions include 'get', 'list', 'create', 'delete', etc.
        :param key_permissions: Optional: A list of permissions to grant for keys in the Key Vault. Example permissions include 'encrypt', 'decrypt', 'wrapKey', 'unwrapKey', etc.
        :param secret_permissions: Optional: A list of permissions to grant for secrets in the Key Vault. Example permissions include 'get', 'list', 'set', 'delete', etc.
        :param storage_permissions: Optional: A list of permissions to grant for storage accounts in the Key Vault. Example permissions include 'get', 'list', 'delete', 'set', 'update', etc.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3436fd84bf104b1bc8cd30d3eb2faadc0f58a40d1eabbb47d487be7507134cd7)
            check_type(argname="argument certificate_permissions", value=certificate_permissions, expected_type=type_hints["certificate_permissions"])
            check_type(argname="argument key_permissions", value=key_permissions, expected_type=type_hints["key_permissions"])
            check_type(argname="argument secret_permissions", value=secret_permissions, expected_type=type_hints["secret_permissions"])
            check_type(argname="argument storage_permissions", value=storage_permissions, expected_type=type_hints["storage_permissions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if certificate_permissions is not None:
            self._values["certificate_permissions"] = certificate_permissions
        if key_permissions is not None:
            self._values["key_permissions"] = key_permissions
        if secret_permissions is not None:
            self._values["secret_permissions"] = secret_permissions
        if storage_permissions is not None:
            self._values["storage_permissions"] = storage_permissions

    @builtins.property
    def certificate_permissions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional: A list of permissions to grant for certificates in the Key Vault.

        Example permissions include 'get', 'list', 'create', 'delete', etc.
        '''
        result = self._values.get("certificate_permissions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def key_permissions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional: A list of permissions to grant for keys in the Key Vault.

        Example permissions include 'encrypt', 'decrypt', 'wrapKey', 'unwrapKey', etc.
        '''
        result = self._values.get("key_permissions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def secret_permissions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional: A list of permissions to grant for secrets in the Key Vault.

        Example permissions include 'get', 'list', 'set', 'delete', etc.
        '''
        result = self._values.get("secret_permissions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def storage_permissions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional: A list of permissions to grant for storage accounts in the Key Vault.

        Example permissions include 'get', 'list', 'delete', 'set', 'update', etc.
        '''
        result = self._values.get("storage_permissions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GrantCustomAccessOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Key(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@microsoft/terraform-cdk-constructs.azure_keyvault.Key",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        access_policies: typing.Sequence[AccessPolicy],
        key_opts: typing.Sequence[builtins.str],
        key_type: builtins.str,
        key_vault_id: "Vault",
        name: builtins.str,
        expires: typing.Optional[builtins.str] = None,
        key_size: typing.Optional[jsii.Number] = None,
        rotation_policy: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_key_vault_key_92bbcedf.KeyVaultKeyRotationPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Constructs a new Key resource in Azure Key Vault.

        This class is responsible for the creation and management of a cryptographic key stored in Azure Key Vault.
        The key can be used for a variety of cryptographic operations, such as encryption, decryption, signing, or
        verifying signatures, depending on the permissions granted. It supports different key types and configurations,
        allowing for customization to meet specific security requirements.

        :param scope: - The scope in which to define this construct, usually representing the Cloud Development Kit (CDK) stack.
        :param id: - The unique identifier for this instance of the Key.
        :param access_policies: 
        :param key_opts: Additional options or attributes related to the key.
        :param key_type: The type of key to create (e.g., RSA, EC, etc.).
        :param key_vault_id: 
        :param name: The name of the key in the Azure Key Vault.
        :param expires: Expiration date of the key. Format: UTC, YYYY-MM-DDTHH:MM:SSZ.
        :param key_size: The size of the key, typically specified for RSA keys.
        :param rotation_policy: The policy for key rotation.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__764ad04fbd1fc7abfe91c3ca71a3f0df1b038969bfda7c952f3021ce45b03094)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = KeyProps(
            access_policies=access_policies,
            key_opts=key_opts,
            key_type=key_type,
            key_vault_id=key_vault_id,
            name=name,
            expires=expires,
            key_size=key_size,
            rotation_policy=rotation_policy,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="vaultKey")
    def vault_key(
        self,
    ) -> _cdktf_cdktf_provider_azurerm_key_vault_key_92bbcedf.KeyVaultKey:
        return typing.cast(_cdktf_cdktf_provider_azurerm_key_vault_key_92bbcedf.KeyVaultKey, jsii.get(self, "vaultKey"))

    @vault_key.setter
    def vault_key(
        self,
        value: _cdktf_cdktf_provider_azurerm_key_vault_key_92bbcedf.KeyVaultKey,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f2906c60b67daeedd0649a513a69c7c29965637edc934b937264e3d9e84d21f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vaultKey", value)


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_keyvault.KeyProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_policies": "accessPolicies",
        "key_opts": "keyOpts",
        "key_type": "keyType",
        "key_vault_id": "keyVaultId",
        "name": "name",
        "expires": "expires",
        "key_size": "keySize",
        "rotation_policy": "rotationPolicy",
    },
)
class KeyProps:
    def __init__(
        self,
        *,
        access_policies: typing.Sequence[AccessPolicy],
        key_opts: typing.Sequence[builtins.str],
        key_type: builtins.str,
        key_vault_id: "Vault",
        name: builtins.str,
        expires: typing.Optional[builtins.str] = None,
        key_size: typing.Optional[jsii.Number] = None,
        rotation_policy: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_key_vault_key_92bbcedf.KeyVaultKeyRotationPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param access_policies: 
        :param key_opts: Additional options or attributes related to the key.
        :param key_type: The type of key to create (e.g., RSA, EC, etc.).
        :param key_vault_id: 
        :param name: The name of the key in the Azure Key Vault.
        :param expires: Expiration date of the key. Format: UTC, YYYY-MM-DDTHH:MM:SSZ.
        :param key_size: The size of the key, typically specified for RSA keys.
        :param rotation_policy: The policy for key rotation.
        '''
        if isinstance(rotation_policy, dict):
            rotation_policy = _cdktf_cdktf_provider_azurerm_key_vault_key_92bbcedf.KeyVaultKeyRotationPolicy(**rotation_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__995ed0d726015be1e472d81cda4bb9836358aa4c155e115c8314614e4171b257)
            check_type(argname="argument access_policies", value=access_policies, expected_type=type_hints["access_policies"])
            check_type(argname="argument key_opts", value=key_opts, expected_type=type_hints["key_opts"])
            check_type(argname="argument key_type", value=key_type, expected_type=type_hints["key_type"])
            check_type(argname="argument key_vault_id", value=key_vault_id, expected_type=type_hints["key_vault_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument expires", value=expires, expected_type=type_hints["expires"])
            check_type(argname="argument key_size", value=key_size, expected_type=type_hints["key_size"])
            check_type(argname="argument rotation_policy", value=rotation_policy, expected_type=type_hints["rotation_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_policies": access_policies,
            "key_opts": key_opts,
            "key_type": key_type,
            "key_vault_id": key_vault_id,
            "name": name,
        }
        if expires is not None:
            self._values["expires"] = expires
        if key_size is not None:
            self._values["key_size"] = key_size
        if rotation_policy is not None:
            self._values["rotation_policy"] = rotation_policy

    @builtins.property
    def access_policies(self) -> typing.List[AccessPolicy]:
        result = self._values.get("access_policies")
        assert result is not None, "Required property 'access_policies' is missing"
        return typing.cast(typing.List[AccessPolicy], result)

    @builtins.property
    def key_opts(self) -> typing.List[builtins.str]:
        '''Additional options or attributes related to the key.'''
        result = self._values.get("key_opts")
        assert result is not None, "Required property 'key_opts' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def key_type(self) -> builtins.str:
        '''The type of key to create (e.g., RSA, EC, etc.).'''
        result = self._values.get("key_type")
        assert result is not None, "Required property 'key_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key_vault_id(self) -> "Vault":
        result = self._values.get("key_vault_id")
        assert result is not None, "Required property 'key_vault_id' is missing"
        return typing.cast("Vault", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the key in the Azure Key Vault.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def expires(self) -> typing.Optional[builtins.str]:
        '''Expiration date of the key.

        Format: UTC, YYYY-MM-DDTHH:MM:SSZ.
        '''
        result = self._values.get("expires")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_size(self) -> typing.Optional[jsii.Number]:
        '''The size of the key, typically specified for RSA keys.'''
        result = self._values.get("key_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def rotation_policy(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_key_vault_key_92bbcedf.KeyVaultKeyRotationPolicy]:
        '''The policy for key rotation.'''
        result = self._values.get("rotation_policy")
        return typing.cast(typing.Optional[_cdktf_cdktf_provider_azurerm_key_vault_key_92bbcedf.KeyVaultKeyRotationPolicy], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KeyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Secret(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@microsoft/terraform-cdk-constructs.azure_keyvault.Secret",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        access_policies: typing.Sequence[AccessPolicy],
        key_vault_id: "Vault",
        name: builtins.str,
        value: builtins.str,
        content_type: typing.Optional[builtins.str] = None,
        expiration_date: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Constructs a new Azure Key Vault Secret within a specified Key Vault.

        This class facilitates the creation and management of a secret, allowing sensitive information to be stored securely
        and accessed as needed while maintaining confidentiality and control through defined access policies.

        :param scope: - The scope in which to define this construct, typically representing the Cloud Development Kit (CDK) stack.
        :param id: - The unique identifier for this instance of the secret.
        :param access_policies: A list of access policies that dictate which identities have what kind of access to the secret. Each policy should detail the permissions and the identity it applies to.
        :param key_vault_id: The Key Vault instance where the secret will be stored.
        :param name: The name of the secret. This name should be unique within the Key Vault instance.
        :param value: The value of the secret. This could be any string, including tokens or passwords.
        :param content_type: Optional content type for the secret. This can be used to describe the type of information the secret contains, or how it can be used.
        :param expiration_date: Optional expiration date for the secret. This should be in an appropriate date string format. If provided, the secret will become invalid after this date.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c78df4e95e03e93ef044f647b9b99dcad3c39f1844594b182e977b52617317f7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SecretProps(
            access_policies=access_policies,
            key_vault_id=key_vault_id,
            name=name,
            value=value,
            content_type=content_type,
            expiration_date=expiration_date,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="secretId")
    def secret_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretId"))

    @secret_id.setter
    def secret_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__000957c0b227f3cb3e6b4710c4ff0c1439839536ed2dd1e6444c6440ae47007c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretId", value)


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_keyvault.SecretProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_policies": "accessPolicies",
        "key_vault_id": "keyVaultId",
        "name": "name",
        "value": "value",
        "content_type": "contentType",
        "expiration_date": "expirationDate",
    },
)
class SecretProps:
    def __init__(
        self,
        *,
        access_policies: typing.Sequence[AccessPolicy],
        key_vault_id: "Vault",
        name: builtins.str,
        value: builtins.str,
        content_type: typing.Optional[builtins.str] = None,
        expiration_date: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining an Azure Key Vault Secret.

        :param access_policies: A list of access policies that dictate which identities have what kind of access to the secret. Each policy should detail the permissions and the identity it applies to.
        :param key_vault_id: The Key Vault instance where the secret will be stored.
        :param name: The name of the secret. This name should be unique within the Key Vault instance.
        :param value: The value of the secret. This could be any string, including tokens or passwords.
        :param content_type: Optional content type for the secret. This can be used to describe the type of information the secret contains, or how it can be used.
        :param expiration_date: Optional expiration date for the secret. This should be in an appropriate date string format. If provided, the secret will become invalid after this date.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d36fbfdf3b4d23e5fe773f0713f10351c70db1fa84f549499f9d58b8ed1ee3f)
            check_type(argname="argument access_policies", value=access_policies, expected_type=type_hints["access_policies"])
            check_type(argname="argument key_vault_id", value=key_vault_id, expected_type=type_hints["key_vault_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument content_type", value=content_type, expected_type=type_hints["content_type"])
            check_type(argname="argument expiration_date", value=expiration_date, expected_type=type_hints["expiration_date"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_policies": access_policies,
            "key_vault_id": key_vault_id,
            "name": name,
            "value": value,
        }
        if content_type is not None:
            self._values["content_type"] = content_type
        if expiration_date is not None:
            self._values["expiration_date"] = expiration_date

    @builtins.property
    def access_policies(self) -> typing.List[AccessPolicy]:
        '''A list of access policies that dictate which identities have what kind of access to the secret.

        Each policy should detail the permissions and the identity it applies to.
        '''
        result = self._values.get("access_policies")
        assert result is not None, "Required property 'access_policies' is missing"
        return typing.cast(typing.List[AccessPolicy], result)

    @builtins.property
    def key_vault_id(self) -> "Vault":
        '''The Key Vault instance where the secret will be stored.'''
        result = self._values.get("key_vault_id")
        assert result is not None, "Required property 'key_vault_id' is missing"
        return typing.cast("Vault", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the secret.

        This name should be unique within the Key Vault instance.
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''The value of the secret.

        This could be any string, including tokens or passwords.
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def content_type(self) -> typing.Optional[builtins.str]:
        '''Optional content type for the secret.

        This can be used to describe the type of information
        the secret contains, or how it can be used.
        '''
        result = self._values.get("content_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expiration_date(self) -> typing.Optional[builtins.str]:
        '''Optional expiration date for the secret.

        This should be in an appropriate date string format.
        If provided, the secret will become invalid after this date.
        '''
        result = self._values.get("expiration_date")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SelfSignedCertificate(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@microsoft/terraform-cdk-constructs.azure_keyvault.SelfSignedCertificate",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        access_policies: typing.Sequence[AccessPolicy],
        dns_names: typing.Sequence[builtins.str],
        key_vault_id: "Vault",
        name: builtins.str,
        subject: builtins.str,
        action_type: typing.Optional[builtins.str] = None,
        days_before_expiry: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Constructs a self-signed certificate within an Azure Key Vault.

        This class is responsible for the creation and management of a self-signed certificate, making it available
        within an Azure Key Vault. The certificate can be used for testing or internal secure communications.

        :param scope: - The scope in which to define this construct, usually representing the Cloud Development Kit (CDK) stack.
        :param id: - The unique identifier for this instance of the certificate.
        :param access_policies: Access policies defining who can access this certificate within the Azure Key Vault.
        :param dns_names: Additional DNS names to be included in the certificate. Useful for creating certificates valid for multiple hostnames.
        :param key_vault_id: The ID of the Azure Key Vault where the certificate will be created and stored.
        :param name: The name of the certificate to be stored in Azure Key Vault.
        :param subject: The subject name for the certificate, typically represented in X.509 distinguished name format.
        :param action_type: Specifies the type of action to perform with the certificate, such as 'create' or 'renew'.
        :param days_before_expiry: Specifies the number of days before expiry when an action should be taken (e.g., renew the certificate).
        :param tags: Tags to be associated with the certificate for organizational purposes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f2fd11aff992ca62fdb1d32287ac5e70f490e423a8220d0fd8b93f168423e61)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SelfSignedCertificateProps(
            access_policies=access_policies,
            dns_names=dns_names,
            key_vault_id=key_vault_id,
            name=name,
            subject=subject,
            action_type=action_type,
            days_before_expiry=days_before_expiry,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(
        self,
    ) -> _cdktf_cdktf_provider_azurerm_key_vault_certificate_92bbcedf.KeyVaultCertificate:
        return typing.cast(_cdktf_cdktf_provider_azurerm_key_vault_certificate_92bbcedf.KeyVaultCertificate, jsii.get(self, "certificate"))

    @certificate.setter
    def certificate(
        self,
        value: _cdktf_cdktf_provider_azurerm_key_vault_certificate_92bbcedf.KeyVaultCertificate,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bcfe32dfda0bfcd75c9886c46d00ae6fe55b59fe44815138f1c45bade1a9a50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificate", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a7832291886fb9d0860c4fe02c693ab9a897d39b628a7dbe1eda21608cd7bbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="secretId")
    def secret_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretId"))

    @secret_id.setter
    def secret_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9590e40faef06e65b262dcbee4614c369cb45c54a88a331ceaf27f397ea5dba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretId", value)


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_keyvault.SelfSignedCertificateProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_policies": "accessPolicies",
        "dns_names": "dnsNames",
        "key_vault_id": "keyVaultId",
        "name": "name",
        "subject": "subject",
        "action_type": "actionType",
        "days_before_expiry": "daysBeforeExpiry",
        "tags": "tags",
    },
)
class SelfSignedCertificateProps:
    def __init__(
        self,
        *,
        access_policies: typing.Sequence[AccessPolicy],
        dns_names: typing.Sequence[builtins.str],
        key_vault_id: "Vault",
        name: builtins.str,
        subject: builtins.str,
        action_type: typing.Optional[builtins.str] = None,
        days_before_expiry: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties required to create a self-signed certificate within Azure Key Vault.

        :param access_policies: Access policies defining who can access this certificate within the Azure Key Vault.
        :param dns_names: Additional DNS names to be included in the certificate. Useful for creating certificates valid for multiple hostnames.
        :param key_vault_id: The ID of the Azure Key Vault where the certificate will be created and stored.
        :param name: The name of the certificate to be stored in Azure Key Vault.
        :param subject: The subject name for the certificate, typically represented in X.509 distinguished name format.
        :param action_type: Specifies the type of action to perform with the certificate, such as 'create' or 'renew'.
        :param days_before_expiry: Specifies the number of days before expiry when an action should be taken (e.g., renew the certificate).
        :param tags: Tags to be associated with the certificate for organizational purposes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e1a75ff875f51795d8bc81864b6795d51c7ecac35b8f6a4b8aea44373ec77ea)
            check_type(argname="argument access_policies", value=access_policies, expected_type=type_hints["access_policies"])
            check_type(argname="argument dns_names", value=dns_names, expected_type=type_hints["dns_names"])
            check_type(argname="argument key_vault_id", value=key_vault_id, expected_type=type_hints["key_vault_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument subject", value=subject, expected_type=type_hints["subject"])
            check_type(argname="argument action_type", value=action_type, expected_type=type_hints["action_type"])
            check_type(argname="argument days_before_expiry", value=days_before_expiry, expected_type=type_hints["days_before_expiry"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_policies": access_policies,
            "dns_names": dns_names,
            "key_vault_id": key_vault_id,
            "name": name,
            "subject": subject,
        }
        if action_type is not None:
            self._values["action_type"] = action_type
        if days_before_expiry is not None:
            self._values["days_before_expiry"] = days_before_expiry
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def access_policies(self) -> typing.List[AccessPolicy]:
        '''Access policies defining who can access this certificate within the Azure Key Vault.'''
        result = self._values.get("access_policies")
        assert result is not None, "Required property 'access_policies' is missing"
        return typing.cast(typing.List[AccessPolicy], result)

    @builtins.property
    def dns_names(self) -> typing.List[builtins.str]:
        '''Additional DNS names to be included in the certificate.

        Useful for creating certificates valid for multiple hostnames.
        '''
        result = self._values.get("dns_names")
        assert result is not None, "Required property 'dns_names' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def key_vault_id(self) -> "Vault":
        '''The ID of the Azure Key Vault where the certificate will be created and stored.'''
        result = self._values.get("key_vault_id")
        assert result is not None, "Required property 'key_vault_id' is missing"
        return typing.cast("Vault", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the certificate to be stored in Azure Key Vault.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subject(self) -> builtins.str:
        '''The subject name for the certificate, typically represented in X.509 distinguished name format.'''
        result = self._values.get("subject")
        assert result is not None, "Required property 'subject' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def action_type(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of action to perform with the certificate, such as 'create' or 'renew'.'''
        result = self._values.get("action_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def days_before_expiry(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of days before expiry when an action should be taken (e.g., renew the certificate).'''
        result = self._values.get("days_before_expiry")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Tags to be associated with the certificate for organizational purposes.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SelfSignedCertificateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Vault(
    _AzureResource_74eec1c4,
    metaclass=jsii.JSIIMeta,
    jsii_type="@microsoft/terraform-cdk-constructs.azure_keyvault.Vault",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        tenant_id: builtins.str,
        network_acls: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_key_vault_92bbcedf.KeyVaultNetworkAcls, typing.Dict[builtins.str, typing.Any]]] = None,
        purge_protection: typing.Optional[builtins.bool] = None,
        resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
        sku: typing.Optional[builtins.str] = None,
        soft_delete_retention_days: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Constructs a new Azure Key Vault resource.

        This class creates and configures an Azure Key Vault, a secure store for managing secrets, keys, certificates, and other sensitive data.
        It supports advanced configurations such as access policies, network rules, and data retention policies.

        :param scope: - The scope in which to define this construct, usually representing the Cloud Development Kit (CDK) stack.
        :param id: - The unique identifier for this instance of the Key Vault.
        :param location: The Azure Region to deploy the Key Vault.
        :param name: The name of the Key Vault.
        :param tenant_id: The Name of the SKU used for this Key Vault. Possible values are standard and premium.
        :param network_acls: The Azure Active Directory tenant ID that should be used for authenticating requests to the key vault.
        :param purge_protection: A map of IP network ACL rules. The key is the IP or IP range in CIDR notation. The value is a description of that IP range.
        :param resource_group: An optional reference to the resource group in which to deploy the Key Vault. If not provided, the Key Vault will be deployed in the default resource group.
        :param sku: The tags to assign to the Key Vault.
        :param soft_delete_retention_days: Specifies whether protection against purge is enabled for this Key Vault. Setting this property to true activates protection against deletion of any active key, secret or certificate in the vault. The setting is effective only if soft delete is also enabled. The default value is false. Once activated, the property cannot be reverted to false.
        :param tags: The tags to assign to the Key Vault.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__917170a8774b61cb3259bde0d15c6881a93b9cdffe2a33390469fe5c8a9e2a05)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = VaultProps(
            location=location,
            name=name,
            tenant_id=tenant_id,
            network_acls=network_acls,
            purge_protection=purge_protection,
            resource_group=resource_group,
            sku=sku,
            soft_delete_retention_days=soft_delete_retention_days,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addCertIssuer")
    def add_cert_issuer(self, name: builtins.str, provider: builtins.str) -> None:
        '''Adds a certificate issuer to the Azure Key Vault.

        This method configures a certificate issuer within the Key Vault, allowing the Key Vault to issue certificates
        through external providers. Configuring an issuer is essential for enabling automated certificate management
        processes, such as issuance and renewal, directly through the Key Vault with a specified Certificate Authority (CA).

        :param name: - The unique name for the certificate issuer within the Key Vault.
        :param provider: - The name of the external provider that will issue the certificates, such as 'DigiCert' or 'GlobalSign'. Example usage:: vault.addCertIssuer( 'myCertIssuer', 'DigiCert' ); This method configures a certificate issuer but does not return any value. The issuer details, including provider name and any necessary credentials (managed externally or through additional method parameters), are set up in the Key Vault for future certificate operations.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2f2c045bea927ac556e9d63c71e26ab25277d8da73f00083296262c6f2b0d08)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(None, jsii.invoke(self, "addCertIssuer", [name, provider]))

    @jsii.member(jsii_name="addKey")
    def add_key(
        self,
        key_vault_key_name: builtins.str,
        key_type: builtins.str,
        key_size: jsii.Number,
        key_opts: typing.Sequence[builtins.str],
        expiration_date: typing.Optional[builtins.str] = None,
    ) -> _cdktf_cdktf_provider_azurerm_key_vault_key_92bbcedf.KeyVaultKey:
        '''Creates a cryptographic key within the Azure Key Vault.

        This method allows the creation of a cryptographic key of specified type and size within the Key Vault. The key can be
        configured with specific operations it can perform, such as encryption, decryption, signing, etc. An optional expiration
        date can also be set to control the key's lifecycle. This method is flexible, supporting various key types and sizes,
        making it suitable for a wide range of cryptographic needs.

        :param key_vault_key_name: - The unique name for the cryptographic key within the Key Vault.
        :param key_type: - The type of cryptographic key to create (e.g., 'RSA', 'EC', 'oct-HSM').
        :param key_size: - The size of the cryptographic key in bits (e.g., 2048, 3072, 4096 for RSA).
        :param key_opts: - A list of cryptographic operations that the key is allowed to perform. Possible values might include 'encrypt', 'decrypt', 'sign', 'verify', 'wrapKey', 'unwrapKey'.
        :param expiration_date: - Optional. The expiration date of the key in ISO 8601 format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ). If provided, the key will no longer be valid after this date, aligning with best practices for key management.

        :return:

        A KeyVaultKey object representing the newly created cryptographic key within the vault.

        Example usage::

        const myKey = vault.addKey(
        'myKey',
        'RSA',
        2048,
        ['encrypt', 'decrypt', 'sign', 'verify'],
        '2030-12-31'
        );

        This method returns the created KeyVaultKey object, enabling immediate use within the application for cryptographic operations.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aed59457372f0c3fa0801aa14cefea7ed0289f41e524d4ada63ecf06b1d232ed)
            check_type(argname="argument key_vault_key_name", value=key_vault_key_name, expected_type=type_hints["key_vault_key_name"])
            check_type(argname="argument key_type", value=key_type, expected_type=type_hints["key_type"])
            check_type(argname="argument key_size", value=key_size, expected_type=type_hints["key_size"])
            check_type(argname="argument key_opts", value=key_opts, expected_type=type_hints["key_opts"])
            check_type(argname="argument expiration_date", value=expiration_date, expected_type=type_hints["expiration_date"])
        return typing.cast(_cdktf_cdktf_provider_azurerm_key_vault_key_92bbcedf.KeyVaultKey, jsii.invoke(self, "addKey", [key_vault_key_name, key_type, key_size, key_opts, expiration_date]))

    @jsii.member(jsii_name="addRSAKey")
    def add_rsa_key(
        self,
        key_vault_key_name: builtins.str,
        expiration_date: typing.Optional[builtins.str] = None,
    ) -> _cdktf_cdktf_provider_azurerm_key_vault_key_92bbcedf.KeyVaultKey:
        '''Creates an RSA cryptographic key within the Azure Key Vault.

        This method facilitates the creation of an RSA key, which is useful for a variety of cryptographic operations such as
        encryption, decryption, digital signature verification, and more. The RSA key created by this method is configurable
        with an optional expiration date and a default key size of 2048 bits. The key operations allowed include decryption,
        encryption, signing, verifying signatures, and key wrapping/unwrapping.

        :param key_vault_key_name: - The unique name for the RSA key within the Key Vault.
        :param expiration_date: - Optional. The expiration date of the key in ISO 8601 format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ). If provided, the key will no longer be valid after this date.

        :return:

        A KeyVaultKey object representing the newly created RSA key within the vault.

        Example usage::

        const rsaKey = vault.addRSAKey(
        'myRSAKey',
        '2030-01-01'
        );

        This method returns the created KeyVaultKey object, allowing further operations or references to the key.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44d7612c9814856bc1bdd84c9c10b3e85c32a5de1d4f059663ecd747493821c4)
            check_type(argname="argument key_vault_key_name", value=key_vault_key_name, expected_type=type_hints["key_vault_key_name"])
            check_type(argname="argument expiration_date", value=expiration_date, expected_type=type_hints["expiration_date"])
        return typing.cast(_cdktf_cdktf_provider_azurerm_key_vault_key_92bbcedf.KeyVaultKey, jsii.invoke(self, "addRSAKey", [key_vault_key_name, expiration_date]))

    @jsii.member(jsii_name="addSecret")
    def add_secret(
        self,
        key_vault_secret_name: builtins.str,
        secret_value: builtins.str,
        expiration_date: typing.Optional[builtins.str] = None,
        content_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new secret within the Azure Key Vault.

        This method facilitates the storage of sensitive information in the form of a secret within the Key Vault.
        Secrets are protected items such as passwords, database connection strings, or any other piece of information
        that needs to be securely stored and accessed. This method allows setting additional properties such as
        expiration date and content type for better management and compliance.

        :param key_vault_secret_name: - The unique name for the secret within the Key Vault.
        :param secret_value: - The sensitive information or data that needs to be securely stored as a secret.
        :param expiration_date: - Optional. The expiration date of the secret in ISO 8601 format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ). If provided, the secret will no longer be valid after this date.
        :param content_type: - Optional. A description of the type of information the secret contains (e.g., 'password', 'connectionString'). This can be used by applications to handle the secret appropriately. Example usage:: vault.addSecret( 'myDatabasePassword', 'p@ssw0rd123!', '2030-01-01', 'databasePassword' ); This method does not return a value. It creates a secret within the Key Vault with the specified properties.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13221bb3d97d7c10cdc53b21cfc108150b47f04a58e6e97ff9ccd6e2c2a55d4b)
            check_type(argname="argument key_vault_secret_name", value=key_vault_secret_name, expected_type=type_hints["key_vault_secret_name"])
            check_type(argname="argument secret_value", value=secret_value, expected_type=type_hints["secret_value"])
            check_type(argname="argument expiration_date", value=expiration_date, expected_type=type_hints["expiration_date"])
            check_type(argname="argument content_type", value=content_type, expected_type=type_hints["content_type"])
        return typing.cast(None, jsii.invoke(self, "addSecret", [key_vault_secret_name, secret_value, expiration_date, content_type]))

    @jsii.member(jsii_name="addSelfSignedCert")
    def add_self_signed_cert(
        self,
        cert_name: builtins.str,
        subject: builtins.str,
        dns_names: typing.Sequence[builtins.str],
        action_type: typing.Optional[builtins.str] = None,
        days_before_expiry: typing.Optional[jsii.Number] = None,
    ) -> _cdktf_cdktf_provider_azurerm_key_vault_certificate_92bbcedf.KeyVaultCertificate:
        '''Creates a self-signed certificate within the Azure Key Vault.

        This method facilitates the creation of a self-signed certificate, which is a digital certificate that is signed by
        its own creator rather than a trusted authority. Self-signed certificates can be useful for testing, internal
        communications, or any scenario where public trust is not required. The method allows specifying subject details,
        DNS names for the certificate, and managing its lifecycle with action types and expiry.

        :param cert_name: - The unique name for the certificate within the Key Vault.
        :param subject: - The subject name of the certificate, typically formatted as an X.500 Distinguished Name (e.g., "CN=example.com").
        :param dns_names: - An array of DNS names that should be associated with this certificate. This is useful for certificates that need to be valid for multiple hostnames.
        :param action_type: - Optional. Specifies the action to be performed with the certificate, such as 'create' or 'renew'.
        :param days_before_expiry: - Optional. Number of days before expiry when an action should be taken, useful for auto-renewal scenarios.

        :return:

        A KeyVaultCertificate object representing the newly created self-signed certificate.

        Example usage::

        const myCertificate = vault.addSelfSignedCert(
        'myCert',
        'CN=mydomain.com',
        ['mydomain.com', 'www.mydomain.com'],
        'create',
        30
        );

        This method returns the KeyVaultCertificate object, enabling it to be used immediately within the application or stored for future use.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb532d7f4c3c84e1e56fae08e207d5a6fbf5e8ee1ba3c7a9c6b13b42ddf77b3f)
            check_type(argname="argument cert_name", value=cert_name, expected_type=type_hints["cert_name"])
            check_type(argname="argument subject", value=subject, expected_type=type_hints["subject"])
            check_type(argname="argument dns_names", value=dns_names, expected_type=type_hints["dns_names"])
            check_type(argname="argument action_type", value=action_type, expected_type=type_hints["action_type"])
            check_type(argname="argument days_before_expiry", value=days_before_expiry, expected_type=type_hints["days_before_expiry"])
        return typing.cast(_cdktf_cdktf_provider_azurerm_key_vault_certificate_92bbcedf.KeyVaultCertificate, jsii.invoke(self, "addSelfSignedCert", [cert_name, subject, dns_names, action_type, days_before_expiry]))

    @jsii.member(jsii_name="grantCertAdminAccess")
    def grant_cert_admin_access(self, azure_ad_group_id: builtins.str) -> None:
        '''Grants administrative access to certificates stored in the Key Vault to a specified Azure AD group.

        :param azure_ad_group_id: - The Azure Active Directory group ID that will receive administrative access to certificates.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73641a86765e12eff8779da1e3d696365f687b93c56fe402482b12aa728e9244)
            check_type(argname="argument azure_ad_group_id", value=azure_ad_group_id, expected_type=type_hints["azure_ad_group_id"])
        return typing.cast(None, jsii.invoke(self, "grantCertAdminAccess", [azure_ad_group_id]))

    @jsii.member(jsii_name="grantCertReaderAccess")
    def grant_cert_reader_access(self, azure_ad_group_id: builtins.str) -> None:
        '''Grants read-only access to certificates stored in the Key Vault to a specified Azure AD group.

        :param azure_ad_group_id: - The Azure Active Directory group ID that will receive read access to certificates.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17b8add7190d8d64361a0ac3cc23e32fa47351b032f69b181322896dba5f7acc)
            check_type(argname="argument azure_ad_group_id", value=azure_ad_group_id, expected_type=type_hints["azure_ad_group_id"])
        return typing.cast(None, jsii.invoke(self, "grantCertReaderAccess", [azure_ad_group_id]))

    @jsii.member(jsii_name="grantCustomAccess")
    def grant_custom_access(
        self,
        azure_ad_group_id: builtins.str,
        *,
        certificate_permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
        key_permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
        secret_permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
        storage_permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Grants custom access based on specified options to an Azure AD group in the Key Vault.

        :param azure_ad_group_id: - The Azure Active Directory group ID that will receive the custom access.
        :param certificate_permissions: Optional: A list of permissions to grant for certificates in the Key Vault. Example permissions include 'get', 'list', 'create', 'delete', etc.
        :param key_permissions: Optional: A list of permissions to grant for keys in the Key Vault. Example permissions include 'encrypt', 'decrypt', 'wrapKey', 'unwrapKey', etc.
        :param secret_permissions: Optional: A list of permissions to grant for secrets in the Key Vault. Example permissions include 'get', 'list', 'set', 'delete', etc.
        :param storage_permissions: Optional: A list of permissions to grant for storage accounts in the Key Vault. Example permissions include 'get', 'list', 'delete', 'set', 'update', etc.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0c3ff9e135caf120495df7de38fe2e782a7a0248c74e21ee768c7f682223dfb)
            check_type(argname="argument azure_ad_group_id", value=azure_ad_group_id, expected_type=type_hints["azure_ad_group_id"])
        options = GrantCustomAccessOptions(
            certificate_permissions=certificate_permissions,
            key_permissions=key_permissions,
            secret_permissions=secret_permissions,
            storage_permissions=storage_permissions,
        )

        return typing.cast(None, jsii.invoke(self, "grantCustomAccess", [azure_ad_group_id, options]))

    @jsii.member(jsii_name="grantKeyAdminAccess")
    def grant_key_admin_access(self, azure_ad_group_id: builtins.str) -> None:
        '''Grants administrative access to keys stored in the Key Vault to a specified Azure AD group.

        :param azure_ad_group_id: - The Azure Active Directory group ID that will receive administrative access to keys.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68ff32d57ec319a01c35a0940b03a2e4562a7bc6050cb8010ab4c18e7f3c21f8)
            check_type(argname="argument azure_ad_group_id", value=azure_ad_group_id, expected_type=type_hints["azure_ad_group_id"])
        return typing.cast(None, jsii.invoke(self, "grantKeyAdminAccess", [azure_ad_group_id]))

    @jsii.member(jsii_name="grantKeyReaderAccess")
    def grant_key_reader_access(self, azure_ad_group_id: builtins.str) -> None:
        '''Grants read-only access to keys stored in the Key Vault to a specified Azure AD group.

        :param azure_ad_group_id: - The Azure Active Directory group ID that will receive read access to keys.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4a4fc98889d3ac21c14e506fcf1ccaa72d368be01047ce9db0e55862ca29561)
            check_type(argname="argument azure_ad_group_id", value=azure_ad_group_id, expected_type=type_hints["azure_ad_group_id"])
        return typing.cast(None, jsii.invoke(self, "grantKeyReaderAccess", [azure_ad_group_id]))

    @jsii.member(jsii_name="grantSecretAdminAccess")
    def grant_secret_admin_access(self, azure_ad_group_id: builtins.str) -> None:
        '''Grants administrative access to secrets stored in the Key Vault to a specified Azure AD group.

        :param azure_ad_group_id: - The Azure Active Directory group ID that will receive administrative access to secrets.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28c5dd3f8478b3fd3664ab3e6a2c52820e7de6333255d890ba903c13839c3fd7)
            check_type(argname="argument azure_ad_group_id", value=azure_ad_group_id, expected_type=type_hints["azure_ad_group_id"])
        return typing.cast(None, jsii.invoke(self, "grantSecretAdminAccess", [azure_ad_group_id]))

    @jsii.member(jsii_name="grantSecretReaderAccess")
    def grant_secret_reader_access(self, azure_ad_group_id: builtins.str) -> None:
        '''Grants read-only access to secrets stored in the Key Vault to a specified Azure AD group.

        :param azure_ad_group_id: - The Azure Active Directory group ID that will receive read access to secrets.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55000ecd371e9c22c7bc145e3c409a38b61720185c5c1d6c9278b5a6413d0696)
            check_type(argname="argument azure_ad_group_id", value=azure_ad_group_id, expected_type=type_hints["azure_ad_group_id"])
        return typing.cast(None, jsii.invoke(self, "grantSecretReaderAccess", [azure_ad_group_id]))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "VaultProps":
        return typing.cast("VaultProps", jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__132293293bc0a019bee63752d4f9c262c329d1d96c14ed0ab713e57d97de3356)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="keyVault")
    def key_vault(self) -> _cdktf_cdktf_provider_azurerm_key_vault_92bbcedf.KeyVault:
        return typing.cast(_cdktf_cdktf_provider_azurerm_key_vault_92bbcedf.KeyVault, jsii.get(self, "keyVault"))

    @key_vault.setter
    def key_vault(
        self,
        value: _cdktf_cdktf_provider_azurerm_key_vault_92bbcedf.KeyVault,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b8adbdb4ccba13cd1fcc80c3a5121a26274d2437c1bb9959fa209488f098e78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVault", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__8d02ea52264d9dfc8cc494f7817103a21aa112c5ddf9274911b6c025d63b47b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroup", value)


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_keyvault.VaultProps",
    jsii_struct_bases=[],
    name_mapping={
        "location": "location",
        "name": "name",
        "tenant_id": "tenantId",
        "network_acls": "networkAcls",
        "purge_protection": "purgeProtection",
        "resource_group": "resourceGroup",
        "sku": "sku",
        "soft_delete_retention_days": "softDeleteRetentionDays",
        "tags": "tags",
    },
)
class VaultProps:
    def __init__(
        self,
        *,
        location: builtins.str,
        name: builtins.str,
        tenant_id: builtins.str,
        network_acls: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_key_vault_92bbcedf.KeyVaultNetworkAcls, typing.Dict[builtins.str, typing.Any]]] = None,
        purge_protection: typing.Optional[builtins.bool] = None,
        resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
        sku: typing.Optional[builtins.str] = None,
        soft_delete_retention_days: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param location: The Azure Region to deploy the Key Vault.
        :param name: The name of the Key Vault.
        :param tenant_id: The Name of the SKU used for this Key Vault. Possible values are standard and premium.
        :param network_acls: The Azure Active Directory tenant ID that should be used for authenticating requests to the key vault.
        :param purge_protection: A map of IP network ACL rules. The key is the IP or IP range in CIDR notation. The value is a description of that IP range.
        :param resource_group: An optional reference to the resource group in which to deploy the Key Vault. If not provided, the Key Vault will be deployed in the default resource group.
        :param sku: The tags to assign to the Key Vault.
        :param soft_delete_retention_days: Specifies whether protection against purge is enabled for this Key Vault. Setting this property to true activates protection against deletion of any active key, secret or certificate in the vault. The setting is effective only if soft delete is also enabled. The default value is false. Once activated, the property cannot be reverted to false.
        :param tags: The tags to assign to the Key Vault.
        '''
        if isinstance(network_acls, dict):
            network_acls = _cdktf_cdktf_provider_azurerm_key_vault_92bbcedf.KeyVaultNetworkAcls(**network_acls)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d60e7a7b69f9363156af0a1f5cf4a395b5df716c2f7327f2030a8e6a84ad4da5)
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tenant_id", value=tenant_id, expected_type=type_hints["tenant_id"])
            check_type(argname="argument network_acls", value=network_acls, expected_type=type_hints["network_acls"])
            check_type(argname="argument purge_protection", value=purge_protection, expected_type=type_hints["purge_protection"])
            check_type(argname="argument resource_group", value=resource_group, expected_type=type_hints["resource_group"])
            check_type(argname="argument sku", value=sku, expected_type=type_hints["sku"])
            check_type(argname="argument soft_delete_retention_days", value=soft_delete_retention_days, expected_type=type_hints["soft_delete_retention_days"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "name": name,
            "tenant_id": tenant_id,
        }
        if network_acls is not None:
            self._values["network_acls"] = network_acls
        if purge_protection is not None:
            self._values["purge_protection"] = purge_protection
        if resource_group is not None:
            self._values["resource_group"] = resource_group
        if sku is not None:
            self._values["sku"] = sku
        if soft_delete_retention_days is not None:
            self._values["soft_delete_retention_days"] = soft_delete_retention_days
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def location(self) -> builtins.str:
        '''The Azure Region to deploy the Key Vault.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the Key Vault.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tenant_id(self) -> builtins.str:
        '''The Name of the SKU used for this Key Vault.

        Possible values are standard and premium.
        '''
        result = self._values.get("tenant_id")
        assert result is not None, "Required property 'tenant_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_acls(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_key_vault_92bbcedf.KeyVaultNetworkAcls]:
        '''The Azure Active Directory tenant ID that should be used for authenticating requests to the key vault.'''
        result = self._values.get("network_acls")
        return typing.cast(typing.Optional[_cdktf_cdktf_provider_azurerm_key_vault_92bbcedf.KeyVaultNetworkAcls], result)

    @builtins.property
    def purge_protection(self) -> typing.Optional[builtins.bool]:
        '''A map of IP network ACL rules.

        The key is the IP or IP range in CIDR notation.
        The value is a description of that IP range.
        '''
        result = self._values.get("purge_protection")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def resource_group(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup]:
        '''An optional reference to the resource group in which to deploy the Key Vault.

        If not provided, the Key Vault will be deployed in the default resource group.
        '''
        result = self._values.get("resource_group")
        return typing.cast(typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup], result)

    @builtins.property
    def sku(self) -> typing.Optional[builtins.str]:
        '''The tags to assign to the Key Vault.'''
        result = self._values.get("sku")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def soft_delete_retention_days(self) -> typing.Optional[jsii.Number]:
        '''Specifies whether protection against purge is enabled for this Key Vault.

        Setting this property to true activates protection against deletion of any active key, secret or certificate in the vault. The setting is effective only if soft delete is also enabled. The default value is false.
        Once activated, the property cannot be reverted to false.
        '''
        result = self._values.get("soft_delete_retention_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The tags to assign to the Key Vault.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VaultProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AccessPolicy",
    "AccessPolicyProps",
    "CertificateIssuer",
    "CertificateIssuerProps",
    "GrantCustomAccessOptions",
    "Key",
    "KeyProps",
    "Secret",
    "SecretProps",
    "SelfSignedCertificate",
    "SelfSignedCertificateProps",
    "Vault",
    "VaultProps",
]

publication.publish()

def _typecheckingstub__fd7fc0b79a19acf1e5e94e93e6997a8d5f2b15e90adea376529cae5a756db705(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    key_vault_id: Vault,
    object_id: builtins.str,
    tenant_id: builtins.str,
    certificate_permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
    key_permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
    secret_permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
    storage_permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cfe410d8def41b97bf697999052e8eae3ba4691c72f03f9db1d7275baf6ed07(
    *,
    key_vault_id: Vault,
    object_id: builtins.str,
    tenant_id: builtins.str,
    certificate_permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
    key_permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
    secret_permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
    storage_permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fd1d912631fc8dde1a769566e3ea99baf2954d0af16be561aae29ad55ace25b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    access_policies: typing.Sequence[AccessPolicy],
    key_vault_id: Vault,
    name: builtins.str,
    provider_name: builtins.str,
    password: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5040b69059943a548e408c33cf899a9e5cd1230fcfac175e830c76b10642f504(
    *,
    access_policies: typing.Sequence[AccessPolicy],
    key_vault_id: Vault,
    name: builtins.str,
    provider_name: builtins.str,
    password: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3436fd84bf104b1bc8cd30d3eb2faadc0f58a40d1eabbb47d487be7507134cd7(
    *,
    certificate_permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
    key_permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
    secret_permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
    storage_permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__764ad04fbd1fc7abfe91c3ca71a3f0df1b038969bfda7c952f3021ce45b03094(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    access_policies: typing.Sequence[AccessPolicy],
    key_opts: typing.Sequence[builtins.str],
    key_type: builtins.str,
    key_vault_id: Vault,
    name: builtins.str,
    expires: typing.Optional[builtins.str] = None,
    key_size: typing.Optional[jsii.Number] = None,
    rotation_policy: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_key_vault_key_92bbcedf.KeyVaultKeyRotationPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f2906c60b67daeedd0649a513a69c7c29965637edc934b937264e3d9e84d21f(
    value: _cdktf_cdktf_provider_azurerm_key_vault_key_92bbcedf.KeyVaultKey,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__995ed0d726015be1e472d81cda4bb9836358aa4c155e115c8314614e4171b257(
    *,
    access_policies: typing.Sequence[AccessPolicy],
    key_opts: typing.Sequence[builtins.str],
    key_type: builtins.str,
    key_vault_id: Vault,
    name: builtins.str,
    expires: typing.Optional[builtins.str] = None,
    key_size: typing.Optional[jsii.Number] = None,
    rotation_policy: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_key_vault_key_92bbcedf.KeyVaultKeyRotationPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c78df4e95e03e93ef044f647b9b99dcad3c39f1844594b182e977b52617317f7(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    access_policies: typing.Sequence[AccessPolicy],
    key_vault_id: Vault,
    name: builtins.str,
    value: builtins.str,
    content_type: typing.Optional[builtins.str] = None,
    expiration_date: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__000957c0b227f3cb3e6b4710c4ff0c1439839536ed2dd1e6444c6440ae47007c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d36fbfdf3b4d23e5fe773f0713f10351c70db1fa84f549499f9d58b8ed1ee3f(
    *,
    access_policies: typing.Sequence[AccessPolicy],
    key_vault_id: Vault,
    name: builtins.str,
    value: builtins.str,
    content_type: typing.Optional[builtins.str] = None,
    expiration_date: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f2fd11aff992ca62fdb1d32287ac5e70f490e423a8220d0fd8b93f168423e61(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    access_policies: typing.Sequence[AccessPolicy],
    dns_names: typing.Sequence[builtins.str],
    key_vault_id: Vault,
    name: builtins.str,
    subject: builtins.str,
    action_type: typing.Optional[builtins.str] = None,
    days_before_expiry: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bcfe32dfda0bfcd75c9886c46d00ae6fe55b59fe44815138f1c45bade1a9a50(
    value: _cdktf_cdktf_provider_azurerm_key_vault_certificate_92bbcedf.KeyVaultCertificate,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a7832291886fb9d0860c4fe02c693ab9a897d39b628a7dbe1eda21608cd7bbf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9590e40faef06e65b262dcbee4614c369cb45c54a88a331ceaf27f397ea5dba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e1a75ff875f51795d8bc81864b6795d51c7ecac35b8f6a4b8aea44373ec77ea(
    *,
    access_policies: typing.Sequence[AccessPolicy],
    dns_names: typing.Sequence[builtins.str],
    key_vault_id: Vault,
    name: builtins.str,
    subject: builtins.str,
    action_type: typing.Optional[builtins.str] = None,
    days_before_expiry: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__917170a8774b61cb3259bde0d15c6881a93b9cdffe2a33390469fe5c8a9e2a05(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    tenant_id: builtins.str,
    network_acls: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_key_vault_92bbcedf.KeyVaultNetworkAcls, typing.Dict[builtins.str, typing.Any]]] = None,
    purge_protection: typing.Optional[builtins.bool] = None,
    resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
    sku: typing.Optional[builtins.str] = None,
    soft_delete_retention_days: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2f2c045bea927ac556e9d63c71e26ab25277d8da73f00083296262c6f2b0d08(
    name: builtins.str,
    provider: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aed59457372f0c3fa0801aa14cefea7ed0289f41e524d4ada63ecf06b1d232ed(
    key_vault_key_name: builtins.str,
    key_type: builtins.str,
    key_size: jsii.Number,
    key_opts: typing.Sequence[builtins.str],
    expiration_date: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44d7612c9814856bc1bdd84c9c10b3e85c32a5de1d4f059663ecd747493821c4(
    key_vault_key_name: builtins.str,
    expiration_date: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13221bb3d97d7c10cdc53b21cfc108150b47f04a58e6e97ff9ccd6e2c2a55d4b(
    key_vault_secret_name: builtins.str,
    secret_value: builtins.str,
    expiration_date: typing.Optional[builtins.str] = None,
    content_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb532d7f4c3c84e1e56fae08e207d5a6fbf5e8ee1ba3c7a9c6b13b42ddf77b3f(
    cert_name: builtins.str,
    subject: builtins.str,
    dns_names: typing.Sequence[builtins.str],
    action_type: typing.Optional[builtins.str] = None,
    days_before_expiry: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73641a86765e12eff8779da1e3d696365f687b93c56fe402482b12aa728e9244(
    azure_ad_group_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17b8add7190d8d64361a0ac3cc23e32fa47351b032f69b181322896dba5f7acc(
    azure_ad_group_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0c3ff9e135caf120495df7de38fe2e782a7a0248c74e21ee768c7f682223dfb(
    azure_ad_group_id: builtins.str,
    *,
    certificate_permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
    key_permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
    secret_permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
    storage_permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68ff32d57ec319a01c35a0940b03a2e4562a7bc6050cb8010ab4c18e7f3c21f8(
    azure_ad_group_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4a4fc98889d3ac21c14e506fcf1ccaa72d368be01047ce9db0e55862ca29561(
    azure_ad_group_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28c5dd3f8478b3fd3664ab3e6a2c52820e7de6333255d890ba903c13839c3fd7(
    azure_ad_group_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55000ecd371e9c22c7bc145e3c409a38b61720185c5c1d6c9278b5a6413d0696(
    azure_ad_group_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__132293293bc0a019bee63752d4f9c262c329d1d96c14ed0ab713e57d97de3356(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b8adbdb4ccba13cd1fcc80c3a5121a26274d2437c1bb9959fa209488f098e78(
    value: _cdktf_cdktf_provider_azurerm_key_vault_92bbcedf.KeyVault,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d02ea52264d9dfc8cc494f7817103a21aa112c5ddf9274911b6c025d63b47b1(
    value: _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d60e7a7b69f9363156af0a1f5cf4a395b5df716c2f7327f2030a8e6a84ad4da5(
    *,
    location: builtins.str,
    name: builtins.str,
    tenant_id: builtins.str,
    network_acls: typing.Optional[typing.Union[_cdktf_cdktf_provider_azurerm_key_vault_92bbcedf.KeyVaultNetworkAcls, typing.Dict[builtins.str, typing.Any]]] = None,
    purge_protection: typing.Optional[builtins.bool] = None,
    resource_group: typing.Optional[_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup] = None,
    sku: typing.Optional[builtins.str] = None,
    soft_delete_retention_days: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
