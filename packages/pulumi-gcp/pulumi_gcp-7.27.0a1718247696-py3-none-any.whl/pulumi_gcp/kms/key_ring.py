# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['KeyRingArgs', 'KeyRing']

@pulumi.input_type
class KeyRingArgs:
    def __init__(__self__, *,
                 location: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a KeyRing resource.
        :param pulumi.Input[str] location: The location for the KeyRing.
               A full list of valid locations can be found by running `gcloud kms locations list`.
               
               
               - - -
        :param pulumi.Input[str] name: The resource name for the KeyRing.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        """
        pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)

    @property
    @pulumi.getter
    def location(self) -> pulumi.Input[str]:
        """
        The location for the KeyRing.
        A full list of valid locations can be found by running `gcloud kms locations list`.


        - - -
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: pulumi.Input[str]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The resource name for the KeyRing.
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
class _KeyRingState:
    def __init__(__self__, *,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering KeyRing resources.
        :param pulumi.Input[str] location: The location for the KeyRing.
               A full list of valid locations can be found by running `gcloud kms locations list`.
               
               
               - - -
        :param pulumi.Input[str] name: The resource name for the KeyRing.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        """
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The location for the KeyRing.
        A full list of valid locations can be found by running `gcloud kms locations list`.


        - - -
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The resource name for the KeyRing.
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


class KeyRing(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        A `KeyRing` is a toplevel logical grouping of `CryptoKeys`.

        > **Note:** KeyRings cannot be deleted from Google Cloud Platform.
        Destroying a provider-managed KeyRing will remove it from state but
        *will not delete the resource from the project.*

        To get more information about KeyRing, see:

        * [API documentation](https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings)
        * How-to Guides
            * [Creating a key ring](https://cloud.google.com/kms/docs/creating-keys#create_a_key_ring)

        ## Example Usage

        ### Kms Key Ring Basic

        ```python
        import pulumi
        import pulumi_gcp as gcp

        example_keyring = gcp.kms.KeyRing("example-keyring",
            name="keyring-example",
            location="global")
        ```

        ## Import

        KeyRing can be imported using any of these accepted formats:

        * `projects/{{project}}/locations/{{location}}/keyRings/{{name}}`

        * `{{project}}/{{location}}/{{name}}`

        * `{{location}}/{{name}}`

        When using the `pulumi import` command, KeyRing can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:kms/keyRing:KeyRing default projects/{{project}}/locations/{{location}}/keyRings/{{name}}
        ```

        ```sh
        $ pulumi import gcp:kms/keyRing:KeyRing default {{project}}/{{location}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:kms/keyRing:KeyRing default {{location}}/{{name}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] location: The location for the KeyRing.
               A full list of valid locations can be found by running `gcloud kms locations list`.
               
               
               - - -
        :param pulumi.Input[str] name: The resource name for the KeyRing.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: KeyRingArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A `KeyRing` is a toplevel logical grouping of `CryptoKeys`.

        > **Note:** KeyRings cannot be deleted from Google Cloud Platform.
        Destroying a provider-managed KeyRing will remove it from state but
        *will not delete the resource from the project.*

        To get more information about KeyRing, see:

        * [API documentation](https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings)
        * How-to Guides
            * [Creating a key ring](https://cloud.google.com/kms/docs/creating-keys#create_a_key_ring)

        ## Example Usage

        ### Kms Key Ring Basic

        ```python
        import pulumi
        import pulumi_gcp as gcp

        example_keyring = gcp.kms.KeyRing("example-keyring",
            name="keyring-example",
            location="global")
        ```

        ## Import

        KeyRing can be imported using any of these accepted formats:

        * `projects/{{project}}/locations/{{location}}/keyRings/{{name}}`

        * `{{project}}/{{location}}/{{name}}`

        * `{{location}}/{{name}}`

        When using the `pulumi import` command, KeyRing can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:kms/keyRing:KeyRing default projects/{{project}}/locations/{{location}}/keyRings/{{name}}
        ```

        ```sh
        $ pulumi import gcp:kms/keyRing:KeyRing default {{project}}/{{location}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:kms/keyRing:KeyRing default {{location}}/{{name}}
        ```

        :param str resource_name: The name of the resource.
        :param KeyRingArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(KeyRingArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = KeyRingArgs.__new__(KeyRingArgs)

            if location is None and not opts.urn:
                raise TypeError("Missing required property 'location'")
            __props__.__dict__["location"] = location
            __props__.__dict__["name"] = name
            __props__.__dict__["project"] = project
        super(KeyRing, __self__).__init__(
            'gcp:kms/keyRing:KeyRing',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            location: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None) -> 'KeyRing':
        """
        Get an existing KeyRing resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] location: The location for the KeyRing.
               A full list of valid locations can be found by running `gcloud kms locations list`.
               
               
               - - -
        :param pulumi.Input[str] name: The resource name for the KeyRing.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _KeyRingState.__new__(_KeyRingState)

        __props__.__dict__["location"] = location
        __props__.__dict__["name"] = name
        __props__.__dict__["project"] = project
        return KeyRing(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The location for the KeyRing.
        A full list of valid locations can be found by running `gcloud kms locations list`.


        - - -
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The resource name for the KeyRing.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

