# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['PeeredDnsDomainArgs', 'PeeredDnsDomain']

@pulumi.input_type
class PeeredDnsDomainArgs:
    def __init__(__self__, *,
                 dns_suffix: pulumi.Input[str],
                 network: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 service: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a PeeredDnsDomain resource.
        :param pulumi.Input[str] dns_suffix: The DNS domain suffix of the peered DNS domain. Make sure to suffix with a `.` (dot).
        :param pulumi.Input[str] network: The network in the consumer project.
        :param pulumi.Input[str] name: Internal name used for the peered DNS domain.
        :param pulumi.Input[str] project: The producer project number. If not provided, the provider project is used.
        :param pulumi.Input[str] service: Private service connection between service and consumer network, defaults to `servicenetworking.googleapis.com`
        """
        pulumi.set(__self__, "dns_suffix", dns_suffix)
        pulumi.set(__self__, "network", network)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if service is not None:
            pulumi.set(__self__, "service", service)

    @property
    @pulumi.getter(name="dnsSuffix")
    def dns_suffix(self) -> pulumi.Input[str]:
        """
        The DNS domain suffix of the peered DNS domain. Make sure to suffix with a `.` (dot).
        """
        return pulumi.get(self, "dns_suffix")

    @dns_suffix.setter
    def dns_suffix(self, value: pulumi.Input[str]):
        pulumi.set(self, "dns_suffix", value)

    @property
    @pulumi.getter
    def network(self) -> pulumi.Input[str]:
        """
        The network in the consumer project.
        """
        return pulumi.get(self, "network")

    @network.setter
    def network(self, value: pulumi.Input[str]):
        pulumi.set(self, "network", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Internal name used for the peered DNS domain.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        """
        The producer project number. If not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter
    def service(self) -> Optional[pulumi.Input[str]]:
        """
        Private service connection between service and consumer network, defaults to `servicenetworking.googleapis.com`
        """
        return pulumi.get(self, "service")

    @service.setter
    def service(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service", value)


@pulumi.input_type
class _PeeredDnsDomainState:
    def __init__(__self__, *,
                 dns_suffix: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network: Optional[pulumi.Input[str]] = None,
                 parent: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 service: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering PeeredDnsDomain resources.
        :param pulumi.Input[str] dns_suffix: The DNS domain suffix of the peered DNS domain. Make sure to suffix with a `.` (dot).
        :param pulumi.Input[str] name: Internal name used for the peered DNS domain.
        :param pulumi.Input[str] network: The network in the consumer project.
        :param pulumi.Input[str] parent: an identifier for the resource with format `services/{{service}}/projects/{{project}}/global/networks/{{network}}`
        :param pulumi.Input[str] project: The producer project number. If not provided, the provider project is used.
        :param pulumi.Input[str] service: Private service connection between service and consumer network, defaults to `servicenetworking.googleapis.com`
        """
        if dns_suffix is not None:
            pulumi.set(__self__, "dns_suffix", dns_suffix)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if network is not None:
            pulumi.set(__self__, "network", network)
        if parent is not None:
            pulumi.set(__self__, "parent", parent)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if service is not None:
            pulumi.set(__self__, "service", service)

    @property
    @pulumi.getter(name="dnsSuffix")
    def dns_suffix(self) -> Optional[pulumi.Input[str]]:
        """
        The DNS domain suffix of the peered DNS domain. Make sure to suffix with a `.` (dot).
        """
        return pulumi.get(self, "dns_suffix")

    @dns_suffix.setter
    def dns_suffix(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "dns_suffix", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Internal name used for the peered DNS domain.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def network(self) -> Optional[pulumi.Input[str]]:
        """
        The network in the consumer project.
        """
        return pulumi.get(self, "network")

    @network.setter
    def network(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "network", value)

    @property
    @pulumi.getter
    def parent(self) -> Optional[pulumi.Input[str]]:
        """
        an identifier for the resource with format `services/{{service}}/projects/{{project}}/global/networks/{{network}}`
        """
        return pulumi.get(self, "parent")

    @parent.setter
    def parent(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "parent", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        """
        The producer project number. If not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter
    def service(self) -> Optional[pulumi.Input[str]]:
        """
        Private service connection between service and consumer network, defaults to `servicenetworking.googleapis.com`
        """
        return pulumi.get(self, "service")

    @service.setter
    def service(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service", value)


class PeeredDnsDomain(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 dns_suffix: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 service: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Allows management of a single peered DNS domain for an existing Google Cloud Platform project.

        When using Google Cloud DNS to manage internal DNS, create peered DNS domains to make your DNS available to services like Google Cloud Build.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_gcp as gcp

        name = gcp.servicenetworking.PeeredDnsDomain("name",
            project="10000000",
            name="example-com",
            network="default",
            dns_suffix="example.com.",
            service="peering-service")
        ```

        ## Import

        Project peered DNS domains can be imported using the `service`, `project`, `network` and `name`, where:

        - `service` is the service connection, defaults to `servicenetworking.googleapis.com`.

        - `project` is the producer project name.

        - `network` is the consumer network name.

        - `name` is the name of your peered DNS domain.

        * `services/{service}/projects/{project}/global/networks/{network}/peeredDnsDomains/{name}`

        When using the `pulumi import` command, project peered DNS domains can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:servicenetworking/peeredDnsDomain:PeeredDnsDomain default services/{service}/projects/{project}/global/networks/{network}/peeredDnsDomains/{name}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] dns_suffix: The DNS domain suffix of the peered DNS domain. Make sure to suffix with a `.` (dot).
        :param pulumi.Input[str] name: Internal name used for the peered DNS domain.
        :param pulumi.Input[str] network: The network in the consumer project.
        :param pulumi.Input[str] project: The producer project number. If not provided, the provider project is used.
        :param pulumi.Input[str] service: Private service connection between service and consumer network, defaults to `servicenetworking.googleapis.com`
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: PeeredDnsDomainArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Allows management of a single peered DNS domain for an existing Google Cloud Platform project.

        When using Google Cloud DNS to manage internal DNS, create peered DNS domains to make your DNS available to services like Google Cloud Build.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_gcp as gcp

        name = gcp.servicenetworking.PeeredDnsDomain("name",
            project="10000000",
            name="example-com",
            network="default",
            dns_suffix="example.com.",
            service="peering-service")
        ```

        ## Import

        Project peered DNS domains can be imported using the `service`, `project`, `network` and `name`, where:

        - `service` is the service connection, defaults to `servicenetworking.googleapis.com`.

        - `project` is the producer project name.

        - `network` is the consumer network name.

        - `name` is the name of your peered DNS domain.

        * `services/{service}/projects/{project}/global/networks/{network}/peeredDnsDomains/{name}`

        When using the `pulumi import` command, project peered DNS domains can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:servicenetworking/peeredDnsDomain:PeeredDnsDomain default services/{service}/projects/{project}/global/networks/{network}/peeredDnsDomains/{name}
        ```

        :param str resource_name: The name of the resource.
        :param PeeredDnsDomainArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PeeredDnsDomainArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 dns_suffix: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 service: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PeeredDnsDomainArgs.__new__(PeeredDnsDomainArgs)

            if dns_suffix is None and not opts.urn:
                raise TypeError("Missing required property 'dns_suffix'")
            __props__.__dict__["dns_suffix"] = dns_suffix
            __props__.__dict__["name"] = name
            if network is None and not opts.urn:
                raise TypeError("Missing required property 'network'")
            __props__.__dict__["network"] = network
            __props__.__dict__["project"] = project
            __props__.__dict__["service"] = service
            __props__.__dict__["parent"] = None
        super(PeeredDnsDomain, __self__).__init__(
            'gcp:servicenetworking/peeredDnsDomain:PeeredDnsDomain',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            dns_suffix: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            network: Optional[pulumi.Input[str]] = None,
            parent: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None,
            service: Optional[pulumi.Input[str]] = None) -> 'PeeredDnsDomain':
        """
        Get an existing PeeredDnsDomain resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] dns_suffix: The DNS domain suffix of the peered DNS domain. Make sure to suffix with a `.` (dot).
        :param pulumi.Input[str] name: Internal name used for the peered DNS domain.
        :param pulumi.Input[str] network: The network in the consumer project.
        :param pulumi.Input[str] parent: an identifier for the resource with format `services/{{service}}/projects/{{project}}/global/networks/{{network}}`
        :param pulumi.Input[str] project: The producer project number. If not provided, the provider project is used.
        :param pulumi.Input[str] service: Private service connection between service and consumer network, defaults to `servicenetworking.googleapis.com`
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _PeeredDnsDomainState.__new__(_PeeredDnsDomainState)

        __props__.__dict__["dns_suffix"] = dns_suffix
        __props__.__dict__["name"] = name
        __props__.__dict__["network"] = network
        __props__.__dict__["parent"] = parent
        __props__.__dict__["project"] = project
        __props__.__dict__["service"] = service
        return PeeredDnsDomain(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="dnsSuffix")
    def dns_suffix(self) -> pulumi.Output[str]:
        """
        The DNS domain suffix of the peered DNS domain. Make sure to suffix with a `.` (dot).
        """
        return pulumi.get(self, "dns_suffix")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Internal name used for the peered DNS domain.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def network(self) -> pulumi.Output[str]:
        """
        The network in the consumer project.
        """
        return pulumi.get(self, "network")

    @property
    @pulumi.getter
    def parent(self) -> pulumi.Output[str]:
        """
        an identifier for the resource with format `services/{{service}}/projects/{{project}}/global/networks/{{network}}`
        """
        return pulumi.get(self, "parent")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        """
        The producer project number. If not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @property
    @pulumi.getter
    def service(self) -> pulumi.Output[Optional[str]]:
        """
        Private service connection between service and consumer network, defaults to `servicenetworking.googleapis.com`
        """
        return pulumi.get(self, "service")

