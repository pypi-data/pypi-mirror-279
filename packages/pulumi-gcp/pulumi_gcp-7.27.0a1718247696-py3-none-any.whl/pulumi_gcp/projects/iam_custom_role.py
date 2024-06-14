# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['IAMCustomRoleArgs', 'IAMCustomRole']

@pulumi.input_type
class IAMCustomRoleArgs:
    def __init__(__self__, *,
                 permissions: pulumi.Input[Sequence[pulumi.Input[str]]],
                 role_id: pulumi.Input[str],
                 title: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 stage: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a IAMCustomRole resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] permissions: The names of the permissions this role grants when bound in an IAM policy. At least one permission must be specified.
        :param pulumi.Input[str] role_id: The camel case role id to use for this role. Cannot contain `-` characters.
        :param pulumi.Input[str] title: A human-readable title for the role.
        :param pulumi.Input[str] description: A human-readable description for the role.
        :param pulumi.Input[str] project: The project that the custom role will be created in.
               Defaults to the provider project configuration.
        :param pulumi.Input[str] stage: The current launch stage of the role.
               Defaults to `GA`.
               List of possible stages is [here](https://cloud.google.com/iam/reference/rest/v1/organizations.roles#Role.RoleLaunchStage).
        """
        pulumi.set(__self__, "permissions", permissions)
        pulumi.set(__self__, "role_id", role_id)
        pulumi.set(__self__, "title", title)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if stage is not None:
            pulumi.set(__self__, "stage", stage)

    @property
    @pulumi.getter
    def permissions(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        The names of the permissions this role grants when bound in an IAM policy. At least one permission must be specified.
        """
        return pulumi.get(self, "permissions")

    @permissions.setter
    def permissions(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "permissions", value)

    @property
    @pulumi.getter(name="roleId")
    def role_id(self) -> pulumi.Input[str]:
        """
        The camel case role id to use for this role. Cannot contain `-` characters.
        """
        return pulumi.get(self, "role_id")

    @role_id.setter
    def role_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "role_id", value)

    @property
    @pulumi.getter
    def title(self) -> pulumi.Input[str]:
        """
        A human-readable title for the role.
        """
        return pulumi.get(self, "title")

    @title.setter
    def title(self, value: pulumi.Input[str]):
        pulumi.set(self, "title", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A human-readable description for the role.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        """
        The project that the custom role will be created in.
        Defaults to the provider project configuration.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter
    def stage(self) -> Optional[pulumi.Input[str]]:
        """
        The current launch stage of the role.
        Defaults to `GA`.
        List of possible stages is [here](https://cloud.google.com/iam/reference/rest/v1/organizations.roles#Role.RoleLaunchStage).
        """
        return pulumi.get(self, "stage")

    @stage.setter
    def stage(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "stage", value)


@pulumi.input_type
class _IAMCustomRoleState:
    def __init__(__self__, *,
                 deleted: Optional[pulumi.Input[bool]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 permissions: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 role_id: Optional[pulumi.Input[str]] = None,
                 stage: Optional[pulumi.Input[str]] = None,
                 title: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering IAMCustomRole resources.
        :param pulumi.Input[bool] deleted: (Optional) The current deleted state of the role.
        :param pulumi.Input[str] description: A human-readable description for the role.
        :param pulumi.Input[str] name: The name of the role in the format `projects/{{project}}/roles/{{role_id}}`. Like `id`, this field can be used as a reference in other resources such as IAM role bindings.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] permissions: The names of the permissions this role grants when bound in an IAM policy. At least one permission must be specified.
        :param pulumi.Input[str] project: The project that the custom role will be created in.
               Defaults to the provider project configuration.
        :param pulumi.Input[str] role_id: The camel case role id to use for this role. Cannot contain `-` characters.
        :param pulumi.Input[str] stage: The current launch stage of the role.
               Defaults to `GA`.
               List of possible stages is [here](https://cloud.google.com/iam/reference/rest/v1/organizations.roles#Role.RoleLaunchStage).
        :param pulumi.Input[str] title: A human-readable title for the role.
        """
        if deleted is not None:
            pulumi.set(__self__, "deleted", deleted)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if permissions is not None:
            pulumi.set(__self__, "permissions", permissions)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if role_id is not None:
            pulumi.set(__self__, "role_id", role_id)
        if stage is not None:
            pulumi.set(__self__, "stage", stage)
        if title is not None:
            pulumi.set(__self__, "title", title)

    @property
    @pulumi.getter
    def deleted(self) -> Optional[pulumi.Input[bool]]:
        """
        (Optional) The current deleted state of the role.
        """
        return pulumi.get(self, "deleted")

    @deleted.setter
    def deleted(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "deleted", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A human-readable description for the role.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the role in the format `projects/{{project}}/roles/{{role_id}}`. Like `id`, this field can be used as a reference in other resources such as IAM role bindings.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def permissions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The names of the permissions this role grants when bound in an IAM policy. At least one permission must be specified.
        """
        return pulumi.get(self, "permissions")

    @permissions.setter
    def permissions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "permissions", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        """
        The project that the custom role will be created in.
        Defaults to the provider project configuration.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter(name="roleId")
    def role_id(self) -> Optional[pulumi.Input[str]]:
        """
        The camel case role id to use for this role. Cannot contain `-` characters.
        """
        return pulumi.get(self, "role_id")

    @role_id.setter
    def role_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "role_id", value)

    @property
    @pulumi.getter
    def stage(self) -> Optional[pulumi.Input[str]]:
        """
        The current launch stage of the role.
        Defaults to `GA`.
        List of possible stages is [here](https://cloud.google.com/iam/reference/rest/v1/organizations.roles#Role.RoleLaunchStage).
        """
        return pulumi.get(self, "stage")

    @stage.setter
    def stage(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "stage", value)

    @property
    @pulumi.getter
    def title(self) -> Optional[pulumi.Input[str]]:
        """
        A human-readable title for the role.
        """
        return pulumi.get(self, "title")

    @title.setter
    def title(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "title", value)


class IAMCustomRole(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 permissions: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 role_id: Optional[pulumi.Input[str]] = None,
                 stage: Optional[pulumi.Input[str]] = None,
                 title: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Allows management of a customized Cloud IAM project role. For more information see
        [the official documentation](https://cloud.google.com/iam/docs/understanding-custom-roles)
        and
        [API](https://cloud.google.com/iam/reference/rest/v1/projects.roles).

        > **Warning:** Note that custom roles in GCP have the concept of a soft-delete. There are two issues that may arise
         from this and how roles are propagated. 1) creating a role may involve undeleting and then updating a role with the
         same name, possibly causing confusing behavior between undelete and update. 2) A deleted role is permanently deleted
         after 7 days, but it can take up to 30 more days (i.e. between 7 and 37 days after deletion) before the role name is
         made available again. This means a deleted role that has been deleted for more than 7 days cannot be changed at all
         by the provider, and new roles cannot share that name.

        ## Example Usage

        This snippet creates a customized IAM role.

        ```python
        import pulumi
        import pulumi_gcp as gcp

        my_custom_role = gcp.projects.IAMCustomRole("my-custom-role",
            role_id="myCustomRole",
            title="My Custom Role",
            description="A description",
            permissions=[
                "iam.roles.list",
                "iam.roles.create",
                "iam.roles.delete",
            ])
        ```

        ## Import

        Custom Roles can be imported using any of these accepted formats:

        * `projects/{{project}}/roles/{{role_id}}`

        * `{{project}}/{{role_id}}`

        * `{{role_id}}`

        When using the `pulumi import` command, Custom Roles can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:projects/iAMCustomRole:IAMCustomRole default projects/{{project}}/roles/{{role_id}}
        ```

        ```sh
        $ pulumi import gcp:projects/iAMCustomRole:IAMCustomRole default {{project}}/{{role_id}}
        ```

        ```sh
        $ pulumi import gcp:projects/iAMCustomRole:IAMCustomRole default {{role_id}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: A human-readable description for the role.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] permissions: The names of the permissions this role grants when bound in an IAM policy. At least one permission must be specified.
        :param pulumi.Input[str] project: The project that the custom role will be created in.
               Defaults to the provider project configuration.
        :param pulumi.Input[str] role_id: The camel case role id to use for this role. Cannot contain `-` characters.
        :param pulumi.Input[str] stage: The current launch stage of the role.
               Defaults to `GA`.
               List of possible stages is [here](https://cloud.google.com/iam/reference/rest/v1/organizations.roles#Role.RoleLaunchStage).
        :param pulumi.Input[str] title: A human-readable title for the role.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: IAMCustomRoleArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Allows management of a customized Cloud IAM project role. For more information see
        [the official documentation](https://cloud.google.com/iam/docs/understanding-custom-roles)
        and
        [API](https://cloud.google.com/iam/reference/rest/v1/projects.roles).

        > **Warning:** Note that custom roles in GCP have the concept of a soft-delete. There are two issues that may arise
         from this and how roles are propagated. 1) creating a role may involve undeleting and then updating a role with the
         same name, possibly causing confusing behavior between undelete and update. 2) A deleted role is permanently deleted
         after 7 days, but it can take up to 30 more days (i.e. between 7 and 37 days after deletion) before the role name is
         made available again. This means a deleted role that has been deleted for more than 7 days cannot be changed at all
         by the provider, and new roles cannot share that name.

        ## Example Usage

        This snippet creates a customized IAM role.

        ```python
        import pulumi
        import pulumi_gcp as gcp

        my_custom_role = gcp.projects.IAMCustomRole("my-custom-role",
            role_id="myCustomRole",
            title="My Custom Role",
            description="A description",
            permissions=[
                "iam.roles.list",
                "iam.roles.create",
                "iam.roles.delete",
            ])
        ```

        ## Import

        Custom Roles can be imported using any of these accepted formats:

        * `projects/{{project}}/roles/{{role_id}}`

        * `{{project}}/{{role_id}}`

        * `{{role_id}}`

        When using the `pulumi import` command, Custom Roles can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:projects/iAMCustomRole:IAMCustomRole default projects/{{project}}/roles/{{role_id}}
        ```

        ```sh
        $ pulumi import gcp:projects/iAMCustomRole:IAMCustomRole default {{project}}/{{role_id}}
        ```

        ```sh
        $ pulumi import gcp:projects/iAMCustomRole:IAMCustomRole default {{role_id}}
        ```

        :param str resource_name: The name of the resource.
        :param IAMCustomRoleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(IAMCustomRoleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 permissions: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 role_id: Optional[pulumi.Input[str]] = None,
                 stage: Optional[pulumi.Input[str]] = None,
                 title: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = IAMCustomRoleArgs.__new__(IAMCustomRoleArgs)

            __props__.__dict__["description"] = description
            if permissions is None and not opts.urn:
                raise TypeError("Missing required property 'permissions'")
            __props__.__dict__["permissions"] = permissions
            __props__.__dict__["project"] = project
            if role_id is None and not opts.urn:
                raise TypeError("Missing required property 'role_id'")
            __props__.__dict__["role_id"] = role_id
            __props__.__dict__["stage"] = stage
            if title is None and not opts.urn:
                raise TypeError("Missing required property 'title'")
            __props__.__dict__["title"] = title
            __props__.__dict__["deleted"] = None
            __props__.__dict__["name"] = None
        super(IAMCustomRole, __self__).__init__(
            'gcp:projects/iAMCustomRole:IAMCustomRole',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            deleted: Optional[pulumi.Input[bool]] = None,
            description: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            permissions: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            project: Optional[pulumi.Input[str]] = None,
            role_id: Optional[pulumi.Input[str]] = None,
            stage: Optional[pulumi.Input[str]] = None,
            title: Optional[pulumi.Input[str]] = None) -> 'IAMCustomRole':
        """
        Get an existing IAMCustomRole resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] deleted: (Optional) The current deleted state of the role.
        :param pulumi.Input[str] description: A human-readable description for the role.
        :param pulumi.Input[str] name: The name of the role in the format `projects/{{project}}/roles/{{role_id}}`. Like `id`, this field can be used as a reference in other resources such as IAM role bindings.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] permissions: The names of the permissions this role grants when bound in an IAM policy. At least one permission must be specified.
        :param pulumi.Input[str] project: The project that the custom role will be created in.
               Defaults to the provider project configuration.
        :param pulumi.Input[str] role_id: The camel case role id to use for this role. Cannot contain `-` characters.
        :param pulumi.Input[str] stage: The current launch stage of the role.
               Defaults to `GA`.
               List of possible stages is [here](https://cloud.google.com/iam/reference/rest/v1/organizations.roles#Role.RoleLaunchStage).
        :param pulumi.Input[str] title: A human-readable title for the role.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _IAMCustomRoleState.__new__(_IAMCustomRoleState)

        __props__.__dict__["deleted"] = deleted
        __props__.__dict__["description"] = description
        __props__.__dict__["name"] = name
        __props__.__dict__["permissions"] = permissions
        __props__.__dict__["project"] = project
        __props__.__dict__["role_id"] = role_id
        __props__.__dict__["stage"] = stage
        __props__.__dict__["title"] = title
        return IAMCustomRole(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def deleted(self) -> pulumi.Output[bool]:
        """
        (Optional) The current deleted state of the role.
        """
        return pulumi.get(self, "deleted")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        A human-readable description for the role.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the role in the format `projects/{{project}}/roles/{{role_id}}`. Like `id`, this field can be used as a reference in other resources such as IAM role bindings.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def permissions(self) -> pulumi.Output[Sequence[str]]:
        """
        The names of the permissions this role grants when bound in an IAM policy. At least one permission must be specified.
        """
        return pulumi.get(self, "permissions")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        """
        The project that the custom role will be created in.
        Defaults to the provider project configuration.
        """
        return pulumi.get(self, "project")

    @property
    @pulumi.getter(name="roleId")
    def role_id(self) -> pulumi.Output[str]:
        """
        The camel case role id to use for this role. Cannot contain `-` characters.
        """
        return pulumi.get(self, "role_id")

    @property
    @pulumi.getter
    def stage(self) -> pulumi.Output[Optional[str]]:
        """
        The current launch stage of the role.
        Defaults to `GA`.
        List of possible stages is [here](https://cloud.google.com/iam/reference/rest/v1/organizations.roles#Role.RoleLaunchStage).
        """
        return pulumi.get(self, "stage")

    @property
    @pulumi.getter
    def title(self) -> pulumi.Output[str]:
        """
        A human-readable title for the role.
        """
        return pulumi.get(self, "title")

