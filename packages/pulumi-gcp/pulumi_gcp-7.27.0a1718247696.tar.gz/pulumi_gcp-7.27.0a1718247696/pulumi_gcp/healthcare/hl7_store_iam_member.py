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
from ._inputs import *

__all__ = ['Hl7StoreIamMemberArgs', 'Hl7StoreIamMember']

@pulumi.input_type
class Hl7StoreIamMemberArgs:
    def __init__(__self__, *,
                 hl7_v2_store_id: pulumi.Input[str],
                 member: pulumi.Input[str],
                 role: pulumi.Input[str],
                 condition: Optional[pulumi.Input['Hl7StoreIamMemberConditionArgs']] = None):
        """
        The set of arguments for constructing a Hl7StoreIamMember resource.
        :param pulumi.Input[str] hl7_v2_store_id: The HL7v2 store ID, in the form
               `{project_id}/{location_name}/{dataset_name}/{hl7_v2_store_name}` or
               `{location_name}/{dataset_name}/{hl7_v2_store_name}`. In the second form, the provider's
               project setting will be used as a fallback.
        :param pulumi.Input[str] member: Identities that will be granted the privilege in `role`.
               Each entry can have one of the following values:
               * **allUsers**: A special identifier that represents anyone who is on the internet; with or without a Google account.
               * **allAuthenticatedUsers**: A special identifier that represents anyone who is authenticated with a Google account or a service account.
               * **user:{emailid}**: An email address that represents a specific Google account. For example, alice@gmail.com or joe@example.com.
               * **serviceAccount:{emailid}**: An email address that represents a service account. For example, my-other-app@appspot.gserviceaccount.com.
               * **group:{emailid}**: An email address that represents a Google group. For example, admins@example.com.
               * **domain:{domain}**: A G Suite domain (primary, instead of alias) name that represents all the users of that domain. For example, google.com or example.com.
        :param pulumi.Input[str] role: The role that should be applied. Only one
               `healthcare.Hl7StoreIamBinding` can be used per role. Note that custom roles must be of the format
               `[projects|organizations]/{parent-name}/roles/{role-name}`.
        """
        pulumi.set(__self__, "hl7_v2_store_id", hl7_v2_store_id)
        pulumi.set(__self__, "member", member)
        pulumi.set(__self__, "role", role)
        if condition is not None:
            pulumi.set(__self__, "condition", condition)

    @property
    @pulumi.getter(name="hl7V2StoreId")
    def hl7_v2_store_id(self) -> pulumi.Input[str]:
        """
        The HL7v2 store ID, in the form
        `{project_id}/{location_name}/{dataset_name}/{hl7_v2_store_name}` or
        `{location_name}/{dataset_name}/{hl7_v2_store_name}`. In the second form, the provider's
        project setting will be used as a fallback.
        """
        return pulumi.get(self, "hl7_v2_store_id")

    @hl7_v2_store_id.setter
    def hl7_v2_store_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "hl7_v2_store_id", value)

    @property
    @pulumi.getter
    def member(self) -> pulumi.Input[str]:
        """
        Identities that will be granted the privilege in `role`.
        Each entry can have one of the following values:
        * **allUsers**: A special identifier that represents anyone who is on the internet; with or without a Google account.
        * **allAuthenticatedUsers**: A special identifier that represents anyone who is authenticated with a Google account or a service account.
        * **user:{emailid}**: An email address that represents a specific Google account. For example, alice@gmail.com or joe@example.com.
        * **serviceAccount:{emailid}**: An email address that represents a service account. For example, my-other-app@appspot.gserviceaccount.com.
        * **group:{emailid}**: An email address that represents a Google group. For example, admins@example.com.
        * **domain:{domain}**: A G Suite domain (primary, instead of alias) name that represents all the users of that domain. For example, google.com or example.com.
        """
        return pulumi.get(self, "member")

    @member.setter
    def member(self, value: pulumi.Input[str]):
        pulumi.set(self, "member", value)

    @property
    @pulumi.getter
    def role(self) -> pulumi.Input[str]:
        """
        The role that should be applied. Only one
        `healthcare.Hl7StoreIamBinding` can be used per role. Note that custom roles must be of the format
        `[projects|organizations]/{parent-name}/roles/{role-name}`.
        """
        return pulumi.get(self, "role")

    @role.setter
    def role(self, value: pulumi.Input[str]):
        pulumi.set(self, "role", value)

    @property
    @pulumi.getter
    def condition(self) -> Optional[pulumi.Input['Hl7StoreIamMemberConditionArgs']]:
        return pulumi.get(self, "condition")

    @condition.setter
    def condition(self, value: Optional[pulumi.Input['Hl7StoreIamMemberConditionArgs']]):
        pulumi.set(self, "condition", value)


@pulumi.input_type
class _Hl7StoreIamMemberState:
    def __init__(__self__, *,
                 condition: Optional[pulumi.Input['Hl7StoreIamMemberConditionArgs']] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 hl7_v2_store_id: Optional[pulumi.Input[str]] = None,
                 member: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Hl7StoreIamMember resources.
        :param pulumi.Input[str] etag: (Computed) The etag of the HL7v2 store's IAM policy.
        :param pulumi.Input[str] hl7_v2_store_id: The HL7v2 store ID, in the form
               `{project_id}/{location_name}/{dataset_name}/{hl7_v2_store_name}` or
               `{location_name}/{dataset_name}/{hl7_v2_store_name}`. In the second form, the provider's
               project setting will be used as a fallback.
        :param pulumi.Input[str] member: Identities that will be granted the privilege in `role`.
               Each entry can have one of the following values:
               * **allUsers**: A special identifier that represents anyone who is on the internet; with or without a Google account.
               * **allAuthenticatedUsers**: A special identifier that represents anyone who is authenticated with a Google account or a service account.
               * **user:{emailid}**: An email address that represents a specific Google account. For example, alice@gmail.com or joe@example.com.
               * **serviceAccount:{emailid}**: An email address that represents a service account. For example, my-other-app@appspot.gserviceaccount.com.
               * **group:{emailid}**: An email address that represents a Google group. For example, admins@example.com.
               * **domain:{domain}**: A G Suite domain (primary, instead of alias) name that represents all the users of that domain. For example, google.com or example.com.
        :param pulumi.Input[str] role: The role that should be applied. Only one
               `healthcare.Hl7StoreIamBinding` can be used per role. Note that custom roles must be of the format
               `[projects|organizations]/{parent-name}/roles/{role-name}`.
        """
        if condition is not None:
            pulumi.set(__self__, "condition", condition)
        if etag is not None:
            pulumi.set(__self__, "etag", etag)
        if hl7_v2_store_id is not None:
            pulumi.set(__self__, "hl7_v2_store_id", hl7_v2_store_id)
        if member is not None:
            pulumi.set(__self__, "member", member)
        if role is not None:
            pulumi.set(__self__, "role", role)

    @property
    @pulumi.getter
    def condition(self) -> Optional[pulumi.Input['Hl7StoreIamMemberConditionArgs']]:
        return pulumi.get(self, "condition")

    @condition.setter
    def condition(self, value: Optional[pulumi.Input['Hl7StoreIamMemberConditionArgs']]):
        pulumi.set(self, "condition", value)

    @property
    @pulumi.getter
    def etag(self) -> Optional[pulumi.Input[str]]:
        """
        (Computed) The etag of the HL7v2 store's IAM policy.
        """
        return pulumi.get(self, "etag")

    @etag.setter
    def etag(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "etag", value)

    @property
    @pulumi.getter(name="hl7V2StoreId")
    def hl7_v2_store_id(self) -> Optional[pulumi.Input[str]]:
        """
        The HL7v2 store ID, in the form
        `{project_id}/{location_name}/{dataset_name}/{hl7_v2_store_name}` or
        `{location_name}/{dataset_name}/{hl7_v2_store_name}`. In the second form, the provider's
        project setting will be used as a fallback.
        """
        return pulumi.get(self, "hl7_v2_store_id")

    @hl7_v2_store_id.setter
    def hl7_v2_store_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "hl7_v2_store_id", value)

    @property
    @pulumi.getter
    def member(self) -> Optional[pulumi.Input[str]]:
        """
        Identities that will be granted the privilege in `role`.
        Each entry can have one of the following values:
        * **allUsers**: A special identifier that represents anyone who is on the internet; with or without a Google account.
        * **allAuthenticatedUsers**: A special identifier that represents anyone who is authenticated with a Google account or a service account.
        * **user:{emailid}**: An email address that represents a specific Google account. For example, alice@gmail.com or joe@example.com.
        * **serviceAccount:{emailid}**: An email address that represents a service account. For example, my-other-app@appspot.gserviceaccount.com.
        * **group:{emailid}**: An email address that represents a Google group. For example, admins@example.com.
        * **domain:{domain}**: A G Suite domain (primary, instead of alias) name that represents all the users of that domain. For example, google.com or example.com.
        """
        return pulumi.get(self, "member")

    @member.setter
    def member(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "member", value)

    @property
    @pulumi.getter
    def role(self) -> Optional[pulumi.Input[str]]:
        """
        The role that should be applied. Only one
        `healthcare.Hl7StoreIamBinding` can be used per role. Note that custom roles must be of the format
        `[projects|organizations]/{parent-name}/roles/{role-name}`.
        """
        return pulumi.get(self, "role")

    @role.setter
    def role(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "role", value)


class Hl7StoreIamMember(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 condition: Optional[pulumi.Input[pulumi.InputType['Hl7StoreIamMemberConditionArgs']]] = None,
                 hl7_v2_store_id: Optional[pulumi.Input[str]] = None,
                 member: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Three different resources help you manage your IAM policy for Healthcare HL7v2 store. Each of these resources serves a different use case:

        * `healthcare.Hl7StoreIamPolicy`: Authoritative. Sets the IAM policy for the HL7v2 store and replaces any existing policy already attached.
        * `healthcare.Hl7StoreIamBinding`: Authoritative for a given role. Updates the IAM policy to grant a role to a list of members. Other roles within the IAM policy for the HL7v2 store are preserved.
        * `healthcare.Hl7StoreIamMember`: Non-authoritative. Updates the IAM policy to grant a role to a new member. Other members for the role for the HL7v2 store are preserved.

        > **Note:** `healthcare.Hl7StoreIamPolicy` **cannot** be used in conjunction with `healthcare.Hl7StoreIamBinding` and `healthcare.Hl7StoreIamMember` or they will fight over what your policy should be.

        > **Note:** `healthcare.Hl7StoreIamBinding` resources **can be** used in conjunction with `healthcare.Hl7StoreIamMember` resources **only if** they do not grant privilege to the same role.

        ## healthcare.Hl7StoreIamPolicy

        ```python
        import pulumi
        import pulumi_gcp as gcp

        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/editor",
            members=["user:jane@example.com"],
        )])
        hl7_v2_store = gcp.healthcare.Hl7StoreIamPolicy("hl7_v2_store",
            hl7_v2_store_id="your-hl7-v2-store-id",
            policy_data=admin.policy_data)
        ```

        ## healthcare.Hl7StoreIamBinding

        ```python
        import pulumi
        import pulumi_gcp as gcp

        hl7_v2_store = gcp.healthcare.Hl7StoreIamBinding("hl7_v2_store",
            hl7_v2_store_id="your-hl7-v2-store-id",
            role="roles/editor",
            members=["user:jane@example.com"])
        ```

        ## healthcare.Hl7StoreIamMember

        ```python
        import pulumi
        import pulumi_gcp as gcp

        hl7_v2_store = gcp.healthcare.Hl7StoreIamMember("hl7_v2_store",
            hl7_v2_store_id="your-hl7-v2-store-id",
            role="roles/editor",
            member="user:jane@example.com")
        ```

        ## healthcare.Hl7StoreIamPolicy

        ```python
        import pulumi
        import pulumi_gcp as gcp

        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/editor",
            members=["user:jane@example.com"],
        )])
        hl7_v2_store = gcp.healthcare.Hl7StoreIamPolicy("hl7_v2_store",
            hl7_v2_store_id="your-hl7-v2-store-id",
            policy_data=admin.policy_data)
        ```

        ## healthcare.Hl7StoreIamBinding

        ```python
        import pulumi
        import pulumi_gcp as gcp

        hl7_v2_store = gcp.healthcare.Hl7StoreIamBinding("hl7_v2_store",
            hl7_v2_store_id="your-hl7-v2-store-id",
            role="roles/editor",
            members=["user:jane@example.com"])
        ```

        ## healthcare.Hl7StoreIamMember

        ```python
        import pulumi
        import pulumi_gcp as gcp

        hl7_v2_store = gcp.healthcare.Hl7StoreIamMember("hl7_v2_store",
            hl7_v2_store_id="your-hl7-v2-store-id",
            role="roles/editor",
            member="user:jane@example.com")
        ```

        ## Import

        ### Importing IAM policies

        IAM policy imports use the identifier of the Google Cloud Healthcare HL7v2 store resource. For example:

        * `"{{project_id}}/{{location}}/{{dataset}}/{{hl7_v2_store}}"`

        An `import` block (Terraform v1.5.0 and later) can be used to import IAM policies:

        tf

        import {

          id = "{{project_id}}/{{location}}/{{dataset}}/{{hl7_v2_store}}"

          to = google_healthcare_hl7_v2_store_iam_policy.default

        }

        The `pulumi import` command can also be used:

        ```sh
        $ pulumi import gcp:healthcare/hl7StoreIamMember:Hl7StoreIamMember default {{project_id}}/{{location}}/{{dataset}}/{{hl7_v2_store}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] hl7_v2_store_id: The HL7v2 store ID, in the form
               `{project_id}/{location_name}/{dataset_name}/{hl7_v2_store_name}` or
               `{location_name}/{dataset_name}/{hl7_v2_store_name}`. In the second form, the provider's
               project setting will be used as a fallback.
        :param pulumi.Input[str] member: Identities that will be granted the privilege in `role`.
               Each entry can have one of the following values:
               * **allUsers**: A special identifier that represents anyone who is on the internet; with or without a Google account.
               * **allAuthenticatedUsers**: A special identifier that represents anyone who is authenticated with a Google account or a service account.
               * **user:{emailid}**: An email address that represents a specific Google account. For example, alice@gmail.com or joe@example.com.
               * **serviceAccount:{emailid}**: An email address that represents a service account. For example, my-other-app@appspot.gserviceaccount.com.
               * **group:{emailid}**: An email address that represents a Google group. For example, admins@example.com.
               * **domain:{domain}**: A G Suite domain (primary, instead of alias) name that represents all the users of that domain. For example, google.com or example.com.
        :param pulumi.Input[str] role: The role that should be applied. Only one
               `healthcare.Hl7StoreIamBinding` can be used per role. Note that custom roles must be of the format
               `[projects|organizations]/{parent-name}/roles/{role-name}`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Hl7StoreIamMemberArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Three different resources help you manage your IAM policy for Healthcare HL7v2 store. Each of these resources serves a different use case:

        * `healthcare.Hl7StoreIamPolicy`: Authoritative. Sets the IAM policy for the HL7v2 store and replaces any existing policy already attached.
        * `healthcare.Hl7StoreIamBinding`: Authoritative for a given role. Updates the IAM policy to grant a role to a list of members. Other roles within the IAM policy for the HL7v2 store are preserved.
        * `healthcare.Hl7StoreIamMember`: Non-authoritative. Updates the IAM policy to grant a role to a new member. Other members for the role for the HL7v2 store are preserved.

        > **Note:** `healthcare.Hl7StoreIamPolicy` **cannot** be used in conjunction with `healthcare.Hl7StoreIamBinding` and `healthcare.Hl7StoreIamMember` or they will fight over what your policy should be.

        > **Note:** `healthcare.Hl7StoreIamBinding` resources **can be** used in conjunction with `healthcare.Hl7StoreIamMember` resources **only if** they do not grant privilege to the same role.

        ## healthcare.Hl7StoreIamPolicy

        ```python
        import pulumi
        import pulumi_gcp as gcp

        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/editor",
            members=["user:jane@example.com"],
        )])
        hl7_v2_store = gcp.healthcare.Hl7StoreIamPolicy("hl7_v2_store",
            hl7_v2_store_id="your-hl7-v2-store-id",
            policy_data=admin.policy_data)
        ```

        ## healthcare.Hl7StoreIamBinding

        ```python
        import pulumi
        import pulumi_gcp as gcp

        hl7_v2_store = gcp.healthcare.Hl7StoreIamBinding("hl7_v2_store",
            hl7_v2_store_id="your-hl7-v2-store-id",
            role="roles/editor",
            members=["user:jane@example.com"])
        ```

        ## healthcare.Hl7StoreIamMember

        ```python
        import pulumi
        import pulumi_gcp as gcp

        hl7_v2_store = gcp.healthcare.Hl7StoreIamMember("hl7_v2_store",
            hl7_v2_store_id="your-hl7-v2-store-id",
            role="roles/editor",
            member="user:jane@example.com")
        ```

        ## healthcare.Hl7StoreIamPolicy

        ```python
        import pulumi
        import pulumi_gcp as gcp

        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/editor",
            members=["user:jane@example.com"],
        )])
        hl7_v2_store = gcp.healthcare.Hl7StoreIamPolicy("hl7_v2_store",
            hl7_v2_store_id="your-hl7-v2-store-id",
            policy_data=admin.policy_data)
        ```

        ## healthcare.Hl7StoreIamBinding

        ```python
        import pulumi
        import pulumi_gcp as gcp

        hl7_v2_store = gcp.healthcare.Hl7StoreIamBinding("hl7_v2_store",
            hl7_v2_store_id="your-hl7-v2-store-id",
            role="roles/editor",
            members=["user:jane@example.com"])
        ```

        ## healthcare.Hl7StoreIamMember

        ```python
        import pulumi
        import pulumi_gcp as gcp

        hl7_v2_store = gcp.healthcare.Hl7StoreIamMember("hl7_v2_store",
            hl7_v2_store_id="your-hl7-v2-store-id",
            role="roles/editor",
            member="user:jane@example.com")
        ```

        ## Import

        ### Importing IAM policies

        IAM policy imports use the identifier of the Google Cloud Healthcare HL7v2 store resource. For example:

        * `"{{project_id}}/{{location}}/{{dataset}}/{{hl7_v2_store}}"`

        An `import` block (Terraform v1.5.0 and later) can be used to import IAM policies:

        tf

        import {

          id = "{{project_id}}/{{location}}/{{dataset}}/{{hl7_v2_store}}"

          to = google_healthcare_hl7_v2_store_iam_policy.default

        }

        The `pulumi import` command can also be used:

        ```sh
        $ pulumi import gcp:healthcare/hl7StoreIamMember:Hl7StoreIamMember default {{project_id}}/{{location}}/{{dataset}}/{{hl7_v2_store}}
        ```

        :param str resource_name: The name of the resource.
        :param Hl7StoreIamMemberArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(Hl7StoreIamMemberArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 condition: Optional[pulumi.Input[pulumi.InputType['Hl7StoreIamMemberConditionArgs']]] = None,
                 hl7_v2_store_id: Optional[pulumi.Input[str]] = None,
                 member: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = Hl7StoreIamMemberArgs.__new__(Hl7StoreIamMemberArgs)

            __props__.__dict__["condition"] = condition
            if hl7_v2_store_id is None and not opts.urn:
                raise TypeError("Missing required property 'hl7_v2_store_id'")
            __props__.__dict__["hl7_v2_store_id"] = hl7_v2_store_id
            if member is None and not opts.urn:
                raise TypeError("Missing required property 'member'")
            __props__.__dict__["member"] = member
            if role is None and not opts.urn:
                raise TypeError("Missing required property 'role'")
            __props__.__dict__["role"] = role
            __props__.__dict__["etag"] = None
        super(Hl7StoreIamMember, __self__).__init__(
            'gcp:healthcare/hl7StoreIamMember:Hl7StoreIamMember',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            condition: Optional[pulumi.Input[pulumi.InputType['Hl7StoreIamMemberConditionArgs']]] = None,
            etag: Optional[pulumi.Input[str]] = None,
            hl7_v2_store_id: Optional[pulumi.Input[str]] = None,
            member: Optional[pulumi.Input[str]] = None,
            role: Optional[pulumi.Input[str]] = None) -> 'Hl7StoreIamMember':
        """
        Get an existing Hl7StoreIamMember resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] etag: (Computed) The etag of the HL7v2 store's IAM policy.
        :param pulumi.Input[str] hl7_v2_store_id: The HL7v2 store ID, in the form
               `{project_id}/{location_name}/{dataset_name}/{hl7_v2_store_name}` or
               `{location_name}/{dataset_name}/{hl7_v2_store_name}`. In the second form, the provider's
               project setting will be used as a fallback.
        :param pulumi.Input[str] member: Identities that will be granted the privilege in `role`.
               Each entry can have one of the following values:
               * **allUsers**: A special identifier that represents anyone who is on the internet; with or without a Google account.
               * **allAuthenticatedUsers**: A special identifier that represents anyone who is authenticated with a Google account or a service account.
               * **user:{emailid}**: An email address that represents a specific Google account. For example, alice@gmail.com or joe@example.com.
               * **serviceAccount:{emailid}**: An email address that represents a service account. For example, my-other-app@appspot.gserviceaccount.com.
               * **group:{emailid}**: An email address that represents a Google group. For example, admins@example.com.
               * **domain:{domain}**: A G Suite domain (primary, instead of alias) name that represents all the users of that domain. For example, google.com or example.com.
        :param pulumi.Input[str] role: The role that should be applied. Only one
               `healthcare.Hl7StoreIamBinding` can be used per role. Note that custom roles must be of the format
               `[projects|organizations]/{parent-name}/roles/{role-name}`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _Hl7StoreIamMemberState.__new__(_Hl7StoreIamMemberState)

        __props__.__dict__["condition"] = condition
        __props__.__dict__["etag"] = etag
        __props__.__dict__["hl7_v2_store_id"] = hl7_v2_store_id
        __props__.__dict__["member"] = member
        __props__.__dict__["role"] = role
        return Hl7StoreIamMember(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def condition(self) -> pulumi.Output[Optional['outputs.Hl7StoreIamMemberCondition']]:
        return pulumi.get(self, "condition")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        (Computed) The etag of the HL7v2 store's IAM policy.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="hl7V2StoreId")
    def hl7_v2_store_id(self) -> pulumi.Output[str]:
        """
        The HL7v2 store ID, in the form
        `{project_id}/{location_name}/{dataset_name}/{hl7_v2_store_name}` or
        `{location_name}/{dataset_name}/{hl7_v2_store_name}`. In the second form, the provider's
        project setting will be used as a fallback.
        """
        return pulumi.get(self, "hl7_v2_store_id")

    @property
    @pulumi.getter
    def member(self) -> pulumi.Output[str]:
        """
        Identities that will be granted the privilege in `role`.
        Each entry can have one of the following values:
        * **allUsers**: A special identifier that represents anyone who is on the internet; with or without a Google account.
        * **allAuthenticatedUsers**: A special identifier that represents anyone who is authenticated with a Google account or a service account.
        * **user:{emailid}**: An email address that represents a specific Google account. For example, alice@gmail.com or joe@example.com.
        * **serviceAccount:{emailid}**: An email address that represents a service account. For example, my-other-app@appspot.gserviceaccount.com.
        * **group:{emailid}**: An email address that represents a Google group. For example, admins@example.com.
        * **domain:{domain}**: A G Suite domain (primary, instead of alias) name that represents all the users of that domain. For example, google.com or example.com.
        """
        return pulumi.get(self, "member")

    @property
    @pulumi.getter
    def role(self) -> pulumi.Output[str]:
        """
        The role that should be applied. Only one
        `healthcare.Hl7StoreIamBinding` can be used per role. Note that custom roles must be of the format
        `[projects|organizations]/{parent-name}/roles/{role-name}`.
        """
        return pulumi.get(self, "role")

