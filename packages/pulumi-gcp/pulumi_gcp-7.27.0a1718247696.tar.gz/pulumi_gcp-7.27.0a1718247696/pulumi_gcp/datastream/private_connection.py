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

__all__ = ['PrivateConnectionArgs', 'PrivateConnection']

@pulumi.input_type
class PrivateConnectionArgs:
    def __init__(__self__, *,
                 display_name: pulumi.Input[str],
                 location: pulumi.Input[str],
                 private_connection_id: pulumi.Input[str],
                 vpc_peering_config: pulumi.Input['PrivateConnectionVpcPeeringConfigArgs'],
                 create_without_validation: Optional[pulumi.Input[bool]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 project: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a PrivateConnection resource.
        :param pulumi.Input[str] display_name: Display name.
        :param pulumi.Input[str] location: The name of the location this private connection is located in.
        :param pulumi.Input[str] private_connection_id: The private connectivity identifier.
        :param pulumi.Input['PrivateConnectionVpcPeeringConfigArgs'] vpc_peering_config: The VPC Peering configuration is used to create VPC peering
               between Datastream and the consumer's VPC.
               Structure is documented below.
        :param pulumi.Input[bool] create_without_validation: If set to true, will skip validations.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Labels. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please
               refer to the field 'effective_labels' for all of the labels present on the resource.
        """
        pulumi.set(__self__, "display_name", display_name)
        pulumi.set(__self__, "location", location)
        pulumi.set(__self__, "private_connection_id", private_connection_id)
        pulumi.set(__self__, "vpc_peering_config", vpc_peering_config)
        if create_without_validation is not None:
            pulumi.set(__self__, "create_without_validation", create_without_validation)
        if labels is not None:
            pulumi.set(__self__, "labels", labels)
        if project is not None:
            pulumi.set(__self__, "project", project)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Input[str]:
        """
        Display name.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter
    def location(self) -> pulumi.Input[str]:
        """
        The name of the location this private connection is located in.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: pulumi.Input[str]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="privateConnectionId")
    def private_connection_id(self) -> pulumi.Input[str]:
        """
        The private connectivity identifier.
        """
        return pulumi.get(self, "private_connection_id")

    @private_connection_id.setter
    def private_connection_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "private_connection_id", value)

    @property
    @pulumi.getter(name="vpcPeeringConfig")
    def vpc_peering_config(self) -> pulumi.Input['PrivateConnectionVpcPeeringConfigArgs']:
        """
        The VPC Peering configuration is used to create VPC peering
        between Datastream and the consumer's VPC.
        Structure is documented below.
        """
        return pulumi.get(self, "vpc_peering_config")

    @vpc_peering_config.setter
    def vpc_peering_config(self, value: pulumi.Input['PrivateConnectionVpcPeeringConfigArgs']):
        pulumi.set(self, "vpc_peering_config", value)

    @property
    @pulumi.getter(name="createWithoutValidation")
    def create_without_validation(self) -> Optional[pulumi.Input[bool]]:
        """
        If set to true, will skip validations.
        """
        return pulumi.get(self, "create_without_validation")

    @create_without_validation.setter
    def create_without_validation(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "create_without_validation", value)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Labels. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please
        refer to the field 'effective_labels' for all of the labels present on the resource.
        """
        return pulumi.get(self, "labels")

    @labels.setter
    def labels(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "labels", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)


@pulumi.input_type
class _PrivateConnectionState:
    def __init__(__self__, *,
                 create_without_validation: Optional[pulumi.Input[bool]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 effective_labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 errors: Optional[pulumi.Input[Sequence[pulumi.Input['PrivateConnectionErrorArgs']]]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 private_connection_id: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 pulumi_labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 state: Optional[pulumi.Input[str]] = None,
                 vpc_peering_config: Optional[pulumi.Input['PrivateConnectionVpcPeeringConfigArgs']] = None):
        """
        Input properties used for looking up and filtering PrivateConnection resources.
        :param pulumi.Input[bool] create_without_validation: If set to true, will skip validations.
        :param pulumi.Input[str] display_name: Display name.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] effective_labels: All of labels (key/value pairs) present on the resource in GCP, including the labels configured through Pulumi, other clients and services.
        :param pulumi.Input[Sequence[pulumi.Input['PrivateConnectionErrorArgs']]] errors: The PrivateConnection error in case of failure.
               Structure is documented below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Labels. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please
               refer to the field 'effective_labels' for all of the labels present on the resource.
        :param pulumi.Input[str] location: The name of the location this private connection is located in.
        :param pulumi.Input[str] name: The resource's name.
        :param pulumi.Input[str] private_connection_id: The private connectivity identifier.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] pulumi_labels: The combination of labels configured directly on the resource
               and default labels configured on the provider.
        :param pulumi.Input[str] state: State of the PrivateConnection.
        :param pulumi.Input['PrivateConnectionVpcPeeringConfigArgs'] vpc_peering_config: The VPC Peering configuration is used to create VPC peering
               between Datastream and the consumer's VPC.
               Structure is documented below.
        """
        if create_without_validation is not None:
            pulumi.set(__self__, "create_without_validation", create_without_validation)
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if effective_labels is not None:
            pulumi.set(__self__, "effective_labels", effective_labels)
        if errors is not None:
            pulumi.set(__self__, "errors", errors)
        if labels is not None:
            pulumi.set(__self__, "labels", labels)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if private_connection_id is not None:
            pulumi.set(__self__, "private_connection_id", private_connection_id)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if pulumi_labels is not None:
            pulumi.set(__self__, "pulumi_labels", pulumi_labels)
        if state is not None:
            pulumi.set(__self__, "state", state)
        if vpc_peering_config is not None:
            pulumi.set(__self__, "vpc_peering_config", vpc_peering_config)

    @property
    @pulumi.getter(name="createWithoutValidation")
    def create_without_validation(self) -> Optional[pulumi.Input[bool]]:
        """
        If set to true, will skip validations.
        """
        return pulumi.get(self, "create_without_validation")

    @create_without_validation.setter
    def create_without_validation(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "create_without_validation", value)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        Display name.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "display_name", value)

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
    @pulumi.getter
    def errors(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['PrivateConnectionErrorArgs']]]]:
        """
        The PrivateConnection error in case of failure.
        Structure is documented below.
        """
        return pulumi.get(self, "errors")

    @errors.setter
    def errors(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['PrivateConnectionErrorArgs']]]]):
        pulumi.set(self, "errors", value)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Labels. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please
        refer to the field 'effective_labels' for all of the labels present on the resource.
        """
        return pulumi.get(self, "labels")

    @labels.setter
    def labels(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "labels", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the location this private connection is located in.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The resource's name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="privateConnectionId")
    def private_connection_id(self) -> Optional[pulumi.Input[str]]:
        """
        The private connectivity identifier.
        """
        return pulumi.get(self, "private_connection_id")

    @private_connection_id.setter
    def private_connection_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "private_connection_id", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter(name="pulumiLabels")
    def pulumi_labels(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        The combination of labels configured directly on the resource
        and default labels configured on the provider.
        """
        return pulumi.get(self, "pulumi_labels")

    @pulumi_labels.setter
    def pulumi_labels(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "pulumi_labels", value)

    @property
    @pulumi.getter
    def state(self) -> Optional[pulumi.Input[str]]:
        """
        State of the PrivateConnection.
        """
        return pulumi.get(self, "state")

    @state.setter
    def state(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "state", value)

    @property
    @pulumi.getter(name="vpcPeeringConfig")
    def vpc_peering_config(self) -> Optional[pulumi.Input['PrivateConnectionVpcPeeringConfigArgs']]:
        """
        The VPC Peering configuration is used to create VPC peering
        between Datastream and the consumer's VPC.
        Structure is documented below.
        """
        return pulumi.get(self, "vpc_peering_config")

    @vpc_peering_config.setter
    def vpc_peering_config(self, value: Optional[pulumi.Input['PrivateConnectionVpcPeeringConfigArgs']]):
        pulumi.set(self, "vpc_peering_config", value)


class PrivateConnection(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 create_without_validation: Optional[pulumi.Input[bool]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 private_connection_id: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 vpc_peering_config: Optional[pulumi.Input[pulumi.InputType['PrivateConnectionVpcPeeringConfigArgs']]] = None,
                 __props__=None):
        """
        The PrivateConnection resource is used to establish private connectivity between Datastream and a customer's network.

        To get more information about PrivateConnection, see:

        * [API documentation](https://cloud.google.com/datastream/docs/reference/rest/v1/projects.locations.privateConnections)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/datastream/docs/create-a-private-connectivity-configuration)

        ## Example Usage

        ### Datastream Private Connection Full

        ```python
        import pulumi
        import pulumi_gcp as gcp

        default_network = gcp.compute.Network("default", name="my-network")
        default = gcp.datastream.PrivateConnection("default",
            display_name="Connection profile",
            location="us-central1",
            private_connection_id="my-connection",
            labels={
                "key": "value",
            },
            vpc_peering_config=gcp.datastream.PrivateConnectionVpcPeeringConfigArgs(
                vpc=default_network.id,
                subnet="10.0.0.0/29",
            ))
        ```

        ## Import

        PrivateConnection can be imported using any of these accepted formats:

        * `projects/{{project}}/locations/{{location}}/privateConnections/{{private_connection_id}}`

        * `{{project}}/{{location}}/{{private_connection_id}}`

        * `{{location}}/{{private_connection_id}}`

        When using the `pulumi import` command, PrivateConnection can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:datastream/privateConnection:PrivateConnection default projects/{{project}}/locations/{{location}}/privateConnections/{{private_connection_id}}
        ```

        ```sh
        $ pulumi import gcp:datastream/privateConnection:PrivateConnection default {{project}}/{{location}}/{{private_connection_id}}
        ```

        ```sh
        $ pulumi import gcp:datastream/privateConnection:PrivateConnection default {{location}}/{{private_connection_id}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] create_without_validation: If set to true, will skip validations.
        :param pulumi.Input[str] display_name: Display name.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Labels. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please
               refer to the field 'effective_labels' for all of the labels present on the resource.
        :param pulumi.Input[str] location: The name of the location this private connection is located in.
        :param pulumi.Input[str] private_connection_id: The private connectivity identifier.
        :param pulumi.Input[pulumi.InputType['PrivateConnectionVpcPeeringConfigArgs']] vpc_peering_config: The VPC Peering configuration is used to create VPC peering
               between Datastream and the consumer's VPC.
               Structure is documented below.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: PrivateConnectionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The PrivateConnection resource is used to establish private connectivity between Datastream and a customer's network.

        To get more information about PrivateConnection, see:

        * [API documentation](https://cloud.google.com/datastream/docs/reference/rest/v1/projects.locations.privateConnections)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/datastream/docs/create-a-private-connectivity-configuration)

        ## Example Usage

        ### Datastream Private Connection Full

        ```python
        import pulumi
        import pulumi_gcp as gcp

        default_network = gcp.compute.Network("default", name="my-network")
        default = gcp.datastream.PrivateConnection("default",
            display_name="Connection profile",
            location="us-central1",
            private_connection_id="my-connection",
            labels={
                "key": "value",
            },
            vpc_peering_config=gcp.datastream.PrivateConnectionVpcPeeringConfigArgs(
                vpc=default_network.id,
                subnet="10.0.0.0/29",
            ))
        ```

        ## Import

        PrivateConnection can be imported using any of these accepted formats:

        * `projects/{{project}}/locations/{{location}}/privateConnections/{{private_connection_id}}`

        * `{{project}}/{{location}}/{{private_connection_id}}`

        * `{{location}}/{{private_connection_id}}`

        When using the `pulumi import` command, PrivateConnection can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:datastream/privateConnection:PrivateConnection default projects/{{project}}/locations/{{location}}/privateConnections/{{private_connection_id}}
        ```

        ```sh
        $ pulumi import gcp:datastream/privateConnection:PrivateConnection default {{project}}/{{location}}/{{private_connection_id}}
        ```

        ```sh
        $ pulumi import gcp:datastream/privateConnection:PrivateConnection default {{location}}/{{private_connection_id}}
        ```

        :param str resource_name: The name of the resource.
        :param PrivateConnectionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PrivateConnectionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 create_without_validation: Optional[pulumi.Input[bool]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 private_connection_id: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 vpc_peering_config: Optional[pulumi.Input[pulumi.InputType['PrivateConnectionVpcPeeringConfigArgs']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PrivateConnectionArgs.__new__(PrivateConnectionArgs)

            __props__.__dict__["create_without_validation"] = create_without_validation
            if display_name is None and not opts.urn:
                raise TypeError("Missing required property 'display_name'")
            __props__.__dict__["display_name"] = display_name
            __props__.__dict__["labels"] = labels
            if location is None and not opts.urn:
                raise TypeError("Missing required property 'location'")
            __props__.__dict__["location"] = location
            if private_connection_id is None and not opts.urn:
                raise TypeError("Missing required property 'private_connection_id'")
            __props__.__dict__["private_connection_id"] = private_connection_id
            __props__.__dict__["project"] = project
            if vpc_peering_config is None and not opts.urn:
                raise TypeError("Missing required property 'vpc_peering_config'")
            __props__.__dict__["vpc_peering_config"] = vpc_peering_config
            __props__.__dict__["effective_labels"] = None
            __props__.__dict__["errors"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["pulumi_labels"] = None
            __props__.__dict__["state"] = None
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["effectiveLabels", "pulumiLabels"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(PrivateConnection, __self__).__init__(
            'gcp:datastream/privateConnection:PrivateConnection',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            create_without_validation: Optional[pulumi.Input[bool]] = None,
            display_name: Optional[pulumi.Input[str]] = None,
            effective_labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            errors: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PrivateConnectionErrorArgs']]]]] = None,
            labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            location: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            private_connection_id: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None,
            pulumi_labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            state: Optional[pulumi.Input[str]] = None,
            vpc_peering_config: Optional[pulumi.Input[pulumi.InputType['PrivateConnectionVpcPeeringConfigArgs']]] = None) -> 'PrivateConnection':
        """
        Get an existing PrivateConnection resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] create_without_validation: If set to true, will skip validations.
        :param pulumi.Input[str] display_name: Display name.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] effective_labels: All of labels (key/value pairs) present on the resource in GCP, including the labels configured through Pulumi, other clients and services.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PrivateConnectionErrorArgs']]]] errors: The PrivateConnection error in case of failure.
               Structure is documented below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Labels. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please
               refer to the field 'effective_labels' for all of the labels present on the resource.
        :param pulumi.Input[str] location: The name of the location this private connection is located in.
        :param pulumi.Input[str] name: The resource's name.
        :param pulumi.Input[str] private_connection_id: The private connectivity identifier.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] pulumi_labels: The combination of labels configured directly on the resource
               and default labels configured on the provider.
        :param pulumi.Input[str] state: State of the PrivateConnection.
        :param pulumi.Input[pulumi.InputType['PrivateConnectionVpcPeeringConfigArgs']] vpc_peering_config: The VPC Peering configuration is used to create VPC peering
               between Datastream and the consumer's VPC.
               Structure is documented below.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _PrivateConnectionState.__new__(_PrivateConnectionState)

        __props__.__dict__["create_without_validation"] = create_without_validation
        __props__.__dict__["display_name"] = display_name
        __props__.__dict__["effective_labels"] = effective_labels
        __props__.__dict__["errors"] = errors
        __props__.__dict__["labels"] = labels
        __props__.__dict__["location"] = location
        __props__.__dict__["name"] = name
        __props__.__dict__["private_connection_id"] = private_connection_id
        __props__.__dict__["project"] = project
        __props__.__dict__["pulumi_labels"] = pulumi_labels
        __props__.__dict__["state"] = state
        __props__.__dict__["vpc_peering_config"] = vpc_peering_config
        return PrivateConnection(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="createWithoutValidation")
    def create_without_validation(self) -> pulumi.Output[Optional[bool]]:
        """
        If set to true, will skip validations.
        """
        return pulumi.get(self, "create_without_validation")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[str]:
        """
        Display name.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="effectiveLabels")
    def effective_labels(self) -> pulumi.Output[Mapping[str, str]]:
        """
        All of labels (key/value pairs) present on the resource in GCP, including the labels configured through Pulumi, other clients and services.
        """
        return pulumi.get(self, "effective_labels")

    @property
    @pulumi.getter
    def errors(self) -> pulumi.Output[Sequence['outputs.PrivateConnectionError']]:
        """
        The PrivateConnection error in case of failure.
        Structure is documented below.
        """
        return pulumi.get(self, "errors")

    @property
    @pulumi.getter
    def labels(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Labels. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please
        refer to the field 'effective_labels' for all of the labels present on the resource.
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The name of the location this private connection is located in.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The resource's name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="privateConnectionId")
    def private_connection_id(self) -> pulumi.Output[str]:
        """
        The private connectivity identifier.
        """
        return pulumi.get(self, "private_connection_id")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        return pulumi.get(self, "project")

    @property
    @pulumi.getter(name="pulumiLabels")
    def pulumi_labels(self) -> pulumi.Output[Mapping[str, str]]:
        """
        The combination of labels configured directly on the resource
        and default labels configured on the provider.
        """
        return pulumi.get(self, "pulumi_labels")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        State of the PrivateConnection.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter(name="vpcPeeringConfig")
    def vpc_peering_config(self) -> pulumi.Output['outputs.PrivateConnectionVpcPeeringConfig']:
        """
        The VPC Peering configuration is used to create VPC peering
        between Datastream and the consumer's VPC.
        Structure is documented below.
        """
        return pulumi.get(self, "vpc_peering_config")

