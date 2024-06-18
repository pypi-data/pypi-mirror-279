'''
# Azure Scheduled Query Rule Alert Construct

This class represents a Scheduled Query Rule Alert resource (a.k.a. Log Query Alert) in Azure.

## What is Azure Scheduled Query Rule Alert?

An Azure Scheduled Query Rule Alert lets us monitor a specific condition in Azure resources using log data. We can use KQL language to analyze logs, set alert triggering conditions when query results meet defined conditions, and configure notifications to respond to potential problems timely. This helps maintain the health, performance, and security of our Azure environment.

You can learn more about Azure Query Rule Alert in the [official Azure documentation](https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/tutorial-log-alert).

## Azure Scheduled Query Rule Alert Class Properties

This class has several properties that control the Alert Rules:

* `name`: The name of the Monitor Scheduled Query Rule.
* `resourceGroupName`: The name of the resource group in which the Monitor Scheduled Query Rule is created.
* `location`: The location of the Monitor Scheduled Query Rule.
* `criteriaOperator`: Specifies the criteria operator. Possible values are Equal, GreaterThan, GreaterThanOrEqual, LessThan,and LessThanOrEqual.
* `criteriaQuery`: The query to run on logs. The results returned by this query are used to populate the alert.
* `criteriaThreshold`: Specifies the criteria threshold value that activates the alert.
* `criteriatimeAggregationMethod`: The type of aggregation to apply to the data points in aggregation granularity. Possible values are Average, Count, Maximum, Minimum,and Total.
* `criteriaMetricMeasureColumn`: Specifies the column containing the metric measure number.
* `evaluationFrequency`: How often the scheduled query rule is evaluated, represented in ISO 8601 duration format. Possible values are PT1M, PT5M, PT10M, PT15M, PT30M, PT45M, PT1H, PT2H, PT3H, PT4H, PT5H, PT6H, P1D.
* `scopes`: Specifies the list of resource IDs that this scheduled query rule is scoped to.
* `severity`: Severity of the alert. Should be an integer between 0 and 4. Value of 0 is severest.
* `windowDuration`: Specifies the period of time in ISO 8601 duration format on which the Scheduled Query Rule will be executed (bin size).
* `criteriaDimension`: (Optional) Specifies the dimension of the criteria.

  * `name`: Name of the dimension.
  * `operator`: Operator for dimension values. Possible values are Exclude,and Include.
  * `values`: List of dimension values. Use a wildcard * to collect all.
* `criteriaFailingPeriods`: (Optional) Specifies the number of evaluation periods.

  * `minimumFailingPeriodsToTriggerAlert`: Specifies the number of violations to trigger an alert. Should be smaller or equal to number_of_evaluation_periods. Possible value is integer between 1 and 6.
  * `numberOfEvaluationPeriods`: Specifies the number of evaluation periods. Possible value is integer between 1 and 6.
* `actionActionGroupId`: (Optional) Specifies the action group IDs to trigger when the alert fires.
* `autoMitigationEnabled`: (Optional) Specifies the flag that indicates whether the alert should be automatically resolved or not. Defaults to false.
* `workspaceAlertsStorageEnabled`: (Optional) Specifies the flag which indicates whether this scheduled query rule check if storage is configured. Defaults to false.
* `description`: (Optional) Specifies the description of the scheduled query rule.
* `displayName`: (Optional) Specifies the display name of the alert rule.
* `enabled`: (Optional) Specifies the flag which indicates whether this scheduled query rule is enabled. Defaults to true.
* `muteActionsAfterAlertDuration`: (Optional) Mute actions for the chosen period of time in ISO 8601 duration format after the alert is fired. Possible values are PT5M, PT10M, PT15M, PT30M, PT45M, PT1H, PT2H, PT3H, PT4H, PT5H, PT6H, P1D and P2D.
* `queryTimeRangeOverride`: (Optional) Set this if the alert evaluation period is different from the query time range. If not specified, the value is window_duration*number_of_evaluation_periods. Possible values are PT5M, PT10M, PT15M, PT20M, PT30M, PT45M, PT1H, PT2H, PT3H, PT4H, PT5H, PT6H, P1D and P2D.
* `skipQueryValidation`: (Optional) Specifies the flag which indicates whether the provided query should be validated or not. Defaults to true.
* `tags`: (Optional) A mapping of tags which should be assigned to the Monitor Scheduled Query Rule.

## Deploying a Scheduled Query Rule Alert

You can deploy a Scheduled Query Rule Alert using this class like so:

```python
  // Create a Resource Group first
  import * as rg from "../azure-resourcegroup";
  const resourceGroup = new rg.Group(this, "myResourceGroup", {
    name: 'myResourceGroup',
    location: 'eastus',
  });

  // Create a Log Analytics Workspace
  import * as law from "../azure-loganalytics";
  const logAnalyticsWorkspace = new la.Workspace(this, 'myLogAnalytics', {
      name: 'myLogAnalytics',
      location: 'eastus',
      resource_group_name: resourceGroup.name,
    });

  // Create a Scheduled Query Rule Alert with defult settings in Log Analytics Workspace
  import * as queryalert from "../azure-queryrulealert";
  const queryRuleAlert = new queryalert.QueryRuleAlert(this, 'queryRuleAlert', {
    name: `qra-${this.name}`,
    resourceGroupName: resourceGroup.name,
    location: 'eastus',
    criteriaOperator: "GreaterThan",
    criteriaQuery: `
AppExceptions
| where Message has "file can not be reloaded"
`,
    criteriaThreshold: 100,
    criteriatimeAggregationMethod: "Count",
    evaluationFrequency: "PT5M",
    windowDuration: "PT30M",
    scopes: [logAnalyticsWorkspace.id],
    severity: 4,
    criteriaFailingPeriods: {
      minimumFailingPeriodsToTriggerAlert: 1,
      numberOfEvaluationPeriods: 1,
    },
  });
```

Full example can be found [here](test/ExampleAzureQueryRuleAlert.ts).
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


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_queryrulealert.BaseAzureQueryRuleAlertProps",
    jsii_struct_bases=[],
    name_mapping={
        "criteria_operator": "criteriaOperator",
        "criteria_query": "criteriaQuery",
        "criteria_threshold": "criteriaThreshold",
        "criteriatime_aggregation_method": "criteriatimeAggregationMethod",
        "evaluation_frequency": "evaluationFrequency",
        "location": "location",
        "name": "name",
        "resource_group": "resourceGroup",
        "severity": "severity",
        "window_duration": "windowDuration",
        "action_action_group_id": "actionActionGroupId",
        "auto_mitigation_enabled": "autoMitigationEnabled",
        "criteria_dimension_name": "criteriaDimensionName",
        "criteria_dimension_operator": "criteriaDimensionOperator",
        "criteria_dimension_values": "criteriaDimensionValues",
        "criteria_fail_minimum_failing_periods_to_trigger_alert": "criteriaFailMinimumFailingPeriodsToTriggerAlert",
        "criteria_fail_number_of_evaluation_periods": "criteriaFailNumberOfEvaluationPeriods",
        "criteria_metric_measure_column": "criteriaMetricMeasureColumn",
        "description": "description",
        "display_name": "displayName",
        "enabled": "enabled",
        "mute_actions_after_alert_duration": "muteActionsAfterAlertDuration",
        "query_time_range_override": "queryTimeRangeOverride",
        "skip_query_validation": "skipQueryValidation",
        "tags": "tags",
        "workspace_alerts_storage_enabled": "workspaceAlertsStorageEnabled",
    },
)
class BaseAzureQueryRuleAlertProps:
    def __init__(
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
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfc4c48635f05a11dfa1bd2d50a2d15acf98f68750654cec7e5e36b3d1239110)
            check_type(argname="argument criteria_operator", value=criteria_operator, expected_type=type_hints["criteria_operator"])
            check_type(argname="argument criteria_query", value=criteria_query, expected_type=type_hints["criteria_query"])
            check_type(argname="argument criteria_threshold", value=criteria_threshold, expected_type=type_hints["criteria_threshold"])
            check_type(argname="argument criteriatime_aggregation_method", value=criteriatime_aggregation_method, expected_type=type_hints["criteriatime_aggregation_method"])
            check_type(argname="argument evaluation_frequency", value=evaluation_frequency, expected_type=type_hints["evaluation_frequency"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group", value=resource_group, expected_type=type_hints["resource_group"])
            check_type(argname="argument severity", value=severity, expected_type=type_hints["severity"])
            check_type(argname="argument window_duration", value=window_duration, expected_type=type_hints["window_duration"])
            check_type(argname="argument action_action_group_id", value=action_action_group_id, expected_type=type_hints["action_action_group_id"])
            check_type(argname="argument auto_mitigation_enabled", value=auto_mitigation_enabled, expected_type=type_hints["auto_mitigation_enabled"])
            check_type(argname="argument criteria_dimension_name", value=criteria_dimension_name, expected_type=type_hints["criteria_dimension_name"])
            check_type(argname="argument criteria_dimension_operator", value=criteria_dimension_operator, expected_type=type_hints["criteria_dimension_operator"])
            check_type(argname="argument criteria_dimension_values", value=criteria_dimension_values, expected_type=type_hints["criteria_dimension_values"])
            check_type(argname="argument criteria_fail_minimum_failing_periods_to_trigger_alert", value=criteria_fail_minimum_failing_periods_to_trigger_alert, expected_type=type_hints["criteria_fail_minimum_failing_periods_to_trigger_alert"])
            check_type(argname="argument criteria_fail_number_of_evaluation_periods", value=criteria_fail_number_of_evaluation_periods, expected_type=type_hints["criteria_fail_number_of_evaluation_periods"])
            check_type(argname="argument criteria_metric_measure_column", value=criteria_metric_measure_column, expected_type=type_hints["criteria_metric_measure_column"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument mute_actions_after_alert_duration", value=mute_actions_after_alert_duration, expected_type=type_hints["mute_actions_after_alert_duration"])
            check_type(argname="argument query_time_range_override", value=query_time_range_override, expected_type=type_hints["query_time_range_override"])
            check_type(argname="argument skip_query_validation", value=skip_query_validation, expected_type=type_hints["skip_query_validation"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument workspace_alerts_storage_enabled", value=workspace_alerts_storage_enabled, expected_type=type_hints["workspace_alerts_storage_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "criteria_operator": criteria_operator,
            "criteria_query": criteria_query,
            "criteria_threshold": criteria_threshold,
            "criteriatime_aggregation_method": criteriatime_aggregation_method,
            "evaluation_frequency": evaluation_frequency,
            "location": location,
            "name": name,
            "resource_group": resource_group,
            "severity": severity,
            "window_duration": window_duration,
        }
        if action_action_group_id is not None:
            self._values["action_action_group_id"] = action_action_group_id
        if auto_mitigation_enabled is not None:
            self._values["auto_mitigation_enabled"] = auto_mitigation_enabled
        if criteria_dimension_name is not None:
            self._values["criteria_dimension_name"] = criteria_dimension_name
        if criteria_dimension_operator is not None:
            self._values["criteria_dimension_operator"] = criteria_dimension_operator
        if criteria_dimension_values is not None:
            self._values["criteria_dimension_values"] = criteria_dimension_values
        if criteria_fail_minimum_failing_periods_to_trigger_alert is not None:
            self._values["criteria_fail_minimum_failing_periods_to_trigger_alert"] = criteria_fail_minimum_failing_periods_to_trigger_alert
        if criteria_fail_number_of_evaluation_periods is not None:
            self._values["criteria_fail_number_of_evaluation_periods"] = criteria_fail_number_of_evaluation_periods
        if criteria_metric_measure_column is not None:
            self._values["criteria_metric_measure_column"] = criteria_metric_measure_column
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if enabled is not None:
            self._values["enabled"] = enabled
        if mute_actions_after_alert_duration is not None:
            self._values["mute_actions_after_alert_duration"] = mute_actions_after_alert_duration
        if query_time_range_override is not None:
            self._values["query_time_range_override"] = query_time_range_override
        if skip_query_validation is not None:
            self._values["skip_query_validation"] = skip_query_validation
        if tags is not None:
            self._values["tags"] = tags
        if workspace_alerts_storage_enabled is not None:
            self._values["workspace_alerts_storage_enabled"] = workspace_alerts_storage_enabled

    @builtins.property
    def criteria_operator(self) -> builtins.str:
        '''Specifies the criteria operator.

        Possible values are Equal, GreaterThan, GreaterThanOrEqual, LessThan,and LessThanOrEqual.
        '''
        result = self._values.get("criteria_operator")
        assert result is not None, "Required property 'criteria_operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def criteria_query(self) -> builtins.str:
        '''The query to run on logs.

        The results returned by this query are used to populate the alert.
        '''
        result = self._values.get("criteria_query")
        assert result is not None, "Required property 'criteria_query' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def criteria_threshold(self) -> jsii.Number:
        '''Specifies the criteria threshold value that activates the alert.'''
        result = self._values.get("criteria_threshold")
        assert result is not None, "Required property 'criteria_threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def criteriatime_aggregation_method(self) -> builtins.str:
        '''The type of aggregation to apply to the data points in aggregation granularity.

        Possible values are Average, Count, Maximum, Minimum,and Total.
        '''
        result = self._values.get("criteriatime_aggregation_method")
        assert result is not None, "Required property 'criteriatime_aggregation_method' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def evaluation_frequency(self) -> builtins.str:
        '''How often the scheduled query rule is evaluated, represented in ISO 8601 duration format.

        Possible values are PT1M, PT5M, PT10M, PT15M, PT30M, PT45M, PT1H, PT2H, PT3H, PT4H, PT5H, PT6H, P1D.
        '''
        result = self._values.get("evaluation_frequency")
        assert result is not None, "Required property 'evaluation_frequency' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location of the Monitor Scheduled Query Rule.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the Monitor Scheduled Query Rule.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group(
        self,
    ) -> _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup:
        '''The name of the resource group in which the Monitor Scheduled Query Rule is created.'''
        result = self._values.get("resource_group")
        assert result is not None, "Required property 'resource_group' is missing"
        return typing.cast(_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup, result)

    @builtins.property
    def severity(self) -> jsii.Number:
        '''Severity of the alert.

        Should be an integer between 0 and 4. Value of 0 is severest.
        '''
        result = self._values.get("severity")
        assert result is not None, "Required property 'severity' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def window_duration(self) -> builtins.str:
        '''Specifies the period of time in ISO 8601 duration format on which the Scheduled Query Rule will be executed (bin size).'''
        result = self._values.get("window_duration")
        assert result is not None, "Required property 'window_duration' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def action_action_group_id(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the action group IDs to trigger when the alert fires.'''
        result = self._values.get("action_action_group_id")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def auto_mitigation_enabled(self) -> typing.Optional[builtins.bool]:
        '''Specifies the flag that indicates whether the alert should be automatically resolved or not.

        :default: false
        '''
        result = self._values.get("auto_mitigation_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def criteria_dimension_name(self) -> typing.Optional[builtins.str]:
        '''Name of the dimension for criteria.'''
        result = self._values.get("criteria_dimension_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def criteria_dimension_operator(self) -> typing.Optional[builtins.str]:
        '''Operator for dimension values.

        Possible values are Exclude, and Include.
        '''
        result = self._values.get("criteria_dimension_operator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def criteria_dimension_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of dimension values.

        Use a wildcard * to collect all.
        '''
        result = self._values.get("criteria_dimension_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def criteria_fail_minimum_failing_periods_to_trigger_alert(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Specifies the number of violations to trigger an alert.

        Should be smaller or equal to number_of_evaluation_periods.
        Possible value is integer between 1 and 6.
        '''
        result = self._values.get("criteria_fail_minimum_failing_periods_to_trigger_alert")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def criteria_fail_number_of_evaluation_periods(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Specifies the number of evaluation periods.

        Possible value is integer between 1 and 6.
        '''
        result = self._values.get("criteria_fail_number_of_evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def criteria_metric_measure_column(self) -> typing.Optional[builtins.str]:
        '''Specifies the column containing the metric measure number.

        criteriaMetricMeasureColumn is required if criteriatimeAggregationMethod is Average, Maximum, Minimum, or Total.
        And criteriaMetricMeasureColumn cannot be specified if criteriatimeAggregationMethod is Count.
        '''
        result = self._values.get("criteria_metric_measure_column")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Specifies the description of the scheduled query rule.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the display name of the alert rule.'''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''Specifies the flag which indicates whether this scheduled query rule is enabled.

        :default: true
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def mute_actions_after_alert_duration(self) -> typing.Optional[builtins.str]:
        '''Mute actions for the chosen period of time in ISO 8601 duration format after the alert is fired.

        Possible values are PT5M, PT10M, PT15M, PT30M, PT45M, PT1H, PT2H, PT3H, PT4H, PT5H, PT6H, P1D and P2D.
        '''
        result = self._values.get("mute_actions_after_alert_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_time_range_override(self) -> typing.Optional[builtins.str]:
        '''Set this if the alert evaluation period is different from the query time range.

        If not specified, the value is window_duration*number_of_evaluation_periods.
        Possible values are PT5M, PT10M, PT15M, PT20M, PT30M, PT45M, PT1H, PT2H, PT3H, PT4H, PT5H, PT6H, P1D and P2D.
        '''
        result = self._values.get("query_time_range_override")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def skip_query_validation(self) -> typing.Optional[builtins.bool]:
        '''Specifies the flag which indicates whether the provided query should be validated or not.

        :default: true
        '''
        result = self._values.get("skip_query_validation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A mapping of tags which should be assigned to the Monitor Scheduled Query Rule.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def workspace_alerts_storage_enabled(self) -> typing.Optional[builtins.bool]:
        '''Specifies the flag which indicates whether this scheduled query rule check if storage is configured.

        :default: false
        '''
        result = self._values.get("workspace_alerts_storage_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BaseAzureQueryRuleAlertProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QueryRuleAlert(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@microsoft/terraform-cdk-constructs.azure_queryrulealert.QueryRuleAlert",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        scopes: typing.Sequence[builtins.str],
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
        '''Represents an Azure Monitor Scheduled Query Rule Alert.

        This class is responsible for the creation and management of a Scheduled Query Rule Alert in Azure Monitor.
        Scheduled Query Rule Alerts execute specified queries at regular intervals over the data collected in Log Analytics
        Workspaces or Application Insights, and alert based on the results of these queries. These alerts can be used to monitor
        application health, infrastructure changes, or compliance with certain conditions.

        :param scope: - The scope in which to define this construct, typically representing the Cloud Development Kit (CDK) stack.
        :param id: - The unique identifier for this instance of the Scheduled Query Rule Alert.
        :param scopes: Specifies the list of resource IDs that this scheduled query rule is scoped to.
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
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__871fa549e631485d708adb7e5fa86adc875e246512bbcef62f473e0e3de924e4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AzureQueryRuleAlertProps(
            scopes=scopes,
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

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="queryRuleAlertProps")
    def query_rule_alert_props(self) -> "AzureQueryRuleAlertProps":
        return typing.cast("AzureQueryRuleAlertProps", jsii.get(self, "queryRuleAlertProps"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36d805099b7b78d1402690a5eff05b181f97f6ce86768a884d2999737a011b0f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c20007e52890215d522bf79c2bb75095e3f727d3ad0566fb1649a7171f47ac3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroup", value)


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_queryrulealert.AzureQueryRuleAlertProps",
    jsii_struct_bases=[BaseAzureQueryRuleAlertProps],
    name_mapping={
        "criteria_operator": "criteriaOperator",
        "criteria_query": "criteriaQuery",
        "criteria_threshold": "criteriaThreshold",
        "criteriatime_aggregation_method": "criteriatimeAggregationMethod",
        "evaluation_frequency": "evaluationFrequency",
        "location": "location",
        "name": "name",
        "resource_group": "resourceGroup",
        "severity": "severity",
        "window_duration": "windowDuration",
        "action_action_group_id": "actionActionGroupId",
        "auto_mitigation_enabled": "autoMitigationEnabled",
        "criteria_dimension_name": "criteriaDimensionName",
        "criteria_dimension_operator": "criteriaDimensionOperator",
        "criteria_dimension_values": "criteriaDimensionValues",
        "criteria_fail_minimum_failing_periods_to_trigger_alert": "criteriaFailMinimumFailingPeriodsToTriggerAlert",
        "criteria_fail_number_of_evaluation_periods": "criteriaFailNumberOfEvaluationPeriods",
        "criteria_metric_measure_column": "criteriaMetricMeasureColumn",
        "description": "description",
        "display_name": "displayName",
        "enabled": "enabled",
        "mute_actions_after_alert_duration": "muteActionsAfterAlertDuration",
        "query_time_range_override": "queryTimeRangeOverride",
        "skip_query_validation": "skipQueryValidation",
        "tags": "tags",
        "workspace_alerts_storage_enabled": "workspaceAlertsStorageEnabled",
        "scopes": "scopes",
    },
)
class AzureQueryRuleAlertProps(BaseAzureQueryRuleAlertProps):
    def __init__(
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
        scopes: typing.Sequence[builtins.str],
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
        :param scopes: Specifies the list of resource IDs that this scheduled query rule is scoped to.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5762d02371a7d7ee3cc504738ea9796923ca00246c5eefa91d3b50206a4e94ee)
            check_type(argname="argument criteria_operator", value=criteria_operator, expected_type=type_hints["criteria_operator"])
            check_type(argname="argument criteria_query", value=criteria_query, expected_type=type_hints["criteria_query"])
            check_type(argname="argument criteria_threshold", value=criteria_threshold, expected_type=type_hints["criteria_threshold"])
            check_type(argname="argument criteriatime_aggregation_method", value=criteriatime_aggregation_method, expected_type=type_hints["criteriatime_aggregation_method"])
            check_type(argname="argument evaluation_frequency", value=evaluation_frequency, expected_type=type_hints["evaluation_frequency"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group", value=resource_group, expected_type=type_hints["resource_group"])
            check_type(argname="argument severity", value=severity, expected_type=type_hints["severity"])
            check_type(argname="argument window_duration", value=window_duration, expected_type=type_hints["window_duration"])
            check_type(argname="argument action_action_group_id", value=action_action_group_id, expected_type=type_hints["action_action_group_id"])
            check_type(argname="argument auto_mitigation_enabled", value=auto_mitigation_enabled, expected_type=type_hints["auto_mitigation_enabled"])
            check_type(argname="argument criteria_dimension_name", value=criteria_dimension_name, expected_type=type_hints["criteria_dimension_name"])
            check_type(argname="argument criteria_dimension_operator", value=criteria_dimension_operator, expected_type=type_hints["criteria_dimension_operator"])
            check_type(argname="argument criteria_dimension_values", value=criteria_dimension_values, expected_type=type_hints["criteria_dimension_values"])
            check_type(argname="argument criteria_fail_minimum_failing_periods_to_trigger_alert", value=criteria_fail_minimum_failing_periods_to_trigger_alert, expected_type=type_hints["criteria_fail_minimum_failing_periods_to_trigger_alert"])
            check_type(argname="argument criteria_fail_number_of_evaluation_periods", value=criteria_fail_number_of_evaluation_periods, expected_type=type_hints["criteria_fail_number_of_evaluation_periods"])
            check_type(argname="argument criteria_metric_measure_column", value=criteria_metric_measure_column, expected_type=type_hints["criteria_metric_measure_column"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument mute_actions_after_alert_duration", value=mute_actions_after_alert_duration, expected_type=type_hints["mute_actions_after_alert_duration"])
            check_type(argname="argument query_time_range_override", value=query_time_range_override, expected_type=type_hints["query_time_range_override"])
            check_type(argname="argument skip_query_validation", value=skip_query_validation, expected_type=type_hints["skip_query_validation"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument workspace_alerts_storage_enabled", value=workspace_alerts_storage_enabled, expected_type=type_hints["workspace_alerts_storage_enabled"])
            check_type(argname="argument scopes", value=scopes, expected_type=type_hints["scopes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "criteria_operator": criteria_operator,
            "criteria_query": criteria_query,
            "criteria_threshold": criteria_threshold,
            "criteriatime_aggregation_method": criteriatime_aggregation_method,
            "evaluation_frequency": evaluation_frequency,
            "location": location,
            "name": name,
            "resource_group": resource_group,
            "severity": severity,
            "window_duration": window_duration,
            "scopes": scopes,
        }
        if action_action_group_id is not None:
            self._values["action_action_group_id"] = action_action_group_id
        if auto_mitigation_enabled is not None:
            self._values["auto_mitigation_enabled"] = auto_mitigation_enabled
        if criteria_dimension_name is not None:
            self._values["criteria_dimension_name"] = criteria_dimension_name
        if criteria_dimension_operator is not None:
            self._values["criteria_dimension_operator"] = criteria_dimension_operator
        if criteria_dimension_values is not None:
            self._values["criteria_dimension_values"] = criteria_dimension_values
        if criteria_fail_minimum_failing_periods_to_trigger_alert is not None:
            self._values["criteria_fail_minimum_failing_periods_to_trigger_alert"] = criteria_fail_minimum_failing_periods_to_trigger_alert
        if criteria_fail_number_of_evaluation_periods is not None:
            self._values["criteria_fail_number_of_evaluation_periods"] = criteria_fail_number_of_evaluation_periods
        if criteria_metric_measure_column is not None:
            self._values["criteria_metric_measure_column"] = criteria_metric_measure_column
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if enabled is not None:
            self._values["enabled"] = enabled
        if mute_actions_after_alert_duration is not None:
            self._values["mute_actions_after_alert_duration"] = mute_actions_after_alert_duration
        if query_time_range_override is not None:
            self._values["query_time_range_override"] = query_time_range_override
        if skip_query_validation is not None:
            self._values["skip_query_validation"] = skip_query_validation
        if tags is not None:
            self._values["tags"] = tags
        if workspace_alerts_storage_enabled is not None:
            self._values["workspace_alerts_storage_enabled"] = workspace_alerts_storage_enabled

    @builtins.property
    def criteria_operator(self) -> builtins.str:
        '''Specifies the criteria operator.

        Possible values are Equal, GreaterThan, GreaterThanOrEqual, LessThan,and LessThanOrEqual.
        '''
        result = self._values.get("criteria_operator")
        assert result is not None, "Required property 'criteria_operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def criteria_query(self) -> builtins.str:
        '''The query to run on logs.

        The results returned by this query are used to populate the alert.
        '''
        result = self._values.get("criteria_query")
        assert result is not None, "Required property 'criteria_query' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def criteria_threshold(self) -> jsii.Number:
        '''Specifies the criteria threshold value that activates the alert.'''
        result = self._values.get("criteria_threshold")
        assert result is not None, "Required property 'criteria_threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def criteriatime_aggregation_method(self) -> builtins.str:
        '''The type of aggregation to apply to the data points in aggregation granularity.

        Possible values are Average, Count, Maximum, Minimum,and Total.
        '''
        result = self._values.get("criteriatime_aggregation_method")
        assert result is not None, "Required property 'criteriatime_aggregation_method' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def evaluation_frequency(self) -> builtins.str:
        '''How often the scheduled query rule is evaluated, represented in ISO 8601 duration format.

        Possible values are PT1M, PT5M, PT10M, PT15M, PT30M, PT45M, PT1H, PT2H, PT3H, PT4H, PT5H, PT6H, P1D.
        '''
        result = self._values.get("evaluation_frequency")
        assert result is not None, "Required property 'evaluation_frequency' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location of the Monitor Scheduled Query Rule.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the Monitor Scheduled Query Rule.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group(
        self,
    ) -> _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup:
        '''The name of the resource group in which the Monitor Scheduled Query Rule is created.'''
        result = self._values.get("resource_group")
        assert result is not None, "Required property 'resource_group' is missing"
        return typing.cast(_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup, result)

    @builtins.property
    def severity(self) -> jsii.Number:
        '''Severity of the alert.

        Should be an integer between 0 and 4. Value of 0 is severest.
        '''
        result = self._values.get("severity")
        assert result is not None, "Required property 'severity' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def window_duration(self) -> builtins.str:
        '''Specifies the period of time in ISO 8601 duration format on which the Scheduled Query Rule will be executed (bin size).'''
        result = self._values.get("window_duration")
        assert result is not None, "Required property 'window_duration' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def action_action_group_id(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the action group IDs to trigger when the alert fires.'''
        result = self._values.get("action_action_group_id")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def auto_mitigation_enabled(self) -> typing.Optional[builtins.bool]:
        '''Specifies the flag that indicates whether the alert should be automatically resolved or not.

        :default: false
        '''
        result = self._values.get("auto_mitigation_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def criteria_dimension_name(self) -> typing.Optional[builtins.str]:
        '''Name of the dimension for criteria.'''
        result = self._values.get("criteria_dimension_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def criteria_dimension_operator(self) -> typing.Optional[builtins.str]:
        '''Operator for dimension values.

        Possible values are Exclude, and Include.
        '''
        result = self._values.get("criteria_dimension_operator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def criteria_dimension_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of dimension values.

        Use a wildcard * to collect all.
        '''
        result = self._values.get("criteria_dimension_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def criteria_fail_minimum_failing_periods_to_trigger_alert(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Specifies the number of violations to trigger an alert.

        Should be smaller or equal to number_of_evaluation_periods.
        Possible value is integer between 1 and 6.
        '''
        result = self._values.get("criteria_fail_minimum_failing_periods_to_trigger_alert")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def criteria_fail_number_of_evaluation_periods(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Specifies the number of evaluation periods.

        Possible value is integer between 1 and 6.
        '''
        result = self._values.get("criteria_fail_number_of_evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def criteria_metric_measure_column(self) -> typing.Optional[builtins.str]:
        '''Specifies the column containing the metric measure number.

        criteriaMetricMeasureColumn is required if criteriatimeAggregationMethod is Average, Maximum, Minimum, or Total.
        And criteriaMetricMeasureColumn cannot be specified if criteriatimeAggregationMethod is Count.
        '''
        result = self._values.get("criteria_metric_measure_column")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Specifies the description of the scheduled query rule.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the display name of the alert rule.'''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''Specifies the flag which indicates whether this scheduled query rule is enabled.

        :default: true
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def mute_actions_after_alert_duration(self) -> typing.Optional[builtins.str]:
        '''Mute actions for the chosen period of time in ISO 8601 duration format after the alert is fired.

        Possible values are PT5M, PT10M, PT15M, PT30M, PT45M, PT1H, PT2H, PT3H, PT4H, PT5H, PT6H, P1D and P2D.
        '''
        result = self._values.get("mute_actions_after_alert_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_time_range_override(self) -> typing.Optional[builtins.str]:
        '''Set this if the alert evaluation period is different from the query time range.

        If not specified, the value is window_duration*number_of_evaluation_periods.
        Possible values are PT5M, PT10M, PT15M, PT20M, PT30M, PT45M, PT1H, PT2H, PT3H, PT4H, PT5H, PT6H, P1D and P2D.
        '''
        result = self._values.get("query_time_range_override")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def skip_query_validation(self) -> typing.Optional[builtins.bool]:
        '''Specifies the flag which indicates whether the provided query should be validated or not.

        :default: true
        '''
        result = self._values.get("skip_query_validation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A mapping of tags which should be assigned to the Monitor Scheduled Query Rule.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def workspace_alerts_storage_enabled(self) -> typing.Optional[builtins.bool]:
        '''Specifies the flag which indicates whether this scheduled query rule check if storage is configured.

        :default: false
        '''
        result = self._values.get("workspace_alerts_storage_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def scopes(self) -> typing.List[builtins.str]:
        '''Specifies the list of resource IDs that this scheduled query rule is scoped to.'''
        result = self._values.get("scopes")
        assert result is not None, "Required property 'scopes' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AzureQueryRuleAlertProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AzureQueryRuleAlertProps",
    "BaseAzureQueryRuleAlertProps",
    "QueryRuleAlert",
]

publication.publish()

def _typecheckingstub__cfc4c48635f05a11dfa1bd2d50a2d15acf98f68750654cec7e5e36b3d1239110(
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
    """Type checking stubs"""
    pass

def _typecheckingstub__871fa549e631485d708adb7e5fa86adc875e246512bbcef62f473e0e3de924e4(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    scopes: typing.Sequence[builtins.str],
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
    """Type checking stubs"""
    pass

def _typecheckingstub__36d805099b7b78d1402690a5eff05b181f97f6ce86768a884d2999737a011b0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c20007e52890215d522bf79c2bb75095e3f727d3ad0566fb1649a7171f47ac3(
    value: _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5762d02371a7d7ee3cc504738ea9796923ca00246c5eefa91d3b50206a4e94ee(
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
    scopes: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass
