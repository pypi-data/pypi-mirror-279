# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = [
    'AccountIamBindingCondition',
    'AccountIamMemberCondition',
    'BudgetAllUpdatesRule',
    'BudgetAmount',
    'BudgetAmountSpecifiedAmount',
    'BudgetBudgetFilter',
    'BudgetBudgetFilterCustomPeriod',
    'BudgetBudgetFilterCustomPeriodEndDate',
    'BudgetBudgetFilterCustomPeriodStartDate',
    'BudgetThresholdRule',
]

@pulumi.output_type
class AccountIamBindingCondition(dict):
    def __init__(__self__, *,
                 expression: str,
                 title: str,
                 description: Optional[str] = None):
        pulumi.set(__self__, "expression", expression)
        pulumi.set(__self__, "title", title)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter
    def expression(self) -> str:
        return pulumi.get(self, "expression")

    @property
    @pulumi.getter
    def title(self) -> str:
        return pulumi.get(self, "title")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        return pulumi.get(self, "description")


@pulumi.output_type
class AccountIamMemberCondition(dict):
    def __init__(__self__, *,
                 expression: str,
                 title: str,
                 description: Optional[str] = None):
        pulumi.set(__self__, "expression", expression)
        pulumi.set(__self__, "title", title)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter
    def expression(self) -> str:
        return pulumi.get(self, "expression")

    @property
    @pulumi.getter
    def title(self) -> str:
        return pulumi.get(self, "title")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        return pulumi.get(self, "description")


@pulumi.output_type
class BudgetAllUpdatesRule(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "disableDefaultIamRecipients":
            suggest = "disable_default_iam_recipients"
        elif key == "monitoringNotificationChannels":
            suggest = "monitoring_notification_channels"
        elif key == "pubsubTopic":
            suggest = "pubsub_topic"
        elif key == "schemaVersion":
            suggest = "schema_version"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in BudgetAllUpdatesRule. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        BudgetAllUpdatesRule.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        BudgetAllUpdatesRule.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 disable_default_iam_recipients: Optional[bool] = None,
                 monitoring_notification_channels: Optional[Sequence[str]] = None,
                 pubsub_topic: Optional[str] = None,
                 schema_version: Optional[str] = None):
        """
        :param bool disable_default_iam_recipients: Boolean. When set to true, disables default notifications sent
               when a threshold is exceeded. Default recipients are
               those with Billing Account Administrators and Billing
               Account Users IAM roles for the target account.
        :param Sequence[str] monitoring_notification_channels: The full resource name of a monitoring notification
               channel in the form
               projects/{project_id}/notificationChannels/{channel_id}.
               A maximum of 5 channels are allowed.
        :param str pubsub_topic: The name of the Cloud Pub/Sub topic where budget related
               messages will be published, in the form
               projects/{project_id}/topics/{topic_id}. Updates are sent
               at regular intervals to the topic.
        :param str schema_version: The schema version of the notification. Only "1.0" is
               accepted. It represents the JSON schema as defined in
               https://cloud.google.com/billing/docs/how-to/budgets#notification_format.
        """
        if disable_default_iam_recipients is not None:
            pulumi.set(__self__, "disable_default_iam_recipients", disable_default_iam_recipients)
        if monitoring_notification_channels is not None:
            pulumi.set(__self__, "monitoring_notification_channels", monitoring_notification_channels)
        if pubsub_topic is not None:
            pulumi.set(__self__, "pubsub_topic", pubsub_topic)
        if schema_version is not None:
            pulumi.set(__self__, "schema_version", schema_version)

    @property
    @pulumi.getter(name="disableDefaultIamRecipients")
    def disable_default_iam_recipients(self) -> Optional[bool]:
        """
        Boolean. When set to true, disables default notifications sent
        when a threshold is exceeded. Default recipients are
        those with Billing Account Administrators and Billing
        Account Users IAM roles for the target account.
        """
        return pulumi.get(self, "disable_default_iam_recipients")

    @property
    @pulumi.getter(name="monitoringNotificationChannels")
    def monitoring_notification_channels(self) -> Optional[Sequence[str]]:
        """
        The full resource name of a monitoring notification
        channel in the form
        projects/{project_id}/notificationChannels/{channel_id}.
        A maximum of 5 channels are allowed.
        """
        return pulumi.get(self, "monitoring_notification_channels")

    @property
    @pulumi.getter(name="pubsubTopic")
    def pubsub_topic(self) -> Optional[str]:
        """
        The name of the Cloud Pub/Sub topic where budget related
        messages will be published, in the form
        projects/{project_id}/topics/{topic_id}. Updates are sent
        at regular intervals to the topic.
        """
        return pulumi.get(self, "pubsub_topic")

    @property
    @pulumi.getter(name="schemaVersion")
    def schema_version(self) -> Optional[str]:
        """
        The schema version of the notification. Only "1.0" is
        accepted. It represents the JSON schema as defined in
        https://cloud.google.com/billing/docs/how-to/budgets#notification_format.
        """
        return pulumi.get(self, "schema_version")


@pulumi.output_type
class BudgetAmount(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "lastPeriodAmount":
            suggest = "last_period_amount"
        elif key == "specifiedAmount":
            suggest = "specified_amount"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in BudgetAmount. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        BudgetAmount.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        BudgetAmount.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 last_period_amount: Optional[bool] = None,
                 specified_amount: Optional['outputs.BudgetAmountSpecifiedAmount'] = None):
        """
        :param bool last_period_amount: Configures a budget amount that is automatically set to 100% of
               last period's spend.
               Boolean. Set value to true to use. Do not set to false, instead
               use the `specified_amount` block.
        :param 'BudgetAmountSpecifiedAmountArgs' specified_amount: A specified amount to use as the budget. currencyCode is
               optional. If specified, it must match the currency of the
               billing account. The currencyCode is provided on output.
               Structure is documented below.
        """
        if last_period_amount is not None:
            pulumi.set(__self__, "last_period_amount", last_period_amount)
        if specified_amount is not None:
            pulumi.set(__self__, "specified_amount", specified_amount)

    @property
    @pulumi.getter(name="lastPeriodAmount")
    def last_period_amount(self) -> Optional[bool]:
        """
        Configures a budget amount that is automatically set to 100% of
        last period's spend.
        Boolean. Set value to true to use. Do not set to false, instead
        use the `specified_amount` block.
        """
        return pulumi.get(self, "last_period_amount")

    @property
    @pulumi.getter(name="specifiedAmount")
    def specified_amount(self) -> Optional['outputs.BudgetAmountSpecifiedAmount']:
        """
        A specified amount to use as the budget. currencyCode is
        optional. If specified, it must match the currency of the
        billing account. The currencyCode is provided on output.
        Structure is documented below.
        """
        return pulumi.get(self, "specified_amount")


@pulumi.output_type
class BudgetAmountSpecifiedAmount(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "currencyCode":
            suggest = "currency_code"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in BudgetAmountSpecifiedAmount. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        BudgetAmountSpecifiedAmount.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        BudgetAmountSpecifiedAmount.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 currency_code: Optional[str] = None,
                 nanos: Optional[int] = None,
                 units: Optional[str] = None):
        """
        :param str currency_code: The 3-letter currency code defined in ISO 4217.
        :param int nanos: Number of nano (10^-9) units of the amount.
               The value must be between -999,999,999 and +999,999,999
               inclusive. If units is positive, nanos must be positive or
               zero. If units is zero, nanos can be positive, zero, or
               negative. If units is negative, nanos must be negative or
               zero. For example $-1.75 is represented as units=-1 and
               nanos=-750,000,000.
               
               - - -
        :param str units: The whole units of the amount. For example if currencyCode
               is "USD", then 1 unit is one US dollar.
        """
        if currency_code is not None:
            pulumi.set(__self__, "currency_code", currency_code)
        if nanos is not None:
            pulumi.set(__self__, "nanos", nanos)
        if units is not None:
            pulumi.set(__self__, "units", units)

    @property
    @pulumi.getter(name="currencyCode")
    def currency_code(self) -> Optional[str]:
        """
        The 3-letter currency code defined in ISO 4217.
        """
        return pulumi.get(self, "currency_code")

    @property
    @pulumi.getter
    def nanos(self) -> Optional[int]:
        """
        Number of nano (10^-9) units of the amount.
        The value must be between -999,999,999 and +999,999,999
        inclusive. If units is positive, nanos must be positive or
        zero. If units is zero, nanos can be positive, zero, or
        negative. If units is negative, nanos must be negative or
        zero. For example $-1.75 is represented as units=-1 and
        nanos=-750,000,000.

        - - -
        """
        return pulumi.get(self, "nanos")

    @property
    @pulumi.getter
    def units(self) -> Optional[str]:
        """
        The whole units of the amount. For example if currencyCode
        is "USD", then 1 unit is one US dollar.
        """
        return pulumi.get(self, "units")


@pulumi.output_type
class BudgetBudgetFilter(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "calendarPeriod":
            suggest = "calendar_period"
        elif key == "creditTypes":
            suggest = "credit_types"
        elif key == "creditTypesTreatment":
            suggest = "credit_types_treatment"
        elif key == "customPeriod":
            suggest = "custom_period"
        elif key == "resourceAncestors":
            suggest = "resource_ancestors"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in BudgetBudgetFilter. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        BudgetBudgetFilter.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        BudgetBudgetFilter.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 calendar_period: Optional[str] = None,
                 credit_types: Optional[Sequence[str]] = None,
                 credit_types_treatment: Optional[str] = None,
                 custom_period: Optional['outputs.BudgetBudgetFilterCustomPeriod'] = None,
                 labels: Optional[Mapping[str, str]] = None,
                 projects: Optional[Sequence[str]] = None,
                 resource_ancestors: Optional[Sequence[str]] = None,
                 services: Optional[Sequence[str]] = None,
                 subaccounts: Optional[Sequence[str]] = None):
        """
        :param str calendar_period: A CalendarPeriod represents the abstract concept of a recurring time period that has a
               canonical start. Grammatically, "the start of the current CalendarPeriod".
               All calendar times begin at 12 AM US and Canadian Pacific Time (UTC-8).
               Exactly one of `calendar_period`, `custom_period` must be provided.
               Possible values are: `MONTH`, `QUARTER`, `YEAR`, `CALENDAR_PERIOD_UNSPECIFIED`.
        :param Sequence[str] credit_types: Optional. If creditTypesTreatment is INCLUDE_SPECIFIED_CREDITS,
               this is a list of credit types to be subtracted from gross cost to determine the spend for threshold calculations. See a list of acceptable credit type values.
               If creditTypesTreatment is not INCLUDE_SPECIFIED_CREDITS, this field must be empty.
               **Note:** If the field has a value in the config and needs to be removed, the field has to be an emtpy array in the config.
        :param str credit_types_treatment: Specifies how credits should be treated when determining spend
               for threshold calculations.
               Default value is `INCLUDE_ALL_CREDITS`.
               Possible values are: `INCLUDE_ALL_CREDITS`, `EXCLUDE_ALL_CREDITS`, `INCLUDE_SPECIFIED_CREDITS`.
        :param 'BudgetBudgetFilterCustomPeriodArgs' custom_period: Specifies to track usage from any start date (required) to any end date (optional).
               This time period is static, it does not recur.
               Exactly one of `calendar_period`, `custom_period` must be provided.
               Structure is documented below.
        :param Mapping[str, str] labels: A single label and value pair specifying that usage from only
               this set of labeled resources should be included in the budget.
        :param Sequence[str] projects: A set of projects of the form projects/{project_number},
               specifying that usage from only this set of projects should be
               included in the budget. If omitted, the report will include
               all usage for the billing account, regardless of which project
               the usage occurred on.
        :param Sequence[str] resource_ancestors: A set of folder and organization names of the form folders/{folderId} or organizations/{organizationId},
               specifying that usage from only this set of folders and organizations should be included in the budget.
               If omitted, the budget includes all usage that the billing account pays for. If the folder or organization
               contains projects that are paid for by a different Cloud Billing account, the budget doesn't apply to those projects.
        :param Sequence[str] services: A set of services of the form services/{service_id},
               specifying that usage from only this set of services should be
               included in the budget. If omitted, the report will include
               usage for all the services. The service names are available
               through the Catalog API:
               https://cloud.google.com/billing/v1/how-tos/catalog-api.
        :param Sequence[str] subaccounts: A set of subaccounts of the form billingAccounts/{account_id},
               specifying that usage from only this set of subaccounts should
               be included in the budget. If a subaccount is set to the name of
               the parent account, usage from the parent account will be included.
               If the field is omitted, the report will include usage from the parent
               account and all subaccounts, if they exist.
               **Note:** If the field has a value in the config and needs to be removed, the field has to be an emtpy array in the config.
        """
        if calendar_period is not None:
            pulumi.set(__self__, "calendar_period", calendar_period)
        if credit_types is not None:
            pulumi.set(__self__, "credit_types", credit_types)
        if credit_types_treatment is not None:
            pulumi.set(__self__, "credit_types_treatment", credit_types_treatment)
        if custom_period is not None:
            pulumi.set(__self__, "custom_period", custom_period)
        if labels is not None:
            pulumi.set(__self__, "labels", labels)
        if projects is not None:
            pulumi.set(__self__, "projects", projects)
        if resource_ancestors is not None:
            pulumi.set(__self__, "resource_ancestors", resource_ancestors)
        if services is not None:
            pulumi.set(__self__, "services", services)
        if subaccounts is not None:
            pulumi.set(__self__, "subaccounts", subaccounts)

    @property
    @pulumi.getter(name="calendarPeriod")
    def calendar_period(self) -> Optional[str]:
        """
        A CalendarPeriod represents the abstract concept of a recurring time period that has a
        canonical start. Grammatically, "the start of the current CalendarPeriod".
        All calendar times begin at 12 AM US and Canadian Pacific Time (UTC-8).
        Exactly one of `calendar_period`, `custom_period` must be provided.
        Possible values are: `MONTH`, `QUARTER`, `YEAR`, `CALENDAR_PERIOD_UNSPECIFIED`.
        """
        return pulumi.get(self, "calendar_period")

    @property
    @pulumi.getter(name="creditTypes")
    def credit_types(self) -> Optional[Sequence[str]]:
        """
        Optional. If creditTypesTreatment is INCLUDE_SPECIFIED_CREDITS,
        this is a list of credit types to be subtracted from gross cost to determine the spend for threshold calculations. See a list of acceptable credit type values.
        If creditTypesTreatment is not INCLUDE_SPECIFIED_CREDITS, this field must be empty.
        **Note:** If the field has a value in the config and needs to be removed, the field has to be an emtpy array in the config.
        """
        return pulumi.get(self, "credit_types")

    @property
    @pulumi.getter(name="creditTypesTreatment")
    def credit_types_treatment(self) -> Optional[str]:
        """
        Specifies how credits should be treated when determining spend
        for threshold calculations.
        Default value is `INCLUDE_ALL_CREDITS`.
        Possible values are: `INCLUDE_ALL_CREDITS`, `EXCLUDE_ALL_CREDITS`, `INCLUDE_SPECIFIED_CREDITS`.
        """
        return pulumi.get(self, "credit_types_treatment")

    @property
    @pulumi.getter(name="customPeriod")
    def custom_period(self) -> Optional['outputs.BudgetBudgetFilterCustomPeriod']:
        """
        Specifies to track usage from any start date (required) to any end date (optional).
        This time period is static, it does not recur.
        Exactly one of `calendar_period`, `custom_period` must be provided.
        Structure is documented below.
        """
        return pulumi.get(self, "custom_period")

    @property
    @pulumi.getter
    def labels(self) -> Optional[Mapping[str, str]]:
        """
        A single label and value pair specifying that usage from only
        this set of labeled resources should be included in the budget.
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def projects(self) -> Optional[Sequence[str]]:
        """
        A set of projects of the form projects/{project_number},
        specifying that usage from only this set of projects should be
        included in the budget. If omitted, the report will include
        all usage for the billing account, regardless of which project
        the usage occurred on.
        """
        return pulumi.get(self, "projects")

    @property
    @pulumi.getter(name="resourceAncestors")
    def resource_ancestors(self) -> Optional[Sequence[str]]:
        """
        A set of folder and organization names of the form folders/{folderId} or organizations/{organizationId},
        specifying that usage from only this set of folders and organizations should be included in the budget.
        If omitted, the budget includes all usage that the billing account pays for. If the folder or organization
        contains projects that are paid for by a different Cloud Billing account, the budget doesn't apply to those projects.
        """
        return pulumi.get(self, "resource_ancestors")

    @property
    @pulumi.getter
    def services(self) -> Optional[Sequence[str]]:
        """
        A set of services of the form services/{service_id},
        specifying that usage from only this set of services should be
        included in the budget. If omitted, the report will include
        usage for all the services. The service names are available
        through the Catalog API:
        https://cloud.google.com/billing/v1/how-tos/catalog-api.
        """
        return pulumi.get(self, "services")

    @property
    @pulumi.getter
    def subaccounts(self) -> Optional[Sequence[str]]:
        """
        A set of subaccounts of the form billingAccounts/{account_id},
        specifying that usage from only this set of subaccounts should
        be included in the budget. If a subaccount is set to the name of
        the parent account, usage from the parent account will be included.
        If the field is omitted, the report will include usage from the parent
        account and all subaccounts, if they exist.
        **Note:** If the field has a value in the config and needs to be removed, the field has to be an emtpy array in the config.
        """
        return pulumi.get(self, "subaccounts")


@pulumi.output_type
class BudgetBudgetFilterCustomPeriod(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "startDate":
            suggest = "start_date"
        elif key == "endDate":
            suggest = "end_date"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in BudgetBudgetFilterCustomPeriod. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        BudgetBudgetFilterCustomPeriod.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        BudgetBudgetFilterCustomPeriod.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 start_date: 'outputs.BudgetBudgetFilterCustomPeriodStartDate',
                 end_date: Optional['outputs.BudgetBudgetFilterCustomPeriodEndDate'] = None):
        """
        :param 'BudgetBudgetFilterCustomPeriodStartDateArgs' start_date: A start date is required. The start date must be after January 1, 2017.
               Structure is documented below.
        :param 'BudgetBudgetFilterCustomPeriodEndDateArgs' end_date: Optional. The end date of the time period. Budgets with elapsed end date won't be processed.
               If unset, specifies to track all usage incurred since the startDate.
               Structure is documented below.
        """
        pulumi.set(__self__, "start_date", start_date)
        if end_date is not None:
            pulumi.set(__self__, "end_date", end_date)

    @property
    @pulumi.getter(name="startDate")
    def start_date(self) -> 'outputs.BudgetBudgetFilterCustomPeriodStartDate':
        """
        A start date is required. The start date must be after January 1, 2017.
        Structure is documented below.
        """
        return pulumi.get(self, "start_date")

    @property
    @pulumi.getter(name="endDate")
    def end_date(self) -> Optional['outputs.BudgetBudgetFilterCustomPeriodEndDate']:
        """
        Optional. The end date of the time period. Budgets with elapsed end date won't be processed.
        If unset, specifies to track all usage incurred since the startDate.
        Structure is documented below.
        """
        return pulumi.get(self, "end_date")


@pulumi.output_type
class BudgetBudgetFilterCustomPeriodEndDate(dict):
    def __init__(__self__, *,
                 day: int,
                 month: int,
                 year: int):
        """
        :param int day: Day of a month. Must be from 1 to 31 and valid for the year and month.
        :param int month: Month of a year. Must be from 1 to 12.
        :param int year: Year of the date. Must be from 1 to 9999.
        """
        pulumi.set(__self__, "day", day)
        pulumi.set(__self__, "month", month)
        pulumi.set(__self__, "year", year)

    @property
    @pulumi.getter
    def day(self) -> int:
        """
        Day of a month. Must be from 1 to 31 and valid for the year and month.
        """
        return pulumi.get(self, "day")

    @property
    @pulumi.getter
    def month(self) -> int:
        """
        Month of a year. Must be from 1 to 12.
        """
        return pulumi.get(self, "month")

    @property
    @pulumi.getter
    def year(self) -> int:
        """
        Year of the date. Must be from 1 to 9999.
        """
        return pulumi.get(self, "year")


@pulumi.output_type
class BudgetBudgetFilterCustomPeriodStartDate(dict):
    def __init__(__self__, *,
                 day: int,
                 month: int,
                 year: int):
        """
        :param int day: Day of a month. Must be from 1 to 31 and valid for the year and month.
        :param int month: Month of a year. Must be from 1 to 12.
        :param int year: Year of the date. Must be from 1 to 9999.
        """
        pulumi.set(__self__, "day", day)
        pulumi.set(__self__, "month", month)
        pulumi.set(__self__, "year", year)

    @property
    @pulumi.getter
    def day(self) -> int:
        """
        Day of a month. Must be from 1 to 31 and valid for the year and month.
        """
        return pulumi.get(self, "day")

    @property
    @pulumi.getter
    def month(self) -> int:
        """
        Month of a year. Must be from 1 to 12.
        """
        return pulumi.get(self, "month")

    @property
    @pulumi.getter
    def year(self) -> int:
        """
        Year of the date. Must be from 1 to 9999.
        """
        return pulumi.get(self, "year")


@pulumi.output_type
class BudgetThresholdRule(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "thresholdPercent":
            suggest = "threshold_percent"
        elif key == "spendBasis":
            suggest = "spend_basis"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in BudgetThresholdRule. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        BudgetThresholdRule.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        BudgetThresholdRule.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 threshold_percent: float,
                 spend_basis: Optional[str] = None):
        """
        :param float threshold_percent: Send an alert when this threshold is exceeded. This is a
               1.0-based percentage, so 0.5 = 50%. Must be >= 0.
        :param str spend_basis: The type of basis used to determine if spend has passed
               the threshold.
               Default value is `CURRENT_SPEND`.
               Possible values are: `CURRENT_SPEND`, `FORECASTED_SPEND`.
        """
        pulumi.set(__self__, "threshold_percent", threshold_percent)
        if spend_basis is not None:
            pulumi.set(__self__, "spend_basis", spend_basis)

    @property
    @pulumi.getter(name="thresholdPercent")
    def threshold_percent(self) -> float:
        """
        Send an alert when this threshold is exceeded. This is a
        1.0-based percentage, so 0.5 = 50%. Must be >= 0.
        """
        return pulumi.get(self, "threshold_percent")

    @property
    @pulumi.getter(name="spendBasis")
    def spend_basis(self) -> Optional[str]:
        """
        The type of basis used to determine if spend has passed
        the threshold.
        Default value is `CURRENT_SPEND`.
        Possible values are: `CURRENT_SPEND`, `FORECASTED_SPEND`.
        """
        return pulumi.get(self, "spend_basis")


