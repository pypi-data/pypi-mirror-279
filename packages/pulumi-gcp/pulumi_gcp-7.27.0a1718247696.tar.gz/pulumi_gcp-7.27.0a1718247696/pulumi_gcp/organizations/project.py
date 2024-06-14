# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ProjectArgs', 'Project']

@pulumi.input_type
class ProjectArgs:
    def __init__(__self__, *,
                 auto_create_network: Optional[pulumi.Input[bool]] = None,
                 billing_account: Optional[pulumi.Input[str]] = None,
                 folder_id: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 project_id: Optional[pulumi.Input[str]] = None,
                 skip_delete: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a Project resource.
        :param pulumi.Input[bool] auto_create_network: Create the 'default' network automatically. Default true. If set to false, the default network will be deleted. Note
               that, for quota purposes, you will still need to have 1 network slot available to create the project successfully, even
               if you set auto_create_network to false, since the network will exist momentarily.
        :param pulumi.Input[str] billing_account: The alphanumeric ID of the billing account this project
               belongs to. The user or service account performing this operation with the provider
               must have at mininum Billing Account User privileges (`roles/billing.user`) on the billing account.
               See [Google Cloud Billing API Access Control](https://cloud.google.com/billing/docs/how-to/billing-access)
               for more details.
        :param pulumi.Input[str] folder_id: The numeric ID of the folder this project should be
               created under. Only one of `org_id` or `folder_id` may be
               specified. If the `folder_id` is specified, then the project is
               created under the specified folder. Changing this forces the
               project to be migrated to the newly specified folder.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: A set of key/value label pairs to assign to the project.
               **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
               Please refer to the field 'effective_labels' for all of the labels present on the resource.
        :param pulumi.Input[str] name: The display name of the project.
        :param pulumi.Input[str] org_id: The numeric ID of the organization this project belongs to.
               Changing this forces a new project to be created.  Only one of
               `org_id` or `folder_id` may be specified. If the `org_id` is
               specified then the project is created at the top level. Changing
               this forces the project to be migrated to the newly specified
               organization.
        :param pulumi.Input[str] project_id: The project ID. Changing this forces a new project to be created.
        :param pulumi.Input[bool] skip_delete: If true, the resource can be deleted
               without deleting the Project via the Google API.
        """
        if auto_create_network is not None:
            pulumi.set(__self__, "auto_create_network", auto_create_network)
        if billing_account is not None:
            pulumi.set(__self__, "billing_account", billing_account)
        if folder_id is not None:
            pulumi.set(__self__, "folder_id", folder_id)
        if labels is not None:
            pulumi.set(__self__, "labels", labels)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if org_id is not None:
            pulumi.set(__self__, "org_id", org_id)
        if project_id is not None:
            pulumi.set(__self__, "project_id", project_id)
        if skip_delete is not None:
            pulumi.set(__self__, "skip_delete", skip_delete)

    @property
    @pulumi.getter(name="autoCreateNetwork")
    def auto_create_network(self) -> Optional[pulumi.Input[bool]]:
        """
        Create the 'default' network automatically. Default true. If set to false, the default network will be deleted. Note
        that, for quota purposes, you will still need to have 1 network slot available to create the project successfully, even
        if you set auto_create_network to false, since the network will exist momentarily.
        """
        return pulumi.get(self, "auto_create_network")

    @auto_create_network.setter
    def auto_create_network(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "auto_create_network", value)

    @property
    @pulumi.getter(name="billingAccount")
    def billing_account(self) -> Optional[pulumi.Input[str]]:
        """
        The alphanumeric ID of the billing account this project
        belongs to. The user or service account performing this operation with the provider
        must have at mininum Billing Account User privileges (`roles/billing.user`) on the billing account.
        See [Google Cloud Billing API Access Control](https://cloud.google.com/billing/docs/how-to/billing-access)
        for more details.
        """
        return pulumi.get(self, "billing_account")

    @billing_account.setter
    def billing_account(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "billing_account", value)

    @property
    @pulumi.getter(name="folderId")
    def folder_id(self) -> Optional[pulumi.Input[str]]:
        """
        The numeric ID of the folder this project should be
        created under. Only one of `org_id` or `folder_id` may be
        specified. If the `folder_id` is specified, then the project is
        created under the specified folder. Changing this forces the
        project to be migrated to the newly specified folder.
        """
        return pulumi.get(self, "folder_id")

    @folder_id.setter
    def folder_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "folder_id", value)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A set of key/value label pairs to assign to the project.
        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.
        """
        return pulumi.get(self, "labels")

    @labels.setter
    def labels(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "labels", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The display name of the project.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> Optional[pulumi.Input[str]]:
        """
        The numeric ID of the organization this project belongs to.
        Changing this forces a new project to be created.  Only one of
        `org_id` or `folder_id` may be specified. If the `org_id` is
        specified then the project is created at the top level. Changing
        this forces the project to be migrated to the newly specified
        organization.
        """
        return pulumi.get(self, "org_id")

    @org_id.setter
    def org_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "org_id", value)

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> Optional[pulumi.Input[str]]:
        """
        The project ID. Changing this forces a new project to be created.
        """
        return pulumi.get(self, "project_id")

    @project_id.setter
    def project_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project_id", value)

    @property
    @pulumi.getter(name="skipDelete")
    def skip_delete(self) -> Optional[pulumi.Input[bool]]:
        """
        If true, the resource can be deleted
        without deleting the Project via the Google API.
        """
        return pulumi.get(self, "skip_delete")

    @skip_delete.setter
    def skip_delete(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "skip_delete", value)


@pulumi.input_type
class _ProjectState:
    def __init__(__self__, *,
                 auto_create_network: Optional[pulumi.Input[bool]] = None,
                 billing_account: Optional[pulumi.Input[str]] = None,
                 effective_labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 folder_id: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 number: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 project_id: Optional[pulumi.Input[str]] = None,
                 pulumi_labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 skip_delete: Optional[pulumi.Input[bool]] = None):
        """
        Input properties used for looking up and filtering Project resources.
        :param pulumi.Input[bool] auto_create_network: Create the 'default' network automatically. Default true. If set to false, the default network will be deleted. Note
               that, for quota purposes, you will still need to have 1 network slot available to create the project successfully, even
               if you set auto_create_network to false, since the network will exist momentarily.
        :param pulumi.Input[str] billing_account: The alphanumeric ID of the billing account this project
               belongs to. The user or service account performing this operation with the provider
               must have at mininum Billing Account User privileges (`roles/billing.user`) on the billing account.
               See [Google Cloud Billing API Access Control](https://cloud.google.com/billing/docs/how-to/billing-access)
               for more details.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] effective_labels: All of labels (key/value pairs) present on the resource in GCP, including the labels configured through Pulumi, other clients and services.
        :param pulumi.Input[str] folder_id: The numeric ID of the folder this project should be
               created under. Only one of `org_id` or `folder_id` may be
               specified. If the `folder_id` is specified, then the project is
               created under the specified folder. Changing this forces the
               project to be migrated to the newly specified folder.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: A set of key/value label pairs to assign to the project.
               **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
               Please refer to the field 'effective_labels' for all of the labels present on the resource.
        :param pulumi.Input[str] name: The display name of the project.
        :param pulumi.Input[str] number: The numeric identifier of the project.
        :param pulumi.Input[str] org_id: The numeric ID of the organization this project belongs to.
               Changing this forces a new project to be created.  Only one of
               `org_id` or `folder_id` may be specified. If the `org_id` is
               specified then the project is created at the top level. Changing
               this forces the project to be migrated to the newly specified
               organization.
        :param pulumi.Input[str] project_id: The project ID. Changing this forces a new project to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] pulumi_labels: The combination of labels configured directly on the resource and default labels configured on the provider.
        :param pulumi.Input[bool] skip_delete: If true, the resource can be deleted
               without deleting the Project via the Google API.
        """
        if auto_create_network is not None:
            pulumi.set(__self__, "auto_create_network", auto_create_network)
        if billing_account is not None:
            pulumi.set(__self__, "billing_account", billing_account)
        if effective_labels is not None:
            pulumi.set(__self__, "effective_labels", effective_labels)
        if folder_id is not None:
            pulumi.set(__self__, "folder_id", folder_id)
        if labels is not None:
            pulumi.set(__self__, "labels", labels)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if number is not None:
            pulumi.set(__self__, "number", number)
        if org_id is not None:
            pulumi.set(__self__, "org_id", org_id)
        if project_id is not None:
            pulumi.set(__self__, "project_id", project_id)
        if pulumi_labels is not None:
            pulumi.set(__self__, "pulumi_labels", pulumi_labels)
        if skip_delete is not None:
            pulumi.set(__self__, "skip_delete", skip_delete)

    @property
    @pulumi.getter(name="autoCreateNetwork")
    def auto_create_network(self) -> Optional[pulumi.Input[bool]]:
        """
        Create the 'default' network automatically. Default true. If set to false, the default network will be deleted. Note
        that, for quota purposes, you will still need to have 1 network slot available to create the project successfully, even
        if you set auto_create_network to false, since the network will exist momentarily.
        """
        return pulumi.get(self, "auto_create_network")

    @auto_create_network.setter
    def auto_create_network(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "auto_create_network", value)

    @property
    @pulumi.getter(name="billingAccount")
    def billing_account(self) -> Optional[pulumi.Input[str]]:
        """
        The alphanumeric ID of the billing account this project
        belongs to. The user or service account performing this operation with the provider
        must have at mininum Billing Account User privileges (`roles/billing.user`) on the billing account.
        See [Google Cloud Billing API Access Control](https://cloud.google.com/billing/docs/how-to/billing-access)
        for more details.
        """
        return pulumi.get(self, "billing_account")

    @billing_account.setter
    def billing_account(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "billing_account", value)

    @property
    @pulumi.getter(name="effectiveLabels")
    def effective_labels(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        All of labels (key/value pairs) present on the resource in GCP, including the labels configured through Pulumi, other clients and services.
        """
        return pulumi.get(self, "effective_labels")

    @effective_labels.setter
    def effective_labels(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "effective_labels", value)

    @property
    @pulumi.getter(name="folderId")
    def folder_id(self) -> Optional[pulumi.Input[str]]:
        """
        The numeric ID of the folder this project should be
        created under. Only one of `org_id` or `folder_id` may be
        specified. If the `folder_id` is specified, then the project is
        created under the specified folder. Changing this forces the
        project to be migrated to the newly specified folder.
        """
        return pulumi.get(self, "folder_id")

    @folder_id.setter
    def folder_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "folder_id", value)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A set of key/value label pairs to assign to the project.
        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.
        """
        return pulumi.get(self, "labels")

    @labels.setter
    def labels(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "labels", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The display name of the project.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def number(self) -> Optional[pulumi.Input[str]]:
        """
        The numeric identifier of the project.
        """
        return pulumi.get(self, "number")

    @number.setter
    def number(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "number", value)

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> Optional[pulumi.Input[str]]:
        """
        The numeric ID of the organization this project belongs to.
        Changing this forces a new project to be created.  Only one of
        `org_id` or `folder_id` may be specified. If the `org_id` is
        specified then the project is created at the top level. Changing
        this forces the project to be migrated to the newly specified
        organization.
        """
        return pulumi.get(self, "org_id")

    @org_id.setter
    def org_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "org_id", value)

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> Optional[pulumi.Input[str]]:
        """
        The project ID. Changing this forces a new project to be created.
        """
        return pulumi.get(self, "project_id")

    @project_id.setter
    def project_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project_id", value)

    @property
    @pulumi.getter(name="pulumiLabels")
    def pulumi_labels(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        The combination of labels configured directly on the resource and default labels configured on the provider.
        """
        return pulumi.get(self, "pulumi_labels")

    @pulumi_labels.setter
    def pulumi_labels(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "pulumi_labels", value)

    @property
    @pulumi.getter(name="skipDelete")
    def skip_delete(self) -> Optional[pulumi.Input[bool]]:
        """
        If true, the resource can be deleted
        without deleting the Project via the Google API.
        """
        return pulumi.get(self, "skip_delete")

    @skip_delete.setter
    def skip_delete(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "skip_delete", value)


class Project(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 auto_create_network: Optional[pulumi.Input[bool]] = None,
                 billing_account: Optional[pulumi.Input[str]] = None,
                 folder_id: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 project_id: Optional[pulumi.Input[str]] = None,
                 skip_delete: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        """
        Allows creation and management of a Google Cloud Platform project.

        Projects created with this resource must be associated with an Organization.
        See the [Organization documentation](https://cloud.google.com/resource-manager/docs/quickstarts) for more details.

        The user or service account that is running this provider when creating a `organizations.Project`
        resource must have `roles/resourcemanager.projectCreator` on the specified organization. See the
        [Access Control for Organizations Using IAM](https://cloud.google.com/resource-manager/docs/access-control-org)
        doc for more information.

        > This resource reads the specified billing account on every pulumi up and plan operation so you must have permissions on the specified billing account.

        To get more information about projects, see:

        * [API documentation](https://cloud.google.com/resource-manager/reference/rest/v1/projects)
        * How-to Guides
            * [Creating and managing projects](https://cloud.google.com/resource-manager/docs/creating-managing-projects)

        ## Example Usage

        ```python
        import pulumi
        import pulumi_gcp as gcp

        my_project = gcp.organizations.Project("my_project",
            name="My Project",
            project_id="your-project-id",
            org_id="1234567")
        ```

        To create a project under a specific folder

        ```python
        import pulumi
        import pulumi_gcp as gcp

        department1 = gcp.organizations.Folder("department1",
            display_name="Department 1",
            parent="organizations/1234567")
        my_project_in_a_folder = gcp.organizations.Project("my_project-in-a-folder",
            name="My Project",
            project_id="your-project-id",
            folder_id=department1.name)
        ```

        ## Import

        Projects can be imported using the `project_id`, e.g.

        * `{{project_id}}`

        When using the `pulumi import` command, Projects can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:organizations/project:Project default {{project_id}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] auto_create_network: Create the 'default' network automatically. Default true. If set to false, the default network will be deleted. Note
               that, for quota purposes, you will still need to have 1 network slot available to create the project successfully, even
               if you set auto_create_network to false, since the network will exist momentarily.
        :param pulumi.Input[str] billing_account: The alphanumeric ID of the billing account this project
               belongs to. The user or service account performing this operation with the provider
               must have at mininum Billing Account User privileges (`roles/billing.user`) on the billing account.
               See [Google Cloud Billing API Access Control](https://cloud.google.com/billing/docs/how-to/billing-access)
               for more details.
        :param pulumi.Input[str] folder_id: The numeric ID of the folder this project should be
               created under. Only one of `org_id` or `folder_id` may be
               specified. If the `folder_id` is specified, then the project is
               created under the specified folder. Changing this forces the
               project to be migrated to the newly specified folder.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: A set of key/value label pairs to assign to the project.
               **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
               Please refer to the field 'effective_labels' for all of the labels present on the resource.
        :param pulumi.Input[str] name: The display name of the project.
        :param pulumi.Input[str] org_id: The numeric ID of the organization this project belongs to.
               Changing this forces a new project to be created.  Only one of
               `org_id` or `folder_id` may be specified. If the `org_id` is
               specified then the project is created at the top level. Changing
               this forces the project to be migrated to the newly specified
               organization.
        :param pulumi.Input[str] project_id: The project ID. Changing this forces a new project to be created.
        :param pulumi.Input[bool] skip_delete: If true, the resource can be deleted
               without deleting the Project via the Google API.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[ProjectArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Allows creation and management of a Google Cloud Platform project.

        Projects created with this resource must be associated with an Organization.
        See the [Organization documentation](https://cloud.google.com/resource-manager/docs/quickstarts) for more details.

        The user or service account that is running this provider when creating a `organizations.Project`
        resource must have `roles/resourcemanager.projectCreator` on the specified organization. See the
        [Access Control for Organizations Using IAM](https://cloud.google.com/resource-manager/docs/access-control-org)
        doc for more information.

        > This resource reads the specified billing account on every pulumi up and plan operation so you must have permissions on the specified billing account.

        To get more information about projects, see:

        * [API documentation](https://cloud.google.com/resource-manager/reference/rest/v1/projects)
        * How-to Guides
            * [Creating and managing projects](https://cloud.google.com/resource-manager/docs/creating-managing-projects)

        ## Example Usage

        ```python
        import pulumi
        import pulumi_gcp as gcp

        my_project = gcp.organizations.Project("my_project",
            name="My Project",
            project_id="your-project-id",
            org_id="1234567")
        ```

        To create a project under a specific folder

        ```python
        import pulumi
        import pulumi_gcp as gcp

        department1 = gcp.organizations.Folder("department1",
            display_name="Department 1",
            parent="organizations/1234567")
        my_project_in_a_folder = gcp.organizations.Project("my_project-in-a-folder",
            name="My Project",
            project_id="your-project-id",
            folder_id=department1.name)
        ```

        ## Import

        Projects can be imported using the `project_id`, e.g.

        * `{{project_id}}`

        When using the `pulumi import` command, Projects can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:organizations/project:Project default {{project_id}}
        ```

        :param str resource_name: The name of the resource.
        :param ProjectArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ProjectArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 auto_create_network: Optional[pulumi.Input[bool]] = None,
                 billing_account: Optional[pulumi.Input[str]] = None,
                 folder_id: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 project_id: Optional[pulumi.Input[str]] = None,
                 skip_delete: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ProjectArgs.__new__(ProjectArgs)

            __props__.__dict__["auto_create_network"] = auto_create_network
            __props__.__dict__["billing_account"] = billing_account
            __props__.__dict__["folder_id"] = folder_id
            __props__.__dict__["labels"] = labels
            __props__.__dict__["name"] = name
            __props__.__dict__["org_id"] = org_id
            __props__.__dict__["project_id"] = project_id
            __props__.__dict__["skip_delete"] = skip_delete
            __props__.__dict__["effective_labels"] = None
            __props__.__dict__["number"] = None
            __props__.__dict__["pulumi_labels"] = None
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["effectiveLabels", "pulumiLabels"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(Project, __self__).__init__(
            'gcp:organizations/project:Project',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            auto_create_network: Optional[pulumi.Input[bool]] = None,
            billing_account: Optional[pulumi.Input[str]] = None,
            effective_labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            folder_id: Optional[pulumi.Input[str]] = None,
            labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            name: Optional[pulumi.Input[str]] = None,
            number: Optional[pulumi.Input[str]] = None,
            org_id: Optional[pulumi.Input[str]] = None,
            project_id: Optional[pulumi.Input[str]] = None,
            pulumi_labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            skip_delete: Optional[pulumi.Input[bool]] = None) -> 'Project':
        """
        Get an existing Project resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] auto_create_network: Create the 'default' network automatically. Default true. If set to false, the default network will be deleted. Note
               that, for quota purposes, you will still need to have 1 network slot available to create the project successfully, even
               if you set auto_create_network to false, since the network will exist momentarily.
        :param pulumi.Input[str] billing_account: The alphanumeric ID of the billing account this project
               belongs to. The user or service account performing this operation with the provider
               must have at mininum Billing Account User privileges (`roles/billing.user`) on the billing account.
               See [Google Cloud Billing API Access Control](https://cloud.google.com/billing/docs/how-to/billing-access)
               for more details.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] effective_labels: All of labels (key/value pairs) present on the resource in GCP, including the labels configured through Pulumi, other clients and services.
        :param pulumi.Input[str] folder_id: The numeric ID of the folder this project should be
               created under. Only one of `org_id` or `folder_id` may be
               specified. If the `folder_id` is specified, then the project is
               created under the specified folder. Changing this forces the
               project to be migrated to the newly specified folder.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: A set of key/value label pairs to assign to the project.
               **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
               Please refer to the field 'effective_labels' for all of the labels present on the resource.
        :param pulumi.Input[str] name: The display name of the project.
        :param pulumi.Input[str] number: The numeric identifier of the project.
        :param pulumi.Input[str] org_id: The numeric ID of the organization this project belongs to.
               Changing this forces a new project to be created.  Only one of
               `org_id` or `folder_id` may be specified. If the `org_id` is
               specified then the project is created at the top level. Changing
               this forces the project to be migrated to the newly specified
               organization.
        :param pulumi.Input[str] project_id: The project ID. Changing this forces a new project to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] pulumi_labels: The combination of labels configured directly on the resource and default labels configured on the provider.
        :param pulumi.Input[bool] skip_delete: If true, the resource can be deleted
               without deleting the Project via the Google API.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ProjectState.__new__(_ProjectState)

        __props__.__dict__["auto_create_network"] = auto_create_network
        __props__.__dict__["billing_account"] = billing_account
        __props__.__dict__["effective_labels"] = effective_labels
        __props__.__dict__["folder_id"] = folder_id
        __props__.__dict__["labels"] = labels
        __props__.__dict__["name"] = name
        __props__.__dict__["number"] = number
        __props__.__dict__["org_id"] = org_id
        __props__.__dict__["project_id"] = project_id
        __props__.__dict__["pulumi_labels"] = pulumi_labels
        __props__.__dict__["skip_delete"] = skip_delete
        return Project(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="autoCreateNetwork")
    def auto_create_network(self) -> pulumi.Output[Optional[bool]]:
        """
        Create the 'default' network automatically. Default true. If set to false, the default network will be deleted. Note
        that, for quota purposes, you will still need to have 1 network slot available to create the project successfully, even
        if you set auto_create_network to false, since the network will exist momentarily.
        """
        return pulumi.get(self, "auto_create_network")

    @property
    @pulumi.getter(name="billingAccount")
    def billing_account(self) -> pulumi.Output[Optional[str]]:
        """
        The alphanumeric ID of the billing account this project
        belongs to. The user or service account performing this operation with the provider
        must have at mininum Billing Account User privileges (`roles/billing.user`) on the billing account.
        See [Google Cloud Billing API Access Control](https://cloud.google.com/billing/docs/how-to/billing-access)
        for more details.
        """
        return pulumi.get(self, "billing_account")

    @property
    @pulumi.getter(name="effectiveLabels")
    def effective_labels(self) -> pulumi.Output[Mapping[str, str]]:
        """
        All of labels (key/value pairs) present on the resource in GCP, including the labels configured through Pulumi, other clients and services.
        """
        return pulumi.get(self, "effective_labels")

    @property
    @pulumi.getter(name="folderId")
    def folder_id(self) -> pulumi.Output[Optional[str]]:
        """
        The numeric ID of the folder this project should be
        created under. Only one of `org_id` or `folder_id` may be
        specified. If the `folder_id` is specified, then the project is
        created under the specified folder. Changing this forces the
        project to be migrated to the newly specified folder.
        """
        return pulumi.get(self, "folder_id")

    @property
    @pulumi.getter
    def labels(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A set of key/value label pairs to assign to the project.
        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The display name of the project.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def number(self) -> pulumi.Output[str]:
        """
        The numeric identifier of the project.
        """
        return pulumi.get(self, "number")

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> pulumi.Output[Optional[str]]:
        """
        The numeric ID of the organization this project belongs to.
        Changing this forces a new project to be created.  Only one of
        `org_id` or `folder_id` may be specified. If the `org_id` is
        specified then the project is created at the top level. Changing
        this forces the project to be migrated to the newly specified
        organization.
        """
        return pulumi.get(self, "org_id")

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> pulumi.Output[str]:
        """
        The project ID. Changing this forces a new project to be created.
        """
        return pulumi.get(self, "project_id")

    @property
    @pulumi.getter(name="pulumiLabels")
    def pulumi_labels(self) -> pulumi.Output[Mapping[str, str]]:
        """
        The combination of labels configured directly on the resource and default labels configured on the provider.
        """
        return pulumi.get(self, "pulumi_labels")

    @property
    @pulumi.getter(name="skipDelete")
    def skip_delete(self) -> pulumi.Output[bool]:
        """
        If true, the resource can be deleted
        without deleting the Project via the Google API.
        """
        return pulumi.get(self, "skip_delete")

