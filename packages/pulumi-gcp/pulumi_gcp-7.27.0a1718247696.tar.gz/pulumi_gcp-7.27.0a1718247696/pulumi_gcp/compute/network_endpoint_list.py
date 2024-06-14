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

__all__ = ['NetworkEndpointListArgs', 'NetworkEndpointList']

@pulumi.input_type
class NetworkEndpointListArgs:
    def __init__(__self__, *,
                 network_endpoint_group: pulumi.Input[str],
                 network_endpoints: Optional[pulumi.Input[Sequence[pulumi.Input['NetworkEndpointListNetworkEndpointArgs']]]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 zone: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a NetworkEndpointList resource.
        :param pulumi.Input[str] network_endpoint_group: The network endpoint group these endpoints are part of.
               
               
               - - -
        :param pulumi.Input[Sequence[pulumi.Input['NetworkEndpointListNetworkEndpointArgs']]] network_endpoints: The network endpoints to be added to the enclosing network endpoint group
               (NEG). Each endpoint specifies an IP address and port, along with
               additional information depending on the NEG type.
               Structure is documented below.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] zone: Zone where the containing network endpoint group is located.
        """
        pulumi.set(__self__, "network_endpoint_group", network_endpoint_group)
        if network_endpoints is not None:
            pulumi.set(__self__, "network_endpoints", network_endpoints)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if zone is not None:
            pulumi.set(__self__, "zone", zone)

    @property
    @pulumi.getter(name="networkEndpointGroup")
    def network_endpoint_group(self) -> pulumi.Input[str]:
        """
        The network endpoint group these endpoints are part of.


        - - -
        """
        return pulumi.get(self, "network_endpoint_group")

    @network_endpoint_group.setter
    def network_endpoint_group(self, value: pulumi.Input[str]):
        pulumi.set(self, "network_endpoint_group", value)

    @property
    @pulumi.getter(name="networkEndpoints")
    def network_endpoints(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['NetworkEndpointListNetworkEndpointArgs']]]]:
        """
        The network endpoints to be added to the enclosing network endpoint group
        (NEG). Each endpoint specifies an IP address and port, along with
        additional information depending on the NEG type.
        Structure is documented below.
        """
        return pulumi.get(self, "network_endpoints")

    @network_endpoints.setter
    def network_endpoints(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['NetworkEndpointListNetworkEndpointArgs']]]]):
        pulumi.set(self, "network_endpoints", value)

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
    def zone(self) -> Optional[pulumi.Input[str]]:
        """
        Zone where the containing network endpoint group is located.
        """
        return pulumi.get(self, "zone")

    @zone.setter
    def zone(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "zone", value)


@pulumi.input_type
class _NetworkEndpointListState:
    def __init__(__self__, *,
                 network_endpoint_group: Optional[pulumi.Input[str]] = None,
                 network_endpoints: Optional[pulumi.Input[Sequence[pulumi.Input['NetworkEndpointListNetworkEndpointArgs']]]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 zone: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering NetworkEndpointList resources.
        :param pulumi.Input[str] network_endpoint_group: The network endpoint group these endpoints are part of.
               
               
               - - -
        :param pulumi.Input[Sequence[pulumi.Input['NetworkEndpointListNetworkEndpointArgs']]] network_endpoints: The network endpoints to be added to the enclosing network endpoint group
               (NEG). Each endpoint specifies an IP address and port, along with
               additional information depending on the NEG type.
               Structure is documented below.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] zone: Zone where the containing network endpoint group is located.
        """
        if network_endpoint_group is not None:
            pulumi.set(__self__, "network_endpoint_group", network_endpoint_group)
        if network_endpoints is not None:
            pulumi.set(__self__, "network_endpoints", network_endpoints)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if zone is not None:
            pulumi.set(__self__, "zone", zone)

    @property
    @pulumi.getter(name="networkEndpointGroup")
    def network_endpoint_group(self) -> Optional[pulumi.Input[str]]:
        """
        The network endpoint group these endpoints are part of.


        - - -
        """
        return pulumi.get(self, "network_endpoint_group")

    @network_endpoint_group.setter
    def network_endpoint_group(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "network_endpoint_group", value)

    @property
    @pulumi.getter(name="networkEndpoints")
    def network_endpoints(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['NetworkEndpointListNetworkEndpointArgs']]]]:
        """
        The network endpoints to be added to the enclosing network endpoint group
        (NEG). Each endpoint specifies an IP address and port, along with
        additional information depending on the NEG type.
        Structure is documented below.
        """
        return pulumi.get(self, "network_endpoints")

    @network_endpoints.setter
    def network_endpoints(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['NetworkEndpointListNetworkEndpointArgs']]]]):
        pulumi.set(self, "network_endpoints", value)

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
    def zone(self) -> Optional[pulumi.Input[str]]:
        """
        Zone where the containing network endpoint group is located.
        """
        return pulumi.get(self, "zone")

    @zone.setter
    def zone(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "zone", value)


class NetworkEndpointList(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 network_endpoint_group: Optional[pulumi.Input[str]] = None,
                 network_endpoints: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NetworkEndpointListNetworkEndpointArgs']]]]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 zone: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        A set of network endpoints belonging to a network endpoint group (NEG). A
        single network endpoint represents a IP address and port combination that is
        part of a specific network endpoint group  (NEG). NEGs are zonal collections
        of these endpoints for GCP resources within a single subnet. **NOTE**:
        Network endpoints cannot be created outside of a network endpoint group.

        This resource is authoritative for a single NEG. Any endpoints not specified
        by this resource will be deleted when the resource configuration is applied.

        > **NOTE** In case the Endpoint's Instance is recreated, it's needed to
        perform `apply` twice. To avoid situations like this, please use this resource
        with the lifecycle `replace_triggered_by` method, with the passed Instance's ID.

        To get more information about NetworkEndpoints, see:

        * [API documentation](https://cloud.google.com/compute/docs/reference/rest/beta/networkEndpointGroups)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/load-balancing/docs/negs/)

        ## Example Usage

        ### Network Endpoints

        ```python
        import pulumi
        import pulumi_gcp as gcp

        my_image = gcp.compute.get_image(family="debian-11",
            project="debian-cloud")
        default = gcp.compute.Network("default",
            name="neg-network",
            auto_create_subnetworks=False)
        default_subnetwork = gcp.compute.Subnetwork("default",
            name="neg-subnetwork",
            ip_cidr_range="10.0.0.1/16",
            region="us-central1",
            network=default.id)
        endpoint_instance1 = gcp.compute.Instance("endpoint-instance1",
            network_interfaces=[gcp.compute.InstanceNetworkInterfaceArgs(
                access_configs=[gcp.compute.InstanceNetworkInterfaceAccessConfigArgs()],
                subnetwork=default_subnetwork.id,
            )],
            name="endpoint-instance1",
            machine_type="e2-medium",
            boot_disk=gcp.compute.InstanceBootDiskArgs(
                initialize_params=gcp.compute.InstanceBootDiskInitializeParamsArgs(
                    image=my_image.self_link,
                ),
            ))
        endpoint_instance2 = gcp.compute.Instance("endpoint-instance2",
            network_interfaces=[gcp.compute.InstanceNetworkInterfaceArgs(
                access_configs=[gcp.compute.InstanceNetworkInterfaceAccessConfigArgs()],
                subnetwork=default_subnetwork.id,
            )],
            name="endpoint-instance2",
            machine_type="e2-medium",
            boot_disk=gcp.compute.InstanceBootDiskArgs(
                initialize_params=gcp.compute.InstanceBootDiskInitializeParamsArgs(
                    image=my_image.self_link,
                ),
            ))
        default_endpoints = gcp.compute.NetworkEndpointList("default-endpoints",
            network_endpoint_group=neg["name"],
            network_endpoints=[
                gcp.compute.NetworkEndpointListNetworkEndpointArgs(
                    instance=endpoint_instance1.name,
                    port=neg["defaultPort"],
                    ip_address=endpoint_instance1.network_interfaces[0].network_ip,
                ),
                gcp.compute.NetworkEndpointListNetworkEndpointArgs(
                    instance=endpoint_instance2.name,
                    port=neg["defaultPort"],
                    ip_address=endpoint_instance2.network_interfaces[0].network_ip,
                ),
            ])
        group = gcp.compute.NetworkEndpointGroup("group",
            name="my-lb-neg",
            network=default.id,
            subnetwork=default_subnetwork.id,
            default_port=90,
            zone="us-central1-a")
        ```

        ## Import

        NetworkEndpoints can be imported using any of these accepted formats:

        * `projects/{{project}}/zones/{{zone}}/networkEndpointGroups/{{network_endpoint_group}}`

        * `{{project}}/{{zone}}/{{network_endpoint_group}}`

        * `{{zone}}/{{network_endpoint_group}}`

        * `{{network_endpoint_group}}`

        When using the `pulumi import` command, NetworkEndpoints can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:compute/networkEndpointList:NetworkEndpointList default projects/{{project}}/zones/{{zone}}/networkEndpointGroups/{{network_endpoint_group}}
        ```

        ```sh
        $ pulumi import gcp:compute/networkEndpointList:NetworkEndpointList default {{project}}/{{zone}}/{{network_endpoint_group}}
        ```

        ```sh
        $ pulumi import gcp:compute/networkEndpointList:NetworkEndpointList default {{zone}}/{{network_endpoint_group}}
        ```

        ```sh
        $ pulumi import gcp:compute/networkEndpointList:NetworkEndpointList default {{network_endpoint_group}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] network_endpoint_group: The network endpoint group these endpoints are part of.
               
               
               - - -
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NetworkEndpointListNetworkEndpointArgs']]]] network_endpoints: The network endpoints to be added to the enclosing network endpoint group
               (NEG). Each endpoint specifies an IP address and port, along with
               additional information depending on the NEG type.
               Structure is documented below.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] zone: Zone where the containing network endpoint group is located.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: NetworkEndpointListArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A set of network endpoints belonging to a network endpoint group (NEG). A
        single network endpoint represents a IP address and port combination that is
        part of a specific network endpoint group  (NEG). NEGs are zonal collections
        of these endpoints for GCP resources within a single subnet. **NOTE**:
        Network endpoints cannot be created outside of a network endpoint group.

        This resource is authoritative for a single NEG. Any endpoints not specified
        by this resource will be deleted when the resource configuration is applied.

        > **NOTE** In case the Endpoint's Instance is recreated, it's needed to
        perform `apply` twice. To avoid situations like this, please use this resource
        with the lifecycle `replace_triggered_by` method, with the passed Instance's ID.

        To get more information about NetworkEndpoints, see:

        * [API documentation](https://cloud.google.com/compute/docs/reference/rest/beta/networkEndpointGroups)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/load-balancing/docs/negs/)

        ## Example Usage

        ### Network Endpoints

        ```python
        import pulumi
        import pulumi_gcp as gcp

        my_image = gcp.compute.get_image(family="debian-11",
            project="debian-cloud")
        default = gcp.compute.Network("default",
            name="neg-network",
            auto_create_subnetworks=False)
        default_subnetwork = gcp.compute.Subnetwork("default",
            name="neg-subnetwork",
            ip_cidr_range="10.0.0.1/16",
            region="us-central1",
            network=default.id)
        endpoint_instance1 = gcp.compute.Instance("endpoint-instance1",
            network_interfaces=[gcp.compute.InstanceNetworkInterfaceArgs(
                access_configs=[gcp.compute.InstanceNetworkInterfaceAccessConfigArgs()],
                subnetwork=default_subnetwork.id,
            )],
            name="endpoint-instance1",
            machine_type="e2-medium",
            boot_disk=gcp.compute.InstanceBootDiskArgs(
                initialize_params=gcp.compute.InstanceBootDiskInitializeParamsArgs(
                    image=my_image.self_link,
                ),
            ))
        endpoint_instance2 = gcp.compute.Instance("endpoint-instance2",
            network_interfaces=[gcp.compute.InstanceNetworkInterfaceArgs(
                access_configs=[gcp.compute.InstanceNetworkInterfaceAccessConfigArgs()],
                subnetwork=default_subnetwork.id,
            )],
            name="endpoint-instance2",
            machine_type="e2-medium",
            boot_disk=gcp.compute.InstanceBootDiskArgs(
                initialize_params=gcp.compute.InstanceBootDiskInitializeParamsArgs(
                    image=my_image.self_link,
                ),
            ))
        default_endpoints = gcp.compute.NetworkEndpointList("default-endpoints",
            network_endpoint_group=neg["name"],
            network_endpoints=[
                gcp.compute.NetworkEndpointListNetworkEndpointArgs(
                    instance=endpoint_instance1.name,
                    port=neg["defaultPort"],
                    ip_address=endpoint_instance1.network_interfaces[0].network_ip,
                ),
                gcp.compute.NetworkEndpointListNetworkEndpointArgs(
                    instance=endpoint_instance2.name,
                    port=neg["defaultPort"],
                    ip_address=endpoint_instance2.network_interfaces[0].network_ip,
                ),
            ])
        group = gcp.compute.NetworkEndpointGroup("group",
            name="my-lb-neg",
            network=default.id,
            subnetwork=default_subnetwork.id,
            default_port=90,
            zone="us-central1-a")
        ```

        ## Import

        NetworkEndpoints can be imported using any of these accepted formats:

        * `projects/{{project}}/zones/{{zone}}/networkEndpointGroups/{{network_endpoint_group}}`

        * `{{project}}/{{zone}}/{{network_endpoint_group}}`

        * `{{zone}}/{{network_endpoint_group}}`

        * `{{network_endpoint_group}}`

        When using the `pulumi import` command, NetworkEndpoints can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:compute/networkEndpointList:NetworkEndpointList default projects/{{project}}/zones/{{zone}}/networkEndpointGroups/{{network_endpoint_group}}
        ```

        ```sh
        $ pulumi import gcp:compute/networkEndpointList:NetworkEndpointList default {{project}}/{{zone}}/{{network_endpoint_group}}
        ```

        ```sh
        $ pulumi import gcp:compute/networkEndpointList:NetworkEndpointList default {{zone}}/{{network_endpoint_group}}
        ```

        ```sh
        $ pulumi import gcp:compute/networkEndpointList:NetworkEndpointList default {{network_endpoint_group}}
        ```

        :param str resource_name: The name of the resource.
        :param NetworkEndpointListArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(NetworkEndpointListArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 network_endpoint_group: Optional[pulumi.Input[str]] = None,
                 network_endpoints: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NetworkEndpointListNetworkEndpointArgs']]]]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 zone: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = NetworkEndpointListArgs.__new__(NetworkEndpointListArgs)

            if network_endpoint_group is None and not opts.urn:
                raise TypeError("Missing required property 'network_endpoint_group'")
            __props__.__dict__["network_endpoint_group"] = network_endpoint_group
            __props__.__dict__["network_endpoints"] = network_endpoints
            __props__.__dict__["project"] = project
            __props__.__dict__["zone"] = zone
        super(NetworkEndpointList, __self__).__init__(
            'gcp:compute/networkEndpointList:NetworkEndpointList',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            network_endpoint_group: Optional[pulumi.Input[str]] = None,
            network_endpoints: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NetworkEndpointListNetworkEndpointArgs']]]]] = None,
            project: Optional[pulumi.Input[str]] = None,
            zone: Optional[pulumi.Input[str]] = None) -> 'NetworkEndpointList':
        """
        Get an existing NetworkEndpointList resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] network_endpoint_group: The network endpoint group these endpoints are part of.
               
               
               - - -
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NetworkEndpointListNetworkEndpointArgs']]]] network_endpoints: The network endpoints to be added to the enclosing network endpoint group
               (NEG). Each endpoint specifies an IP address and port, along with
               additional information depending on the NEG type.
               Structure is documented below.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] zone: Zone where the containing network endpoint group is located.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _NetworkEndpointListState.__new__(_NetworkEndpointListState)

        __props__.__dict__["network_endpoint_group"] = network_endpoint_group
        __props__.__dict__["network_endpoints"] = network_endpoints
        __props__.__dict__["project"] = project
        __props__.__dict__["zone"] = zone
        return NetworkEndpointList(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="networkEndpointGroup")
    def network_endpoint_group(self) -> pulumi.Output[str]:
        """
        The network endpoint group these endpoints are part of.


        - - -
        """
        return pulumi.get(self, "network_endpoint_group")

    @property
    @pulumi.getter(name="networkEndpoints")
    def network_endpoints(self) -> pulumi.Output[Optional[Sequence['outputs.NetworkEndpointListNetworkEndpoint']]]:
        """
        The network endpoints to be added to the enclosing network endpoint group
        (NEG). Each endpoint specifies an IP address and port, along with
        additional information depending on the NEG type.
        Structure is documented below.
        """
        return pulumi.get(self, "network_endpoints")

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
    def zone(self) -> pulumi.Output[str]:
        """
        Zone where the containing network endpoint group is located.
        """
        return pulumi.get(self, "zone")

