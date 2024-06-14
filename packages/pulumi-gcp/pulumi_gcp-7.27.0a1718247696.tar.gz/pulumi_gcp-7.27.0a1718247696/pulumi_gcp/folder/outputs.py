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
    'AccessApprovalSettingsEnrolledService',
    'IAMBindingCondition',
    'IAMMemberCondition',
    'IamAuditConfigAuditLogConfig',
    'OrganizationPolicyBooleanPolicy',
    'OrganizationPolicyListPolicy',
    'OrganizationPolicyListPolicyAllow',
    'OrganizationPolicyListPolicyDeny',
    'OrganizationPolicyRestorePolicy',
    'GetOrganizationPolicyBooleanPolicyResult',
    'GetOrganizationPolicyListPolicyResult',
    'GetOrganizationPolicyListPolicyAllowResult',
    'GetOrganizationPolicyListPolicyDenyResult',
    'GetOrganizationPolicyRestorePolicyResult',
]

@pulumi.output_type
class AccessApprovalSettingsEnrolledService(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "cloudProduct":
            suggest = "cloud_product"
        elif key == "enrollmentLevel":
            suggest = "enrollment_level"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AccessApprovalSettingsEnrolledService. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AccessApprovalSettingsEnrolledService.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AccessApprovalSettingsEnrolledService.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 cloud_product: str,
                 enrollment_level: Optional[str] = None):
        """
        :param str cloud_product: The product for which Access Approval will be enrolled. Allowed values are listed (case-sensitive):
               * all
               * App Engine
               * BigQuery
               * Cloud Bigtable
               * Cloud Key Management Service
               * Compute Engine
               * Cloud Dataflow
               * Cloud Identity and Access Management
               * Cloud Pub/Sub
               * Cloud Storage
               * Persistent Disk
               Note: These values are supported as input, but considered a legacy format:
               * all
               * appengine.googleapis.com
               * bigquery.googleapis.com
               * bigtable.googleapis.com
               * cloudkms.googleapis.com
               * compute.googleapis.com
               * dataflow.googleapis.com
               * iam.googleapis.com
               * pubsub.googleapis.com
               * storage.googleapis.com
        :param str enrollment_level: The enrollment level of the service.
               Default value is `BLOCK_ALL`.
               Possible values are: `BLOCK_ALL`.
               
               - - -
        """
        pulumi.set(__self__, "cloud_product", cloud_product)
        if enrollment_level is not None:
            pulumi.set(__self__, "enrollment_level", enrollment_level)

    @property
    @pulumi.getter(name="cloudProduct")
    def cloud_product(self) -> str:
        """
        The product for which Access Approval will be enrolled. Allowed values are listed (case-sensitive):
        * all
        * App Engine
        * BigQuery
        * Cloud Bigtable
        * Cloud Key Management Service
        * Compute Engine
        * Cloud Dataflow
        * Cloud Identity and Access Management
        * Cloud Pub/Sub
        * Cloud Storage
        * Persistent Disk
        Note: These values are supported as input, but considered a legacy format:
        * all
        * appengine.googleapis.com
        * bigquery.googleapis.com
        * bigtable.googleapis.com
        * cloudkms.googleapis.com
        * compute.googleapis.com
        * dataflow.googleapis.com
        * iam.googleapis.com
        * pubsub.googleapis.com
        * storage.googleapis.com
        """
        return pulumi.get(self, "cloud_product")

    @property
    @pulumi.getter(name="enrollmentLevel")
    def enrollment_level(self) -> Optional[str]:
        """
        The enrollment level of the service.
        Default value is `BLOCK_ALL`.
        Possible values are: `BLOCK_ALL`.

        - - -
        """
        return pulumi.get(self, "enrollment_level")


@pulumi.output_type
class IAMBindingCondition(dict):
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
class IAMMemberCondition(dict):
    def __init__(__self__, *,
                 expression: str,
                 title: str,
                 description: Optional[str] = None):
        """
        :param str expression: Textual representation of an expression in Common Expression Language syntax.
        :param str title: A title for the expression, i.e. a short string describing its purpose.
        :param str description: An optional description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI.
               
               > **Warning:** This provider considers the `role` and condition contents (`title`+`description`+`expression`) as the
               identifier for the binding. This means that if any part of the condition is changed out-of-band, the provider will
               consider it to be an entirely different resource and will treat it as such.
        """
        pulumi.set(__self__, "expression", expression)
        pulumi.set(__self__, "title", title)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter
    def expression(self) -> str:
        """
        Textual representation of an expression in Common Expression Language syntax.
        """
        return pulumi.get(self, "expression")

    @property
    @pulumi.getter
    def title(self) -> str:
        """
        A title for the expression, i.e. a short string describing its purpose.
        """
        return pulumi.get(self, "title")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        An optional description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI.

        > **Warning:** This provider considers the `role` and condition contents (`title`+`description`+`expression`) as the
        identifier for the binding. This means that if any part of the condition is changed out-of-band, the provider will
        consider it to be an entirely different resource and will treat it as such.
        """
        return pulumi.get(self, "description")


@pulumi.output_type
class IamAuditConfigAuditLogConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "logType":
            suggest = "log_type"
        elif key == "exemptedMembers":
            suggest = "exempted_members"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in IamAuditConfigAuditLogConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        IamAuditConfigAuditLogConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        IamAuditConfigAuditLogConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 log_type: str,
                 exempted_members: Optional[Sequence[str]] = None):
        """
        :param str log_type: Permission type for which logging is to be configured.  Must be one of `DATA_READ`, `DATA_WRITE`, or `ADMIN_READ`.
        :param Sequence[str] exempted_members: Identities that do not cause logging for this type of permission.  The format is the same as that for `members`.
        """
        pulumi.set(__self__, "log_type", log_type)
        if exempted_members is not None:
            pulumi.set(__self__, "exempted_members", exempted_members)

    @property
    @pulumi.getter(name="logType")
    def log_type(self) -> str:
        """
        Permission type for which logging is to be configured.  Must be one of `DATA_READ`, `DATA_WRITE`, or `ADMIN_READ`.
        """
        return pulumi.get(self, "log_type")

    @property
    @pulumi.getter(name="exemptedMembers")
    def exempted_members(self) -> Optional[Sequence[str]]:
        """
        Identities that do not cause logging for this type of permission.  The format is the same as that for `members`.
        """
        return pulumi.get(self, "exempted_members")


@pulumi.output_type
class OrganizationPolicyBooleanPolicy(dict):
    def __init__(__self__, *,
                 enforced: bool):
        """
        :param bool enforced: If true, then the Policy is enforced. If false, then any configuration is acceptable.
        """
        pulumi.set(__self__, "enforced", enforced)

    @property
    @pulumi.getter
    def enforced(self) -> bool:
        """
        If true, then the Policy is enforced. If false, then any configuration is acceptable.
        """
        return pulumi.get(self, "enforced")


@pulumi.output_type
class OrganizationPolicyListPolicy(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "inheritFromParent":
            suggest = "inherit_from_parent"
        elif key == "suggestedValue":
            suggest = "suggested_value"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in OrganizationPolicyListPolicy. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        OrganizationPolicyListPolicy.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        OrganizationPolicyListPolicy.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 allow: Optional['outputs.OrganizationPolicyListPolicyAllow'] = None,
                 deny: Optional['outputs.OrganizationPolicyListPolicyDeny'] = None,
                 inherit_from_parent: Optional[bool] = None,
                 suggested_value: Optional[str] = None):
        """
        :param 'OrganizationPolicyListPolicyAllowArgs' allow: or `deny` - (Optional) One or the other must be set.
        :param 'OrganizationPolicyListPolicyDenyArgs' deny: One or the other must be set.
        :param bool inherit_from_parent: If set to true, the values from the effective Policy of the parent resource
               are inherited, meaning the values set in this Policy are added to the values inherited up the hierarchy.
               
               The `allow` or `deny` blocks support:
        :param str suggested_value: The Google Cloud Console will try to default to a configuration that matches the value specified in this field.
        """
        if allow is not None:
            pulumi.set(__self__, "allow", allow)
        if deny is not None:
            pulumi.set(__self__, "deny", deny)
        if inherit_from_parent is not None:
            pulumi.set(__self__, "inherit_from_parent", inherit_from_parent)
        if suggested_value is not None:
            pulumi.set(__self__, "suggested_value", suggested_value)

    @property
    @pulumi.getter
    def allow(self) -> Optional['outputs.OrganizationPolicyListPolicyAllow']:
        """
        or `deny` - (Optional) One or the other must be set.
        """
        return pulumi.get(self, "allow")

    @property
    @pulumi.getter
    def deny(self) -> Optional['outputs.OrganizationPolicyListPolicyDeny']:
        """
        One or the other must be set.
        """
        return pulumi.get(self, "deny")

    @property
    @pulumi.getter(name="inheritFromParent")
    def inherit_from_parent(self) -> Optional[bool]:
        """
        If set to true, the values from the effective Policy of the parent resource
        are inherited, meaning the values set in this Policy are added to the values inherited up the hierarchy.

        The `allow` or `deny` blocks support:
        """
        return pulumi.get(self, "inherit_from_parent")

    @property
    @pulumi.getter(name="suggestedValue")
    def suggested_value(self) -> Optional[str]:
        """
        The Google Cloud Console will try to default to a configuration that matches the value specified in this field.
        """
        return pulumi.get(self, "suggested_value")


@pulumi.output_type
class OrganizationPolicyListPolicyAllow(dict):
    def __init__(__self__, *,
                 all: Optional[bool] = None,
                 values: Optional[Sequence[str]] = None):
        """
        :param bool all: The policy allows or denies all values.
        :param Sequence[str] values: The policy can define specific values that are allowed or denied.
        """
        if all is not None:
            pulumi.set(__self__, "all", all)
        if values is not None:
            pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter
    def all(self) -> Optional[bool]:
        """
        The policy allows or denies all values.
        """
        return pulumi.get(self, "all")

    @property
    @pulumi.getter
    def values(self) -> Optional[Sequence[str]]:
        """
        The policy can define specific values that are allowed or denied.
        """
        return pulumi.get(self, "values")


@pulumi.output_type
class OrganizationPolicyListPolicyDeny(dict):
    def __init__(__self__, *,
                 all: Optional[bool] = None,
                 values: Optional[Sequence[str]] = None):
        """
        :param bool all: The policy allows or denies all values.
        :param Sequence[str] values: The policy can define specific values that are allowed or denied.
        """
        if all is not None:
            pulumi.set(__self__, "all", all)
        if values is not None:
            pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter
    def all(self) -> Optional[bool]:
        """
        The policy allows or denies all values.
        """
        return pulumi.get(self, "all")

    @property
    @pulumi.getter
    def values(self) -> Optional[Sequence[str]]:
        """
        The policy can define specific values that are allowed or denied.
        """
        return pulumi.get(self, "values")


@pulumi.output_type
class OrganizationPolicyRestorePolicy(dict):
    def __init__(__self__, *,
                 default: bool):
        """
        :param bool default: May only be set to true. If set, then the default Policy is restored.
        """
        pulumi.set(__self__, "default", default)

    @property
    @pulumi.getter
    def default(self) -> bool:
        """
        May only be set to true. If set, then the default Policy is restored.
        """
        return pulumi.get(self, "default")


@pulumi.output_type
class GetOrganizationPolicyBooleanPolicyResult(dict):
    def __init__(__self__, *,
                 enforced: bool):
        """
        :param bool enforced: If true, then the Policy is enforced. If false, then any configuration is acceptable.
        """
        pulumi.set(__self__, "enforced", enforced)

    @property
    @pulumi.getter
    def enforced(self) -> bool:
        """
        If true, then the Policy is enforced. If false, then any configuration is acceptable.
        """
        return pulumi.get(self, "enforced")


@pulumi.output_type
class GetOrganizationPolicyListPolicyResult(dict):
    def __init__(__self__, *,
                 allows: Sequence['outputs.GetOrganizationPolicyListPolicyAllowResult'],
                 denies: Sequence['outputs.GetOrganizationPolicyListPolicyDenyResult'],
                 inherit_from_parent: bool,
                 suggested_value: str):
        """
        :param Sequence['GetOrganizationPolicyListPolicyAllowArgs'] allows: One or the other must be set.
        :param Sequence['GetOrganizationPolicyListPolicyDenyArgs'] denies: One or the other must be set.
        :param bool inherit_from_parent: If set to true, the values from the effective Policy of the parent resource are inherited, meaning the values set in this Policy are added to the values inherited up the hierarchy.
        :param str suggested_value: The Google Cloud Console will try to default to a configuration that matches the value specified in this field.
        """
        pulumi.set(__self__, "allows", allows)
        pulumi.set(__self__, "denies", denies)
        pulumi.set(__self__, "inherit_from_parent", inherit_from_parent)
        pulumi.set(__self__, "suggested_value", suggested_value)

    @property
    @pulumi.getter
    def allows(self) -> Sequence['outputs.GetOrganizationPolicyListPolicyAllowResult']:
        """
        One or the other must be set.
        """
        return pulumi.get(self, "allows")

    @property
    @pulumi.getter
    def denies(self) -> Sequence['outputs.GetOrganizationPolicyListPolicyDenyResult']:
        """
        One or the other must be set.
        """
        return pulumi.get(self, "denies")

    @property
    @pulumi.getter(name="inheritFromParent")
    def inherit_from_parent(self) -> bool:
        """
        If set to true, the values from the effective Policy of the parent resource are inherited, meaning the values set in this Policy are added to the values inherited up the hierarchy.
        """
        return pulumi.get(self, "inherit_from_parent")

    @property
    @pulumi.getter(name="suggestedValue")
    def suggested_value(self) -> str:
        """
        The Google Cloud Console will try to default to a configuration that matches the value specified in this field.
        """
        return pulumi.get(self, "suggested_value")


@pulumi.output_type
class GetOrganizationPolicyListPolicyAllowResult(dict):
    def __init__(__self__, *,
                 all: bool,
                 values: Sequence[str]):
        """
        :param bool all: The policy allows or denies all values.
        :param Sequence[str] values: The policy can define specific values that are allowed or denied.
        """
        pulumi.set(__self__, "all", all)
        pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter
    def all(self) -> bool:
        """
        The policy allows or denies all values.
        """
        return pulumi.get(self, "all")

    @property
    @pulumi.getter
    def values(self) -> Sequence[str]:
        """
        The policy can define specific values that are allowed or denied.
        """
        return pulumi.get(self, "values")


@pulumi.output_type
class GetOrganizationPolicyListPolicyDenyResult(dict):
    def __init__(__self__, *,
                 all: bool,
                 values: Sequence[str]):
        """
        :param bool all: The policy allows or denies all values.
        :param Sequence[str] values: The policy can define specific values that are allowed or denied.
        """
        pulumi.set(__self__, "all", all)
        pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter
    def all(self) -> bool:
        """
        The policy allows or denies all values.
        """
        return pulumi.get(self, "all")

    @property
    @pulumi.getter
    def values(self) -> Sequence[str]:
        """
        The policy can define specific values that are allowed or denied.
        """
        return pulumi.get(self, "values")


@pulumi.output_type
class GetOrganizationPolicyRestorePolicyResult(dict):
    def __init__(__self__, *,
                 default: bool):
        """
        :param bool default: May only be set to true. If set, then the default Policy is restored.
        """
        pulumi.set(__self__, "default", default)

    @property
    @pulumi.getter
    def default(self) -> bool:
        """
        May only be set to true. If set, then the default Policy is restored.
        """
        return pulumi.get(self, "default")


