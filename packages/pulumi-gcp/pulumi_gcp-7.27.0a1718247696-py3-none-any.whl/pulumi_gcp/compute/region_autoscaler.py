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

__all__ = ['RegionAutoscalerArgs', 'RegionAutoscaler']

@pulumi.input_type
class RegionAutoscalerArgs:
    def __init__(__self__, *,
                 autoscaling_policy: pulumi.Input['RegionAutoscalerAutoscalingPolicyArgs'],
                 target: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a RegionAutoscaler resource.
        :param pulumi.Input['RegionAutoscalerAutoscalingPolicyArgs'] autoscaling_policy: The configuration parameters for the autoscaling algorithm. You can
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
        :param pulumi.Input[str] region: URL of the region where the instance group resides.
        """
        pulumi.set(__self__, "autoscaling_policy", autoscaling_policy)
        pulumi.set(__self__, "target", target)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if region is not None:
            pulumi.set(__self__, "region", region)

    @property
    @pulumi.getter(name="autoscalingPolicy")
    def autoscaling_policy(self) -> pulumi.Input['RegionAutoscalerAutoscalingPolicyArgs']:
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
    def autoscaling_policy(self, value: pulumi.Input['RegionAutoscalerAutoscalingPolicyArgs']):
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
    def region(self) -> Optional[pulumi.Input[str]]:
        """
        URL of the region where the instance group resides.
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "region", value)


@pulumi.input_type
class _RegionAutoscalerState:
    def __init__(__self__, *,
                 autoscaling_policy: Optional[pulumi.Input['RegionAutoscalerAutoscalingPolicyArgs']] = None,
                 creation_timestamp: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 self_link: Optional[pulumi.Input[str]] = None,
                 target: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering RegionAutoscaler resources.
        :param pulumi.Input['RegionAutoscalerAutoscalingPolicyArgs'] autoscaling_policy: The configuration parameters for the autoscaling algorithm. You can
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
        :param pulumi.Input[str] region: URL of the region where the instance group resides.
        :param pulumi.Input[str] self_link: The URI of the created resource.
        :param pulumi.Input[str] target: URL of the managed instance group that this autoscaler will scale.
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
        if region is not None:
            pulumi.set(__self__, "region", region)
        if self_link is not None:
            pulumi.set(__self__, "self_link", self_link)
        if target is not None:
            pulumi.set(__self__, "target", target)

    @property
    @pulumi.getter(name="autoscalingPolicy")
    def autoscaling_policy(self) -> Optional[pulumi.Input['RegionAutoscalerAutoscalingPolicyArgs']]:
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
    def autoscaling_policy(self, value: Optional[pulumi.Input['RegionAutoscalerAutoscalingPolicyArgs']]):
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
    @pulumi.getter
    def region(self) -> Optional[pulumi.Input[str]]:
        """
        URL of the region where the instance group resides.
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


class RegionAutoscaler(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 autoscaling_policy: Optional[pulumi.Input[pulumi.InputType['RegionAutoscalerAutoscalingPolicyArgs']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 target: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Represents an Autoscaler resource.

        Autoscalers allow you to automatically scale virtual machine instances in
        managed instance groups according to an autoscaling policy that you
        define.

        To get more information about RegionAutoscaler, see:

        * [API documentation](https://cloud.google.com/compute/docs/reference/rest/v1/regionAutoscalers)
        * How-to Guides
            * [Autoscaling Groups of Instances](https://cloud.google.com/compute/docs/autoscaler/)

        ## Example Usage

        ### Region Autoscaler Basic

        ```python
        import pulumi
        import pulumi_gcp as gcp

        foobar_instance_template = gcp.compute.InstanceTemplate("foobar",
            name="my-instance-template",
            machine_type="e2-standard-4",
            disks=[gcp.compute.InstanceTemplateDiskArgs(
                source_image="debian-cloud/debian-11",
                disk_size_gb=250,
            )],
            network_interfaces=[gcp.compute.InstanceTemplateNetworkInterfaceArgs(
                network="default",
                access_configs=[gcp.compute.InstanceTemplateNetworkInterfaceAccessConfigArgs(
                    network_tier="PREMIUM",
                )],
            )],
            service_account=gcp.compute.InstanceTemplateServiceAccountArgs(
                scopes=[
                    "https://www.googleapis.com/auth/devstorage.read_only",
                    "https://www.googleapis.com/auth/logging.write",
                    "https://www.googleapis.com/auth/monitoring.write",
                    "https://www.googleapis.com/auth/pubsub",
                    "https://www.googleapis.com/auth/service.management.readonly",
                    "https://www.googleapis.com/auth/servicecontrol",
                    "https://www.googleapis.com/auth/trace.append",
                ],
            ))
        foobar_target_pool = gcp.compute.TargetPool("foobar", name="my-target-pool")
        foobar_region_instance_group_manager = gcp.compute.RegionInstanceGroupManager("foobar",
            name="my-region-igm",
            region="us-central1",
            versions=[gcp.compute.RegionInstanceGroupManagerVersionArgs(
                instance_template=foobar_instance_template.id,
                name="primary",
            )],
            target_pools=[foobar_target_pool.id],
            base_instance_name="foobar")
        foobar = gcp.compute.RegionAutoscaler("foobar",
            name="my-region-autoscaler",
            region="us-central1",
            target=foobar_region_instance_group_manager.id,
            autoscaling_policy=gcp.compute.RegionAutoscalerAutoscalingPolicyArgs(
                max_replicas=5,
                min_replicas=1,
                cooldown_period=60,
                cpu_utilization=gcp.compute.RegionAutoscalerAutoscalingPolicyCpuUtilizationArgs(
                    target=0.5,
                ),
            ))
        debian9 = gcp.compute.get_image(family="debian-11",
            project="debian-cloud")
        ```

        ## Import

        RegionAutoscaler can be imported using any of these accepted formats:

        * `projects/{{project}}/regions/{{region}}/autoscalers/{{name}}`

        * `{{project}}/{{region}}/{{name}}`

        * `{{region}}/{{name}}`

        * `{{name}}`

        When using the `pulumi import` command, RegionAutoscaler can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:compute/regionAutoscaler:RegionAutoscaler default projects/{{project}}/regions/{{region}}/autoscalers/{{name}}
        ```

        ```sh
        $ pulumi import gcp:compute/regionAutoscaler:RegionAutoscaler default {{project}}/{{region}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:compute/regionAutoscaler:RegionAutoscaler default {{region}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:compute/regionAutoscaler:RegionAutoscaler default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['RegionAutoscalerAutoscalingPolicyArgs']] autoscaling_policy: The configuration parameters for the autoscaling algorithm. You can
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
        :param pulumi.Input[str] region: URL of the region where the instance group resides.
        :param pulumi.Input[str] target: URL of the managed instance group that this autoscaler will scale.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: RegionAutoscalerArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Represents an Autoscaler resource.

        Autoscalers allow you to automatically scale virtual machine instances in
        managed instance groups according to an autoscaling policy that you
        define.

        To get more information about RegionAutoscaler, see:

        * [API documentation](https://cloud.google.com/compute/docs/reference/rest/v1/regionAutoscalers)
        * How-to Guides
            * [Autoscaling Groups of Instances](https://cloud.google.com/compute/docs/autoscaler/)

        ## Example Usage

        ### Region Autoscaler Basic

        ```python
        import pulumi
        import pulumi_gcp as gcp

        foobar_instance_template = gcp.compute.InstanceTemplate("foobar",
            name="my-instance-template",
            machine_type="e2-standard-4",
            disks=[gcp.compute.InstanceTemplateDiskArgs(
                source_image="debian-cloud/debian-11",
                disk_size_gb=250,
            )],
            network_interfaces=[gcp.compute.InstanceTemplateNetworkInterfaceArgs(
                network="default",
                access_configs=[gcp.compute.InstanceTemplateNetworkInterfaceAccessConfigArgs(
                    network_tier="PREMIUM",
                )],
            )],
            service_account=gcp.compute.InstanceTemplateServiceAccountArgs(
                scopes=[
                    "https://www.googleapis.com/auth/devstorage.read_only",
                    "https://www.googleapis.com/auth/logging.write",
                    "https://www.googleapis.com/auth/monitoring.write",
                    "https://www.googleapis.com/auth/pubsub",
                    "https://www.googleapis.com/auth/service.management.readonly",
                    "https://www.googleapis.com/auth/servicecontrol",
                    "https://www.googleapis.com/auth/trace.append",
                ],
            ))
        foobar_target_pool = gcp.compute.TargetPool("foobar", name="my-target-pool")
        foobar_region_instance_group_manager = gcp.compute.RegionInstanceGroupManager("foobar",
            name="my-region-igm",
            region="us-central1",
            versions=[gcp.compute.RegionInstanceGroupManagerVersionArgs(
                instance_template=foobar_instance_template.id,
                name="primary",
            )],
            target_pools=[foobar_target_pool.id],
            base_instance_name="foobar")
        foobar = gcp.compute.RegionAutoscaler("foobar",
            name="my-region-autoscaler",
            region="us-central1",
            target=foobar_region_instance_group_manager.id,
            autoscaling_policy=gcp.compute.RegionAutoscalerAutoscalingPolicyArgs(
                max_replicas=5,
                min_replicas=1,
                cooldown_period=60,
                cpu_utilization=gcp.compute.RegionAutoscalerAutoscalingPolicyCpuUtilizationArgs(
                    target=0.5,
                ),
            ))
        debian9 = gcp.compute.get_image(family="debian-11",
            project="debian-cloud")
        ```

        ## Import

        RegionAutoscaler can be imported using any of these accepted formats:

        * `projects/{{project}}/regions/{{region}}/autoscalers/{{name}}`

        * `{{project}}/{{region}}/{{name}}`

        * `{{region}}/{{name}}`

        * `{{name}}`

        When using the `pulumi import` command, RegionAutoscaler can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:compute/regionAutoscaler:RegionAutoscaler default projects/{{project}}/regions/{{region}}/autoscalers/{{name}}
        ```

        ```sh
        $ pulumi import gcp:compute/regionAutoscaler:RegionAutoscaler default {{project}}/{{region}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:compute/regionAutoscaler:RegionAutoscaler default {{region}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:compute/regionAutoscaler:RegionAutoscaler default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param RegionAutoscalerArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RegionAutoscalerArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 autoscaling_policy: Optional[pulumi.Input[pulumi.InputType['RegionAutoscalerAutoscalingPolicyArgs']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 target: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = RegionAutoscalerArgs.__new__(RegionAutoscalerArgs)

            if autoscaling_policy is None and not opts.urn:
                raise TypeError("Missing required property 'autoscaling_policy'")
            __props__.__dict__["autoscaling_policy"] = autoscaling_policy
            __props__.__dict__["description"] = description
            __props__.__dict__["name"] = name
            __props__.__dict__["project"] = project
            __props__.__dict__["region"] = region
            if target is None and not opts.urn:
                raise TypeError("Missing required property 'target'")
            __props__.__dict__["target"] = target
            __props__.__dict__["creation_timestamp"] = None
            __props__.__dict__["self_link"] = None
        super(RegionAutoscaler, __self__).__init__(
            'gcp:compute/regionAutoscaler:RegionAutoscaler',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            autoscaling_policy: Optional[pulumi.Input[pulumi.InputType['RegionAutoscalerAutoscalingPolicyArgs']]] = None,
            creation_timestamp: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None,
            region: Optional[pulumi.Input[str]] = None,
            self_link: Optional[pulumi.Input[str]] = None,
            target: Optional[pulumi.Input[str]] = None) -> 'RegionAutoscaler':
        """
        Get an existing RegionAutoscaler resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['RegionAutoscalerAutoscalingPolicyArgs']] autoscaling_policy: The configuration parameters for the autoscaling algorithm. You can
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
        :param pulumi.Input[str] region: URL of the region where the instance group resides.
        :param pulumi.Input[str] self_link: The URI of the created resource.
        :param pulumi.Input[str] target: URL of the managed instance group that this autoscaler will scale.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _RegionAutoscalerState.__new__(_RegionAutoscalerState)

        __props__.__dict__["autoscaling_policy"] = autoscaling_policy
        __props__.__dict__["creation_timestamp"] = creation_timestamp
        __props__.__dict__["description"] = description
        __props__.__dict__["name"] = name
        __props__.__dict__["project"] = project
        __props__.__dict__["region"] = region
        __props__.__dict__["self_link"] = self_link
        __props__.__dict__["target"] = target
        return RegionAutoscaler(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="autoscalingPolicy")
    def autoscaling_policy(self) -> pulumi.Output['outputs.RegionAutoscalerAutoscalingPolicy']:
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
    @pulumi.getter
    def region(self) -> pulumi.Output[str]:
        """
        URL of the region where the instance group resides.
        """
        return pulumi.get(self, "region")

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

