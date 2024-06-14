# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ExternalAddressArgs', 'ExternalAddress']

@pulumi.input_type
class ExternalAddressArgs:
    def __init__(__self__, *,
                 internal_ip: pulumi.Input[str],
                 parent: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ExternalAddress resource.
        :param pulumi.Input[str] internal_ip: The internal IP address of a workload VM.
        :param pulumi.Input[str] parent: The resource name of the private cloud to create a new external address in.
               Resource names are schemeless URIs that follow the conventions in https://cloud.google.com/apis/design/resource_names.
               For example: projects/my-project/locations/us-west1-a/privateClouds/my-cloud
        :param pulumi.Input[str] description: User-provided description for this resource.
        :param pulumi.Input[str] name: The ID of the external IP Address.
               
               
               - - -
        """
        pulumi.set(__self__, "internal_ip", internal_ip)
        pulumi.set(__self__, "parent", parent)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="internalIp")
    def internal_ip(self) -> pulumi.Input[str]:
        """
        The internal IP address of a workload VM.
        """
        return pulumi.get(self, "internal_ip")

    @internal_ip.setter
    def internal_ip(self, value: pulumi.Input[str]):
        pulumi.set(self, "internal_ip", value)

    @property
    @pulumi.getter
    def parent(self) -> pulumi.Input[str]:
        """
        The resource name of the private cloud to create a new external address in.
        Resource names are schemeless URIs that follow the conventions in https://cloud.google.com/apis/design/resource_names.
        For example: projects/my-project/locations/us-west1-a/privateClouds/my-cloud
        """
        return pulumi.get(self, "parent")

    @parent.setter
    def parent(self, value: pulumi.Input[str]):
        pulumi.set(self, "parent", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        User-provided description for this resource.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the external IP Address.


        - - -
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _ExternalAddressState:
    def __init__(__self__, *,
                 create_time: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 external_ip: Optional[pulumi.Input[str]] = None,
                 internal_ip: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 parent: Optional[pulumi.Input[str]] = None,
                 state: Optional[pulumi.Input[str]] = None,
                 uid: Optional[pulumi.Input[str]] = None,
                 update_time: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ExternalAddress resources.
        :param pulumi.Input[str] create_time: Creation time of this resource.
               A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and
               up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".
        :param pulumi.Input[str] description: User-provided description for this resource.
        :param pulumi.Input[str] external_ip: The external IP address of a workload VM.
        :param pulumi.Input[str] internal_ip: The internal IP address of a workload VM.
        :param pulumi.Input[str] name: The ID of the external IP Address.
               
               
               - - -
        :param pulumi.Input[str] parent: The resource name of the private cloud to create a new external address in.
               Resource names are schemeless URIs that follow the conventions in https://cloud.google.com/apis/design/resource_names.
               For example: projects/my-project/locations/us-west1-a/privateClouds/my-cloud
        :param pulumi.Input[str] state: State of the resource.
        :param pulumi.Input[str] uid: System-generated unique identifier for the resource.
        :param pulumi.Input[str] update_time: Last updated time of this resource.
               A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine
               fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".
        """
        if create_time is not None:
            pulumi.set(__self__, "create_time", create_time)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if external_ip is not None:
            pulumi.set(__self__, "external_ip", external_ip)
        if internal_ip is not None:
            pulumi.set(__self__, "internal_ip", internal_ip)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if parent is not None:
            pulumi.set(__self__, "parent", parent)
        if state is not None:
            pulumi.set(__self__, "state", state)
        if uid is not None:
            pulumi.set(__self__, "uid", uid)
        if update_time is not None:
            pulumi.set(__self__, "update_time", update_time)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> Optional[pulumi.Input[str]]:
        """
        Creation time of this resource.
        A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and
        up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".
        """
        return pulumi.get(self, "create_time")

    @create_time.setter
    def create_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "create_time", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        User-provided description for this resource.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="externalIp")
    def external_ip(self) -> Optional[pulumi.Input[str]]:
        """
        The external IP address of a workload VM.
        """
        return pulumi.get(self, "external_ip")

    @external_ip.setter
    def external_ip(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "external_ip", value)

    @property
    @pulumi.getter(name="internalIp")
    def internal_ip(self) -> Optional[pulumi.Input[str]]:
        """
        The internal IP address of a workload VM.
        """
        return pulumi.get(self, "internal_ip")

    @internal_ip.setter
    def internal_ip(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "internal_ip", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the external IP Address.


        - - -
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def parent(self) -> Optional[pulumi.Input[str]]:
        """
        The resource name of the private cloud to create a new external address in.
        Resource names are schemeless URIs that follow the conventions in https://cloud.google.com/apis/design/resource_names.
        For example: projects/my-project/locations/us-west1-a/privateClouds/my-cloud
        """
        return pulumi.get(self, "parent")

    @parent.setter
    def parent(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "parent", value)

    @property
    @pulumi.getter
    def state(self) -> Optional[pulumi.Input[str]]:
        """
        State of the resource.
        """
        return pulumi.get(self, "state")

    @state.setter
    def state(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "state", value)

    @property
    @pulumi.getter
    def uid(self) -> Optional[pulumi.Input[str]]:
        """
        System-generated unique identifier for the resource.
        """
        return pulumi.get(self, "uid")

    @uid.setter
    def uid(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "uid", value)

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> Optional[pulumi.Input[str]]:
        """
        Last updated time of this resource.
        A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine
        fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".
        """
        return pulumi.get(self, "update_time")

    @update_time.setter
    def update_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "update_time", value)


class ExternalAddress(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 internal_ip: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 parent: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        An allocated external IP address and its corresponding internal IP address in a private cloud.

        To get more information about ExternalAddress, see:

        * [API documentation](https://cloud.google.com/vmware-engine/docs/reference/rest/v1/projects.locations.privateClouds.externalAddresses)

        ## Example Usage

        ### Vmware Engine External Address Basic

        ```python
        import pulumi
        import pulumi_gcp as gcp

        external_address_nw = gcp.vmwareengine.Network("external-address-nw",
            name="pc-nw",
            location="global",
            type="STANDARD",
            description="PC network description.")
        external_address_pc = gcp.vmwareengine.PrivateCloud("external-address-pc",
            location="-a",
            name="sample-pc",
            description="Sample test PC.",
            network_config=gcp.vmwareengine.PrivateCloudNetworkConfigArgs(
                management_cidr="192.168.50.0/24",
                vmware_engine_network=external_address_nw.id,
            ),
            management_cluster=gcp.vmwareengine.PrivateCloudManagementClusterArgs(
                cluster_id="sample-mgmt-cluster",
                node_type_configs=[gcp.vmwareengine.PrivateCloudManagementClusterNodeTypeConfigArgs(
                    node_type_id="standard-72",
                    node_count=3,
                )],
            ))
        external_address_np = gcp.vmwareengine.NetworkPolicy("external-address-np",
            location="",
            name="sample-np",
            edge_services_cidr="192.168.30.0/26",
            vmware_engine_network=external_address_nw.id)
        vmw_engine_external_address = gcp.vmwareengine.ExternalAddress("vmw-engine-external-address",
            name="sample-external-address",
            parent=external_address_pc.id,
            internal_ip="192.168.0.66",
            description="Sample description.",
            opts=pulumi.ResourceOptions(depends_on=[external_address_np]))
        ```

        ## Import

        ExternalAddress can be imported using any of these accepted formats:

        * `{{parent}}/externalAddresses/{{name}}`

        When using the `pulumi import` command, ExternalAddress can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:vmwareengine/externalAddress:ExternalAddress default {{parent}}/externalAddresses/{{name}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: User-provided description for this resource.
        :param pulumi.Input[str] internal_ip: The internal IP address of a workload VM.
        :param pulumi.Input[str] name: The ID of the external IP Address.
               
               
               - - -
        :param pulumi.Input[str] parent: The resource name of the private cloud to create a new external address in.
               Resource names are schemeless URIs that follow the conventions in https://cloud.google.com/apis/design/resource_names.
               For example: projects/my-project/locations/us-west1-a/privateClouds/my-cloud
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ExternalAddressArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        An allocated external IP address and its corresponding internal IP address in a private cloud.

        To get more information about ExternalAddress, see:

        * [API documentation](https://cloud.google.com/vmware-engine/docs/reference/rest/v1/projects.locations.privateClouds.externalAddresses)

        ## Example Usage

        ### Vmware Engine External Address Basic

        ```python
        import pulumi
        import pulumi_gcp as gcp

        external_address_nw = gcp.vmwareengine.Network("external-address-nw",
            name="pc-nw",
            location="global",
            type="STANDARD",
            description="PC network description.")
        external_address_pc = gcp.vmwareengine.PrivateCloud("external-address-pc",
            location="-a",
            name="sample-pc",
            description="Sample test PC.",
            network_config=gcp.vmwareengine.PrivateCloudNetworkConfigArgs(
                management_cidr="192.168.50.0/24",
                vmware_engine_network=external_address_nw.id,
            ),
            management_cluster=gcp.vmwareengine.PrivateCloudManagementClusterArgs(
                cluster_id="sample-mgmt-cluster",
                node_type_configs=[gcp.vmwareengine.PrivateCloudManagementClusterNodeTypeConfigArgs(
                    node_type_id="standard-72",
                    node_count=3,
                )],
            ))
        external_address_np = gcp.vmwareengine.NetworkPolicy("external-address-np",
            location="",
            name="sample-np",
            edge_services_cidr="192.168.30.0/26",
            vmware_engine_network=external_address_nw.id)
        vmw_engine_external_address = gcp.vmwareengine.ExternalAddress("vmw-engine-external-address",
            name="sample-external-address",
            parent=external_address_pc.id,
            internal_ip="192.168.0.66",
            description="Sample description.",
            opts=pulumi.ResourceOptions(depends_on=[external_address_np]))
        ```

        ## Import

        ExternalAddress can be imported using any of these accepted formats:

        * `{{parent}}/externalAddresses/{{name}}`

        When using the `pulumi import` command, ExternalAddress can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:vmwareengine/externalAddress:ExternalAddress default {{parent}}/externalAddresses/{{name}}
        ```

        :param str resource_name: The name of the resource.
        :param ExternalAddressArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ExternalAddressArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 internal_ip: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 parent: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ExternalAddressArgs.__new__(ExternalAddressArgs)

            __props__.__dict__["description"] = description
            if internal_ip is None and not opts.urn:
                raise TypeError("Missing required property 'internal_ip'")
            __props__.__dict__["internal_ip"] = internal_ip
            __props__.__dict__["name"] = name
            if parent is None and not opts.urn:
                raise TypeError("Missing required property 'parent'")
            __props__.__dict__["parent"] = parent
            __props__.__dict__["create_time"] = None
            __props__.__dict__["external_ip"] = None
            __props__.__dict__["state"] = None
            __props__.__dict__["uid"] = None
            __props__.__dict__["update_time"] = None
        super(ExternalAddress, __self__).__init__(
            'gcp:vmwareengine/externalAddress:ExternalAddress',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            create_time: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            external_ip: Optional[pulumi.Input[str]] = None,
            internal_ip: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            parent: Optional[pulumi.Input[str]] = None,
            state: Optional[pulumi.Input[str]] = None,
            uid: Optional[pulumi.Input[str]] = None,
            update_time: Optional[pulumi.Input[str]] = None) -> 'ExternalAddress':
        """
        Get an existing ExternalAddress resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] create_time: Creation time of this resource.
               A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and
               up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".
        :param pulumi.Input[str] description: User-provided description for this resource.
        :param pulumi.Input[str] external_ip: The external IP address of a workload VM.
        :param pulumi.Input[str] internal_ip: The internal IP address of a workload VM.
        :param pulumi.Input[str] name: The ID of the external IP Address.
               
               
               - - -
        :param pulumi.Input[str] parent: The resource name of the private cloud to create a new external address in.
               Resource names are schemeless URIs that follow the conventions in https://cloud.google.com/apis/design/resource_names.
               For example: projects/my-project/locations/us-west1-a/privateClouds/my-cloud
        :param pulumi.Input[str] state: State of the resource.
        :param pulumi.Input[str] uid: System-generated unique identifier for the resource.
        :param pulumi.Input[str] update_time: Last updated time of this resource.
               A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine
               fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ExternalAddressState.__new__(_ExternalAddressState)

        __props__.__dict__["create_time"] = create_time
        __props__.__dict__["description"] = description
        __props__.__dict__["external_ip"] = external_ip
        __props__.__dict__["internal_ip"] = internal_ip
        __props__.__dict__["name"] = name
        __props__.__dict__["parent"] = parent
        __props__.__dict__["state"] = state
        __props__.__dict__["uid"] = uid
        __props__.__dict__["update_time"] = update_time
        return ExternalAddress(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> pulumi.Output[str]:
        """
        Creation time of this resource.
        A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and
        up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        User-provided description for this resource.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="externalIp")
    def external_ip(self) -> pulumi.Output[str]:
        """
        The external IP address of a workload VM.
        """
        return pulumi.get(self, "external_ip")

    @property
    @pulumi.getter(name="internalIp")
    def internal_ip(self) -> pulumi.Output[str]:
        """
        The internal IP address of a workload VM.
        """
        return pulumi.get(self, "internal_ip")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The ID of the external IP Address.


        - - -
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def parent(self) -> pulumi.Output[str]:
        """
        The resource name of the private cloud to create a new external address in.
        Resource names are schemeless URIs that follow the conventions in https://cloud.google.com/apis/design/resource_names.
        For example: projects/my-project/locations/us-west1-a/privateClouds/my-cloud
        """
        return pulumi.get(self, "parent")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        State of the resource.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def uid(self) -> pulumi.Output[str]:
        """
        System-generated unique identifier for the resource.
        """
        return pulumi.get(self, "uid")

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> pulumi.Output[str]:
        """
        Last updated time of this resource.
        A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine
        fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".
        """
        return pulumi.get(self, "update_time")

