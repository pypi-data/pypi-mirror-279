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

__all__ = ['QueueIamMemberArgs', 'QueueIamMember']

@pulumi.input_type
class QueueIamMemberArgs:
    def __init__(__self__, *,
                 member: pulumi.Input[str],
                 role: pulumi.Input[str],
                 condition: Optional[pulumi.Input['QueueIamMemberConditionArgs']] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a QueueIamMember resource.
        :param pulumi.Input[str] member: Identities that will be granted the privilege in `role`.
               Each entry can have one of the following values:
               * **allUsers**: A special identifier that represents anyone who is on the internet; with or without a Google account.
               * **allAuthenticatedUsers**: A special identifier that represents anyone who is authenticated with a Google account or a service account.
               * **user:{emailid}**: An email address that represents a specific Google account. For example, alice@gmail.com or joe@example.com.
               * **serviceAccount:{emailid}**: An email address that represents a service account. For example, my-other-app@appspot.gserviceaccount.com.
               * **group:{emailid}**: An email address that represents a Google group. For example, admins@example.com.
               * **domain:{domain}**: A G Suite domain (primary, instead of alias) name that represents all the users of that domain. For example, google.com or example.com.
               * **projectOwner:projectid**: Owners of the given project. For example, "projectOwner:my-example-project"
               * **projectEditor:projectid**: Editors of the given project. For example, "projectEditor:my-example-project"
               * **projectViewer:projectid**: Viewers of the given project. For example, "projectViewer:my-example-project"
        :param pulumi.Input[str] role: The role that should be applied. Only one
               `cloudtasks.QueueIamBinding` can be used per role. Note that custom roles must be of the format
               `[projects|organizations]/{parent-name}/roles/{role-name}`.
        :param pulumi.Input[str] location: The location of the queue Used to find the parent resource to bind the IAM policy to. If not specified,
               the value will be parsed from the identifier of the parent resource. If no location is provided in the parent identifier and no
               location is specified, it is taken from the provider configuration.
        :param pulumi.Input[str] name: Used to find the parent resource to bind the IAM policy to
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
        """
        pulumi.set(__self__, "member", member)
        pulumi.set(__self__, "role", role)
        if condition is not None:
            pulumi.set(__self__, "condition", condition)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)

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
        * **projectOwner:projectid**: Owners of the given project. For example, "projectOwner:my-example-project"
        * **projectEditor:projectid**: Editors of the given project. For example, "projectEditor:my-example-project"
        * **projectViewer:projectid**: Viewers of the given project. For example, "projectViewer:my-example-project"
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
        `cloudtasks.QueueIamBinding` can be used per role. Note that custom roles must be of the format
        `[projects|organizations]/{parent-name}/roles/{role-name}`.
        """
        return pulumi.get(self, "role")

    @role.setter
    def role(self, value: pulumi.Input[str]):
        pulumi.set(self, "role", value)

    @property
    @pulumi.getter
    def condition(self) -> Optional[pulumi.Input['QueueIamMemberConditionArgs']]:
        return pulumi.get(self, "condition")

    @condition.setter
    def condition(self, value: Optional[pulumi.Input['QueueIamMemberConditionArgs']]):
        pulumi.set(self, "condition", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The location of the queue Used to find the parent resource to bind the IAM policy to. If not specified,
        the value will be parsed from the identifier of the parent resource. If no location is provided in the parent identifier and no
        location is specified, it is taken from the provider configuration.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Used to find the parent resource to bind the IAM policy to
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

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
class _QueueIamMemberState:
    def __init__(__self__, *,
                 condition: Optional[pulumi.Input['QueueIamMemberConditionArgs']] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 member: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering QueueIamMember resources.
        :param pulumi.Input[str] etag: (Computed) The etag of the IAM policy.
        :param pulumi.Input[str] location: The location of the queue Used to find the parent resource to bind the IAM policy to. If not specified,
               the value will be parsed from the identifier of the parent resource. If no location is provided in the parent identifier and no
               location is specified, it is taken from the provider configuration.
        :param pulumi.Input[str] member: Identities that will be granted the privilege in `role`.
               Each entry can have one of the following values:
               * **allUsers**: A special identifier that represents anyone who is on the internet; with or without a Google account.
               * **allAuthenticatedUsers**: A special identifier that represents anyone who is authenticated with a Google account or a service account.
               * **user:{emailid}**: An email address that represents a specific Google account. For example, alice@gmail.com or joe@example.com.
               * **serviceAccount:{emailid}**: An email address that represents a service account. For example, my-other-app@appspot.gserviceaccount.com.
               * **group:{emailid}**: An email address that represents a Google group. For example, admins@example.com.
               * **domain:{domain}**: A G Suite domain (primary, instead of alias) name that represents all the users of that domain. For example, google.com or example.com.
               * **projectOwner:projectid**: Owners of the given project. For example, "projectOwner:my-example-project"
               * **projectEditor:projectid**: Editors of the given project. For example, "projectEditor:my-example-project"
               * **projectViewer:projectid**: Viewers of the given project. For example, "projectViewer:my-example-project"
        :param pulumi.Input[str] name: Used to find the parent resource to bind the IAM policy to
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
        :param pulumi.Input[str] role: The role that should be applied. Only one
               `cloudtasks.QueueIamBinding` can be used per role. Note that custom roles must be of the format
               `[projects|organizations]/{parent-name}/roles/{role-name}`.
        """
        if condition is not None:
            pulumi.set(__self__, "condition", condition)
        if etag is not None:
            pulumi.set(__self__, "etag", etag)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if member is not None:
            pulumi.set(__self__, "member", member)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if role is not None:
            pulumi.set(__self__, "role", role)

    @property
    @pulumi.getter
    def condition(self) -> Optional[pulumi.Input['QueueIamMemberConditionArgs']]:
        return pulumi.get(self, "condition")

    @condition.setter
    def condition(self, value: Optional[pulumi.Input['QueueIamMemberConditionArgs']]):
        pulumi.set(self, "condition", value)

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
        The location of the queue Used to find the parent resource to bind the IAM policy to. If not specified,
        the value will be parsed from the identifier of the parent resource. If no location is provided in the parent identifier and no
        location is specified, it is taken from the provider configuration.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

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
        * **projectOwner:projectid**: Owners of the given project. For example, "projectOwner:my-example-project"
        * **projectEditor:projectid**: Editors of the given project. For example, "projectEditor:my-example-project"
        * **projectViewer:projectid**: Viewers of the given project. For example, "projectViewer:my-example-project"
        """
        return pulumi.get(self, "member")

    @member.setter
    def member(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "member", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Used to find the parent resource to bind the IAM policy to
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

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

    @property
    @pulumi.getter
    def role(self) -> Optional[pulumi.Input[str]]:
        """
        The role that should be applied. Only one
        `cloudtasks.QueueIamBinding` can be used per role. Note that custom roles must be of the format
        `[projects|organizations]/{parent-name}/roles/{role-name}`.
        """
        return pulumi.get(self, "role")

    @role.setter
    def role(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "role", value)


class QueueIamMember(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 condition: Optional[pulumi.Input[pulumi.InputType['QueueIamMemberConditionArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 member: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Three different resources help you manage your IAM policy for Cloud Tasks Queue. Each of these resources serves a different use case:

        * `cloudtasks.QueueIamPolicy`: Authoritative. Sets the IAM policy for the queue and replaces any existing policy already attached.
        * `cloudtasks.QueueIamBinding`: Authoritative for a given role. Updates the IAM policy to grant a role to a list of members. Other roles within the IAM policy for the queue are preserved.
        * `cloudtasks.QueueIamMember`: Non-authoritative. Updates the IAM policy to grant a role to a new member. Other members for the role for the queue are preserved.

        A data source can be used to retrieve policy data in advent you do not need creation

        * `cloudtasks.QueueIamPolicy`: Retrieves the IAM policy for the queue

        > **Note:** `cloudtasks.QueueIamPolicy` **cannot** be used in conjunction with `cloudtasks.QueueIamBinding` and `cloudtasks.QueueIamMember` or they will fight over what your policy should be.

        > **Note:** `cloudtasks.QueueIamBinding` resources **can be** used in conjunction with `cloudtasks.QueueIamMember` resources **only if** they do not grant privilege to the same role.

        ## cloudtasks.QueueIamPolicy

        ```python
        import pulumi
        import pulumi_gcp as gcp

        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/viewer",
            members=["user:jane@example.com"],
        )])
        policy = gcp.cloudtasks.QueueIamPolicy("policy",
            project=default["project"],
            location=default["location"],
            name=default["name"],
            policy_data=admin.policy_data)
        ```

        ## cloudtasks.QueueIamBinding

        ```python
        import pulumi
        import pulumi_gcp as gcp

        binding = gcp.cloudtasks.QueueIamBinding("binding",
            project=default["project"],
            location=default["location"],
            name=default["name"],
            role="roles/viewer",
            members=["user:jane@example.com"])
        ```

        ## cloudtasks.QueueIamMember

        ```python
        import pulumi
        import pulumi_gcp as gcp

        member = gcp.cloudtasks.QueueIamMember("member",
            project=default["project"],
            location=default["location"],
            name=default["name"],
            role="roles/viewer",
            member="user:jane@example.com")
        ```

        ## cloudtasks.QueueIamPolicy

        ```python
        import pulumi
        import pulumi_gcp as gcp

        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/viewer",
            members=["user:jane@example.com"],
        )])
        policy = gcp.cloudtasks.QueueIamPolicy("policy",
            project=default["project"],
            location=default["location"],
            name=default["name"],
            policy_data=admin.policy_data)
        ```

        ## cloudtasks.QueueIamBinding

        ```python
        import pulumi
        import pulumi_gcp as gcp

        binding = gcp.cloudtasks.QueueIamBinding("binding",
            project=default["project"],
            location=default["location"],
            name=default["name"],
            role="roles/viewer",
            members=["user:jane@example.com"])
        ```

        ## cloudtasks.QueueIamMember

        ```python
        import pulumi
        import pulumi_gcp as gcp

        member = gcp.cloudtasks.QueueIamMember("member",
            project=default["project"],
            location=default["location"],
            name=default["name"],
            role="roles/viewer",
            member="user:jane@example.com")
        ```

        ## Import

        For all import syntaxes, the "resource in question" can take any of the following forms:

        * projects/{{project}}/locations/{{location}}/queues/{{name}}

        * {{project}}/{{location}}/{{name}}

        * {{location}}/{{name}}

        * {{name}}

        Any variables not passed in the import command will be taken from the provider configuration.

        Cloud Tasks queue IAM resources can be imported using the resource identifiers, role, and member.

        IAM member imports use space-delimited identifiers: the resource in question, the role, and the member identity, e.g.

        ```sh
        $ pulumi import gcp:cloudtasks/queueIamMember:QueueIamMember editor "projects/{{project}}/locations/{{location}}/queues/{{queue}} roles/viewer user:jane@example.com"
        ```

        IAM binding imports use space-delimited identifiers: the resource in question and the role, e.g.

        ```sh
        $ pulumi import gcp:cloudtasks/queueIamMember:QueueIamMember editor "projects/{{project}}/locations/{{location}}/queues/{{queue}} roles/viewer"
        ```

        IAM policy imports use the identifier of the resource in question, e.g.

        ```sh
        $ pulumi import gcp:cloudtasks/queueIamMember:QueueIamMember editor projects/{{project}}/locations/{{location}}/queues/{{queue}}
        ```

        -> **Custom Roles**: If you're importing a IAM resource with a custom role, make sure to use the

         full name of the custom role, e.g. `[projects/my-project|organizations/my-org]/roles/my-custom-role`.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] location: The location of the queue Used to find the parent resource to bind the IAM policy to. If not specified,
               the value will be parsed from the identifier of the parent resource. If no location is provided in the parent identifier and no
               location is specified, it is taken from the provider configuration.
        :param pulumi.Input[str] member: Identities that will be granted the privilege in `role`.
               Each entry can have one of the following values:
               * **allUsers**: A special identifier that represents anyone who is on the internet; with or without a Google account.
               * **allAuthenticatedUsers**: A special identifier that represents anyone who is authenticated with a Google account or a service account.
               * **user:{emailid}**: An email address that represents a specific Google account. For example, alice@gmail.com or joe@example.com.
               * **serviceAccount:{emailid}**: An email address that represents a service account. For example, my-other-app@appspot.gserviceaccount.com.
               * **group:{emailid}**: An email address that represents a Google group. For example, admins@example.com.
               * **domain:{domain}**: A G Suite domain (primary, instead of alias) name that represents all the users of that domain. For example, google.com or example.com.
               * **projectOwner:projectid**: Owners of the given project. For example, "projectOwner:my-example-project"
               * **projectEditor:projectid**: Editors of the given project. For example, "projectEditor:my-example-project"
               * **projectViewer:projectid**: Viewers of the given project. For example, "projectViewer:my-example-project"
        :param pulumi.Input[str] name: Used to find the parent resource to bind the IAM policy to
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
        :param pulumi.Input[str] role: The role that should be applied. Only one
               `cloudtasks.QueueIamBinding` can be used per role. Note that custom roles must be of the format
               `[projects|organizations]/{parent-name}/roles/{role-name}`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: QueueIamMemberArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Three different resources help you manage your IAM policy for Cloud Tasks Queue. Each of these resources serves a different use case:

        * `cloudtasks.QueueIamPolicy`: Authoritative. Sets the IAM policy for the queue and replaces any existing policy already attached.
        * `cloudtasks.QueueIamBinding`: Authoritative for a given role. Updates the IAM policy to grant a role to a list of members. Other roles within the IAM policy for the queue are preserved.
        * `cloudtasks.QueueIamMember`: Non-authoritative. Updates the IAM policy to grant a role to a new member. Other members for the role for the queue are preserved.

        A data source can be used to retrieve policy data in advent you do not need creation

        * `cloudtasks.QueueIamPolicy`: Retrieves the IAM policy for the queue

        > **Note:** `cloudtasks.QueueIamPolicy` **cannot** be used in conjunction with `cloudtasks.QueueIamBinding` and `cloudtasks.QueueIamMember` or they will fight over what your policy should be.

        > **Note:** `cloudtasks.QueueIamBinding` resources **can be** used in conjunction with `cloudtasks.QueueIamMember` resources **only if** they do not grant privilege to the same role.

        ## cloudtasks.QueueIamPolicy

        ```python
        import pulumi
        import pulumi_gcp as gcp

        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/viewer",
            members=["user:jane@example.com"],
        )])
        policy = gcp.cloudtasks.QueueIamPolicy("policy",
            project=default["project"],
            location=default["location"],
            name=default["name"],
            policy_data=admin.policy_data)
        ```

        ## cloudtasks.QueueIamBinding

        ```python
        import pulumi
        import pulumi_gcp as gcp

        binding = gcp.cloudtasks.QueueIamBinding("binding",
            project=default["project"],
            location=default["location"],
            name=default["name"],
            role="roles/viewer",
            members=["user:jane@example.com"])
        ```

        ## cloudtasks.QueueIamMember

        ```python
        import pulumi
        import pulumi_gcp as gcp

        member = gcp.cloudtasks.QueueIamMember("member",
            project=default["project"],
            location=default["location"],
            name=default["name"],
            role="roles/viewer",
            member="user:jane@example.com")
        ```

        ## cloudtasks.QueueIamPolicy

        ```python
        import pulumi
        import pulumi_gcp as gcp

        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/viewer",
            members=["user:jane@example.com"],
        )])
        policy = gcp.cloudtasks.QueueIamPolicy("policy",
            project=default["project"],
            location=default["location"],
            name=default["name"],
            policy_data=admin.policy_data)
        ```

        ## cloudtasks.QueueIamBinding

        ```python
        import pulumi
        import pulumi_gcp as gcp

        binding = gcp.cloudtasks.QueueIamBinding("binding",
            project=default["project"],
            location=default["location"],
            name=default["name"],
            role="roles/viewer",
            members=["user:jane@example.com"])
        ```

        ## cloudtasks.QueueIamMember

        ```python
        import pulumi
        import pulumi_gcp as gcp

        member = gcp.cloudtasks.QueueIamMember("member",
            project=default["project"],
            location=default["location"],
            name=default["name"],
            role="roles/viewer",
            member="user:jane@example.com")
        ```

        ## Import

        For all import syntaxes, the "resource in question" can take any of the following forms:

        * projects/{{project}}/locations/{{location}}/queues/{{name}}

        * {{project}}/{{location}}/{{name}}

        * {{location}}/{{name}}

        * {{name}}

        Any variables not passed in the import command will be taken from the provider configuration.

        Cloud Tasks queue IAM resources can be imported using the resource identifiers, role, and member.

        IAM member imports use space-delimited identifiers: the resource in question, the role, and the member identity, e.g.

        ```sh
        $ pulumi import gcp:cloudtasks/queueIamMember:QueueIamMember editor "projects/{{project}}/locations/{{location}}/queues/{{queue}} roles/viewer user:jane@example.com"
        ```

        IAM binding imports use space-delimited identifiers: the resource in question and the role, e.g.

        ```sh
        $ pulumi import gcp:cloudtasks/queueIamMember:QueueIamMember editor "projects/{{project}}/locations/{{location}}/queues/{{queue}} roles/viewer"
        ```

        IAM policy imports use the identifier of the resource in question, e.g.

        ```sh
        $ pulumi import gcp:cloudtasks/queueIamMember:QueueIamMember editor projects/{{project}}/locations/{{location}}/queues/{{queue}}
        ```

        -> **Custom Roles**: If you're importing a IAM resource with a custom role, make sure to use the

         full name of the custom role, e.g. `[projects/my-project|organizations/my-org]/roles/my-custom-role`.

        :param str resource_name: The name of the resource.
        :param QueueIamMemberArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(QueueIamMemberArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 condition: Optional[pulumi.Input[pulumi.InputType['QueueIamMemberConditionArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 member: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = QueueIamMemberArgs.__new__(QueueIamMemberArgs)

            __props__.__dict__["condition"] = condition
            __props__.__dict__["location"] = location
            if member is None and not opts.urn:
                raise TypeError("Missing required property 'member'")
            __props__.__dict__["member"] = member
            __props__.__dict__["name"] = name
            __props__.__dict__["project"] = project
            if role is None and not opts.urn:
                raise TypeError("Missing required property 'role'")
            __props__.__dict__["role"] = role
            __props__.__dict__["etag"] = None
        super(QueueIamMember, __self__).__init__(
            'gcp:cloudtasks/queueIamMember:QueueIamMember',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            condition: Optional[pulumi.Input[pulumi.InputType['QueueIamMemberConditionArgs']]] = None,
            etag: Optional[pulumi.Input[str]] = None,
            location: Optional[pulumi.Input[str]] = None,
            member: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None,
            role: Optional[pulumi.Input[str]] = None) -> 'QueueIamMember':
        """
        Get an existing QueueIamMember resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] etag: (Computed) The etag of the IAM policy.
        :param pulumi.Input[str] location: The location of the queue Used to find the parent resource to bind the IAM policy to. If not specified,
               the value will be parsed from the identifier of the parent resource. If no location is provided in the parent identifier and no
               location is specified, it is taken from the provider configuration.
        :param pulumi.Input[str] member: Identities that will be granted the privilege in `role`.
               Each entry can have one of the following values:
               * **allUsers**: A special identifier that represents anyone who is on the internet; with or without a Google account.
               * **allAuthenticatedUsers**: A special identifier that represents anyone who is authenticated with a Google account or a service account.
               * **user:{emailid}**: An email address that represents a specific Google account. For example, alice@gmail.com or joe@example.com.
               * **serviceAccount:{emailid}**: An email address that represents a service account. For example, my-other-app@appspot.gserviceaccount.com.
               * **group:{emailid}**: An email address that represents a Google group. For example, admins@example.com.
               * **domain:{domain}**: A G Suite domain (primary, instead of alias) name that represents all the users of that domain. For example, google.com or example.com.
               * **projectOwner:projectid**: Owners of the given project. For example, "projectOwner:my-example-project"
               * **projectEditor:projectid**: Editors of the given project. For example, "projectEditor:my-example-project"
               * **projectViewer:projectid**: Viewers of the given project. For example, "projectViewer:my-example-project"
        :param pulumi.Input[str] name: Used to find the parent resource to bind the IAM policy to
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
        :param pulumi.Input[str] role: The role that should be applied. Only one
               `cloudtasks.QueueIamBinding` can be used per role. Note that custom roles must be of the format
               `[projects|organizations]/{parent-name}/roles/{role-name}`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _QueueIamMemberState.__new__(_QueueIamMemberState)

        __props__.__dict__["condition"] = condition
        __props__.__dict__["etag"] = etag
        __props__.__dict__["location"] = location
        __props__.__dict__["member"] = member
        __props__.__dict__["name"] = name
        __props__.__dict__["project"] = project
        __props__.__dict__["role"] = role
        return QueueIamMember(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def condition(self) -> pulumi.Output[Optional['outputs.QueueIamMemberCondition']]:
        return pulumi.get(self, "condition")

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
        The location of the queue Used to find the parent resource to bind the IAM policy to. If not specified,
        the value will be parsed from the identifier of the parent resource. If no location is provided in the parent identifier and no
        location is specified, it is taken from the provider configuration.
        """
        return pulumi.get(self, "location")

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
        * **projectOwner:projectid**: Owners of the given project. For example, "projectOwner:my-example-project"
        * **projectEditor:projectid**: Editors of the given project. For example, "projectEditor:my-example-project"
        * **projectViewer:projectid**: Viewers of the given project. For example, "projectViewer:my-example-project"
        """
        return pulumi.get(self, "member")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Used to find the parent resource to bind the IAM policy to
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
        """
        return pulumi.get(self, "project")

    @property
    @pulumi.getter
    def role(self) -> pulumi.Output[str]:
        """
        The role that should be applied. Only one
        `cloudtasks.QueueIamBinding` can be used per role. Note that custom roles must be of the format
        `[projects|organizations]/{parent-name}/roles/{role-name}`.
        """
        return pulumi.get(self, "role")

