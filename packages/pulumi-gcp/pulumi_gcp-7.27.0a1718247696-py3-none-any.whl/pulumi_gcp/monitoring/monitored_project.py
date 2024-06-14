# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['MonitoredProjectArgs', 'MonitoredProject']

@pulumi.input_type
class MonitoredProjectArgs:
    def __init__(__self__, *,
                 metrics_scope: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a MonitoredProject resource.
        :param pulumi.Input[str] metrics_scope: Required. The resource name of the existing Metrics Scope that will monitor this project. Example: locations/global/metricsScopes/{SCOPING_PROJECT_ID_OR_NUMBER}
               
               
               - - -
        :param pulumi.Input[str] name: Immutable. The resource name of the `MonitoredProject`. On input, the resource name includes the scoping project ID and monitored project ID. On output, it contains the equivalent project numbers. Example: `locations/global/metricsScopes/{SCOPING_PROJECT_ID_OR_NUMBER}/projects/{MONITORED_PROJECT_ID_OR_NUMBER}`
        """
        pulumi.set(__self__, "metrics_scope", metrics_scope)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="metricsScope")
    def metrics_scope(self) -> pulumi.Input[str]:
        """
        Required. The resource name of the existing Metrics Scope that will monitor this project. Example: locations/global/metricsScopes/{SCOPING_PROJECT_ID_OR_NUMBER}


        - - -
        """
        return pulumi.get(self, "metrics_scope")

    @metrics_scope.setter
    def metrics_scope(self, value: pulumi.Input[str]):
        pulumi.set(self, "metrics_scope", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Immutable. The resource name of the `MonitoredProject`. On input, the resource name includes the scoping project ID and monitored project ID. On output, it contains the equivalent project numbers. Example: `locations/global/metricsScopes/{SCOPING_PROJECT_ID_OR_NUMBER}/projects/{MONITORED_PROJECT_ID_OR_NUMBER}`
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _MonitoredProjectState:
    def __init__(__self__, *,
                 create_time: Optional[pulumi.Input[str]] = None,
                 metrics_scope: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering MonitoredProject resources.
        :param pulumi.Input[str] create_time: Output only. The time when this `MonitoredProject` was created.
        :param pulumi.Input[str] metrics_scope: Required. The resource name of the existing Metrics Scope that will monitor this project. Example: locations/global/metricsScopes/{SCOPING_PROJECT_ID_OR_NUMBER}
               
               
               - - -
        :param pulumi.Input[str] name: Immutable. The resource name of the `MonitoredProject`. On input, the resource name includes the scoping project ID and monitored project ID. On output, it contains the equivalent project numbers. Example: `locations/global/metricsScopes/{SCOPING_PROJECT_ID_OR_NUMBER}/projects/{MONITORED_PROJECT_ID_OR_NUMBER}`
        """
        if create_time is not None:
            pulumi.set(__self__, "create_time", create_time)
        if metrics_scope is not None:
            pulumi.set(__self__, "metrics_scope", metrics_scope)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> Optional[pulumi.Input[str]]:
        """
        Output only. The time when this `MonitoredProject` was created.
        """
        return pulumi.get(self, "create_time")

    @create_time.setter
    def create_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "create_time", value)

    @property
    @pulumi.getter(name="metricsScope")
    def metrics_scope(self) -> Optional[pulumi.Input[str]]:
        """
        Required. The resource name of the existing Metrics Scope that will monitor this project. Example: locations/global/metricsScopes/{SCOPING_PROJECT_ID_OR_NUMBER}


        - - -
        """
        return pulumi.get(self, "metrics_scope")

    @metrics_scope.setter
    def metrics_scope(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "metrics_scope", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Immutable. The resource name of the `MonitoredProject`. On input, the resource name includes the scoping project ID and monitored project ID. On output, it contains the equivalent project numbers. Example: `locations/global/metricsScopes/{SCOPING_PROJECT_ID_OR_NUMBER}/projects/{MONITORED_PROJECT_ID_OR_NUMBER}`
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


class MonitoredProject(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 metrics_scope: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        A [project being monitored](https://cloud.google.com/monitoring/settings/multiple-projects#create-multi) by a Metrics Scope.

        To get more information about MonitoredProject, see:

        * [API documentation](https://cloud.google.com/monitoring/api/ref_v3/rest/v1/locations.global.metricsScopes.projects)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/monitoring/settings/manage-api)

        ## Example Usage

        ### Monitoring Monitored Project Basic

        ```python
        import pulumi
        import pulumi_gcp as gcp

        basic = gcp.organizations.Project("basic",
            project_id="m-id",
            name="m-id-display",
            org_id="123456789")
        primary = gcp.monitoring.MonitoredProject("primary",
            metrics_scope="my-project-name",
            name=basic.project_id)
        ```

        ## Import

        MonitoredProject can be imported using any of these accepted formats:

        * `v1/locations/global/metricsScopes/{{name}}`

        * `{{name}}`

        When using the `pulumi import` command, MonitoredProject can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:monitoring/monitoredProject:MonitoredProject default v1/locations/global/metricsScopes/{{name}}
        ```

        ```sh
        $ pulumi import gcp:monitoring/monitoredProject:MonitoredProject default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] metrics_scope: Required. The resource name of the existing Metrics Scope that will monitor this project. Example: locations/global/metricsScopes/{SCOPING_PROJECT_ID_OR_NUMBER}
               
               
               - - -
        :param pulumi.Input[str] name: Immutable. The resource name of the `MonitoredProject`. On input, the resource name includes the scoping project ID and monitored project ID. On output, it contains the equivalent project numbers. Example: `locations/global/metricsScopes/{SCOPING_PROJECT_ID_OR_NUMBER}/projects/{MONITORED_PROJECT_ID_OR_NUMBER}`
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: MonitoredProjectArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A [project being monitored](https://cloud.google.com/monitoring/settings/multiple-projects#create-multi) by a Metrics Scope.

        To get more information about MonitoredProject, see:

        * [API documentation](https://cloud.google.com/monitoring/api/ref_v3/rest/v1/locations.global.metricsScopes.projects)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/monitoring/settings/manage-api)

        ## Example Usage

        ### Monitoring Monitored Project Basic

        ```python
        import pulumi
        import pulumi_gcp as gcp

        basic = gcp.organizations.Project("basic",
            project_id="m-id",
            name="m-id-display",
            org_id="123456789")
        primary = gcp.monitoring.MonitoredProject("primary",
            metrics_scope="my-project-name",
            name=basic.project_id)
        ```

        ## Import

        MonitoredProject can be imported using any of these accepted formats:

        * `v1/locations/global/metricsScopes/{{name}}`

        * `{{name}}`

        When using the `pulumi import` command, MonitoredProject can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:monitoring/monitoredProject:MonitoredProject default v1/locations/global/metricsScopes/{{name}}
        ```

        ```sh
        $ pulumi import gcp:monitoring/monitoredProject:MonitoredProject default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param MonitoredProjectArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(MonitoredProjectArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 metrics_scope: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = MonitoredProjectArgs.__new__(MonitoredProjectArgs)

            if metrics_scope is None and not opts.urn:
                raise TypeError("Missing required property 'metrics_scope'")
            __props__.__dict__["metrics_scope"] = metrics_scope
            __props__.__dict__["name"] = name
            __props__.__dict__["create_time"] = None
        super(MonitoredProject, __self__).__init__(
            'gcp:monitoring/monitoredProject:MonitoredProject',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            create_time: Optional[pulumi.Input[str]] = None,
            metrics_scope: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None) -> 'MonitoredProject':
        """
        Get an existing MonitoredProject resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] create_time: Output only. The time when this `MonitoredProject` was created.
        :param pulumi.Input[str] metrics_scope: Required. The resource name of the existing Metrics Scope that will monitor this project. Example: locations/global/metricsScopes/{SCOPING_PROJECT_ID_OR_NUMBER}
               
               
               - - -
        :param pulumi.Input[str] name: Immutable. The resource name of the `MonitoredProject`. On input, the resource name includes the scoping project ID and monitored project ID. On output, it contains the equivalent project numbers. Example: `locations/global/metricsScopes/{SCOPING_PROJECT_ID_OR_NUMBER}/projects/{MONITORED_PROJECT_ID_OR_NUMBER}`
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _MonitoredProjectState.__new__(_MonitoredProjectState)

        __props__.__dict__["create_time"] = create_time
        __props__.__dict__["metrics_scope"] = metrics_scope
        __props__.__dict__["name"] = name
        return MonitoredProject(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> pulumi.Output[str]:
        """
        Output only. The time when this `MonitoredProject` was created.
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter(name="metricsScope")
    def metrics_scope(self) -> pulumi.Output[str]:
        """
        Required. The resource name of the existing Metrics Scope that will monitor this project. Example: locations/global/metricsScopes/{SCOPING_PROJECT_ID_OR_NUMBER}


        - - -
        """
        return pulumi.get(self, "metrics_scope")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Immutable. The resource name of the `MonitoredProject`. On input, the resource name includes the scoping project ID and monitored project ID. On output, it contains the equivalent project numbers. Example: `locations/global/metricsScopes/{SCOPING_PROJECT_ID_OR_NUMBER}/projects/{MONITORED_PROJECT_ID_OR_NUMBER}`
        """
        return pulumi.get(self, "name")

