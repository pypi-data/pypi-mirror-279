# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['PublicDelegatedPrefixArgs', 'PublicDelegatedPrefix']

@pulumi.input_type
class PublicDelegatedPrefixArgs:
    def __init__(__self__, *,
                 ip_cidr_range: pulumi.Input[str],
                 parent_prefix: pulumi.Input[str],
                 region: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 is_live_migration: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a PublicDelegatedPrefix resource.
        :param pulumi.Input[str] ip_cidr_range: The IPv4 address range, in CIDR format, represented by this public advertised prefix.
               
               
               - - -
        :param pulumi.Input[str] parent_prefix: The URL of parent prefix. Either PublicAdvertisedPrefix or PublicDelegatedPrefix.
        :param pulumi.Input[str] region: A region where the prefix will reside.
        :param pulumi.Input[str] description: An optional description of this resource.
        :param pulumi.Input[bool] is_live_migration: If true, the prefix will be live migrated.
        :param pulumi.Input[str] name: Name of the resource. The name must be 1-63 characters long, and
               comply with RFC1035. Specifically, the name must be 1-63 characters
               long and match the regular expression `a-z?`
               which means the first character must be a lowercase letter, and all
               following characters must be a dash, lowercase letter, or digit,
               except the last character, which cannot be a dash.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        """
        pulumi.set(__self__, "ip_cidr_range", ip_cidr_range)
        pulumi.set(__self__, "parent_prefix", parent_prefix)
        pulumi.set(__self__, "region", region)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if is_live_migration is not None:
            pulumi.set(__self__, "is_live_migration", is_live_migration)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)

    @property
    @pulumi.getter(name="ipCidrRange")
    def ip_cidr_range(self) -> pulumi.Input[str]:
        """
        The IPv4 address range, in CIDR format, represented by this public advertised prefix.


        - - -
        """
        return pulumi.get(self, "ip_cidr_range")

    @ip_cidr_range.setter
    def ip_cidr_range(self, value: pulumi.Input[str]):
        pulumi.set(self, "ip_cidr_range", value)

    @property
    @pulumi.getter(name="parentPrefix")
    def parent_prefix(self) -> pulumi.Input[str]:
        """
        The URL of parent prefix. Either PublicAdvertisedPrefix or PublicDelegatedPrefix.
        """
        return pulumi.get(self, "parent_prefix")

    @parent_prefix.setter
    def parent_prefix(self, value: pulumi.Input[str]):
        pulumi.set(self, "parent_prefix", value)

    @property
    @pulumi.getter
    def region(self) -> pulumi.Input[str]:
        """
        A region where the prefix will reside.
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: pulumi.Input[str]):
        pulumi.set(self, "region", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        An optional description of this resource.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="isLiveMigration")
    def is_live_migration(self) -> Optional[pulumi.Input[bool]]:
        """
        If true, the prefix will be live migrated.
        """
        return pulumi.get(self, "is_live_migration")

    @is_live_migration.setter
    def is_live_migration(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_live_migration", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the resource. The name must be 1-63 characters long, and
        comply with RFC1035. Specifically, the name must be 1-63 characters
        long and match the regular expression `a-z?`
        which means the first character must be a lowercase letter, and all
        following characters must be a dash, lowercase letter, or digit,
        except the last character, which cannot be a dash.
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
        If it is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)


@pulumi.input_type
class _PublicDelegatedPrefixState:
    def __init__(__self__, *,
                 description: Optional[pulumi.Input[str]] = None,
                 ip_cidr_range: Optional[pulumi.Input[str]] = None,
                 is_live_migration: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 parent_prefix: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 self_link: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering PublicDelegatedPrefix resources.
        :param pulumi.Input[str] description: An optional description of this resource.
        :param pulumi.Input[str] ip_cidr_range: The IPv4 address range, in CIDR format, represented by this public advertised prefix.
               
               
               - - -
        :param pulumi.Input[bool] is_live_migration: If true, the prefix will be live migrated.
        :param pulumi.Input[str] name: Name of the resource. The name must be 1-63 characters long, and
               comply with RFC1035. Specifically, the name must be 1-63 characters
               long and match the regular expression `a-z?`
               which means the first character must be a lowercase letter, and all
               following characters must be a dash, lowercase letter, or digit,
               except the last character, which cannot be a dash.
        :param pulumi.Input[str] parent_prefix: The URL of parent prefix. Either PublicAdvertisedPrefix or PublicDelegatedPrefix.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: A region where the prefix will reside.
        :param pulumi.Input[str] self_link: The URI of the created resource.
        """
        if description is not None:
            pulumi.set(__self__, "description", description)
        if ip_cidr_range is not None:
            pulumi.set(__self__, "ip_cidr_range", ip_cidr_range)
        if is_live_migration is not None:
            pulumi.set(__self__, "is_live_migration", is_live_migration)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if parent_prefix is not None:
            pulumi.set(__self__, "parent_prefix", parent_prefix)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if region is not None:
            pulumi.set(__self__, "region", region)
        if self_link is not None:
            pulumi.set(__self__, "self_link", self_link)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        An optional description of this resource.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="ipCidrRange")
    def ip_cidr_range(self) -> Optional[pulumi.Input[str]]:
        """
        The IPv4 address range, in CIDR format, represented by this public advertised prefix.


        - - -
        """
        return pulumi.get(self, "ip_cidr_range")

    @ip_cidr_range.setter
    def ip_cidr_range(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ip_cidr_range", value)

    @property
    @pulumi.getter(name="isLiveMigration")
    def is_live_migration(self) -> Optional[pulumi.Input[bool]]:
        """
        If true, the prefix will be live migrated.
        """
        return pulumi.get(self, "is_live_migration")

    @is_live_migration.setter
    def is_live_migration(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_live_migration", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the resource. The name must be 1-63 characters long, and
        comply with RFC1035. Specifically, the name must be 1-63 characters
        long and match the regular expression `a-z?`
        which means the first character must be a lowercase letter, and all
        following characters must be a dash, lowercase letter, or digit,
        except the last character, which cannot be a dash.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="parentPrefix")
    def parent_prefix(self) -> Optional[pulumi.Input[str]]:
        """
        The URL of parent prefix. Either PublicAdvertisedPrefix or PublicDelegatedPrefix.
        """
        return pulumi.get(self, "parent_prefix")

    @parent_prefix.setter
    def parent_prefix(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "parent_prefix", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter
    def region(self) -> Optional[pulumi.Input[str]]:
        """
        A region where the prefix will reside.
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "region", value)

    @property
    @pulumi.getter(name="selfLink")
    def self_link(self) -> Optional[pulumi.Input[str]]:
        """
        The URI of the created resource.
        """
        return pulumi.get(self, "self_link")

    @self_link.setter
    def self_link(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "self_link", value)


class PublicDelegatedPrefix(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 ip_cidr_range: Optional[pulumi.Input[str]] = None,
                 is_live_migration: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 parent_prefix: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Represents a PublicDelegatedPrefix for use with bring your own IP addresses (BYOIP).

        To get more information about PublicDelegatedPrefix, see:

        * [API documentation](https://cloud.google.com/compute/docs/reference/rest/v1/publicDelegatedPrefixes)
        * How-to Guides
            * [Using bring your own IP](https://cloud.google.com/vpc/docs/using-bring-your-own-ip)

        ## Example Usage

        ### Public Delegated Prefixes Basic

        ```python
        import pulumi
        import pulumi_gcp as gcp

        advertised = gcp.compute.PublicAdvertisedPrefix("advertised",
            name="my-prefix",
            description="description",
            dns_verification_ip="127.127.0.0",
            ip_cidr_range="127.127.0.0/16")
        prefixes = gcp.compute.PublicDelegatedPrefix("prefixes",
            name="my-prefix",
            region="us-central1",
            description="my description",
            ip_cidr_range="127.127.0.0/24",
            parent_prefix=advertised.id)
        ```

        ## Import

        PublicDelegatedPrefix can be imported using any of these accepted formats:

        * `projects/{{project}}/regions/{{region}}/publicDelegatedPrefixes/{{name}}`

        * `{{project}}/{{region}}/{{name}}`

        * `{{region}}/{{name}}`

        * `{{name}}`

        When using the `pulumi import` command, PublicDelegatedPrefix can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:compute/publicDelegatedPrefix:PublicDelegatedPrefix default projects/{{project}}/regions/{{region}}/publicDelegatedPrefixes/{{name}}
        ```

        ```sh
        $ pulumi import gcp:compute/publicDelegatedPrefix:PublicDelegatedPrefix default {{project}}/{{region}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:compute/publicDelegatedPrefix:PublicDelegatedPrefix default {{region}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:compute/publicDelegatedPrefix:PublicDelegatedPrefix default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: An optional description of this resource.
        :param pulumi.Input[str] ip_cidr_range: The IPv4 address range, in CIDR format, represented by this public advertised prefix.
               
               
               - - -
        :param pulumi.Input[bool] is_live_migration: If true, the prefix will be live migrated.
        :param pulumi.Input[str] name: Name of the resource. The name must be 1-63 characters long, and
               comply with RFC1035. Specifically, the name must be 1-63 characters
               long and match the regular expression `a-z?`
               which means the first character must be a lowercase letter, and all
               following characters must be a dash, lowercase letter, or digit,
               except the last character, which cannot be a dash.
        :param pulumi.Input[str] parent_prefix: The URL of parent prefix. Either PublicAdvertisedPrefix or PublicDelegatedPrefix.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: A region where the prefix will reside.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: PublicDelegatedPrefixArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Represents a PublicDelegatedPrefix for use with bring your own IP addresses (BYOIP).

        To get more information about PublicDelegatedPrefix, see:

        * [API documentation](https://cloud.google.com/compute/docs/reference/rest/v1/publicDelegatedPrefixes)
        * How-to Guides
            * [Using bring your own IP](https://cloud.google.com/vpc/docs/using-bring-your-own-ip)

        ## Example Usage

        ### Public Delegated Prefixes Basic

        ```python
        import pulumi
        import pulumi_gcp as gcp

        advertised = gcp.compute.PublicAdvertisedPrefix("advertised",
            name="my-prefix",
            description="description",
            dns_verification_ip="127.127.0.0",
            ip_cidr_range="127.127.0.0/16")
        prefixes = gcp.compute.PublicDelegatedPrefix("prefixes",
            name="my-prefix",
            region="us-central1",
            description="my description",
            ip_cidr_range="127.127.0.0/24",
            parent_prefix=advertised.id)
        ```

        ## Import

        PublicDelegatedPrefix can be imported using any of these accepted formats:

        * `projects/{{project}}/regions/{{region}}/publicDelegatedPrefixes/{{name}}`

        * `{{project}}/{{region}}/{{name}}`

        * `{{region}}/{{name}}`

        * `{{name}}`

        When using the `pulumi import` command, PublicDelegatedPrefix can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:compute/publicDelegatedPrefix:PublicDelegatedPrefix default projects/{{project}}/regions/{{region}}/publicDelegatedPrefixes/{{name}}
        ```

        ```sh
        $ pulumi import gcp:compute/publicDelegatedPrefix:PublicDelegatedPrefix default {{project}}/{{region}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:compute/publicDelegatedPrefix:PublicDelegatedPrefix default {{region}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:compute/publicDelegatedPrefix:PublicDelegatedPrefix default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param PublicDelegatedPrefixArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PublicDelegatedPrefixArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 ip_cidr_range: Optional[pulumi.Input[str]] = None,
                 is_live_migration: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 parent_prefix: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PublicDelegatedPrefixArgs.__new__(PublicDelegatedPrefixArgs)

            __props__.__dict__["description"] = description
            if ip_cidr_range is None and not opts.urn:
                raise TypeError("Missing required property 'ip_cidr_range'")
            __props__.__dict__["ip_cidr_range"] = ip_cidr_range
            __props__.__dict__["is_live_migration"] = is_live_migration
            __props__.__dict__["name"] = name
            if parent_prefix is None and not opts.urn:
                raise TypeError("Missing required property 'parent_prefix'")
            __props__.__dict__["parent_prefix"] = parent_prefix
            __props__.__dict__["project"] = project
            if region is None and not opts.urn:
                raise TypeError("Missing required property 'region'")
            __props__.__dict__["region"] = region
            __props__.__dict__["self_link"] = None
        super(PublicDelegatedPrefix, __self__).__init__(
            'gcp:compute/publicDelegatedPrefix:PublicDelegatedPrefix',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            description: Optional[pulumi.Input[str]] = None,
            ip_cidr_range: Optional[pulumi.Input[str]] = None,
            is_live_migration: Optional[pulumi.Input[bool]] = None,
            name: Optional[pulumi.Input[str]] = None,
            parent_prefix: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None,
            region: Optional[pulumi.Input[str]] = None,
            self_link: Optional[pulumi.Input[str]] = None) -> 'PublicDelegatedPrefix':
        """
        Get an existing PublicDelegatedPrefix resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: An optional description of this resource.
        :param pulumi.Input[str] ip_cidr_range: The IPv4 address range, in CIDR format, represented by this public advertised prefix.
               
               
               - - -
        :param pulumi.Input[bool] is_live_migration: If true, the prefix will be live migrated.
        :param pulumi.Input[str] name: Name of the resource. The name must be 1-63 characters long, and
               comply with RFC1035. Specifically, the name must be 1-63 characters
               long and match the regular expression `a-z?`
               which means the first character must be a lowercase letter, and all
               following characters must be a dash, lowercase letter, or digit,
               except the last character, which cannot be a dash.
        :param pulumi.Input[str] parent_prefix: The URL of parent prefix. Either PublicAdvertisedPrefix or PublicDelegatedPrefix.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: A region where the prefix will reside.
        :param pulumi.Input[str] self_link: The URI of the created resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _PublicDelegatedPrefixState.__new__(_PublicDelegatedPrefixState)

        __props__.__dict__["description"] = description
        __props__.__dict__["ip_cidr_range"] = ip_cidr_range
        __props__.__dict__["is_live_migration"] = is_live_migration
        __props__.__dict__["name"] = name
        __props__.__dict__["parent_prefix"] = parent_prefix
        __props__.__dict__["project"] = project
        __props__.__dict__["region"] = region
        __props__.__dict__["self_link"] = self_link
        return PublicDelegatedPrefix(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        An optional description of this resource.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="ipCidrRange")
    def ip_cidr_range(self) -> pulumi.Output[str]:
        """
        The IPv4 address range, in CIDR format, represented by this public advertised prefix.


        - - -
        """
        return pulumi.get(self, "ip_cidr_range")

    @property
    @pulumi.getter(name="isLiveMigration")
    def is_live_migration(self) -> pulumi.Output[Optional[bool]]:
        """
        If true, the prefix will be live migrated.
        """
        return pulumi.get(self, "is_live_migration")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the resource. The name must be 1-63 characters long, and
        comply with RFC1035. Specifically, the name must be 1-63 characters
        long and match the regular expression `a-z?`
        which means the first character must be a lowercase letter, and all
        following characters must be a dash, lowercase letter, or digit,
        except the last character, which cannot be a dash.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="parentPrefix")
    def parent_prefix(self) -> pulumi.Output[str]:
        """
        The URL of parent prefix. Either PublicAdvertisedPrefix or PublicDelegatedPrefix.
        """
        return pulumi.get(self, "parent_prefix")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @property
    @pulumi.getter
    def region(self) -> pulumi.Output[str]:
        """
        A region where the prefix will reside.
        """
        return pulumi.get(self, "region")

    @property
    @pulumi.getter(name="selfLink")
    def self_link(self) -> pulumi.Output[str]:
        """
        The URI of the created resource.
        """
        return pulumi.get(self, "self_link")

