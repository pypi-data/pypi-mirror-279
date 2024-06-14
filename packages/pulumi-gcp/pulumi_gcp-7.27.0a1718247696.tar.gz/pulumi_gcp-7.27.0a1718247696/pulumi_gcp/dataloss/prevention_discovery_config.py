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

__all__ = ['PreventionDiscoveryConfigArgs', 'PreventionDiscoveryConfig']

@pulumi.input_type
class PreventionDiscoveryConfigArgs:
    def __init__(__self__, *,
                 location: pulumi.Input[str],
                 parent: pulumi.Input[str],
                 actions: Optional[pulumi.Input[Sequence[pulumi.Input['PreventionDiscoveryConfigActionArgs']]]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 inspect_templates: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 org_config: Optional[pulumi.Input['PreventionDiscoveryConfigOrgConfigArgs']] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 targets: Optional[pulumi.Input[Sequence[pulumi.Input['PreventionDiscoveryConfigTargetArgs']]]] = None):
        """
        The set of arguments for constructing a PreventionDiscoveryConfig resource.
        :param pulumi.Input[str] location: Location to create the discovery config in.
               
               
               - - -
        :param pulumi.Input[str] parent: The parent of the discovery config in any of the following formats:
               * `projects/{{project}}/locations/{{location}}`
               * `organizations/{{organization_id}}/locations/{{location}}`
        :param pulumi.Input[Sequence[pulumi.Input['PreventionDiscoveryConfigActionArgs']]] actions: Actions to execute at the completion of scanning
               Structure is documented below.
        :param pulumi.Input[str] display_name: Display Name (max 1000 Chars)
        :param pulumi.Input[Sequence[pulumi.Input[str]]] inspect_templates: Detection logic for profile generation
        :param pulumi.Input['PreventionDiscoveryConfigOrgConfigArgs'] org_config: A nested object resource
               Structure is documented below.
        :param pulumi.Input[str] status: Required. A status for this configuration
               Possible values are: `RUNNING`, `PAUSED`.
        :param pulumi.Input[Sequence[pulumi.Input['PreventionDiscoveryConfigTargetArgs']]] targets: Target to match against for determining what to scan and how frequently
               Structure is documented below.
        """
        pulumi.set(__self__, "location", location)
        pulumi.set(__self__, "parent", parent)
        if actions is not None:
            pulumi.set(__self__, "actions", actions)
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if inspect_templates is not None:
            pulumi.set(__self__, "inspect_templates", inspect_templates)
        if org_config is not None:
            pulumi.set(__self__, "org_config", org_config)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if targets is not None:
            pulumi.set(__self__, "targets", targets)

    @property
    @pulumi.getter
    def location(self) -> pulumi.Input[str]:
        """
        Location to create the discovery config in.


        - - -
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: pulumi.Input[str]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def parent(self) -> pulumi.Input[str]:
        """
        The parent of the discovery config in any of the following formats:
        * `projects/{{project}}/locations/{{location}}`
        * `organizations/{{organization_id}}/locations/{{location}}`
        """
        return pulumi.get(self, "parent")

    @parent.setter
    def parent(self, value: pulumi.Input[str]):
        pulumi.set(self, "parent", value)

    @property
    @pulumi.getter
    def actions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['PreventionDiscoveryConfigActionArgs']]]]:
        """
        Actions to execute at the completion of scanning
        Structure is documented below.
        """
        return pulumi.get(self, "actions")

    @actions.setter
    def actions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['PreventionDiscoveryConfigActionArgs']]]]):
        pulumi.set(self, "actions", value)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        Display Name (max 1000 Chars)
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter(name="inspectTemplates")
    def inspect_templates(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Detection logic for profile generation
        """
        return pulumi.get(self, "inspect_templates")

    @inspect_templates.setter
    def inspect_templates(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "inspect_templates", value)

    @property
    @pulumi.getter(name="orgConfig")
    def org_config(self) -> Optional[pulumi.Input['PreventionDiscoveryConfigOrgConfigArgs']]:
        """
        A nested object resource
        Structure is documented below.
        """
        return pulumi.get(self, "org_config")

    @org_config.setter
    def org_config(self, value: Optional[pulumi.Input['PreventionDiscoveryConfigOrgConfigArgs']]):
        pulumi.set(self, "org_config", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        Required. A status for this configuration
        Possible values are: `RUNNING`, `PAUSED`.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter
    def targets(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['PreventionDiscoveryConfigTargetArgs']]]]:
        """
        Target to match against for determining what to scan and how frequently
        Structure is documented below.
        """
        return pulumi.get(self, "targets")

    @targets.setter
    def targets(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['PreventionDiscoveryConfigTargetArgs']]]]):
        pulumi.set(self, "targets", value)


@pulumi.input_type
class _PreventionDiscoveryConfigState:
    def __init__(__self__, *,
                 actions: Optional[pulumi.Input[Sequence[pulumi.Input['PreventionDiscoveryConfigActionArgs']]]] = None,
                 create_time: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 errors: Optional[pulumi.Input[Sequence[pulumi.Input['PreventionDiscoveryConfigErrorArgs']]]] = None,
                 inspect_templates: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 last_run_time: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 org_config: Optional[pulumi.Input['PreventionDiscoveryConfigOrgConfigArgs']] = None,
                 parent: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 targets: Optional[pulumi.Input[Sequence[pulumi.Input['PreventionDiscoveryConfigTargetArgs']]]] = None,
                 update_time: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering PreventionDiscoveryConfig resources.
        :param pulumi.Input[Sequence[pulumi.Input['PreventionDiscoveryConfigActionArgs']]] actions: Actions to execute at the completion of scanning
               Structure is documented below.
        :param pulumi.Input[str] create_time: Output only. The creation timestamp of a DiscoveryConfig.
        :param pulumi.Input[str] display_name: Display Name (max 1000 Chars)
        :param pulumi.Input[Sequence[pulumi.Input['PreventionDiscoveryConfigErrorArgs']]] errors: Output only. A stream of errors encountered when the config was activated. Repeated errors may result in the config automatically being paused. Output only field. Will return the last 100 errors. Whenever the config is modified this list will be cleared.
               Structure is documented below.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] inspect_templates: Detection logic for profile generation
        :param pulumi.Input[str] last_run_time: Output only. The timestamp of the last time this config was executed
        :param pulumi.Input[str] location: Location to create the discovery config in.
               
               
               - - -
        :param pulumi.Input[str] name: Unique resource name for the DiscoveryConfig, assigned by the service when the DiscoveryConfig is created.
        :param pulumi.Input['PreventionDiscoveryConfigOrgConfigArgs'] org_config: A nested object resource
               Structure is documented below.
        :param pulumi.Input[str] parent: The parent of the discovery config in any of the following formats:
               * `projects/{{project}}/locations/{{location}}`
               * `organizations/{{organization_id}}/locations/{{location}}`
        :param pulumi.Input[str] status: Required. A status for this configuration
               Possible values are: `RUNNING`, `PAUSED`.
        :param pulumi.Input[Sequence[pulumi.Input['PreventionDiscoveryConfigTargetArgs']]] targets: Target to match against for determining what to scan and how frequently
               Structure is documented below.
        :param pulumi.Input[str] update_time: Output only. The last update timestamp of a DiscoveryConfig.
        """
        if actions is not None:
            pulumi.set(__self__, "actions", actions)
        if create_time is not None:
            pulumi.set(__self__, "create_time", create_time)
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if errors is not None:
            pulumi.set(__self__, "errors", errors)
        if inspect_templates is not None:
            pulumi.set(__self__, "inspect_templates", inspect_templates)
        if last_run_time is not None:
            pulumi.set(__self__, "last_run_time", last_run_time)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if org_config is not None:
            pulumi.set(__self__, "org_config", org_config)
        if parent is not None:
            pulumi.set(__self__, "parent", parent)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if targets is not None:
            pulumi.set(__self__, "targets", targets)
        if update_time is not None:
            pulumi.set(__self__, "update_time", update_time)

    @property
    @pulumi.getter
    def actions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['PreventionDiscoveryConfigActionArgs']]]]:
        """
        Actions to execute at the completion of scanning
        Structure is documented below.
        """
        return pulumi.get(self, "actions")

    @actions.setter
    def actions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['PreventionDiscoveryConfigActionArgs']]]]):
        pulumi.set(self, "actions", value)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> Optional[pulumi.Input[str]]:
        """
        Output only. The creation timestamp of a DiscoveryConfig.
        """
        return pulumi.get(self, "create_time")

    @create_time.setter
    def create_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "create_time", value)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        Display Name (max 1000 Chars)
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter
    def errors(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['PreventionDiscoveryConfigErrorArgs']]]]:
        """
        Output only. A stream of errors encountered when the config was activated. Repeated errors may result in the config automatically being paused. Output only field. Will return the last 100 errors. Whenever the config is modified this list will be cleared.
        Structure is documented below.
        """
        return pulumi.get(self, "errors")

    @errors.setter
    def errors(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['PreventionDiscoveryConfigErrorArgs']]]]):
        pulumi.set(self, "errors", value)

    @property
    @pulumi.getter(name="inspectTemplates")
    def inspect_templates(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Detection logic for profile generation
        """
        return pulumi.get(self, "inspect_templates")

    @inspect_templates.setter
    def inspect_templates(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "inspect_templates", value)

    @property
    @pulumi.getter(name="lastRunTime")
    def last_run_time(self) -> Optional[pulumi.Input[str]]:
        """
        Output only. The timestamp of the last time this config was executed
        """
        return pulumi.get(self, "last_run_time")

    @last_run_time.setter
    def last_run_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "last_run_time", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Location to create the discovery config in.


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
        Unique resource name for the DiscoveryConfig, assigned by the service when the DiscoveryConfig is created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="orgConfig")
    def org_config(self) -> Optional[pulumi.Input['PreventionDiscoveryConfigOrgConfigArgs']]:
        """
        A nested object resource
        Structure is documented below.
        """
        return pulumi.get(self, "org_config")

    @org_config.setter
    def org_config(self, value: Optional[pulumi.Input['PreventionDiscoveryConfigOrgConfigArgs']]):
        pulumi.set(self, "org_config", value)

    @property
    @pulumi.getter
    def parent(self) -> Optional[pulumi.Input[str]]:
        """
        The parent of the discovery config in any of the following formats:
        * `projects/{{project}}/locations/{{location}}`
        * `organizations/{{organization_id}}/locations/{{location}}`
        """
        return pulumi.get(self, "parent")

    @parent.setter
    def parent(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "parent", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        Required. A status for this configuration
        Possible values are: `RUNNING`, `PAUSED`.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter
    def targets(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['PreventionDiscoveryConfigTargetArgs']]]]:
        """
        Target to match against for determining what to scan and how frequently
        Structure is documented below.
        """
        return pulumi.get(self, "targets")

    @targets.setter
    def targets(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['PreventionDiscoveryConfigTargetArgs']]]]):
        pulumi.set(self, "targets", value)

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> Optional[pulumi.Input[str]]:
        """
        Output only. The last update timestamp of a DiscoveryConfig.
        """
        return pulumi.get(self, "update_time")

    @update_time.setter
    def update_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "update_time", value)


class PreventionDiscoveryConfig(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 actions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PreventionDiscoveryConfigActionArgs']]]]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 inspect_templates: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 org_config: Optional[pulumi.Input[pulumi.InputType['PreventionDiscoveryConfigOrgConfigArgs']]] = None,
                 parent: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 targets: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PreventionDiscoveryConfigTargetArgs']]]]] = None,
                 __props__=None):
        """
        Configuration for discovery to scan resources for profile generation. Only one discovery configuration may exist per organization, folder, or project.

        To get more information about DiscoveryConfig, see:

        * [API documentation](https://cloud.google.com/dlp/docs/reference/rest/v2/projects.locations.discoveryConfigs)
        * How-to Guides
            * [Schedule inspection scan](https://cloud.google.com/dlp/docs/schedule-inspection-scan)

        ## Example Usage

        ## Import

        DiscoveryConfig can be imported using any of these accepted formats:

        * `{{parent}}/discoveryConfigs/{{name}}`

        * `{{parent}}/{{name}}`

        When using the `pulumi import` command, DiscoveryConfig can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:dataloss/preventionDiscoveryConfig:PreventionDiscoveryConfig default {{parent}}/discoveryConfigs/{{name}}
        ```

        ```sh
        $ pulumi import gcp:dataloss/preventionDiscoveryConfig:PreventionDiscoveryConfig default {{parent}}/{{name}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PreventionDiscoveryConfigActionArgs']]]] actions: Actions to execute at the completion of scanning
               Structure is documented below.
        :param pulumi.Input[str] display_name: Display Name (max 1000 Chars)
        :param pulumi.Input[Sequence[pulumi.Input[str]]] inspect_templates: Detection logic for profile generation
        :param pulumi.Input[str] location: Location to create the discovery config in.
               
               
               - - -
        :param pulumi.Input[pulumi.InputType['PreventionDiscoveryConfigOrgConfigArgs']] org_config: A nested object resource
               Structure is documented below.
        :param pulumi.Input[str] parent: The parent of the discovery config in any of the following formats:
               * `projects/{{project}}/locations/{{location}}`
               * `organizations/{{organization_id}}/locations/{{location}}`
        :param pulumi.Input[str] status: Required. A status for this configuration
               Possible values are: `RUNNING`, `PAUSED`.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PreventionDiscoveryConfigTargetArgs']]]] targets: Target to match against for determining what to scan and how frequently
               Structure is documented below.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: PreventionDiscoveryConfigArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Configuration for discovery to scan resources for profile generation. Only one discovery configuration may exist per organization, folder, or project.

        To get more information about DiscoveryConfig, see:

        * [API documentation](https://cloud.google.com/dlp/docs/reference/rest/v2/projects.locations.discoveryConfigs)
        * How-to Guides
            * [Schedule inspection scan](https://cloud.google.com/dlp/docs/schedule-inspection-scan)

        ## Example Usage

        ## Import

        DiscoveryConfig can be imported using any of these accepted formats:

        * `{{parent}}/discoveryConfigs/{{name}}`

        * `{{parent}}/{{name}}`

        When using the `pulumi import` command, DiscoveryConfig can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:dataloss/preventionDiscoveryConfig:PreventionDiscoveryConfig default {{parent}}/discoveryConfigs/{{name}}
        ```

        ```sh
        $ pulumi import gcp:dataloss/preventionDiscoveryConfig:PreventionDiscoveryConfig default {{parent}}/{{name}}
        ```

        :param str resource_name: The name of the resource.
        :param PreventionDiscoveryConfigArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PreventionDiscoveryConfigArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 actions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PreventionDiscoveryConfigActionArgs']]]]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 inspect_templates: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 org_config: Optional[pulumi.Input[pulumi.InputType['PreventionDiscoveryConfigOrgConfigArgs']]] = None,
                 parent: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 targets: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PreventionDiscoveryConfigTargetArgs']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PreventionDiscoveryConfigArgs.__new__(PreventionDiscoveryConfigArgs)

            __props__.__dict__["actions"] = actions
            __props__.__dict__["display_name"] = display_name
            __props__.__dict__["inspect_templates"] = inspect_templates
            if location is None and not opts.urn:
                raise TypeError("Missing required property 'location'")
            __props__.__dict__["location"] = location
            __props__.__dict__["org_config"] = org_config
            if parent is None and not opts.urn:
                raise TypeError("Missing required property 'parent'")
            __props__.__dict__["parent"] = parent
            __props__.__dict__["status"] = status
            __props__.__dict__["targets"] = targets
            __props__.__dict__["create_time"] = None
            __props__.__dict__["errors"] = None
            __props__.__dict__["last_run_time"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["update_time"] = None
        super(PreventionDiscoveryConfig, __self__).__init__(
            'gcp:dataloss/preventionDiscoveryConfig:PreventionDiscoveryConfig',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            actions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PreventionDiscoveryConfigActionArgs']]]]] = None,
            create_time: Optional[pulumi.Input[str]] = None,
            display_name: Optional[pulumi.Input[str]] = None,
            errors: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PreventionDiscoveryConfigErrorArgs']]]]] = None,
            inspect_templates: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            last_run_time: Optional[pulumi.Input[str]] = None,
            location: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            org_config: Optional[pulumi.Input[pulumi.InputType['PreventionDiscoveryConfigOrgConfigArgs']]] = None,
            parent: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[str]] = None,
            targets: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PreventionDiscoveryConfigTargetArgs']]]]] = None,
            update_time: Optional[pulumi.Input[str]] = None) -> 'PreventionDiscoveryConfig':
        """
        Get an existing PreventionDiscoveryConfig resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PreventionDiscoveryConfigActionArgs']]]] actions: Actions to execute at the completion of scanning
               Structure is documented below.
        :param pulumi.Input[str] create_time: Output only. The creation timestamp of a DiscoveryConfig.
        :param pulumi.Input[str] display_name: Display Name (max 1000 Chars)
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PreventionDiscoveryConfigErrorArgs']]]] errors: Output only. A stream of errors encountered when the config was activated. Repeated errors may result in the config automatically being paused. Output only field. Will return the last 100 errors. Whenever the config is modified this list will be cleared.
               Structure is documented below.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] inspect_templates: Detection logic for profile generation
        :param pulumi.Input[str] last_run_time: Output only. The timestamp of the last time this config was executed
        :param pulumi.Input[str] location: Location to create the discovery config in.
               
               
               - - -
        :param pulumi.Input[str] name: Unique resource name for the DiscoveryConfig, assigned by the service when the DiscoveryConfig is created.
        :param pulumi.Input[pulumi.InputType['PreventionDiscoveryConfigOrgConfigArgs']] org_config: A nested object resource
               Structure is documented below.
        :param pulumi.Input[str] parent: The parent of the discovery config in any of the following formats:
               * `projects/{{project}}/locations/{{location}}`
               * `organizations/{{organization_id}}/locations/{{location}}`
        :param pulumi.Input[str] status: Required. A status for this configuration
               Possible values are: `RUNNING`, `PAUSED`.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PreventionDiscoveryConfigTargetArgs']]]] targets: Target to match against for determining what to scan and how frequently
               Structure is documented below.
        :param pulumi.Input[str] update_time: Output only. The last update timestamp of a DiscoveryConfig.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _PreventionDiscoveryConfigState.__new__(_PreventionDiscoveryConfigState)

        __props__.__dict__["actions"] = actions
        __props__.__dict__["create_time"] = create_time
        __props__.__dict__["display_name"] = display_name
        __props__.__dict__["errors"] = errors
        __props__.__dict__["inspect_templates"] = inspect_templates
        __props__.__dict__["last_run_time"] = last_run_time
        __props__.__dict__["location"] = location
        __props__.__dict__["name"] = name
        __props__.__dict__["org_config"] = org_config
        __props__.__dict__["parent"] = parent
        __props__.__dict__["status"] = status
        __props__.__dict__["targets"] = targets
        __props__.__dict__["update_time"] = update_time
        return PreventionDiscoveryConfig(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def actions(self) -> pulumi.Output[Optional[Sequence['outputs.PreventionDiscoveryConfigAction']]]:
        """
        Actions to execute at the completion of scanning
        Structure is documented below.
        """
        return pulumi.get(self, "actions")

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> pulumi.Output[str]:
        """
        Output only. The creation timestamp of a DiscoveryConfig.
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[Optional[str]]:
        """
        Display Name (max 1000 Chars)
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def errors(self) -> pulumi.Output[Sequence['outputs.PreventionDiscoveryConfigError']]:
        """
        Output only. A stream of errors encountered when the config was activated. Repeated errors may result in the config automatically being paused. Output only field. Will return the last 100 errors. Whenever the config is modified this list will be cleared.
        Structure is documented below.
        """
        return pulumi.get(self, "errors")

    @property
    @pulumi.getter(name="inspectTemplates")
    def inspect_templates(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Detection logic for profile generation
        """
        return pulumi.get(self, "inspect_templates")

    @property
    @pulumi.getter(name="lastRunTime")
    def last_run_time(self) -> pulumi.Output[str]:
        """
        Output only. The timestamp of the last time this config was executed
        """
        return pulumi.get(self, "last_run_time")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Location to create the discovery config in.


        - - -
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Unique resource name for the DiscoveryConfig, assigned by the service when the DiscoveryConfig is created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="orgConfig")
    def org_config(self) -> pulumi.Output[Optional['outputs.PreventionDiscoveryConfigOrgConfig']]:
        """
        A nested object resource
        Structure is documented below.
        """
        return pulumi.get(self, "org_config")

    @property
    @pulumi.getter
    def parent(self) -> pulumi.Output[str]:
        """
        The parent of the discovery config in any of the following formats:
        * `projects/{{project}}/locations/{{location}}`
        * `organizations/{{organization_id}}/locations/{{location}}`
        """
        return pulumi.get(self, "parent")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[Optional[str]]:
        """
        Required. A status for this configuration
        Possible values are: `RUNNING`, `PAUSED`.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def targets(self) -> pulumi.Output[Optional[Sequence['outputs.PreventionDiscoveryConfigTarget']]]:
        """
        Target to match against for determining what to scan and how frequently
        Structure is documented below.
        """
        return pulumi.get(self, "targets")

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> pulumi.Output[str]:
        """
        Output only. The last update timestamp of a DiscoveryConfig.
        """
        return pulumi.get(self, "update_time")

