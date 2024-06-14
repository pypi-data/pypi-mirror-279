# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['TagBindingArgs', 'TagBinding']

@pulumi.input_type
class TagBindingArgs:
    def __init__(__self__, *,
                 parent: pulumi.Input[str],
                 tag_value: pulumi.Input[str]):
        """
        The set of arguments for constructing a TagBinding resource.
        :param pulumi.Input[str] parent: The full resource name of the resource the TagValue is bound to. E.g. //cloudresourcemanager.googleapis.com/projects/123
        :param pulumi.Input[str] tag_value: The TagValue of the TagBinding. Must be of the form tagValues/456.
               
               
               - - -
        """
        pulumi.set(__self__, "parent", parent)
        pulumi.set(__self__, "tag_value", tag_value)

    @property
    @pulumi.getter
    def parent(self) -> pulumi.Input[str]:
        """
        The full resource name of the resource the TagValue is bound to. E.g. //cloudresourcemanager.googleapis.com/projects/123
        """
        return pulumi.get(self, "parent")

    @parent.setter
    def parent(self, value: pulumi.Input[str]):
        pulumi.set(self, "parent", value)

    @property
    @pulumi.getter(name="tagValue")
    def tag_value(self) -> pulumi.Input[str]:
        """
        The TagValue of the TagBinding. Must be of the form tagValues/456.


        - - -
        """
        return pulumi.get(self, "tag_value")

    @tag_value.setter
    def tag_value(self, value: pulumi.Input[str]):
        pulumi.set(self, "tag_value", value)


@pulumi.input_type
class _TagBindingState:
    def __init__(__self__, *,
                 name: Optional[pulumi.Input[str]] = None,
                 parent: Optional[pulumi.Input[str]] = None,
                 tag_value: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering TagBinding resources.
        :param pulumi.Input[str] name: The generated id for the TagBinding. This is a string of the form: `tagBindings/{full-resource-name}/{tag-value-name}`
        :param pulumi.Input[str] parent: The full resource name of the resource the TagValue is bound to. E.g. //cloudresourcemanager.googleapis.com/projects/123
        :param pulumi.Input[str] tag_value: The TagValue of the TagBinding. Must be of the form tagValues/456.
               
               
               - - -
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if parent is not None:
            pulumi.set(__self__, "parent", parent)
        if tag_value is not None:
            pulumi.set(__self__, "tag_value", tag_value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The generated id for the TagBinding. This is a string of the form: `tagBindings/{full-resource-name}/{tag-value-name}`
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def parent(self) -> Optional[pulumi.Input[str]]:
        """
        The full resource name of the resource the TagValue is bound to. E.g. //cloudresourcemanager.googleapis.com/projects/123
        """
        return pulumi.get(self, "parent")

    @parent.setter
    def parent(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "parent", value)

    @property
    @pulumi.getter(name="tagValue")
    def tag_value(self) -> Optional[pulumi.Input[str]]:
        """
        The TagValue of the TagBinding. Must be of the form tagValues/456.


        - - -
        """
        return pulumi.get(self, "tag_value")

    @tag_value.setter
    def tag_value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "tag_value", value)


class TagBinding(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 parent: Optional[pulumi.Input[str]] = None,
                 tag_value: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        A TagBinding represents a connection between a TagValue and a cloud resource (currently project, folder, or organization). Once a TagBinding is created, the TagValue is applied to all the descendants of the cloud resource.

        To get more information about TagBinding, see:

        * [API documentation](https://cloud.google.com/resource-manager/reference/rest/v3/tagBindings)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/resource-manager/docs/tags/tags-creating-and-managing)

        ## Example Usage

        ### Tag Binding Basic

        ```python
        import pulumi
        import pulumi_gcp as gcp

        project = gcp.organizations.Project("project",
            project_id="project_id",
            name="project_id",
            org_id="123456789")
        key = gcp.tags.TagKey("key",
            parent="organizations/123456789",
            short_name="keyname",
            description="For keyname resources.")
        value = gcp.tags.TagValue("value",
            parent=key.name.apply(lambda name: f"tagKeys/{name}"),
            short_name="valuename",
            description="For valuename resources.")
        binding = gcp.tags.TagBinding("binding",
            parent=project.number.apply(lambda number: f"//cloudresourcemanager.googleapis.com/projects/{number}"),
            tag_value=value.name.apply(lambda name: f"tagValues/{name}"))
        ```

        ## Import

        TagBinding can be imported using any of these accepted formats:

        * `tagBindings/{{name}}`

        * `{{name}}`

        When using the `pulumi import` command, TagBinding can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:tags/tagBinding:TagBinding default tagBindings/{{name}}
        ```

        ```sh
        $ pulumi import gcp:tags/tagBinding:TagBinding default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] parent: The full resource name of the resource the TagValue is bound to. E.g. //cloudresourcemanager.googleapis.com/projects/123
        :param pulumi.Input[str] tag_value: The TagValue of the TagBinding. Must be of the form tagValues/456.
               
               
               - - -
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: TagBindingArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A TagBinding represents a connection between a TagValue and a cloud resource (currently project, folder, or organization). Once a TagBinding is created, the TagValue is applied to all the descendants of the cloud resource.

        To get more information about TagBinding, see:

        * [API documentation](https://cloud.google.com/resource-manager/reference/rest/v3/tagBindings)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/resource-manager/docs/tags/tags-creating-and-managing)

        ## Example Usage

        ### Tag Binding Basic

        ```python
        import pulumi
        import pulumi_gcp as gcp

        project = gcp.organizations.Project("project",
            project_id="project_id",
            name="project_id",
            org_id="123456789")
        key = gcp.tags.TagKey("key",
            parent="organizations/123456789",
            short_name="keyname",
            description="For keyname resources.")
        value = gcp.tags.TagValue("value",
            parent=key.name.apply(lambda name: f"tagKeys/{name}"),
            short_name="valuename",
            description="For valuename resources.")
        binding = gcp.tags.TagBinding("binding",
            parent=project.number.apply(lambda number: f"//cloudresourcemanager.googleapis.com/projects/{number}"),
            tag_value=value.name.apply(lambda name: f"tagValues/{name}"))
        ```

        ## Import

        TagBinding can be imported using any of these accepted formats:

        * `tagBindings/{{name}}`

        * `{{name}}`

        When using the `pulumi import` command, TagBinding can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:tags/tagBinding:TagBinding default tagBindings/{{name}}
        ```

        ```sh
        $ pulumi import gcp:tags/tagBinding:TagBinding default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param TagBindingArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(TagBindingArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 parent: Optional[pulumi.Input[str]] = None,
                 tag_value: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = TagBindingArgs.__new__(TagBindingArgs)

            if parent is None and not opts.urn:
                raise TypeError("Missing required property 'parent'")
            __props__.__dict__["parent"] = parent
            if tag_value is None and not opts.urn:
                raise TypeError("Missing required property 'tag_value'")
            __props__.__dict__["tag_value"] = tag_value
            __props__.__dict__["name"] = None
        super(TagBinding, __self__).__init__(
            'gcp:tags/tagBinding:TagBinding',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            name: Optional[pulumi.Input[str]] = None,
            parent: Optional[pulumi.Input[str]] = None,
            tag_value: Optional[pulumi.Input[str]] = None) -> 'TagBinding':
        """
        Get an existing TagBinding resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: The generated id for the TagBinding. This is a string of the form: `tagBindings/{full-resource-name}/{tag-value-name}`
        :param pulumi.Input[str] parent: The full resource name of the resource the TagValue is bound to. E.g. //cloudresourcemanager.googleapis.com/projects/123
        :param pulumi.Input[str] tag_value: The TagValue of the TagBinding. Must be of the form tagValues/456.
               
               
               - - -
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _TagBindingState.__new__(_TagBindingState)

        __props__.__dict__["name"] = name
        __props__.__dict__["parent"] = parent
        __props__.__dict__["tag_value"] = tag_value
        return TagBinding(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The generated id for the TagBinding. This is a string of the form: `tagBindings/{full-resource-name}/{tag-value-name}`
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def parent(self) -> pulumi.Output[str]:
        """
        The full resource name of the resource the TagValue is bound to. E.g. //cloudresourcemanager.googleapis.com/projects/123
        """
        return pulumi.get(self, "parent")

    @property
    @pulumi.getter(name="tagValue")
    def tag_value(self) -> pulumi.Output[str]:
        """
        The TagValue of the TagBinding. Must be of the form tagValues/456.


        - - -
        """
        return pulumi.get(self, "tag_value")

