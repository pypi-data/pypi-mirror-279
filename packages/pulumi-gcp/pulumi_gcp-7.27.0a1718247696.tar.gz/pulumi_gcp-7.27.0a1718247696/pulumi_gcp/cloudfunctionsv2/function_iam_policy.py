# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['FunctionIamPolicyArgs', 'FunctionIamPolicy']

@pulumi.input_type
class FunctionIamPolicyArgs:
    def __init__(__self__, *,
                 cloud_function: pulumi.Input[str],
                 policy_data: pulumi.Input[str],
                 location: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a FunctionIamPolicy resource.
        :param pulumi.Input[str] cloud_function: Used to find the parent resource to bind the IAM policy to
        :param pulumi.Input[str] policy_data: The policy data generated by
               a `organizations_get_iam_policy` data source.
        :param pulumi.Input[str] location: The location of this cloud function. Used to find the parent resource to bind the IAM policy to. If not specified,
               the value will be parsed from the identifier of the parent resource. If no location is provided in the parent identifier and no
               location is specified, it is taken from the provider configuration.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
        """
        pulumi.set(__self__, "cloud_function", cloud_function)
        pulumi.set(__self__, "policy_data", policy_data)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if project is not None:
            pulumi.set(__self__, "project", project)

    @property
    @pulumi.getter(name="cloudFunction")
    def cloud_function(self) -> pulumi.Input[str]:
        """
        Used to find the parent resource to bind the IAM policy to
        """
        return pulumi.get(self, "cloud_function")

    @cloud_function.setter
    def cloud_function(self, value: pulumi.Input[str]):
        pulumi.set(self, "cloud_function", value)

    @property
    @pulumi.getter(name="policyData")
    def policy_data(self) -> pulumi.Input[str]:
        """
        The policy data generated by
        a `organizations_get_iam_policy` data source.
        """
        return pulumi.get(self, "policy_data")

    @policy_data.setter
    def policy_data(self, value: pulumi.Input[str]):
        pulumi.set(self, "policy_data", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The location of this cloud function. Used to find the parent resource to bind the IAM policy to. If not specified,
        the value will be parsed from the identifier of the parent resource. If no location is provided in the parent identifier and no
        location is specified, it is taken from the provider configuration.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)


@pulumi.input_type
class _FunctionIamPolicyState:
    def __init__(__self__, *,
                 cloud_function: Optional[pulumi.Input[str]] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 policy_data: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering FunctionIamPolicy resources.
        :param pulumi.Input[str] cloud_function: Used to find the parent resource to bind the IAM policy to
        :param pulumi.Input[str] etag: (Computed) The etag of the IAM policy.
        :param pulumi.Input[str] location: The location of this cloud function. Used to find the parent resource to bind the IAM policy to. If not specified,
               the value will be parsed from the identifier of the parent resource. If no location is provided in the parent identifier and no
               location is specified, it is taken from the provider configuration.
        :param pulumi.Input[str] policy_data: The policy data generated by
               a `organizations_get_iam_policy` data source.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
        """
        if cloud_function is not None:
            pulumi.set(__self__, "cloud_function", cloud_function)
        if etag is not None:
            pulumi.set(__self__, "etag", etag)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if policy_data is not None:
            pulumi.set(__self__, "policy_data", policy_data)
        if project is not None:
            pulumi.set(__self__, "project", project)

    @property
    @pulumi.getter(name="cloudFunction")
    def cloud_function(self) -> Optional[pulumi.Input[str]]:
        """
        Used to find the parent resource to bind the IAM policy to
        """
        return pulumi.get(self, "cloud_function")

    @cloud_function.setter
    def cloud_function(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cloud_function", value)

    @property
    @pulumi.getter
    def etag(self) -> Optional[pulumi.Input[str]]:
        """
        (Computed) The etag of the IAM policy.
        """
        return pulumi.get(self, "etag")

    @etag.setter
    def etag(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "etag", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The location of this cloud function. Used to find the parent resource to bind the IAM policy to. If not specified,
        the value will be parsed from the identifier of the parent resource. If no location is provided in the parent identifier and no
        location is specified, it is taken from the provider configuration.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="policyData")
    def policy_data(self) -> Optional[pulumi.Input[str]]:
        """
        The policy data generated by
        a `organizations_get_iam_policy` data source.
        """
        return pulumi.get(self, "policy_data")

    @policy_data.setter
    def policy_data(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy_data", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)


class FunctionIamPolicy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cloud_function: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 policy_data: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Three different resources help you manage your IAM policy for Cloud Functions (2nd gen) function. Each of these resources serves a different use case:

        * `cloudfunctionsv2.FunctionIamPolicy`: Authoritative. Sets the IAM policy for the function and replaces any existing policy already attached.
        * `cloudfunctionsv2.FunctionIamBinding`: Authoritative for a given role. Updates the IAM policy to grant a role to a list of members. Other roles within the IAM policy for the function are preserved.
        * `cloudfunctionsv2.FunctionIamMember`: Non-authoritative. Updates the IAM policy to grant a role to a new member. Other members for the role for the function are preserved.

        A data source can be used to retrieve policy data in advent you do not need creation

        * `cloudfunctionsv2.FunctionIamPolicy`: Retrieves the IAM policy for the function

        > **Note:** `cloudfunctionsv2.FunctionIamPolicy` **cannot** be used in conjunction with `cloudfunctionsv2.FunctionIamBinding` and `cloudfunctionsv2.FunctionIamMember` or they will fight over what your policy should be.

        > **Note:** `cloudfunctionsv2.FunctionIamBinding` resources **can be** used in conjunction with `cloudfunctionsv2.FunctionIamMember` resources **only if** they do not grant privilege to the same role.

        ## cloudfunctionsv2.FunctionIamPolicy

        ```python
        import pulumi
        import pulumi_gcp as gcp

        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/viewer",
            members=["user:jane@example.com"],
        )])
        policy = gcp.cloudfunctionsv2.FunctionIamPolicy("policy",
            project=function["project"],
            location=function["location"],
            cloud_function=function["name"],
            policy_data=admin.policy_data)
        ```

        ## cloudfunctionsv2.FunctionIamBinding

        ```python
        import pulumi
        import pulumi_gcp as gcp

        binding = gcp.cloudfunctionsv2.FunctionIamBinding("binding",
            project=function["project"],
            location=function["location"],
            cloud_function=function["name"],
            role="roles/viewer",
            members=["user:jane@example.com"])
        ```

        ## cloudfunctionsv2.FunctionIamMember

        ```python
        import pulumi
        import pulumi_gcp as gcp

        member = gcp.cloudfunctionsv2.FunctionIamMember("member",
            project=function["project"],
            location=function["location"],
            cloud_function=function["name"],
            role="roles/viewer",
            member="user:jane@example.com")
        ```

        ## cloudfunctionsv2.FunctionIamPolicy

        ```python
        import pulumi
        import pulumi_gcp as gcp

        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/viewer",
            members=["user:jane@example.com"],
        )])
        policy = gcp.cloudfunctionsv2.FunctionIamPolicy("policy",
            project=function["project"],
            location=function["location"],
            cloud_function=function["name"],
            policy_data=admin.policy_data)
        ```

        ## cloudfunctionsv2.FunctionIamBinding

        ```python
        import pulumi
        import pulumi_gcp as gcp

        binding = gcp.cloudfunctionsv2.FunctionIamBinding("binding",
            project=function["project"],
            location=function["location"],
            cloud_function=function["name"],
            role="roles/viewer",
            members=["user:jane@example.com"])
        ```

        ## cloudfunctionsv2.FunctionIamMember

        ```python
        import pulumi
        import pulumi_gcp as gcp

        member = gcp.cloudfunctionsv2.FunctionIamMember("member",
            project=function["project"],
            location=function["location"],
            cloud_function=function["name"],
            role="roles/viewer",
            member="user:jane@example.com")
        ```

        ## Import

        For all import syntaxes, the "resource in question" can take any of the following forms:

        * projects/{{project}}/locations/{{location}}/functions/{{cloud_function}}

        * {{project}}/{{location}}/{{cloud_function}}

        * {{location}}/{{cloud_function}}

        * {{cloud_function}}

        Any variables not passed in the import command will be taken from the provider configuration.

        Cloud Functions (2nd gen) function IAM resources can be imported using the resource identifiers, role, and member.

        IAM member imports use space-delimited identifiers: the resource in question, the role, and the member identity, e.g.

        ```sh
        $ pulumi import gcp:cloudfunctionsv2/functionIamPolicy:FunctionIamPolicy editor "projects/{{project}}/locations/{{location}}/functions/{{cloud_function}} roles/viewer user:jane@example.com"
        ```

        IAM binding imports use space-delimited identifiers: the resource in question and the role, e.g.

        ```sh
        $ pulumi import gcp:cloudfunctionsv2/functionIamPolicy:FunctionIamPolicy editor "projects/{{project}}/locations/{{location}}/functions/{{cloud_function}} roles/viewer"
        ```

        IAM policy imports use the identifier of the resource in question, e.g.

        ```sh
        $ pulumi import gcp:cloudfunctionsv2/functionIamPolicy:FunctionIamPolicy editor projects/{{project}}/locations/{{location}}/functions/{{cloud_function}}
        ```

        -> **Custom Roles**: If you're importing a IAM resource with a custom role, make sure to use the

         full name of the custom role, e.g. `[projects/my-project|organizations/my-org]/roles/my-custom-role`.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cloud_function: Used to find the parent resource to bind the IAM policy to
        :param pulumi.Input[str] location: The location of this cloud function. Used to find the parent resource to bind the IAM policy to. If not specified,
               the value will be parsed from the identifier of the parent resource. If no location is provided in the parent identifier and no
               location is specified, it is taken from the provider configuration.
        :param pulumi.Input[str] policy_data: The policy data generated by
               a `organizations_get_iam_policy` data source.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: FunctionIamPolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Three different resources help you manage your IAM policy for Cloud Functions (2nd gen) function. Each of these resources serves a different use case:

        * `cloudfunctionsv2.FunctionIamPolicy`: Authoritative. Sets the IAM policy for the function and replaces any existing policy already attached.
        * `cloudfunctionsv2.FunctionIamBinding`: Authoritative for a given role. Updates the IAM policy to grant a role to a list of members. Other roles within the IAM policy for the function are preserved.
        * `cloudfunctionsv2.FunctionIamMember`: Non-authoritative. Updates the IAM policy to grant a role to a new member. Other members for the role for the function are preserved.

        A data source can be used to retrieve policy data in advent you do not need creation

        * `cloudfunctionsv2.FunctionIamPolicy`: Retrieves the IAM policy for the function

        > **Note:** `cloudfunctionsv2.FunctionIamPolicy` **cannot** be used in conjunction with `cloudfunctionsv2.FunctionIamBinding` and `cloudfunctionsv2.FunctionIamMember` or they will fight over what your policy should be.

        > **Note:** `cloudfunctionsv2.FunctionIamBinding` resources **can be** used in conjunction with `cloudfunctionsv2.FunctionIamMember` resources **only if** they do not grant privilege to the same role.

        ## cloudfunctionsv2.FunctionIamPolicy

        ```python
        import pulumi
        import pulumi_gcp as gcp

        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/viewer",
            members=["user:jane@example.com"],
        )])
        policy = gcp.cloudfunctionsv2.FunctionIamPolicy("policy",
            project=function["project"],
            location=function["location"],
            cloud_function=function["name"],
            policy_data=admin.policy_data)
        ```

        ## cloudfunctionsv2.FunctionIamBinding

        ```python
        import pulumi
        import pulumi_gcp as gcp

        binding = gcp.cloudfunctionsv2.FunctionIamBinding("binding",
            project=function["project"],
            location=function["location"],
            cloud_function=function["name"],
            role="roles/viewer",
            members=["user:jane@example.com"])
        ```

        ## cloudfunctionsv2.FunctionIamMember

        ```python
        import pulumi
        import pulumi_gcp as gcp

        member = gcp.cloudfunctionsv2.FunctionIamMember("member",
            project=function["project"],
            location=function["location"],
            cloud_function=function["name"],
            role="roles/viewer",
            member="user:jane@example.com")
        ```

        ## cloudfunctionsv2.FunctionIamPolicy

        ```python
        import pulumi
        import pulumi_gcp as gcp

        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/viewer",
            members=["user:jane@example.com"],
        )])
        policy = gcp.cloudfunctionsv2.FunctionIamPolicy("policy",
            project=function["project"],
            location=function["location"],
            cloud_function=function["name"],
            policy_data=admin.policy_data)
        ```

        ## cloudfunctionsv2.FunctionIamBinding

        ```python
        import pulumi
        import pulumi_gcp as gcp

        binding = gcp.cloudfunctionsv2.FunctionIamBinding("binding",
            project=function["project"],
            location=function["location"],
            cloud_function=function["name"],
            role="roles/viewer",
            members=["user:jane@example.com"])
        ```

        ## cloudfunctionsv2.FunctionIamMember

        ```python
        import pulumi
        import pulumi_gcp as gcp

        member = gcp.cloudfunctionsv2.FunctionIamMember("member",
            project=function["project"],
            location=function["location"],
            cloud_function=function["name"],
            role="roles/viewer",
            member="user:jane@example.com")
        ```

        ## Import

        For all import syntaxes, the "resource in question" can take any of the following forms:

        * projects/{{project}}/locations/{{location}}/functions/{{cloud_function}}

        * {{project}}/{{location}}/{{cloud_function}}

        * {{location}}/{{cloud_function}}

        * {{cloud_function}}

        Any variables not passed in the import command will be taken from the provider configuration.

        Cloud Functions (2nd gen) function IAM resources can be imported using the resource identifiers, role, and member.

        IAM member imports use space-delimited identifiers: the resource in question, the role, and the member identity, e.g.

        ```sh
        $ pulumi import gcp:cloudfunctionsv2/functionIamPolicy:FunctionIamPolicy editor "projects/{{project}}/locations/{{location}}/functions/{{cloud_function}} roles/viewer user:jane@example.com"
        ```

        IAM binding imports use space-delimited identifiers: the resource in question and the role, e.g.

        ```sh
        $ pulumi import gcp:cloudfunctionsv2/functionIamPolicy:FunctionIamPolicy editor "projects/{{project}}/locations/{{location}}/functions/{{cloud_function}} roles/viewer"
        ```

        IAM policy imports use the identifier of the resource in question, e.g.

        ```sh
        $ pulumi import gcp:cloudfunctionsv2/functionIamPolicy:FunctionIamPolicy editor projects/{{project}}/locations/{{location}}/functions/{{cloud_function}}
        ```

        -> **Custom Roles**: If you're importing a IAM resource with a custom role, make sure to use the

         full name of the custom role, e.g. `[projects/my-project|organizations/my-org]/roles/my-custom-role`.

        :param str resource_name: The name of the resource.
        :param FunctionIamPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(FunctionIamPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cloud_function: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 policy_data: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = FunctionIamPolicyArgs.__new__(FunctionIamPolicyArgs)

            if cloud_function is None and not opts.urn:
                raise TypeError("Missing required property 'cloud_function'")
            __props__.__dict__["cloud_function"] = cloud_function
            __props__.__dict__["location"] = location
            if policy_data is None and not opts.urn:
                raise TypeError("Missing required property 'policy_data'")
            __props__.__dict__["policy_data"] = policy_data
            __props__.__dict__["project"] = project
            __props__.__dict__["etag"] = None
        super(FunctionIamPolicy, __self__).__init__(
            'gcp:cloudfunctionsv2/functionIamPolicy:FunctionIamPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            cloud_function: Optional[pulumi.Input[str]] = None,
            etag: Optional[pulumi.Input[str]] = None,
            location: Optional[pulumi.Input[str]] = None,
            policy_data: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None) -> 'FunctionIamPolicy':
        """
        Get an existing FunctionIamPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cloud_function: Used to find the parent resource to bind the IAM policy to
        :param pulumi.Input[str] etag: (Computed) The etag of the IAM policy.
        :param pulumi.Input[str] location: The location of this cloud function. Used to find the parent resource to bind the IAM policy to. If not specified,
               the value will be parsed from the identifier of the parent resource. If no location is provided in the parent identifier and no
               location is specified, it is taken from the provider configuration.
        :param pulumi.Input[str] policy_data: The policy data generated by
               a `organizations_get_iam_policy` data source.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _FunctionIamPolicyState.__new__(_FunctionIamPolicyState)

        __props__.__dict__["cloud_function"] = cloud_function
        __props__.__dict__["etag"] = etag
        __props__.__dict__["location"] = location
        __props__.__dict__["policy_data"] = policy_data
        __props__.__dict__["project"] = project
        return FunctionIamPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="cloudFunction")
    def cloud_function(self) -> pulumi.Output[str]:
        """
        Used to find the parent resource to bind the IAM policy to
        """
        return pulumi.get(self, "cloud_function")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        (Computed) The etag of the IAM policy.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The location of this cloud function. Used to find the parent resource to bind the IAM policy to. If not specified,
        the value will be parsed from the identifier of the parent resource. If no location is provided in the parent identifier and no
        location is specified, it is taken from the provider configuration.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="policyData")
    def policy_data(self) -> pulumi.Output[str]:
        """
        The policy data generated by
        a `organizations_get_iam_policy` data source.
        """
        return pulumi.get(self, "policy_data")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
        """
        return pulumi.get(self, "project")

