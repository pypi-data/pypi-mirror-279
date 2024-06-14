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

__all__ = ['AutoscalerArgs', 'Autoscaler']

@pulumi.input_type
class AutoscalerArgs:
    def __init__(__self__, *,
                 autoscaling_policy: pulumi.Input['AutoscalerAutoscalingPolicyArgs'],
                 target: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 zone: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Autoscaler resource.
        :param pulumi.Input['AutoscalerAutoscalingPolicyArgs'] autoscaling_policy: The configuration parameters for the autoscaling algorithm. You can
               define one or more of the policies for an autoscaler: cpuUtilization,
               customMetricUtilizations, and loadBalancingUtilization.
               If none of these are specified, the default will be to autoscale based
               on cpuUtilization to 0.6 or 60%.
               Structure is documented below.
        :param pulumi.Input[str] target: URL of the managed instance group that this autoscaler will scale.
        :param pulumi.Input[str] description: An optional description of this resource.
        :param pulumi.Input[str] name: Name of the resource. The name must be 1-63 characters long and match
               the regular expression `a-z?` which means the
               first character must be a lowercase letter, and all following
               characters must be a dash, lowercase letter, or digit, except the last
               character, which cannot be a dash.
        :param pulumi.Input[str] zone: URL of the zone where the instance group resides.
        """
        pulumi.set(__self__, "autoscaling_policy", autoscaling_policy)
        pulumi.set(__self__, "target", target)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if zone is not None:
            pulumi.set(__self__, "zone", zone)

    @property
    @pulumi.getter(name="autoscalingPolicy")
    def autoscaling_policy(self) -> pulumi.Input['AutoscalerAutoscalingPolicyArgs']:
        """
        The configuration parameters for the autoscaling algorithm. You can
        define one or more of the policies for an autoscaler: cpuUtilization,
        customMetricUtilizations, and loadBalancingUtilization.
        If none of these are specified, the default will be to autoscale based
        on cpuUtilization to 0.6 or 60%.
        Structure is documented below.
        """
        return pulumi.get(self, "autoscaling_policy")

    @autoscaling_policy.setter
    def autoscaling_policy(self, value: pulumi.Input['AutoscalerAutoscalingPolicyArgs']):
        pulumi.set(self, "autoscaling_policy", value)

    @property
    @pulumi.getter
    def target(self) -> pulumi.Input[str]:
        """
        URL of the managed instance group that this autoscaler will scale.
        """
        return pulumi.get(self, "target")

    @target.setter
    def target(self, value: pulumi.Input[str]):
        pulumi.set(self, "target", value)

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
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the resource. The name must be 1-63 characters long and match
        the regular expression `a-z?` which means the
        first character must be a lowercase letter, and all following
        characters must be a dash, lowercase letter, or digit, except the last
        character, which cannot be a dash.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter
    def zone(self) -> Optional[pulumi.Input[str]]:
        """
        URL of the zone where the instance group resides.
        """
        return pulumi.get(self, "zone")

    @zone.setter
    def zone(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "zone", value)


@pulumi.input_type
class _AutoscalerState:
    def __init__(__self__, *,
                 autoscaling_policy: Optional[pulumi.Input['AutoscalerAutoscalingPolicyArgs']] = None,
                 creation_timestamp: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 self_link: Optional[pulumi.Input[str]] = None,
                 target: Optional[pulumi.Input[str]] = None,
                 zone: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Autoscaler resources.
        :param pulumi.Input['AutoscalerAutoscalingPolicyArgs'] autoscaling_policy: The configuration parameters for the autoscaling algorithm. You can
               define one or more of the policies for an autoscaler: cpuUtilization,
               customMetricUtilizations, and loadBalancingUtilization.
               If none of these are specified, the default will be to autoscale based
               on cpuUtilization to 0.6 or 60%.
               Structure is documented below.
        :param pulumi.Input[str] creation_timestamp: Creation timestamp in RFC3339 text format.
        :param pulumi.Input[str] description: An optional description of this resource.
        :param pulumi.Input[str] name: Name of the resource. The name must be 1-63 characters long and match
               the regular expression `a-z?` which means the
               first character must be a lowercase letter, and all following
               characters must be a dash, lowercase letter, or digit, except the last
               character, which cannot be a dash.
        :param pulumi.Input[str] self_link: The URI of the created resource.
        :param pulumi.Input[str] target: URL of the managed instance group that this autoscaler will scale.
        :param pulumi.Input[str] zone: URL of the zone where the instance group resides.
        """
        if autoscaling_policy is not None:
            pulumi.set(__self__, "autoscaling_policy", autoscaling_policy)
        if creation_timestamp is not None:
            pulumi.set(__self__, "creation_timestamp", creation_timestamp)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if self_link is not None:
            pulumi.set(__self__, "self_link", self_link)
        if target is not None:
            pulumi.set(__self__, "target", target)
        if zone is not None:
            pulumi.set(__self__, "zone", zone)

    @property
    @pulumi.getter(name="autoscalingPolicy")
    def autoscaling_policy(self) -> Optional[pulumi.Input['AutoscalerAutoscalingPolicyArgs']]:
        """
        The configuration parameters for the autoscaling algorithm. You can
        define one or more of the policies for an autoscaler: cpuUtilization,
        customMetricUtilizations, and loadBalancingUtilization.
        If none of these are specified, the default will be to autoscale based
        on cpuUtilization to 0.6 or 60%.
        Structure is documented below.
        """
        return pulumi.get(self, "autoscaling_policy")

    @autoscaling_policy.setter
    def autoscaling_policy(self, value: Optional[pulumi.Input['AutoscalerAutoscalingPolicyArgs']]):
        pulumi.set(self, "autoscaling_policy", value)

    @property
    @pulumi.getter(name="creationTimestamp")
    def creation_timestamp(self) -> Optional[pulumi.Input[str]]:
        """
        Creation timestamp in RFC3339 text format.
        """
        return pulumi.get(self, "creation_timestamp")

    @creation_timestamp.setter
    def creation_timestamp(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "creation_timestamp", value)

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
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the resource. The name must be 1-63 characters long and match
        the regular expression `a-z?` which means the
        first character must be a lowercase letter, and all following
        characters must be a dash, lowercase letter, or digit, except the last
        character, which cannot be a dash.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)

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

    @property
    @pulumi.getter
    def target(self) -> Optional[pulumi.Input[str]]:
        """
        URL of the managed instance group that this autoscaler will scale.
        """
        return pulumi.get(self, "target")

    @target.setter
    def target(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "target", value)

    @property
    @pulumi.getter
    def zone(self) -> Optional[pulumi.Input[str]]:
        """
        URL of the zone where the instance group resides.
        """
        return pulumi.get(self, "zone")

    @zone.setter
    def zone(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "zone", value)


class Autoscaler(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 autoscaling_policy: Optional[pulumi.Input[pulumi.InputType['AutoscalerAutoscalingPolicyArgs']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 target: Optional[pulumi.Input[str]] = None,
                 zone: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Represents an Autoscaler resource.

        Autoscalers allow you to automatically scale virtual machine instances in
        managed instance groups according to an autoscaling policy that you
        define.

        To get more information about Autoscaler, see:

        * [API documentation](https://cloud.google.com/compute/docs/reference/rest/v1/autoscalers)
        * How-to Guides
            * [Autoscaling Groups of Instances](https://cloud.google.com/compute/docs/autoscaler/)

        ## Example Usage

        ### Autoscaler Single Instance

        ```python
        import pulumi
        import pulumi_gcp as gcp

        debian9 = gcp.compute.get_image(family="debian-11",
            project="debian-cloud")
        default_instance_template = gcp.compute.InstanceTemplate("default",
            name="my-instance-template",
            machine_type="e2-medium",
            can_ip_forward=False,
            tags=[
                "foo",
                "bar",
            ],
            disks=[gcp.compute.InstanceTemplateDiskArgs(
                source_image=debian9.id,
            )],
            network_interfaces=[gcp.compute.InstanceTemplateNetworkInterfaceArgs(
                network="default",
            )],
            metadata={
                "foo": "bar",
            },
            service_account=gcp.compute.InstanceTemplateServiceAccountArgs(
                scopes=[
                    "userinfo-email",
                    "compute-ro",
                    "storage-ro",
                ],
            ))
        default_target_pool = gcp.compute.TargetPool("default", name="my-target-pool")
        default_instance_group_manager = gcp.compute.InstanceGroupManager("default",
            name="my-igm",
            zone="us-central1-f",
            versions=[gcp.compute.InstanceGroupManagerVersionArgs(
                instance_template=default_instance_template.id,
                name="primary",
            )],
            target_pools=[default_target_pool.id],
            base_instance_name="autoscaler-sample")
        default = gcp.compute.Autoscaler("default",
            name="my-autoscaler",
            zone="us-central1-f",
            target=default_instance_group_manager.id,
            autoscaling_policy=gcp.compute.AutoscalerAutoscalingPolicyArgs(
                max_replicas=5,
                min_replicas=1,
                cooldown_period=60,
                metrics=[gcp.compute.AutoscalerAutoscalingPolicyMetricArgs(
                    name="pubsub.googleapis.com/subscription/num_undelivered_messages",
                    filter="resource.type = pubsub_subscription AND resource.label.subscription_id = our-subscription",
                    single_instance_assignment=65535,
                )],
            ))
        ```
        ### Autoscaler Basic

        ```python
        import pulumi
        import pulumi_gcp as gcp

        debian9 = gcp.compute.get_image(family="debian-11",
            project="debian-cloud")
        foobar_instance_template = gcp.compute.InstanceTemplate("foobar",
            name="my-instance-template",
            machine_type="e2-medium",
            can_ip_forward=False,
            tags=[
                "foo",
                "bar",
            ],
            disks=[gcp.compute.InstanceTemplateDiskArgs(
                source_image=debian9.id,
            )],
            network_interfaces=[gcp.compute.InstanceTemplateNetworkInterfaceArgs(
                network="default",
            )],
            metadata={
                "foo": "bar",
            },
            service_account=gcp.compute.InstanceTemplateServiceAccountArgs(
                scopes=[
                    "userinfo-email",
                    "compute-ro",
                    "storage-ro",
                ],
            ))
        foobar_target_pool = gcp.compute.TargetPool("foobar", name="my-target-pool")
        foobar_instance_group_manager = gcp.compute.InstanceGroupManager("foobar",
            name="my-igm",
            zone="us-central1-f",
            versions=[gcp.compute.InstanceGroupManagerVersionArgs(
                instance_template=foobar_instance_template.id,
                name="primary",
            )],
            target_pools=[foobar_target_pool.id],
            base_instance_name="foobar")
        foobar = gcp.compute.Autoscaler("foobar",
            name="my-autoscaler",
            zone="us-central1-f",
            target=foobar_instance_group_manager.id,
            autoscaling_policy=gcp.compute.AutoscalerAutoscalingPolicyArgs(
                max_replicas=5,
                min_replicas=1,
                cooldown_period=60,
                cpu_utilization=gcp.compute.AutoscalerAutoscalingPolicyCpuUtilizationArgs(
                    target=0.5,
                ),
            ))
        ```

        ## Import

        Autoscaler can be imported using any of these accepted formats:

        * `projects/{{project}}/zones/{{zone}}/autoscalers/{{name}}`

        * `{{project}}/{{zone}}/{{name}}`

        * `{{zone}}/{{name}}`

        * `{{name}}`

        When using the `pulumi import` command, Autoscaler can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:compute/autoscaler:Autoscaler default projects/{{project}}/zones/{{zone}}/autoscalers/{{name}}
        ```

        ```sh
        $ pulumi import gcp:compute/autoscaler:Autoscaler default {{project}}/{{zone}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:compute/autoscaler:Autoscaler default {{zone}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:compute/autoscaler:Autoscaler default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['AutoscalerAutoscalingPolicyArgs']] autoscaling_policy: The configuration parameters for the autoscaling algorithm. You can
               define one or more of the policies for an autoscaler: cpuUtilization,
               customMetricUtilizations, and loadBalancingUtilization.
               If none of these are specified, the default will be to autoscale based
               on cpuUtilization to 0.6 or 60%.
               Structure is documented below.
        :param pulumi.Input[str] description: An optional description of this resource.
        :param pulumi.Input[str] name: Name of the resource. The name must be 1-63 characters long and match
               the regular expression `a-z?` which means the
               first character must be a lowercase letter, and all following
               characters must be a dash, lowercase letter, or digit, except the last
               character, which cannot be a dash.
        :param pulumi.Input[str] target: URL of the managed instance group that this autoscaler will scale.
        :param pulumi.Input[str] zone: URL of the zone where the instance group resides.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AutoscalerArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Represents an Autoscaler resource.

        Autoscalers allow you to automatically scale virtual machine instances in
        managed instance groups according to an autoscaling policy that you
        define.

        To get more information about Autoscaler, see:

        * [API documentation](https://cloud.google.com/compute/docs/reference/rest/v1/autoscalers)
        * How-to Guides
            * [Autoscaling Groups of Instances](https://cloud.google.com/compute/docs/autoscaler/)

        ## Example Usage

        ### Autoscaler Single Instance

        ```python
        import pulumi
        import pulumi_gcp as gcp

        debian9 = gcp.compute.get_image(family="debian-11",
            project="debian-cloud")
        default_instance_template = gcp.compute.InstanceTemplate("default",
            name="my-instance-template",
            machine_type="e2-medium",
            can_ip_forward=False,
            tags=[
                "foo",
                "bar",
            ],
            disks=[gcp.compute.InstanceTemplateDiskArgs(
                source_image=debian9.id,
            )],
            network_interfaces=[gcp.compute.InstanceTemplateNetworkInterfaceArgs(
                network="default",
            )],
            metadata={
                "foo": "bar",
            },
            service_account=gcp.compute.InstanceTemplateServiceAccountArgs(
                scopes=[
                    "userinfo-email",
                    "compute-ro",
                    "storage-ro",
                ],
            ))
        default_target_pool = gcp.compute.TargetPool("default", name="my-target-pool")
        default_instance_group_manager = gcp.compute.InstanceGroupManager("default",
            name="my-igm",
            zone="us-central1-f",
            versions=[gcp.compute.InstanceGroupManagerVersionArgs(
                instance_template=default_instance_template.id,
                name="primary",
            )],
            target_pools=[default_target_pool.id],
            base_instance_name="autoscaler-sample")
        default = gcp.compute.Autoscaler("default",
            name="my-autoscaler",
            zone="us-central1-f",
            target=default_instance_group_manager.id,
            autoscaling_policy=gcp.compute.AutoscalerAutoscalingPolicyArgs(
                max_replicas=5,
                min_replicas=1,
                cooldown_period=60,
                metrics=[gcp.compute.AutoscalerAutoscalingPolicyMetricArgs(
                    name="pubsub.googleapis.com/subscription/num_undelivered_messages",
                    filter="resource.type = pubsub_subscription AND resource.label.subscription_id = our-subscription",
                    single_instance_assignment=65535,
                )],
            ))
        ```
        ### Autoscaler Basic

        ```python
        import pulumi
        import pulumi_gcp as gcp

        debian9 = gcp.compute.get_image(family="debian-11",
            project="debian-cloud")
        foobar_instance_template = gcp.compute.InstanceTemplate("foobar",
            name="my-instance-template",
            machine_type="e2-medium",
            can_ip_forward=False,
            tags=[
                "foo",
                "bar",
            ],
            disks=[gcp.compute.InstanceTemplateDiskArgs(
                source_image=debian9.id,
            )],
            network_interfaces=[gcp.compute.InstanceTemplateNetworkInterfaceArgs(
                network="default",
            )],
            metadata={
                "foo": "bar",
            },
            service_account=gcp.compute.InstanceTemplateServiceAccountArgs(
                scopes=[
                    "userinfo-email",
                    "compute-ro",
                    "storage-ro",
                ],
            ))
        foobar_target_pool = gcp.compute.TargetPool("foobar", name="my-target-pool")
        foobar_instance_group_manager = gcp.compute.InstanceGroupManager("foobar",
            name="my-igm",
            zone="us-central1-f",
            versions=[gcp.compute.InstanceGroupManagerVersionArgs(
                instance_template=foobar_instance_template.id,
                name="primary",
            )],
            target_pools=[foobar_target_pool.id],
            base_instance_name="foobar")
        foobar = gcp.compute.Autoscaler("foobar",
            name="my-autoscaler",
            zone="us-central1-f",
            target=foobar_instance_group_manager.id,
            autoscaling_policy=gcp.compute.AutoscalerAutoscalingPolicyArgs(
                max_replicas=5,
                min_replicas=1,
                cooldown_period=60,
                cpu_utilization=gcp.compute.AutoscalerAutoscalingPolicyCpuUtilizationArgs(
                    target=0.5,
                ),
            ))
        ```

        ## Import

        Autoscaler can be imported using any of these accepted formats:

        * `projects/{{project}}/zones/{{zone}}/autoscalers/{{name}}`

        * `{{project}}/{{zone}}/{{name}}`

        * `{{zone}}/{{name}}`

        * `{{name}}`

        When using the `pulumi import` command, Autoscaler can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:compute/autoscaler:Autoscaler default projects/{{project}}/zones/{{zone}}/autoscalers/{{name}}
        ```

        ```sh
        $ pulumi import gcp:compute/autoscaler:Autoscaler default {{project}}/{{zone}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:compute/autoscaler:Autoscaler default {{zone}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:compute/autoscaler:Autoscaler default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param AutoscalerArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AutoscalerArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 autoscaling_policy: Optional[pulumi.Input[pulumi.InputType['AutoscalerAutoscalingPolicyArgs']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 target: Optional[pulumi.Input[str]] = None,
                 zone: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AutoscalerArgs.__new__(AutoscalerArgs)

            if autoscaling_policy is None and not opts.urn:
                raise TypeError("Missing required property 'autoscaling_policy'")
            __props__.__dict__["autoscaling_policy"] = autoscaling_policy
            __props__.__dict__["description"] = description
            __props__.__dict__["name"] = name
            __props__.__dict__["project"] = project
            if target is None and not opts.urn:
                raise TypeError("Missing required property 'target'")
            __props__.__dict__["target"] = target
            __props__.__dict__["zone"] = zone
            __props__.__dict__["creation_timestamp"] = None
            __props__.__dict__["self_link"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="gcp:compute/autoscalar:Autoscalar")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Autoscaler, __self__).__init__(
            'gcp:compute/autoscaler:Autoscaler',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            autoscaling_policy: Optional[pulumi.Input[pulumi.InputType['AutoscalerAutoscalingPolicyArgs']]] = None,
            creation_timestamp: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None,
            self_link: Optional[pulumi.Input[str]] = None,
            target: Optional[pulumi.Input[str]] = None,
            zone: Optional[pulumi.Input[str]] = None) -> 'Autoscaler':
        """
        Get an existing Autoscaler resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['AutoscalerAutoscalingPolicyArgs']] autoscaling_policy: The configuration parameters for the autoscaling algorithm. You can
               define one or more of the policies for an autoscaler: cpuUtilization,
               customMetricUtilizations, and loadBalancingUtilization.
               If none of these are specified, the default will be to autoscale based
               on cpuUtilization to 0.6 or 60%.
               Structure is documented below.
        :param pulumi.Input[str] creation_timestamp: Creation timestamp in RFC3339 text format.
        :param pulumi.Input[str] description: An optional description of this resource.
        :param pulumi.Input[str] name: Name of the resource. The name must be 1-63 characters long and match
               the regular expression `a-z?` which means the
               first character must be a lowercase letter, and all following
               characters must be a dash, lowercase letter, or digit, except the last
               character, which cannot be a dash.
        :param pulumi.Input[str] self_link: The URI of the created resource.
        :param pulumi.Input[str] target: URL of the managed instance group that this autoscaler will scale.
        :param pulumi.Input[str] zone: URL of the zone where the instance group resides.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AutoscalerState.__new__(_AutoscalerState)

        __props__.__dict__["autoscaling_policy"] = autoscaling_policy
        __props__.__dict__["creation_timestamp"] = creation_timestamp
        __props__.__dict__["description"] = description
        __props__.__dict__["name"] = name
        __props__.__dict__["project"] = project
        __props__.__dict__["self_link"] = self_link
        __props__.__dict__["target"] = target
        __props__.__dict__["zone"] = zone
        return Autoscaler(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="autoscalingPolicy")
    def autoscaling_policy(self) -> pulumi.Output['outputs.AutoscalerAutoscalingPolicy']:
        """
        The configuration parameters for the autoscaling algorithm. You can
        define one or more of the policies for an autoscaler: cpuUtilization,
        customMetricUtilizations, and loadBalancingUtilization.
        If none of these are specified, the default will be to autoscale based
        on cpuUtilization to 0.6 or 60%.
        Structure is documented below.
        """
        return pulumi.get(self, "autoscaling_policy")

    @property
    @pulumi.getter(name="creationTimestamp")
    def creation_timestamp(self) -> pulumi.Output[str]:
        """
        Creation timestamp in RFC3339 text format.
        """
        return pulumi.get(self, "creation_timestamp")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        An optional description of this resource.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the resource. The name must be 1-63 characters long and match
        the regular expression `a-z?` which means the
        first character must be a lowercase letter, and all following
        characters must be a dash, lowercase letter, or digit, except the last
        character, which cannot be a dash.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        return pulumi.get(self, "project")

    @property
    @pulumi.getter(name="selfLink")
    def self_link(self) -> pulumi.Output[str]:
        """
        The URI of the created resource.
        """
        return pulumi.get(self, "self_link")

    @property
    @pulumi.getter
    def target(self) -> pulumi.Output[str]:
        """
        URL of the managed instance group that this autoscaler will scale.
        """
        return pulumi.get(self, "target")

    @property
    @pulumi.getter
    def zone(self) -> pulumi.Output[str]:
        """
        URL of the zone where the instance group resides.
        """
        return pulumi.get(self, "zone")

