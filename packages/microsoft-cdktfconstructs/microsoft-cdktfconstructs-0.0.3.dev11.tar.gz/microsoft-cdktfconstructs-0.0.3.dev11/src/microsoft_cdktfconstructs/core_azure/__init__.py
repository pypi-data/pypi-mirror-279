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
from ..azure_metricalert import (
    IBaseMetricAlertProps as _IBaseMetricAlertProps_12d2ea58
)
from ..azure_queryrulealert import (
    BaseAzureQueryRuleAlertProps as _BaseAzureQueryRuleAlertProps_4043a0fa
)


class AzureResource(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@microsoft/terraform-cdk-constructs.core_azure.AzureResource",
):
    def __init__(self, scope: _constructs_77d1e7e8.Construct, id: builtins.str) -> None:
        '''
        :param scope: -
        :param id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d809bb91fb460c3d8c1da4639116017ae9094849dd971e79bced0656169e740)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [scope, id])

    @jsii.member(jsii_name="addAccess")
    def add_access(
        self,
        object_id: builtins.str,
        custom_role_name: builtins.str,
    ) -> None:
        '''Adds an access role assignment for a specified Azure AD object (e.g., user, group, service principal) within this RBAC construct's scope.

        This method creates a new role assignment which grants the specified Azure AD object access to resources
        at the scope defined by this construct. This is useful for programmatically managing access controls,
        ensuring only authorized users or systems can perform specific actions on Azure resources.

        :param object_id: - The unique identifier of the Azure AD object (user, group, or service principal) that will receive the role assignment.
        :param custom_role_name: - The human-readable name of the Azure RBAC role to be assigned. This role defines the permissions that the object will have. Example usage:: // Example: Assign a "Reader" role to a user for the current RBAC scope rbacInstance.addAccess('user-object-id', 'Reader');
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ec54763e2192509c84ee5593e5da4ef4239aca1590aee01d4bb81aa39fb7408)
            check_type(argname="argument object_id", value=object_id, expected_type=type_hints["object_id"])
            check_type(argname="argument custom_role_name", value=custom_role_name, expected_type=type_hints["custom_role_name"])
        return typing.cast(None, jsii.invoke(self, "addAccess", [object_id, custom_role_name]))

    @jsii.member(jsii_name="addDiagSettings")
    def add_diag_settings(
        self,
        *,
        eventhub_authorization_rule_id: typing.Optional[builtins.str] = None,
        eventhub_name: typing.Optional[builtins.str] = None,
        log_analytics_destination_type: typing.Optional[builtins.str] = None,
        log_analytics_workspace_id: typing.Optional[builtins.str] = None,
        log_categories: typing.Optional[typing.Sequence[builtins.str]] = None,
        metric_categories: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        partner_solution_id: typing.Optional[builtins.str] = None,
        storage_account_id: typing.Optional[builtins.str] = None,
    ) -> "DiagnosticSettings":
        '''Adds diagnostic settings to a specified resource within this construct.

        This method creates and configures a new DiagnosticSettings instance which captures and routes
        diagnostic data (logs and metrics) to the specified destinations such as Azure Monitor,
        an Event Hubs instance, a Log Analytics workspace, or an Azure Storage account.

        :param eventhub_authorization_rule_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.71.0/docs/resources/monitor_diagnostic_setting#eventhub_authorization_rule_id MonitorDiagnosticSetting#eventhub_authorization_rule_id}.
        :param eventhub_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.71.0/docs/resources/monitor_diagnostic_setting#eventhub_name MonitorDiagnosticSetting#eventhub_name}.
        :param log_analytics_destination_type: When set to 'Dedicated' logs sent to a Log Analytics workspace will go into resource specific tables, instead of the legacy AzureDiagnostics table.
        :param log_analytics_workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.71.0/docs/resources/monitor_diagnostic_setting#log_analytics_workspace_id MonitorDiagnosticSetting#log_analytics_workspace_id}.
        :param log_categories: Log Diagnostic categories. Default: null
        :param metric_categories: Diagnostic Metrics. Default: null
        :param name: Name of the diagnostic settings resource.
        :param partner_solution_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.71.0/docs/resources/monitor_diagnostic_setting#partner_solution_id MonitorDiagnosticSetting#partner_solution_id}.
        :param storage_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.71.0/docs/resources/monitor_diagnostic_setting#storage_account_id MonitorDiagnosticSetting#storage_account_id}.

        :return:

        An instance of the DiagnosticSettings class, configured with the provided properties.

        Example usage::

        const diagSettings = resource.addDiagSettings({
        name: 'custom-diag-settings',
        logAnalyticsWorkspaceId: 'workspace-id',
        eventhubAuthorizationRuleId: 'auth-rule-id',
        eventhubName: 'eventhub-name',
        storageAccountId: 'storage-account-id'
        });
        '''
        props = BaseDiagnosticSettingsProps(
            eventhub_authorization_rule_id=eventhub_authorization_rule_id,
            eventhub_name=eventhub_name,
            log_analytics_destination_type=log_analytics_destination_type,
            log_analytics_workspace_id=log_analytics_workspace_id,
            log_categories=log_categories,
            metric_categories=metric_categories,
            name=name,
            partner_solution_id=partner_solution_id,
            storage_account_id=storage_account_id,
        )

        return typing.cast("DiagnosticSettings", jsii.invoke(self, "addDiagSettings", [props]))

    @jsii.member(jsii_name="setupResourceGroup")
    def _setup_resource_group(
        self,
        props: typing.Any,
    ) -> _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86a048b49abd3669d94dd16efa624109867367b2a77395f1efa91ed040fc0ae6)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup, jsii.invoke(self, "setupResourceGroup", [props]))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c76bd62be03329945b350ba9cbdea9590e8d54e5f751f7be82e789363200b281)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="resourceGroup")
    @abc.abstractmethod
    def resource_group(
        self,
    ) -> _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup:
        ...

    @resource_group.setter
    @abc.abstractmethod
    def resource_group(
        self,
        value: _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup,
    ) -> None:
        ...


class _AzureResourceProxy(AzureResource):
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ec98b98f30c15ce877c15ada05260a413f2e1e07468ff9124c9e8c7413dc8e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroup", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, AzureResource).__jsii_proxy_class__ = lambda : _AzureResourceProxy


class AzureResourceWithAlert(
    AzureResource,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@microsoft/terraform-cdk-constructs.core_azure.AzureResourceWithAlert",
):
    def __init__(self, scope: _constructs_77d1e7e8.Construct, id: builtins.str) -> None:
        '''
        :param scope: -
        :param id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a45c4ecedb362baec5e5a9092dddfd5804232a4339f634bec4aea7bcfd647a80)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [scope, id])

    @jsii.member(jsii_name="addMetricAlert")
    def add_metric_alert(self, props: _IBaseMetricAlertProps_12d2ea58) -> None:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65d4eb9ef355ec1d15f73a29b1f1e435c0a47019ec2ac5b552cdab9e9bab1852)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(None, jsii.invoke(self, "addMetricAlert", [props]))

    @jsii.member(jsii_name="addQueryRuleAlert")
    def add_query_rule_alert(
        self,
        *,
        criteria_operator: builtins.str,
        criteria_query: builtins.str,
        criteria_threshold: jsii.Number,
        criteriatime_aggregation_method: builtins.str,
        evaluation_frequency: builtins.str,
        location: builtins.str,
        name: builtins.str,
        resource_group: _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup,
        severity: jsii.Number,
        window_duration: builtins.str,
        action_action_group_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        auto_mitigation_enabled: typing.Optional[builtins.bool] = None,
        criteria_dimension_name: typing.Optional[builtins.str] = None,
        criteria_dimension_operator: typing.Optional[builtins.str] = None,
        criteria_dimension_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        criteria_fail_minimum_failing_periods_to_trigger_alert: typing.Optional[jsii.Number] = None,
        criteria_fail_number_of_evaluation_periods: typing.Optional[jsii.Number] = None,
        criteria_metric_measure_column: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        mute_actions_after_alert_duration: typing.Optional[builtins.str] = None,
        query_time_range_override: typing.Optional[builtins.str] = None,
        skip_query_validation: typing.Optional[builtins.bool] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        workspace_alerts_storage_enabled: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param criteria_operator: Specifies the criteria operator. Possible values are Equal, GreaterThan, GreaterThanOrEqual, LessThan,and LessThanOrEqual.
        :param criteria_query: The query to run on logs. The results returned by this query are used to populate the alert.
        :param criteria_threshold: Specifies the criteria threshold value that activates the alert.
        :param criteriatime_aggregation_method: The type of aggregation to apply to the data points in aggregation granularity. Possible values are Average, Count, Maximum, Minimum,and Total.
        :param evaluation_frequency: How often the scheduled query rule is evaluated, represented in ISO 8601 duration format. Possible values are PT1M, PT5M, PT10M, PT15M, PT30M, PT45M, PT1H, PT2H, PT3H, PT4H, PT5H, PT6H, P1D.
        :param location: The location of the Monitor Scheduled Query Rule.
        :param name: The name of the Monitor Scheduled Query Rule.
        :param resource_group: The name of the resource group in which the Monitor Scheduled Query Rule is created.
        :param severity: Severity of the alert. Should be an integer between 0 and 4. Value of 0 is severest.
        :param window_duration: Specifies the period of time in ISO 8601 duration format on which the Scheduled Query Rule will be executed (bin size).
        :param action_action_group_id: Specifies the action group IDs to trigger when the alert fires.
        :param auto_mitigation_enabled: Specifies the flag that indicates whether the alert should be automatically resolved or not. Default: false
        :param criteria_dimension_name: Name of the dimension for criteria.
        :param criteria_dimension_operator: Operator for dimension values. Possible values are Exclude, and Include.
        :param criteria_dimension_values: List of dimension values. Use a wildcard * to collect all.
        :param criteria_fail_minimum_failing_periods_to_trigger_alert: Specifies the number of violations to trigger an alert. Should be smaller or equal to number_of_evaluation_periods. Possible value is integer between 1 and 6.
        :param criteria_fail_number_of_evaluation_periods: Specifies the number of evaluation periods. Possible value is integer between 1 and 6.
        :param criteria_metric_measure_column: Specifies the column containing the metric measure number. criteriaMetricMeasureColumn is required if criteriatimeAggregationMethod is Average, Maximum, Minimum, or Total. And criteriaMetricMeasureColumn cannot be specified if criteriatimeAggregationMethod is Count.
        :param description: Specifies the description of the scheduled query rule.
        :param display_name: Specifies the display name of the alert rule.
        :param enabled: Specifies the flag which indicates whether this scheduled query rule is enabled. Default: true
        :param mute_actions_after_alert_duration: Mute actions for the chosen period of time in ISO 8601 duration format after the alert is fired. Possible values are PT5M, PT10M, PT15M, PT30M, PT45M, PT1H, PT2H, PT3H, PT4H, PT5H, PT6H, P1D and P2D.
        :param query_time_range_override: Set this if the alert evaluation period is different from the query time range. If not specified, the value is window_duration*number_of_evaluation_periods. Possible values are PT5M, PT10M, PT15M, PT20M, PT30M, PT45M, PT1H, PT2H, PT3H, PT4H, PT5H, PT6H, P1D and P2D.
        :param skip_query_validation: Specifies the flag which indicates whether the provided query should be validated or not. Default: true
        :param tags: A mapping of tags which should be assigned to the Monitor Scheduled Query Rule.
        :param workspace_alerts_storage_enabled: Specifies the flag which indicates whether this scheduled query rule check if storage is configured. Default: false
        '''
        props = _BaseAzureQueryRuleAlertProps_4043a0fa(
            criteria_operator=criteria_operator,
            criteria_query=criteria_query,
            criteria_threshold=criteria_threshold,
            criteriatime_aggregation_method=criteriatime_aggregation_method,
            evaluation_frequency=evaluation_frequency,
            location=location,
            name=name,
            resource_group=resource_group,
            severity=severity,
            window_duration=window_duration,
            action_action_group_id=action_action_group_id,
            auto_mitigation_enabled=auto_mitigation_enabled,
            criteria_dimension_name=criteria_dimension_name,
            criteria_dimension_operator=criteria_dimension_operator,
            criteria_dimension_values=criteria_dimension_values,
            criteria_fail_minimum_failing_periods_to_trigger_alert=criteria_fail_minimum_failing_periods_to_trigger_alert,
            criteria_fail_number_of_evaluation_periods=criteria_fail_number_of_evaluation_periods,
            criteria_metric_measure_column=criteria_metric_measure_column,
            description=description,
            display_name=display_name,
            enabled=enabled,
            mute_actions_after_alert_duration=mute_actions_after_alert_duration,
            query_time_range_override=query_time_range_override,
            skip_query_validation=skip_query_validation,
            tags=tags,
            workspace_alerts_storage_enabled=workspace_alerts_storage_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "addQueryRuleAlert", [props]))


class _AzureResourceWithAlertProxy(
    AzureResourceWithAlert,
    jsii.proxy_for(AzureResource), # type: ignore[misc]
):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, AzureResourceWithAlert).__jsii_proxy_class__ = lambda : _AzureResourceWithAlertProxy


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.core_azure.BaseDiagnosticSettingsProps",
    jsii_struct_bases=[],
    name_mapping={
        "eventhub_authorization_rule_id": "eventhubAuthorizationRuleId",
        "eventhub_name": "eventhubName",
        "log_analytics_destination_type": "logAnalyticsDestinationType",
        "log_analytics_workspace_id": "logAnalyticsWorkspaceId",
        "log_categories": "logCategories",
        "metric_categories": "metricCategories",
        "name": "name",
        "partner_solution_id": "partnerSolutionId",
        "storage_account_id": "storageAccountId",
    },
)
class BaseDiagnosticSettingsProps:
    def __init__(
        self,
        *,
        eventhub_authorization_rule_id: typing.Optional[builtins.str] = None,
        eventhub_name: typing.Optional[builtins.str] = None,
        log_analytics_destination_type: typing.Optional[builtins.str] = None,
        log_analytics_workspace_id: typing.Optional[builtins.str] = None,
        log_categories: typing.Optional[typing.Sequence[builtins.str]] = None,
        metric_categories: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        partner_solution_id: typing.Optional[builtins.str] = None,
        storage_account_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param eventhub_authorization_rule_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.71.0/docs/resources/monitor_diagnostic_setting#eventhub_authorization_rule_id MonitorDiagnosticSetting#eventhub_authorization_rule_id}.
        :param eventhub_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.71.0/docs/resources/monitor_diagnostic_setting#eventhub_name MonitorDiagnosticSetting#eventhub_name}.
        :param log_analytics_destination_type: When set to 'Dedicated' logs sent to a Log Analytics workspace will go into resource specific tables, instead of the legacy AzureDiagnostics table.
        :param log_analytics_workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.71.0/docs/resources/monitor_diagnostic_setting#log_analytics_workspace_id MonitorDiagnosticSetting#log_analytics_workspace_id}.
        :param log_categories: Log Diagnostic categories. Default: null
        :param metric_categories: Diagnostic Metrics. Default: null
        :param name: Name of the diagnostic settings resource.
        :param partner_solution_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.71.0/docs/resources/monitor_diagnostic_setting#partner_solution_id MonitorDiagnosticSetting#partner_solution_id}.
        :param storage_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.71.0/docs/resources/monitor_diagnostic_setting#storage_account_id MonitorDiagnosticSetting#storage_account_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de79486227d0f87abf4c04407e9d3509a556e6555a06340dd21f60a0a790062f)
            check_type(argname="argument eventhub_authorization_rule_id", value=eventhub_authorization_rule_id, expected_type=type_hints["eventhub_authorization_rule_id"])
            check_type(argname="argument eventhub_name", value=eventhub_name, expected_type=type_hints["eventhub_name"])
            check_type(argname="argument log_analytics_destination_type", value=log_analytics_destination_type, expected_type=type_hints["log_analytics_destination_type"])
            check_type(argname="argument log_analytics_workspace_id", value=log_analytics_workspace_id, expected_type=type_hints["log_analytics_workspace_id"])
            check_type(argname="argument log_categories", value=log_categories, expected_type=type_hints["log_categories"])
            check_type(argname="argument metric_categories", value=metric_categories, expected_type=type_hints["metric_categories"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument partner_solution_id", value=partner_solution_id, expected_type=type_hints["partner_solution_id"])
            check_type(argname="argument storage_account_id", value=storage_account_id, expected_type=type_hints["storage_account_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if eventhub_authorization_rule_id is not None:
            self._values["eventhub_authorization_rule_id"] = eventhub_authorization_rule_id
        if eventhub_name is not None:
            self._values["eventhub_name"] = eventhub_name
        if log_analytics_destination_type is not None:
            self._values["log_analytics_destination_type"] = log_analytics_destination_type
        if log_analytics_workspace_id is not None:
            self._values["log_analytics_workspace_id"] = log_analytics_workspace_id
        if log_categories is not None:
            self._values["log_categories"] = log_categories
        if metric_categories is not None:
            self._values["metric_categories"] = metric_categories
        if name is not None:
            self._values["name"] = name
        if partner_solution_id is not None:
            self._values["partner_solution_id"] = partner_solution_id
        if storage_account_id is not None:
            self._values["storage_account_id"] = storage_account_id

    @builtins.property
    def eventhub_authorization_rule_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.71.0/docs/resources/monitor_diagnostic_setting#eventhub_authorization_rule_id MonitorDiagnosticSetting#eventhub_authorization_rule_id}.'''
        result = self._values.get("eventhub_authorization_rule_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def eventhub_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.71.0/docs/resources/monitor_diagnostic_setting#eventhub_name MonitorDiagnosticSetting#eventhub_name}.'''
        result = self._values.get("eventhub_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_analytics_destination_type(self) -> typing.Optional[builtins.str]:
        '''When set to 'Dedicated' logs sent to a Log Analytics workspace will go into resource specific tables, instead of the legacy AzureDiagnostics table.'''
        result = self._values.get("log_analytics_destination_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_analytics_workspace_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.71.0/docs/resources/monitor_diagnostic_setting#log_analytics_workspace_id MonitorDiagnosticSetting#log_analytics_workspace_id}.'''
        result = self._values.get("log_analytics_workspace_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_categories(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Log Diagnostic categories.

        :default: null
        '''
        result = self._values.get("log_categories")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metric_categories(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Diagnostic Metrics.

        :default: null
        '''
        result = self._values.get("metric_categories")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the diagnostic settings resource.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def partner_solution_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.71.0/docs/resources/monitor_diagnostic_setting#partner_solution_id MonitorDiagnosticSetting#partner_solution_id}.'''
        result = self._values.get("partner_solution_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_account_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.71.0/docs/resources/monitor_diagnostic_setting#storage_account_id MonitorDiagnosticSetting#storage_account_id}.'''
        result = self._values.get("storage_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BaseDiagnosticSettingsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DiagnosticSettings(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@microsoft/terraform-cdk-constructs.core_azure.DiagnosticSettings",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        target_resource_id: builtins.str,
        eventhub_authorization_rule_id: typing.Optional[builtins.str] = None,
        eventhub_name: typing.Optional[builtins.str] = None,
        log_analytics_destination_type: typing.Optional[builtins.str] = None,
        log_analytics_workspace_id: typing.Optional[builtins.str] = None,
        log_categories: typing.Optional[typing.Sequence[builtins.str]] = None,
        metric_categories: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        partner_solution_id: typing.Optional[builtins.str] = None,
        storage_account_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Manages the diagnostic settings for monitoring Azure resources.

        This class is responsible for configuring Azure Monitor Diagnostic Settings to collect and route metrics and logs from
        Azure resources to monitoring and analytics services. Diagnostic settings can be applied to resources like VMs,
        App Services, and more, allowing collected data to be sent to Event Hubs, Log Analytics workspaces, or Azure Storage.

        :param scope: - The scope in which to define this construct, typically representing the Cloud Development Kit (CDK) stack.
        :param id: - The unique identifier for this instance of the diagnostic settings.
        :param target_resource_id: Target resource id to enable diagnostic settings on.
        :param eventhub_authorization_rule_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.71.0/docs/resources/monitor_diagnostic_setting#eventhub_authorization_rule_id MonitorDiagnosticSetting#eventhub_authorization_rule_id}.
        :param eventhub_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.71.0/docs/resources/monitor_diagnostic_setting#eventhub_name MonitorDiagnosticSetting#eventhub_name}.
        :param log_analytics_destination_type: When set to 'Dedicated' logs sent to a Log Analytics workspace will go into resource specific tables, instead of the legacy AzureDiagnostics table.
        :param log_analytics_workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.71.0/docs/resources/monitor_diagnostic_setting#log_analytics_workspace_id MonitorDiagnosticSetting#log_analytics_workspace_id}.
        :param log_categories: Log Diagnostic categories. Default: null
        :param metric_categories: Diagnostic Metrics. Default: null
        :param name: Name of the diagnostic settings resource.
        :param partner_solution_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.71.0/docs/resources/monitor_diagnostic_setting#partner_solution_id MonitorDiagnosticSetting#partner_solution_id}.
        :param storage_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.71.0/docs/resources/monitor_diagnostic_setting#storage_account_id MonitorDiagnosticSetting#storage_account_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80dd62adebc7a2ecc3019588edf51d7d9a53544a31ff561745a03f0a50b7b15b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DiagnosticSettingsProps(
            target_resource_id=target_resource_id,
            eventhub_authorization_rule_id=eventhub_authorization_rule_id,
            eventhub_name=eventhub_name,
            log_analytics_destination_type=log_analytics_destination_type,
            log_analytics_workspace_id=log_analytics_workspace_id,
            log_categories=log_categories,
            metric_categories=metric_categories,
            name=name,
            partner_solution_id=partner_solution_id,
            storage_account_id=storage_account_id,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "DiagnosticSettingsProps":
        return typing.cast("DiagnosticSettingsProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.core_azure.DiagnosticSettingsProps",
    jsii_struct_bases=[BaseDiagnosticSettingsProps],
    name_mapping={
        "eventhub_authorization_rule_id": "eventhubAuthorizationRuleId",
        "eventhub_name": "eventhubName",
        "log_analytics_destination_type": "logAnalyticsDestinationType",
        "log_analytics_workspace_id": "logAnalyticsWorkspaceId",
        "log_categories": "logCategories",
        "metric_categories": "metricCategories",
        "name": "name",
        "partner_solution_id": "partnerSolutionId",
        "storage_account_id": "storageAccountId",
        "target_resource_id": "targetResourceId",
    },
)
class DiagnosticSettingsProps(BaseDiagnosticSettingsProps):
    def __init__(
        self,
        *,
        eventhub_authorization_rule_id: typing.Optional[builtins.str] = None,
        eventhub_name: typing.Optional[builtins.str] = None,
        log_analytics_destination_type: typing.Optional[builtins.str] = None,
        log_analytics_workspace_id: typing.Optional[builtins.str] = None,
        log_categories: typing.Optional[typing.Sequence[builtins.str]] = None,
        metric_categories: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        partner_solution_id: typing.Optional[builtins.str] = None,
        storage_account_id: typing.Optional[builtins.str] = None,
        target_resource_id: builtins.str,
    ) -> None:
        '''
        :param eventhub_authorization_rule_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.71.0/docs/resources/monitor_diagnostic_setting#eventhub_authorization_rule_id MonitorDiagnosticSetting#eventhub_authorization_rule_id}.
        :param eventhub_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.71.0/docs/resources/monitor_diagnostic_setting#eventhub_name MonitorDiagnosticSetting#eventhub_name}.
        :param log_analytics_destination_type: When set to 'Dedicated' logs sent to a Log Analytics workspace will go into resource specific tables, instead of the legacy AzureDiagnostics table.
        :param log_analytics_workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.71.0/docs/resources/monitor_diagnostic_setting#log_analytics_workspace_id MonitorDiagnosticSetting#log_analytics_workspace_id}.
        :param log_categories: Log Diagnostic categories. Default: null
        :param metric_categories: Diagnostic Metrics. Default: null
        :param name: Name of the diagnostic settings resource.
        :param partner_solution_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.71.0/docs/resources/monitor_diagnostic_setting#partner_solution_id MonitorDiagnosticSetting#partner_solution_id}.
        :param storage_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.71.0/docs/resources/monitor_diagnostic_setting#storage_account_id MonitorDiagnosticSetting#storage_account_id}.
        :param target_resource_id: Target resource id to enable diagnostic settings on.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddb054a038163bb87907b34921a1066d096e6cd55f0734949bd32592e76d01f9)
            check_type(argname="argument eventhub_authorization_rule_id", value=eventhub_authorization_rule_id, expected_type=type_hints["eventhub_authorization_rule_id"])
            check_type(argname="argument eventhub_name", value=eventhub_name, expected_type=type_hints["eventhub_name"])
            check_type(argname="argument log_analytics_destination_type", value=log_analytics_destination_type, expected_type=type_hints["log_analytics_destination_type"])
            check_type(argname="argument log_analytics_workspace_id", value=log_analytics_workspace_id, expected_type=type_hints["log_analytics_workspace_id"])
            check_type(argname="argument log_categories", value=log_categories, expected_type=type_hints["log_categories"])
            check_type(argname="argument metric_categories", value=metric_categories, expected_type=type_hints["metric_categories"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument partner_solution_id", value=partner_solution_id, expected_type=type_hints["partner_solution_id"])
            check_type(argname="argument storage_account_id", value=storage_account_id, expected_type=type_hints["storage_account_id"])
            check_type(argname="argument target_resource_id", value=target_resource_id, expected_type=type_hints["target_resource_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target_resource_id": target_resource_id,
        }
        if eventhub_authorization_rule_id is not None:
            self._values["eventhub_authorization_rule_id"] = eventhub_authorization_rule_id
        if eventhub_name is not None:
            self._values["eventhub_name"] = eventhub_name
        if log_analytics_destination_type is not None:
            self._values["log_analytics_destination_type"] = log_analytics_destination_type
        if log_analytics_workspace_id is not None:
            self._values["log_analytics_workspace_id"] = log_analytics_workspace_id
        if log_categories is not None:
            self._values["log_categories"] = log_categories
        if metric_categories is not None:
            self._values["metric_categories"] = metric_categories
        if name is not None:
            self._values["name"] = name
        if partner_solution_id is not None:
            self._values["partner_solution_id"] = partner_solution_id
        if storage_account_id is not None:
            self._values["storage_account_id"] = storage_account_id

    @builtins.property
    def eventhub_authorization_rule_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.71.0/docs/resources/monitor_diagnostic_setting#eventhub_authorization_rule_id MonitorDiagnosticSetting#eventhub_authorization_rule_id}.'''
        result = self._values.get("eventhub_authorization_rule_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def eventhub_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.71.0/docs/resources/monitor_diagnostic_setting#eventhub_name MonitorDiagnosticSetting#eventhub_name}.'''
        result = self._values.get("eventhub_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_analytics_destination_type(self) -> typing.Optional[builtins.str]:
        '''When set to 'Dedicated' logs sent to a Log Analytics workspace will go into resource specific tables, instead of the legacy AzureDiagnostics table.'''
        result = self._values.get("log_analytics_destination_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_analytics_workspace_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.71.0/docs/resources/monitor_diagnostic_setting#log_analytics_workspace_id MonitorDiagnosticSetting#log_analytics_workspace_id}.'''
        result = self._values.get("log_analytics_workspace_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_categories(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Log Diagnostic categories.

        :default: null
        '''
        result = self._values.get("log_categories")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metric_categories(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Diagnostic Metrics.

        :default: null
        '''
        result = self._values.get("metric_categories")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the diagnostic settings resource.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def partner_solution_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.71.0/docs/resources/monitor_diagnostic_setting#partner_solution_id MonitorDiagnosticSetting#partner_solution_id}.'''
        result = self._values.get("partner_solution_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_account_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/3.71.0/docs/resources/monitor_diagnostic_setting#storage_account_id MonitorDiagnosticSetting#storage_account_id}.'''
        result = self._values.get("storage_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_resource_id(self) -> builtins.str:
        '''Target resource id to enable diagnostic settings on.'''
        result = self._values.get("target_resource_id")
        assert result is not None, "Required property 'target_resource_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DiagnosticSettingsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Rbac(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@microsoft/terraform-cdk-constructs.core_azure.Rbac",
):
    def __init__(
        self,
        scope_: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        object_id: builtins.str,
        role_definition_name: builtins.str,
        scope: builtins.str,
        role_definition_uuid: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Manages Role-Based Access Control (RBAC) assignments within Azure.

        This class is responsible for creating and managing RBAC role assignments in Azure, which control permissions for Azure AD
        identities to manage Azure resources. It supports assigning roles at different scopes such as subscriptions, resource groups,
        or specific resources.

        :param scope_: - The scope in which to define this construct, typically representing the Cloud Development Kit (CDK) stack.
        :param id: - The unique identifier for this instance of the RBAC assignment.
        :param object_id: The unique identifier for objects in Azure AD, such as users, groups, or service principals.
        :param role_definition_name: The human-readable name of the Azure RBAC role, e.g., "Virtual Machine Contributor".
        :param scope: The scope at which the RBAC role assignment is applied. This could be a subscription, resource group, or a specific resource.
        :param role_definition_uuid: The universally unique identifier (UUID) for the Azure RBAC role definition. To find the UUID for a role using Azure CLI, use the command: ``az role definition list --name "Role Name" --query "[].name" -o tsv``
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95b52367ed6e90462817903b7daae252347f5ce187dece5a3502e3c3599976f2)
            check_type(argname="argument scope_", value=scope_, expected_type=type_hints["scope_"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = RbacProps(
            object_id=object_id,
            role_definition_name=role_definition_name,
            scope=scope,
            role_definition_uuid=role_definition_uuid,
        )

        jsii.create(self.__class__, self, [scope_, id, props])


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.core_azure.RbacProps",
    jsii_struct_bases=[],
    name_mapping={
        "object_id": "objectId",
        "role_definition_name": "roleDefinitionName",
        "scope": "scope",
        "role_definition_uuid": "roleDefinitionUUID",
    },
)
class RbacProps:
    def __init__(
        self,
        *,
        object_id: builtins.str,
        role_definition_name: builtins.str,
        scope: builtins.str,
        role_definition_uuid: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param object_id: The unique identifier for objects in Azure AD, such as users, groups, or service principals.
        :param role_definition_name: The human-readable name of the Azure RBAC role, e.g., "Virtual Machine Contributor".
        :param scope: The scope at which the RBAC role assignment is applied. This could be a subscription, resource group, or a specific resource.
        :param role_definition_uuid: The universally unique identifier (UUID) for the Azure RBAC role definition. To find the UUID for a role using Azure CLI, use the command: ``az role definition list --name "Role Name" --query "[].name" -o tsv``
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa201a06ac30874dc3cfb95c09452934bc1463c17d71006408982de04ddf0234)
            check_type(argname="argument object_id", value=object_id, expected_type=type_hints["object_id"])
            check_type(argname="argument role_definition_name", value=role_definition_name, expected_type=type_hints["role_definition_name"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument role_definition_uuid", value=role_definition_uuid, expected_type=type_hints["role_definition_uuid"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object_id": object_id,
            "role_definition_name": role_definition_name,
            "scope": scope,
        }
        if role_definition_uuid is not None:
            self._values["role_definition_uuid"] = role_definition_uuid

    @builtins.property
    def object_id(self) -> builtins.str:
        '''The unique identifier for objects in Azure AD, such as users, groups, or service principals.'''
        result = self._values.get("object_id")
        assert result is not None, "Required property 'object_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_definition_name(self) -> builtins.str:
        '''The human-readable name of the Azure RBAC role, e.g., "Virtual Machine Contributor".'''
        result = self._values.get("role_definition_name")
        assert result is not None, "Required property 'role_definition_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scope(self) -> builtins.str:
        '''The scope at which the RBAC role assignment is applied.

        This could be a subscription, resource group, or a specific resource.
        '''
        result = self._values.get("scope")
        assert result is not None, "Required property 'scope' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_definition_uuid(self) -> typing.Optional[builtins.str]:
        '''The universally unique identifier (UUID) for the Azure RBAC role definition.

        To find the UUID for a role using Azure CLI, use the command:
        ``az role definition list --name "Role Name" --query "[].name" -o tsv``
        '''
        result = self._values.get("role_definition_uuid")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RbacProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AzureResource",
    "AzureResourceWithAlert",
    "BaseDiagnosticSettingsProps",
    "DiagnosticSettings",
    "DiagnosticSettingsProps",
    "Rbac",
    "RbacProps",
]

publication.publish()

def _typecheckingstub__0d809bb91fb460c3d8c1da4639116017ae9094849dd971e79bced0656169e740(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ec54763e2192509c84ee5593e5da4ef4239aca1590aee01d4bb81aa39fb7408(
    object_id: builtins.str,
    custom_role_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86a048b49abd3669d94dd16efa624109867367b2a77395f1efa91ed040fc0ae6(
    props: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c76bd62be03329945b350ba9cbdea9590e8d54e5f751f7be82e789363200b281(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ec98b98f30c15ce877c15ada05260a413f2e1e07468ff9124c9e8c7413dc8e4(
    value: _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a45c4ecedb362baec5e5a9092dddfd5804232a4339f634bec4aea7bcfd647a80(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65d4eb9ef355ec1d15f73a29b1f1e435c0a47019ec2ac5b552cdab9e9bab1852(
    props: _IBaseMetricAlertProps_12d2ea58,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de79486227d0f87abf4c04407e9d3509a556e6555a06340dd21f60a0a790062f(
    *,
    eventhub_authorization_rule_id: typing.Optional[builtins.str] = None,
    eventhub_name: typing.Optional[builtins.str] = None,
    log_analytics_destination_type: typing.Optional[builtins.str] = None,
    log_analytics_workspace_id: typing.Optional[builtins.str] = None,
    log_categories: typing.Optional[typing.Sequence[builtins.str]] = None,
    metric_categories: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    partner_solution_id: typing.Optional[builtins.str] = None,
    storage_account_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80dd62adebc7a2ecc3019588edf51d7d9a53544a31ff561745a03f0a50b7b15b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    target_resource_id: builtins.str,
    eventhub_authorization_rule_id: typing.Optional[builtins.str] = None,
    eventhub_name: typing.Optional[builtins.str] = None,
    log_analytics_destination_type: typing.Optional[builtins.str] = None,
    log_analytics_workspace_id: typing.Optional[builtins.str] = None,
    log_categories: typing.Optional[typing.Sequence[builtins.str]] = None,
    metric_categories: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    partner_solution_id: typing.Optional[builtins.str] = None,
    storage_account_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddb054a038163bb87907b34921a1066d096e6cd55f0734949bd32592e76d01f9(
    *,
    eventhub_authorization_rule_id: typing.Optional[builtins.str] = None,
    eventhub_name: typing.Optional[builtins.str] = None,
    log_analytics_destination_type: typing.Optional[builtins.str] = None,
    log_analytics_workspace_id: typing.Optional[builtins.str] = None,
    log_categories: typing.Optional[typing.Sequence[builtins.str]] = None,
    metric_categories: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    partner_solution_id: typing.Optional[builtins.str] = None,
    storage_account_id: typing.Optional[builtins.str] = None,
    target_resource_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95b52367ed6e90462817903b7daae252347f5ce187dece5a3502e3c3599976f2(
    scope_: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    object_id: builtins.str,
    role_definition_name: builtins.str,
    scope: builtins.str,
    role_definition_uuid: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa201a06ac30874dc3cfb95c09452934bc1463c17d71006408982de04ddf0234(
    *,
    object_id: builtins.str,
    role_definition_name: builtins.str,
    scope: builtins.str,
    role_definition_uuid: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
