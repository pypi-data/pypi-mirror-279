'''
# Azure Metric Alert Construct

This class represents a Metric Alert resource in Azure.

## What is Azure Metric Alert?

An Azure Metric Alert monitors a pre-computed and pre-aggregated metric over a period of time. We can use Azure provided metrics (see official doc for [dimensions supported](https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-metric-near-real-time#metrics-and-dimensions-supported) ) or custom metrics. There are two types of Metric Alerts: `Static alert` and `Dynamic alert`. `Static Metric Alert` is given a static threshold to monitor, whereas `Dynamic Metric Alert` is leverage Azure Machine Learning to learn the normal pattern of metric and alert when the metric is outside of the normal pattern. The alert can also be configured to auto-mitigate when the metric returns to a healthy state.

## Azure Metric Alert Class Properties

This class has several properties that control the Alert Rules:

* `name` - The name of the Metric Alert.
* `resourceGroupName` - The name of the resource group in which the Metric Alert is created.
* `scopes` - A set of strings of resource IDs at which the metric criteria should be applied.
* `criteria` - (Optional) One ore more criteria. Either Criteria or dynamicCriteria is required.
* `dynamicCriteria` - (Optional) One ore more dynamic criteria. Either Criteria or dynamicCriteria is required.
* `enabled` - (Optional) Should this Metric Alert be enabled? Defaults to `true`.
* `automitigate` - (Optional) Should the alerts in this Metric Alert be auto resolved? Defaults to `true`.
* `frequency` - (Optional) The evaluation frequency of this Metric Alert, represented in ISO 8601 duration format. Possible values are PT1M, PT5M, PT15M, PT30M and PT1H. Defaults to `PT5M`.
* `windowSize` - (Optional) The period of time that is used to monitor alert activity, represented in ISO 8601 duration format. This value must be greater than frequency. Possible values are PT1M, PT5M, PT15M, PT30M, PT1H, PT6H, PT12H and P1D. Defaults to `PT5M`.
* `severity` - (Optional) The severity of this Metric Alert. Possible values are 0, 1, 2, 3 and 4. Defaults to `3`.
* `description` - (Optional) The description of this Metric Alert.
* `action` - (Optional) The action block of this Metric Alert.
* `targetResourceType` - (Optional) The resource type (e.g. Microsoft.Compute/virtualMachines) of the target resource. This is Required when using a Subscription as scope, a Resource Group as scope or Multiple Scopes.
* `targetResourceLocation` - (Optional) The location of the target resource. This is Required when using a Subscription as scope, a Resource Group as scope or Multiple Scopes.
* `tags` - (Optional) A mapping of tags to assign to the resource.

## Deploying a Metric Alert

You can deploy a Metric Alert using this class like so:

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

  // Create a Metric Alert with defult settings in Log Analytics Workspace
  import * as ma from "./lib/azure-metricalert";
  new ma.MetricAlert(this, 'metricAlert', {
    name: `myMetricalert`,
    resourceGroupName: resourceGroup.name,
    scopes: [logAnalyticsWorkspace.id],
    criteria: [
      {
        metricName: "Heartbeat",
        metricNamespace: "Microsoft.operationalinsights/workspaces",
        aggregation: "Average",
        operator: "LessThan",
        threshold: 100,
      },
    ],
  });
```

Full example can be found [here](test/ExampleMetricAlert.ts).
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


@jsii.interface(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_metricalert.IBaseMetricAlertProps"
)
class IBaseMetricAlertProps(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the Metric Alert.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#name}
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> typing.Optional[typing.List["MetricAlertActionProp"]]:
        ...

    @builtins.property
    @jsii.member(jsii_name="criteria")
    def criteria(self) -> typing.Optional[typing.List["MetricAlertCriteriaProp"]]:
        '''One ore more criteria.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#criteria}
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of this Metric Alert.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#description}
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="dynamicCriteria")
    def dynamic_criteria(
        self,
    ) -> typing.Optional[typing.List["MetricAlertDynamicCritiriaProps"]]:
        '''One ore more dynamic criteria.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#dynamic_criteria}
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A mapping of tags to assign to the resource.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#tags}
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="targetResourceLocation")
    def target_resource_location(self) -> typing.Optional[builtins.str]:
        '''The location of the target resource.

        This is Required when using a Subscription as scope, a Resource Group as scope or Multiple Scopes.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#target_resource_location}
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="targetResourceType")
    def target_resource_type(self) -> typing.Optional[builtins.str]:
        '''The resource type (e.g. Microsoft.Compute/virtualMachines) of the target resource. This is Required when using a Subscription as scope, a Resource Group as scope or Multiple Scopes.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#target_resource_type}
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="automitigate")
    def automitigate(self) -> typing.Optional[builtins.bool]:
        '''Should the alerts in this Metric Alert be auto resolved?

        :default: true

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#auto_mitigate}
        '''
        ...

    @automitigate.setter
    def automitigate(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''Should this Metric Alert be enabled?

        :default: true

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#enabled}
        '''
        ...

    @enabled.setter
    def enabled(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="frequency")
    def frequency(self) -> typing.Optional[builtins.str]:
        '''The evaluation frequency of this Metric Alert, represented in ISO 8601 duration format.

        Possible values are PT1M, PT5M, PT15M, PT30M and PT1H.

        :default: PT5M

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#frequency}
        '''
        ...

    @frequency.setter
    def frequency(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="severity")
    def severity(self) -> typing.Optional[jsii.Number]:
        '''The severity of this Metric Alert.

        Possible values are 0, 1, 2, 3 and 4.

        :default: 3

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#severity}
        '''
        ...

    @severity.setter
    def severity(self, value: typing.Optional[jsii.Number]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="windowSize")
    def window_size(self) -> typing.Optional[builtins.str]:
        '''The period of time that is used to monitor alert activity, represented in ISO 8601 duration format.

        This value must be greater than frequency. Possible values are PT1M, PT5M, PT15M, PT30M, PT1H, PT6H, PT12H and P1D.

        :default: PT5M

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#window_size}
        '''
        ...

    @window_size.setter
    def window_size(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _IBaseMetricAlertPropsProxy:
    __jsii_type__: typing.ClassVar[str] = "@microsoft/terraform-cdk-constructs.azure_metricalert.IBaseMetricAlertProps"

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the Metric Alert.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#name}
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> typing.Optional[typing.List["MetricAlertActionProp"]]:
        return typing.cast(typing.Optional[typing.List["MetricAlertActionProp"]], jsii.get(self, "action"))

    @builtins.property
    @jsii.member(jsii_name="criteria")
    def criteria(self) -> typing.Optional[typing.List["MetricAlertCriteriaProp"]]:
        '''One ore more criteria.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#criteria}
        '''
        return typing.cast(typing.Optional[typing.List["MetricAlertCriteriaProp"]], jsii.get(self, "criteria"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of this Metric Alert.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#description}
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="dynamicCriteria")
    def dynamic_criteria(
        self,
    ) -> typing.Optional[typing.List["MetricAlertDynamicCritiriaProps"]]:
        '''One ore more dynamic criteria.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#dynamic_criteria}
        '''
        return typing.cast(typing.Optional[typing.List["MetricAlertDynamicCritiriaProps"]], jsii.get(self, "dynamicCriteria"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A mapping of tags to assign to the resource.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#tags}
        '''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="targetResourceLocation")
    def target_resource_location(self) -> typing.Optional[builtins.str]:
        '''The location of the target resource.

        This is Required when using a Subscription as scope, a Resource Group as scope or Multiple Scopes.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#target_resource_location}
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetResourceLocation"))

    @builtins.property
    @jsii.member(jsii_name="targetResourceType")
    def target_resource_type(self) -> typing.Optional[builtins.str]:
        '''The resource type (e.g. Microsoft.Compute/virtualMachines) of the target resource. This is Required when using a Subscription as scope, a Resource Group as scope or Multiple Scopes.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#target_resource_type}
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetResourceType"))

    @builtins.property
    @jsii.member(jsii_name="automitigate")
    def automitigate(self) -> typing.Optional[builtins.bool]:
        '''Should the alerts in this Metric Alert be auto resolved?

        :default: true

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#auto_mitigate}
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "automitigate"))

    @automitigate.setter
    def automitigate(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9b6d2f05b6ed0d46af4ec9192122ef44c3980479c396d43304bb0b9b694e113)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "automitigate", value)

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''Should this Metric Alert be enabled?

        :default: true

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#enabled}
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a71a6bc41cbe01c48e85fc89a6e119390fa9f8a525e7cf56ded112c85d2ce1b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="frequency")
    def frequency(self) -> typing.Optional[builtins.str]:
        '''The evaluation frequency of this Metric Alert, represented in ISO 8601 duration format.

        Possible values are PT1M, PT5M, PT15M, PT30M and PT1H.

        :default: PT5M

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#frequency}
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "frequency"))

    @frequency.setter
    def frequency(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6121ecbd0831518b2ec58c88fba21c560e324250edb73d3cb548e7b87b63cb7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frequency", value)

    @builtins.property
    @jsii.member(jsii_name="severity")
    def severity(self) -> typing.Optional[jsii.Number]:
        '''The severity of this Metric Alert.

        Possible values are 0, 1, 2, 3 and 4.

        :default: 3

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#severity}
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "severity"))

    @severity.setter
    def severity(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4208080d1e6a948e5cd36c58ec3192a87a4670c52f57c2611997528c85acd7f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "severity", value)

    @builtins.property
    @jsii.member(jsii_name="windowSize")
    def window_size(self) -> typing.Optional[builtins.str]:
        '''The period of time that is used to monitor alert activity, represented in ISO 8601 duration format.

        This value must be greater than frequency. Possible values are PT1M, PT5M, PT15M, PT30M, PT1H, PT6H, PT12H and P1D.

        :default: PT5M

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#window_size}
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "windowSize"))

    @window_size.setter
    def window_size(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32d092155070280bb1f6c612ff5cfd8100865141ec1f19899057122299f11708)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "windowSize", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IBaseMetricAlertProps).__jsii_proxy_class__ = lambda : _IBaseMetricAlertPropsProxy


@jsii.interface(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_metricalert.IMetricAlertProps"
)
class IMetricAlertProps(IBaseMetricAlertProps, typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="resourceGroup")
    def resource_group(
        self,
    ) -> _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup:
        '''The name of the resource group in which the Metric Alert is created.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#resource_group_name}
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="scopes")
    def scopes(self) -> typing.List[builtins.str]:
        '''A set of strings of resource IDs at which the metric criteria should be applied.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#scopes}
        '''
        ...


class _IMetricAlertPropsProxy(
    jsii.proxy_for(IBaseMetricAlertProps), # type: ignore[misc]
):
    __jsii_type__: typing.ClassVar[str] = "@microsoft/terraform-cdk-constructs.azure_metricalert.IMetricAlertProps"

    @builtins.property
    @jsii.member(jsii_name="resourceGroup")
    def resource_group(
        self,
    ) -> _cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup:
        '''The name of the resource group in which the Metric Alert is created.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#resource_group_name}
        '''
        return typing.cast(_cdktf_cdktf_provider_azurerm_resource_group_92bbcedf.ResourceGroup, jsii.get(self, "resourceGroup"))

    @builtins.property
    @jsii.member(jsii_name="scopes")
    def scopes(self) -> typing.List[builtins.str]:
        '''A set of strings of resource IDs at which the metric criteria should be applied.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#scopes}
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scopes"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IMetricAlertProps).__jsii_proxy_class__ = lambda : _IMetricAlertPropsProxy


class MetricAlert(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@microsoft/terraform-cdk-constructs.azure_metricalert.MetricAlert",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        props: IMetricAlertProps,
    ) -> None:
        '''Represents a Metric Alert in Azure Monitor, which is used to automatically monitor metrics across Azure services and trigger actions when certain conditions are met.

        This class encapsulates the configuration and management of a Metric Alert, allowing users to define alert rules based on the metrics from their Azure resources. Metric Alerts can help in proactively managing the health, performance, and availability of Azure services.

        Properties:

        - ``name``: The name of the Metric Alert, which must be unique within the resource group.
        - ``description``: Optional. A description of what the Metric Alert monitors and potential impact or remediation.
        - ``enabled``: Indicates whether the alert rule is enabled. Disabled rules will not fire.
        - ``autoMitigate``: Specifies whether the alert should attempt auto-mitigation actions when triggered.
        - ``frequency``: The frequency of evaluation for the alert rule, determining how often the rule is checked.
        - ``severity``: The severity level assigned to the alert. This helps in categorizing the urgency of the alert.
        - ``targetResourceType``: Specifies the type of Azure resource the alert rule applies to, necessary for scoping the alert.
        - ``targetResourceLocation``: Specifies the location of the target resource, required when the alert rule covers resources in multiple locations.
        - ``windowSize``: The period over which data is collected for analysis, which must be greater than the frequency of evaluation.
        - ``tags``: User-defined tags to help organize and identify resources within Azure.
        - ``criteria``: The conditions that trigger the alert. This can be static or dynamic, based on the behavior of the monitored metric over time.
        - ``dynamicCriteria``: Advanced configurations for criteria that dynamically adjust thresholds based on historical data.
        - ``scopes``: The specific resources that the Metric Alert is scoped to monitor.
        - ``resourceGroup``: The Azure Resource Group in which this Metric Alert is defined.

        Example usage::

           const cpuAlertProps: IMetricAlertProps = {
             name: 'High CPU Usage Alert',
             resourceGroup: resourceGroupInstance,
             scopes: [vm.id],
             criteria: [
               {
                 metricName: 'Percentage CPU',
                 operator: 'GreaterThan',
                 threshold: 80,
                 aggregation: 'Average'
               }
             ],
             frequency: 'PT1M',
             windowSize: 'PT5M',
             severity: 3,
             enabled: true
           };

           const cpuAlert = new MetricAlert(this, 'cpuUsageAlert', cpuAlertProps);

        This configuration defines a Metric Alert that monitors CPU usage across specified virtual machines, triggering an alert if the CPU usage exceeds 80% over a 5-minute window, evaluated every minute.

        :param scope: -
        :param id: -
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89a31dd72d07a3fb3ea9f11c966fd677dff2f202fa495d954aa9d15a60a7539b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> IMetricAlertProps:
        return typing.cast(IMetricAlertProps, jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_metricalert.MetricAlertActionProp",
    jsii_struct_bases=[],
    name_mapping={"action_group_id": "actionGroupId"},
)
class MetricAlertActionProp:
    def __init__(self, *, action_group_id: typing.Sequence[builtins.str]) -> None:
        '''
        :param action_group_id: The ID of the Action Group.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#action}
        :description: The Action to trigger when the Metric Alert fires.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c10e6a840860f6b4069b766a02a280d1a0fbeb3f59e8d4149c18a3a463743083)
            check_type(argname="argument action_group_id", value=action_group_id, expected_type=type_hints["action_group_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action_group_id": action_group_id,
        }

    @builtins.property
    def action_group_id(self) -> typing.List[builtins.str]:
        '''The ID of the Action Group.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#action_group_id}
        '''
        result = self._values.get("action_group_id")
        assert result is not None, "Required property 'action_group_id' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetricAlertActionProp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_metricalert.MetricAlertCriteriaBaseProps",
    jsii_struct_bases=[],
    name_mapping={
        "aggregation": "aggregation",
        "metric_name": "metricName",
        "metric_namespace": "metricNamespace",
        "operator": "operator",
        "dimension": "dimension",
        "skip_metric_validation": "skipMetricValidation",
    },
)
class MetricAlertCriteriaBaseProps:
    def __init__(
        self,
        *,
        aggregation: builtins.str,
        metric_name: builtins.str,
        metric_namespace: builtins.str,
        operator: builtins.str,
        dimension: typing.Optional[typing.Sequence[typing.Union["MetricAlertCriteriaDimensionProp", typing.Dict[builtins.str, typing.Any]]]] = None,
        skip_metric_validation: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param aggregation: The aggregation type to apply to the metric. Possible values are Average, Count, Minimum, Maximum and Total.
        :param metric_name: The name of the metric to monitor.
        :param metric_namespace: The namespace of the metric.
        :param operator: The operator to apply to the metric. Possible values are Equals, NotEquals, GreaterThan, GreaterThanOrEqual, LessThan and LessThanOrEqual.
        :param dimension: One or more dimensions.
        :param skip_metric_validation: Skip the metric validation to allow creating an alert rule on a custom metric that isn't yet emitted? Default: false.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#criteria}
        :description: The base criteria properties for a Metric Alert.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d07a7654959ce4d1f3e2cfa72b5acc5537f57d967a4d561b13ea4c9114815c6)
            check_type(argname="argument aggregation", value=aggregation, expected_type=type_hints["aggregation"])
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument metric_namespace", value=metric_namespace, expected_type=type_hints["metric_namespace"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument dimension", value=dimension, expected_type=type_hints["dimension"])
            check_type(argname="argument skip_metric_validation", value=skip_metric_validation, expected_type=type_hints["skip_metric_validation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "aggregation": aggregation,
            "metric_name": metric_name,
            "metric_namespace": metric_namespace,
            "operator": operator,
        }
        if dimension is not None:
            self._values["dimension"] = dimension
        if skip_metric_validation is not None:
            self._values["skip_metric_validation"] = skip_metric_validation

    @builtins.property
    def aggregation(self) -> builtins.str:
        '''The aggregation type to apply to the metric.

        Possible values are Average, Count, Minimum, Maximum and Total.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#aggregation}
        '''
        result = self._values.get("aggregation")
        assert result is not None, "Required property 'aggregation' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metric_name(self) -> builtins.str:
        '''The name of the metric to monitor.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#metric_name}
        '''
        result = self._values.get("metric_name")
        assert result is not None, "Required property 'metric_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metric_namespace(self) -> builtins.str:
        '''The namespace of the metric.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#metric_namespace}
        '''
        result = self._values.get("metric_namespace")
        assert result is not None, "Required property 'metric_namespace' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def operator(self) -> builtins.str:
        '''The operator to apply to the metric.

        Possible values are Equals, NotEquals, GreaterThan, GreaterThanOrEqual, LessThan and LessThanOrEqual.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dimension(
        self,
    ) -> typing.Optional[typing.List["MetricAlertCriteriaDimensionProp"]]:
        '''One or more dimensions.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#dimension}
        '''
        result = self._values.get("dimension")
        return typing.cast(typing.Optional[typing.List["MetricAlertCriteriaDimensionProp"]], result)

    @builtins.property
    def skip_metric_validation(self) -> typing.Optional[builtins.bool]:
        '''Skip the metric validation to allow creating an alert rule on a custom metric that isn't yet emitted?

        :default: false.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#skip_metric_validation}
        '''
        result = self._values.get("skip_metric_validation")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetricAlertCriteriaBaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_metricalert.MetricAlertCriteriaDimensionProp",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "operator": "operator", "values": "values"},
)
class MetricAlertCriteriaDimensionProp:
    def __init__(
        self,
        *,
        name: builtins.str,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param name: The dimension name.
        :param operator: The dimension operator. Possible values are Include, Exclude and StartsWith.
        :param values: The dimension values. Use a wildcard * to collect all.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#dimension}
        :description: The dimension properties for a Metric Alert Criteria.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fad1a3301130bfb3fc3685343a7ae98a55d316b0f52af7dc52f87c22204f7e84)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "operator": operator,
            "values": values,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''The dimension name.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#dimension_name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def operator(self) -> builtins.str:
        '''The dimension operator.

        Possible values are Include, Exclude and StartsWith.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#dimension_operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''The dimension values.

        Use a wildcard * to collect all.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#dimension_values}
        '''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetricAlertCriteriaDimensionProp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_metricalert.MetricAlertCriteriaProp",
    jsii_struct_bases=[MetricAlertCriteriaBaseProps],
    name_mapping={
        "aggregation": "aggregation",
        "metric_name": "metricName",
        "metric_namespace": "metricNamespace",
        "operator": "operator",
        "dimension": "dimension",
        "skip_metric_validation": "skipMetricValidation",
        "threshold": "threshold",
    },
)
class MetricAlertCriteriaProp(MetricAlertCriteriaBaseProps):
    def __init__(
        self,
        *,
        aggregation: builtins.str,
        metric_name: builtins.str,
        metric_namespace: builtins.str,
        operator: builtins.str,
        dimension: typing.Optional[typing.Sequence[typing.Union[MetricAlertCriteriaDimensionProp, typing.Dict[builtins.str, typing.Any]]]] = None,
        skip_metric_validation: typing.Optional[builtins.bool] = None,
        threshold: jsii.Number,
    ) -> None:
        '''
        :param aggregation: The aggregation type to apply to the metric. Possible values are Average, Count, Minimum, Maximum and Total.
        :param metric_name: The name of the metric to monitor.
        :param metric_namespace: The namespace of the metric.
        :param operator: The operator to apply to the metric. Possible values are Equals, NotEquals, GreaterThan, GreaterThanOrEqual, LessThan and LessThanOrEqual.
        :param dimension: One or more dimensions.
        :param skip_metric_validation: Skip the metric validation to allow creating an alert rule on a custom metric that isn't yet emitted? Default: false.
        :param threshold: The threshold value for the metric that triggers the alert.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#criteria}
        :description: The criteria properties for a Metric Alert.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8510797c51c82823528fa3e989c82b1aa00ee5541f39bca355ff9b7797b0d91)
            check_type(argname="argument aggregation", value=aggregation, expected_type=type_hints["aggregation"])
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument metric_namespace", value=metric_namespace, expected_type=type_hints["metric_namespace"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument dimension", value=dimension, expected_type=type_hints["dimension"])
            check_type(argname="argument skip_metric_validation", value=skip_metric_validation, expected_type=type_hints["skip_metric_validation"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "aggregation": aggregation,
            "metric_name": metric_name,
            "metric_namespace": metric_namespace,
            "operator": operator,
            "threshold": threshold,
        }
        if dimension is not None:
            self._values["dimension"] = dimension
        if skip_metric_validation is not None:
            self._values["skip_metric_validation"] = skip_metric_validation

    @builtins.property
    def aggregation(self) -> builtins.str:
        '''The aggregation type to apply to the metric.

        Possible values are Average, Count, Minimum, Maximum and Total.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#aggregation}
        '''
        result = self._values.get("aggregation")
        assert result is not None, "Required property 'aggregation' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metric_name(self) -> builtins.str:
        '''The name of the metric to monitor.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#metric_name}
        '''
        result = self._values.get("metric_name")
        assert result is not None, "Required property 'metric_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metric_namespace(self) -> builtins.str:
        '''The namespace of the metric.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#metric_namespace}
        '''
        result = self._values.get("metric_namespace")
        assert result is not None, "Required property 'metric_namespace' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def operator(self) -> builtins.str:
        '''The operator to apply to the metric.

        Possible values are Equals, NotEquals, GreaterThan, GreaterThanOrEqual, LessThan and LessThanOrEqual.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dimension(
        self,
    ) -> typing.Optional[typing.List[MetricAlertCriteriaDimensionProp]]:
        '''One or more dimensions.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#dimension}
        '''
        result = self._values.get("dimension")
        return typing.cast(typing.Optional[typing.List[MetricAlertCriteriaDimensionProp]], result)

    @builtins.property
    def skip_metric_validation(self) -> typing.Optional[builtins.bool]:
        '''Skip the metric validation to allow creating an alert rule on a custom metric that isn't yet emitted?

        :default: false.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#skip_metric_validation}
        '''
        result = self._values.get("skip_metric_validation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def threshold(self) -> jsii.Number:
        '''The threshold value for the metric that triggers the alert.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#threshold}
        '''
        result = self._values.get("threshold")
        assert result is not None, "Required property 'threshold' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetricAlertCriteriaProp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@microsoft/terraform-cdk-constructs.azure_metricalert.MetricAlertDynamicCritiriaProps",
    jsii_struct_bases=[MetricAlertCriteriaBaseProps],
    name_mapping={
        "aggregation": "aggregation",
        "metric_name": "metricName",
        "metric_namespace": "metricNamespace",
        "operator": "operator",
        "dimension": "dimension",
        "skip_metric_validation": "skipMetricValidation",
        "alert_sensitivity": "alertSensitivity",
        "evaluation_failure_count": "evaluationFailureCount",
        "evaluation_total_count": "evaluationTotalCount",
        "ignore_data_before": "ignoreDataBefore",
    },
)
class MetricAlertDynamicCritiriaProps(MetricAlertCriteriaBaseProps):
    def __init__(
        self,
        *,
        aggregation: builtins.str,
        metric_name: builtins.str,
        metric_namespace: builtins.str,
        operator: builtins.str,
        dimension: typing.Optional[typing.Sequence[typing.Union[MetricAlertCriteriaDimensionProp, typing.Dict[builtins.str, typing.Any]]]] = None,
        skip_metric_validation: typing.Optional[builtins.bool] = None,
        alert_sensitivity: builtins.str,
        evaluation_failure_count: typing.Optional[jsii.Number] = None,
        evaluation_total_count: typing.Optional[jsii.Number] = None,
        ignore_data_before: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aggregation: The aggregation type to apply to the metric. Possible values are Average, Count, Minimum, Maximum and Total.
        :param metric_name: The name of the metric to monitor.
        :param metric_namespace: The namespace of the metric.
        :param operator: The operator to apply to the metric. Possible values are Equals, NotEquals, GreaterThan, GreaterThanOrEqual, LessThan and LessThanOrEqual.
        :param dimension: One or more dimensions.
        :param skip_metric_validation: Skip the metric validation to allow creating an alert rule on a custom metric that isn't yet emitted? Default: false.
        :param alert_sensitivity: The extent of deviation required to trigger an alert. Possible values are Low, Medium and High.
        :param evaluation_failure_count: The number of violations to trigger an alert. Should be smaller or equal to evaluation_total_count. Default: 4
        :param evaluation_total_count: he number of aggregated lookback points. The lookback time window is calculated based on the aggregation granularity (window_size) and the selected number of aggregated points. Default: 4
        :param ignore_data_before: The ISO8601 date from which to start learning the metric historical data and calculate the dynamic thresholds.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#dynamic_criteria}
        :description: The dynamic criteria properties for a Metric Alert.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d030599e7ae14372ed150135a09a1fcf950eb248e6001aca2429d30a74f4a8d)
            check_type(argname="argument aggregation", value=aggregation, expected_type=type_hints["aggregation"])
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument metric_namespace", value=metric_namespace, expected_type=type_hints["metric_namespace"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument dimension", value=dimension, expected_type=type_hints["dimension"])
            check_type(argname="argument skip_metric_validation", value=skip_metric_validation, expected_type=type_hints["skip_metric_validation"])
            check_type(argname="argument alert_sensitivity", value=alert_sensitivity, expected_type=type_hints["alert_sensitivity"])
            check_type(argname="argument evaluation_failure_count", value=evaluation_failure_count, expected_type=type_hints["evaluation_failure_count"])
            check_type(argname="argument evaluation_total_count", value=evaluation_total_count, expected_type=type_hints["evaluation_total_count"])
            check_type(argname="argument ignore_data_before", value=ignore_data_before, expected_type=type_hints["ignore_data_before"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "aggregation": aggregation,
            "metric_name": metric_name,
            "metric_namespace": metric_namespace,
            "operator": operator,
            "alert_sensitivity": alert_sensitivity,
        }
        if dimension is not None:
            self._values["dimension"] = dimension
        if skip_metric_validation is not None:
            self._values["skip_metric_validation"] = skip_metric_validation
        if evaluation_failure_count is not None:
            self._values["evaluation_failure_count"] = evaluation_failure_count
        if evaluation_total_count is not None:
            self._values["evaluation_total_count"] = evaluation_total_count
        if ignore_data_before is not None:
            self._values["ignore_data_before"] = ignore_data_before

    @builtins.property
    def aggregation(self) -> builtins.str:
        '''The aggregation type to apply to the metric.

        Possible values are Average, Count, Minimum, Maximum and Total.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#aggregation}
        '''
        result = self._values.get("aggregation")
        assert result is not None, "Required property 'aggregation' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metric_name(self) -> builtins.str:
        '''The name of the metric to monitor.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#metric_name}
        '''
        result = self._values.get("metric_name")
        assert result is not None, "Required property 'metric_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metric_namespace(self) -> builtins.str:
        '''The namespace of the metric.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#metric_namespace}
        '''
        result = self._values.get("metric_namespace")
        assert result is not None, "Required property 'metric_namespace' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def operator(self) -> builtins.str:
        '''The operator to apply to the metric.

        Possible values are Equals, NotEquals, GreaterThan, GreaterThanOrEqual, LessThan and LessThanOrEqual.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dimension(
        self,
    ) -> typing.Optional[typing.List[MetricAlertCriteriaDimensionProp]]:
        '''One or more dimensions.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#dimension}
        '''
        result = self._values.get("dimension")
        return typing.cast(typing.Optional[typing.List[MetricAlertCriteriaDimensionProp]], result)

    @builtins.property
    def skip_metric_validation(self) -> typing.Optional[builtins.bool]:
        '''Skip the metric validation to allow creating an alert rule on a custom metric that isn't yet emitted?

        :default: false.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#skip_metric_validation}
        '''
        result = self._values.get("skip_metric_validation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def alert_sensitivity(self) -> builtins.str:
        '''The extent of deviation required to trigger an alert.

        Possible values are Low, Medium and High.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#alert_sensitivity}
        '''
        result = self._values.get("alert_sensitivity")
        assert result is not None, "Required property 'alert_sensitivity' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def evaluation_failure_count(self) -> typing.Optional[jsii.Number]:
        '''The number of violations to trigger an alert.

        Should be smaller or equal to evaluation_total_count.

        :default: 4

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#evaluation_failure_count}
        '''
        result = self._values.get("evaluation_failure_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def evaluation_total_count(self) -> typing.Optional[jsii.Number]:
        '''he number of aggregated lookback points.

        The lookback time window is calculated based on the aggregation granularity (window_size) and the selected number of aggregated points.

        :default: 4

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#evaluation_total_count}
        '''
        result = self._values.get("evaluation_total_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ignore_data_before(self) -> typing.Optional[builtins.str]:
        '''The ISO8601 date from which to start learning the metric historical data and calculate the dynamic thresholds.

        :see: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_metric_alert.html#ignore_data_before}
        '''
        result = self._values.get("ignore_data_before")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetricAlertDynamicCritiriaProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "IBaseMetricAlertProps",
    "IMetricAlertProps",
    "MetricAlert",
    "MetricAlertActionProp",
    "MetricAlertCriteriaBaseProps",
    "MetricAlertCriteriaDimensionProp",
    "MetricAlertCriteriaProp",
    "MetricAlertDynamicCritiriaProps",
]

publication.publish()

def _typecheckingstub__d9b6d2f05b6ed0d46af4ec9192122ef44c3980479c396d43304bb0b9b694e113(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a71a6bc41cbe01c48e85fc89a6e119390fa9f8a525e7cf56ded112c85d2ce1b4(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6121ecbd0831518b2ec58c88fba21c560e324250edb73d3cb548e7b87b63cb7a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4208080d1e6a948e5cd36c58ec3192a87a4670c52f57c2611997528c85acd7f0(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32d092155070280bb1f6c612ff5cfd8100865141ec1f19899057122299f11708(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89a31dd72d07a3fb3ea9f11c966fd677dff2f202fa495d954aa9d15a60a7539b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    props: IMetricAlertProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c10e6a840860f6b4069b766a02a280d1a0fbeb3f59e8d4149c18a3a463743083(
    *,
    action_group_id: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d07a7654959ce4d1f3e2cfa72b5acc5537f57d967a4d561b13ea4c9114815c6(
    *,
    aggregation: builtins.str,
    metric_name: builtins.str,
    metric_namespace: builtins.str,
    operator: builtins.str,
    dimension: typing.Optional[typing.Sequence[typing.Union[MetricAlertCriteriaDimensionProp, typing.Dict[builtins.str, typing.Any]]]] = None,
    skip_metric_validation: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fad1a3301130bfb3fc3685343a7ae98a55d316b0f52af7dc52f87c22204f7e84(
    *,
    name: builtins.str,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8510797c51c82823528fa3e989c82b1aa00ee5541f39bca355ff9b7797b0d91(
    *,
    aggregation: builtins.str,
    metric_name: builtins.str,
    metric_namespace: builtins.str,
    operator: builtins.str,
    dimension: typing.Optional[typing.Sequence[typing.Union[MetricAlertCriteriaDimensionProp, typing.Dict[builtins.str, typing.Any]]]] = None,
    skip_metric_validation: typing.Optional[builtins.bool] = None,
    threshold: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d030599e7ae14372ed150135a09a1fcf950eb248e6001aca2429d30a74f4a8d(
    *,
    aggregation: builtins.str,
    metric_name: builtins.str,
    metric_namespace: builtins.str,
    operator: builtins.str,
    dimension: typing.Optional[typing.Sequence[typing.Union[MetricAlertCriteriaDimensionProp, typing.Dict[builtins.str, typing.Any]]]] = None,
    skip_metric_validation: typing.Optional[builtins.bool] = None,
    alert_sensitivity: builtins.str,
    evaluation_failure_count: typing.Optional[jsii.Number] = None,
    evaluation_total_count: typing.Optional[jsii.Number] = None,
    ignore_data_before: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
