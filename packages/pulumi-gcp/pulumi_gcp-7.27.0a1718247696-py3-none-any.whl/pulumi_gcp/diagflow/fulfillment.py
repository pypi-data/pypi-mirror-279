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

__all__ = ['FulfillmentArgs', 'Fulfillment']

@pulumi.input_type
class FulfillmentArgs:
    def __init__(__self__, *,
                 display_name: pulumi.Input[str],
                 enabled: Optional[pulumi.Input[bool]] = None,
                 features: Optional[pulumi.Input[Sequence[pulumi.Input['FulfillmentFeatureArgs']]]] = None,
                 generic_web_service: Optional[pulumi.Input['FulfillmentGenericWebServiceArgs']] = None,
                 project: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Fulfillment resource.
        :param pulumi.Input[str] display_name: The human-readable name of the fulfillment, unique within the agent.
               
               
               - - -
        :param pulumi.Input[bool] enabled: Whether fulfillment is enabled.
        :param pulumi.Input[Sequence[pulumi.Input['FulfillmentFeatureArgs']]] features: The field defines whether the fulfillment is enabled for certain features.
               Structure is documented below.
        :param pulumi.Input['FulfillmentGenericWebServiceArgs'] generic_web_service: Represents configuration for a generic web service. Dialogflow supports two mechanisms for authentications: - Basic authentication with username and password. - Authentication with additional authentication headers.
               Structure is documented below.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        """
        pulumi.set(__self__, "display_name", display_name)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if features is not None:
            pulumi.set(__self__, "features", features)
        if generic_web_service is not None:
            pulumi.set(__self__, "generic_web_service", generic_web_service)
        if project is not None:
            pulumi.set(__self__, "project", project)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Input[str]:
        """
        The human-readable name of the fulfillment, unique within the agent.


        - - -
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether fulfillment is enabled.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter
    def features(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['FulfillmentFeatureArgs']]]]:
        """
        The field defines whether the fulfillment is enabled for certain features.
        Structure is documented below.
        """
        return pulumi.get(self, "features")

    @features.setter
    def features(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['FulfillmentFeatureArgs']]]]):
        pulumi.set(self, "features", value)

    @property
    @pulumi.getter(name="genericWebService")
    def generic_web_service(self) -> Optional[pulumi.Input['FulfillmentGenericWebServiceArgs']]:
        """
        Represents configuration for a generic web service. Dialogflow supports two mechanisms for authentications: - Basic authentication with username and password. - Authentication with additional authentication headers.
        Structure is documented below.
        """
        return pulumi.get(self, "generic_web_service")

    @generic_web_service.setter
    def generic_web_service(self, value: Optional[pulumi.Input['FulfillmentGenericWebServiceArgs']]):
        pulumi.set(self, "generic_web_service", value)

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
class _FulfillmentState:
    def __init__(__self__, *,
                 display_name: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 features: Optional[pulumi.Input[Sequence[pulumi.Input['FulfillmentFeatureArgs']]]] = None,
                 generic_web_service: Optional[pulumi.Input['FulfillmentGenericWebServiceArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Fulfillment resources.
        :param pulumi.Input[str] display_name: The human-readable name of the fulfillment, unique within the agent.
               
               
               - - -
        :param pulumi.Input[bool] enabled: Whether fulfillment is enabled.
        :param pulumi.Input[Sequence[pulumi.Input['FulfillmentFeatureArgs']]] features: The field defines whether the fulfillment is enabled for certain features.
               Structure is documented below.
        :param pulumi.Input['FulfillmentGenericWebServiceArgs'] generic_web_service: Represents configuration for a generic web service. Dialogflow supports two mechanisms for authentications: - Basic authentication with username and password. - Authentication with additional authentication headers.
               Structure is documented below.
        :param pulumi.Input[str] name: The unique identifier of the fulfillment.
               Format: projects/<Project ID>/agent/fulfillment - projects/<Project ID>/locations/<Location ID>/agent/fulfillment
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        """
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if features is not None:
            pulumi.set(__self__, "features", features)
        if generic_web_service is not None:
            pulumi.set(__self__, "generic_web_service", generic_web_service)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        The human-readable name of the fulfillment, unique within the agent.


        - - -
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether fulfillment is enabled.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter
    def features(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['FulfillmentFeatureArgs']]]]:
        """
        The field defines whether the fulfillment is enabled for certain features.
        Structure is documented below.
        """
        return pulumi.get(self, "features")

    @features.setter
    def features(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['FulfillmentFeatureArgs']]]]):
        pulumi.set(self, "features", value)

    @property
    @pulumi.getter(name="genericWebService")
    def generic_web_service(self) -> Optional[pulumi.Input['FulfillmentGenericWebServiceArgs']]:
        """
        Represents configuration for a generic web service. Dialogflow supports two mechanisms for authentications: - Basic authentication with username and password. - Authentication with additional authentication headers.
        Structure is documented below.
        """
        return pulumi.get(self, "generic_web_service")

    @generic_web_service.setter
    def generic_web_service(self, value: Optional[pulumi.Input['FulfillmentGenericWebServiceArgs']]):
        pulumi.set(self, "generic_web_service", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The unique identifier of the fulfillment.
        Format: projects/<Project ID>/agent/fulfillment - projects/<Project ID>/locations/<Location ID>/agent/fulfillment
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


class Fulfillment(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 features: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['FulfillmentFeatureArgs']]]]] = None,
                 generic_web_service: Optional[pulumi.Input[pulumi.InputType['FulfillmentGenericWebServiceArgs']]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        By default, your agent responds to a matched intent with a static response. If you're using one of the integration options, you can provide a more dynamic response by using fulfillment. When you enable fulfillment for an intent, Dialogflow responds to that intent by calling a service that you define. For example, if an end-user wants to schedule a haircut on Friday, your service can check your database and respond to the end-user with availability information for Friday.

        To get more information about Fulfillment, see:

        * [API documentation](https://cloud.google.com/dialogflow/es/docs/reference/rest/v2/projects.agent/getFulfillment)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/dialogflow/es/docs/fulfillment-overview)

        ## Example Usage

        ### Dialogflow Fulfillment Basic

        ```python
        import pulumi
        import pulumi_gcp as gcp

        basic_agent = gcp.diagflow.Agent("basic_agent",
            display_name="example_agent",
            default_language_code="en",
            time_zone="America/New_York")
        basic_fulfillment = gcp.diagflow.Fulfillment("basic_fulfillment",
            display_name="basic-fulfillment",
            enabled=True,
            generic_web_service=gcp.diagflow.FulfillmentGenericWebServiceArgs(
                uri="https://google.com",
                username="admin",
                password="password",
                request_headers={
                    "name": "wrench",
                },
            ),
            opts=pulumi.ResourceOptions(depends_on=[basic_agent]))
        ```

        ## Import

        Fulfillment can be imported using any of these accepted formats:

        * `{{name}}`

        When using the `pulumi import` command, Fulfillment can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:diagflow/fulfillment:Fulfillment default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] display_name: The human-readable name of the fulfillment, unique within the agent.
               
               
               - - -
        :param pulumi.Input[bool] enabled: Whether fulfillment is enabled.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['FulfillmentFeatureArgs']]]] features: The field defines whether the fulfillment is enabled for certain features.
               Structure is documented below.
        :param pulumi.Input[pulumi.InputType['FulfillmentGenericWebServiceArgs']] generic_web_service: Represents configuration for a generic web service. Dialogflow supports two mechanisms for authentications: - Basic authentication with username and password. - Authentication with additional authentication headers.
               Structure is documented below.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: FulfillmentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        By default, your agent responds to a matched intent with a static response. If you're using one of the integration options, you can provide a more dynamic response by using fulfillment. When you enable fulfillment for an intent, Dialogflow responds to that intent by calling a service that you define. For example, if an end-user wants to schedule a haircut on Friday, your service can check your database and respond to the end-user with availability information for Friday.

        To get more information about Fulfillment, see:

        * [API documentation](https://cloud.google.com/dialogflow/es/docs/reference/rest/v2/projects.agent/getFulfillment)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/dialogflow/es/docs/fulfillment-overview)

        ## Example Usage

        ### Dialogflow Fulfillment Basic

        ```python
        import pulumi
        import pulumi_gcp as gcp

        basic_agent = gcp.diagflow.Agent("basic_agent",
            display_name="example_agent",
            default_language_code="en",
            time_zone="America/New_York")
        basic_fulfillment = gcp.diagflow.Fulfillment("basic_fulfillment",
            display_name="basic-fulfillment",
            enabled=True,
            generic_web_service=gcp.diagflow.FulfillmentGenericWebServiceArgs(
                uri="https://google.com",
                username="admin",
                password="password",
                request_headers={
                    "name": "wrench",
                },
            ),
            opts=pulumi.ResourceOptions(depends_on=[basic_agent]))
        ```

        ## Import

        Fulfillment can be imported using any of these accepted formats:

        * `{{name}}`

        When using the `pulumi import` command, Fulfillment can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:diagflow/fulfillment:Fulfillment default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param FulfillmentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(FulfillmentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 features: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['FulfillmentFeatureArgs']]]]] = None,
                 generic_web_service: Optional[pulumi.Input[pulumi.InputType['FulfillmentGenericWebServiceArgs']]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = FulfillmentArgs.__new__(FulfillmentArgs)

            if display_name is None and not opts.urn:
                raise TypeError("Missing required property 'display_name'")
            __props__.__dict__["display_name"] = display_name
            __props__.__dict__["enabled"] = enabled
            __props__.__dict__["features"] = features
            __props__.__dict__["generic_web_service"] = generic_web_service
            __props__.__dict__["project"] = project
            __props__.__dict__["name"] = None
        super(Fulfillment, __self__).__init__(
            'gcp:diagflow/fulfillment:Fulfillment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            display_name: Optional[pulumi.Input[str]] = None,
            enabled: Optional[pulumi.Input[bool]] = None,
            features: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['FulfillmentFeatureArgs']]]]] = None,
            generic_web_service: Optional[pulumi.Input[pulumi.InputType['FulfillmentGenericWebServiceArgs']]] = None,
            name: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None) -> 'Fulfillment':
        """
        Get an existing Fulfillment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] display_name: The human-readable name of the fulfillment, unique within the agent.
               
               
               - - -
        :param pulumi.Input[bool] enabled: Whether fulfillment is enabled.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['FulfillmentFeatureArgs']]]] features: The field defines whether the fulfillment is enabled for certain features.
               Structure is documented below.
        :param pulumi.Input[pulumi.InputType['FulfillmentGenericWebServiceArgs']] generic_web_service: Represents configuration for a generic web service. Dialogflow supports two mechanisms for authentications: - Basic authentication with username and password. - Authentication with additional authentication headers.
               Structure is documented below.
        :param pulumi.Input[str] name: The unique identifier of the fulfillment.
               Format: projects/<Project ID>/agent/fulfillment - projects/<Project ID>/locations/<Location ID>/agent/fulfillment
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _FulfillmentState.__new__(_FulfillmentState)

        __props__.__dict__["display_name"] = display_name
        __props__.__dict__["enabled"] = enabled
        __props__.__dict__["features"] = features
        __props__.__dict__["generic_web_service"] = generic_web_service
        __props__.__dict__["name"] = name
        __props__.__dict__["project"] = project
        return Fulfillment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[str]:
        """
        The human-readable name of the fulfillment, unique within the agent.


        - - -
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether fulfillment is enabled.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter
    def features(self) -> pulumi.Output[Optional[Sequence['outputs.FulfillmentFeature']]]:
        """
        The field defines whether the fulfillment is enabled for certain features.
        Structure is documented below.
        """
        return pulumi.get(self, "features")

    @property
    @pulumi.getter(name="genericWebService")
    def generic_web_service(self) -> pulumi.Output[Optional['outputs.FulfillmentGenericWebService']]:
        """
        Represents configuration for a generic web service. Dialogflow supports two mechanisms for authentications: - Basic authentication with username and password. - Authentication with additional authentication headers.
        Structure is documented below.
        """
        return pulumi.get(self, "generic_web_service")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The unique identifier of the fulfillment.
        Format: projects/<Project ID>/agent/fulfillment - projects/<Project ID>/locations/<Location ID>/agent/fulfillment
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

