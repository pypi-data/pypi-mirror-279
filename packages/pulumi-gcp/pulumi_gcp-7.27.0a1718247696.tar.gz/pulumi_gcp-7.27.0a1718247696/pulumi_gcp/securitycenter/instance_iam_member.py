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

__all__ = ['InstanceIamMemberArgs', 'InstanceIamMember']

@pulumi.input_type
class InstanceIamMemberArgs:
    def __init__(__self__, *,
                 member: pulumi.Input[str],
                 role: pulumi.Input[str],
                 condition: Optional[pulumi.Input['InstanceIamMemberConditionArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a InstanceIamMember resource.
        :param pulumi.Input[str] name: The ID of the instance or a fully qualified identifier for the instance.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: The region of the Data Fusion instance.
        """
        pulumi.set(__self__, "member", member)
        pulumi.set(__self__, "role", role)
        if condition is not None:
            pulumi.set(__self__, "condition", condition)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if region is not None:
            pulumi.set(__self__, "region", region)

    @property
    @pulumi.getter
    def member(self) -> pulumi.Input[str]:
        return pulumi.get(self, "member")

    @member.setter
    def member(self, value: pulumi.Input[str]):
        pulumi.set(self, "member", value)

    @property
    @pulumi.getter
    def role(self) -> pulumi.Input[str]:
        return pulumi.get(self, "role")

    @role.setter
    def role(self, value: pulumi.Input[str]):
        pulumi.set(self, "role", value)

    @property
    @pulumi.getter
    def condition(self) -> Optional[pulumi.Input['InstanceIamMemberConditionArgs']]:
        return pulumi.get(self, "condition")

    @condition.setter
    def condition(self, value: Optional[pulumi.Input['InstanceIamMemberConditionArgs']]):
        pulumi.set(self, "condition", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the instance or a fully qualified identifier for the instance.
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

    @property
    @pulumi.getter
    def region(self) -> Optional[pulumi.Input[str]]:
        """
        The region of the Data Fusion instance.
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "region", value)


@pulumi.input_type
class _InstanceIamMemberState:
    def __init__(__self__, *,
                 condition: Optional[pulumi.Input['InstanceIamMemberConditionArgs']] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 member: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering InstanceIamMember resources.
        :param pulumi.Input[str] name: The ID of the instance or a fully qualified identifier for the instance.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: The region of the Data Fusion instance.
        """
        if condition is not None:
            pulumi.set(__self__, "condition", condition)
        if etag is not None:
            pulumi.set(__self__, "etag", etag)
        if member is not None:
            pulumi.set(__self__, "member", member)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if region is not None:
            pulumi.set(__self__, "region", region)
        if role is not None:
            pulumi.set(__self__, "role", role)

    @property
    @pulumi.getter
    def condition(self) -> Optional[pulumi.Input['InstanceIamMemberConditionArgs']]:
        return pulumi.get(self, "condition")

    @condition.setter
    def condition(self, value: Optional[pulumi.Input['InstanceIamMemberConditionArgs']]):
        pulumi.set(self, "condition", value)

    @property
    @pulumi.getter
    def etag(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "etag")

    @etag.setter
    def etag(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "etag", value)

    @property
    @pulumi.getter
    def member(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "member")

    @member.setter
    def member(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "member", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the instance or a fully qualified identifier for the instance.
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

    @property
    @pulumi.getter
    def region(self) -> Optional[pulumi.Input[str]]:
        """
        The region of the Data Fusion instance.
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "region", value)

    @property
    @pulumi.getter
    def role(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "role")

    @role.setter
    def role(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "role", value)


class InstanceIamMember(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 condition: Optional[pulumi.Input[pulumi.InputType['InstanceIamMemberConditionArgs']]] = None,
                 member: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Represents a Data Fusion instance.

        To get more information about Instance, see:

        * [API documentation](https://cloud.google.com/data-fusion/docs/reference/rest/v1beta1/projects.locations.instances)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/data-fusion/docs/)

        ## Example Usage

        ### Data Fusion Instance Basic

        ```python
        import pulumi
        import pulumi_gcp as gcp

        basic_instance = gcp.datafusion.Instance("basic_instance",
            name="my-instance",
            region="us-central1",
            type="BASIC")
        ```
        ### Data Fusion Instance Full

        ```python
        import pulumi
        import pulumi_gcp as gcp

        default = gcp.appengine.get_default_service_account()
        network = gcp.compute.Network("network", name="datafusion-full-network")
        private_ip_alloc = gcp.compute.GlobalAddress("private_ip_alloc",
            name="datafusion-ip-alloc",
            address_type="INTERNAL",
            purpose="VPC_PEERING",
            prefix_length=22,
            network=network.id)
        extended_instance = gcp.datafusion.Instance("extended_instance",
            name="my-instance",
            description="My Data Fusion instance",
            display_name="My Data Fusion instance",
            region="us-central1",
            type="BASIC",
            enable_stackdriver_logging=True,
            enable_stackdriver_monitoring=True,
            private_instance=True,
            dataproc_service_account=default.email,
            labels={
                "example_key": "example_value",
            },
            network_config=gcp.datafusion.InstanceNetworkConfigArgs(
                network="default",
                ip_allocation=pulumi.Output.all(private_ip_alloc.address, private_ip_alloc.prefix_length).apply(lambda address, prefix_length: f"{address}/{prefix_length}"),
            ),
            accelerators=[gcp.datafusion.InstanceAcceleratorArgs(
                accelerator_type="CDC",
                state="ENABLED",
            )])
        ```
        ### Data Fusion Instance Cmek

        ```python
        import pulumi
        import pulumi_gcp as gcp

        key_ring = gcp.kms.KeyRing("key_ring",
            name="my-instance",
            location="us-central1")
        crypto_key = gcp.kms.CryptoKey("crypto_key",
            name="my-instance",
            key_ring=key_ring.id)
        project = gcp.organizations.get_project()
        crypto_key_member = gcp.kms.CryptoKeyIAMMember("crypto_key_member",
            crypto_key_id=crypto_key.id,
            role="roles/cloudkms.cryptoKeyEncrypterDecrypter",
            member=f"serviceAccount:service-{project.number}@gcp-sa-datafusion.iam.gserviceaccount.com")
        cmek = gcp.datafusion.Instance("cmek",
            name="my-instance",
            region="us-central1",
            type="BASIC",
            crypto_key_config=gcp.datafusion.InstanceCryptoKeyConfigArgs(
                key_reference=crypto_key.id,
            ),
            opts=pulumi.ResourceOptions(depends_on=[crypto_key_member]))
        ```
        ### Data Fusion Instance Enterprise

        ```python
        import pulumi
        import pulumi_gcp as gcp

        enterprise_instance = gcp.datafusion.Instance("enterprise_instance",
            name="my-instance",
            region="us-central1",
            type="ENTERPRISE",
            enable_rbac=True)
        ```
        ### Data Fusion Instance Event

        ```python
        import pulumi
        import pulumi_gcp as gcp

        event_topic = gcp.pubsub.Topic("event", name="my-instance")
        event = gcp.datafusion.Instance("event",
            name="my-instance",
            region="us-central1",
            type="BASIC",
            event_publish_config=gcp.datafusion.InstanceEventPublishConfigArgs(
                enabled=True,
                topic=event_topic.id,
            ))
        ```
        ### Data Fusion Instance Zone

        ```python
        import pulumi
        import pulumi_gcp as gcp

        zone = gcp.datafusion.Instance("zone",
            name="my-instance",
            region="us-central1",
            zone="us-central1-a",
            type="DEVELOPER")
        ```

        ## Import

        Instance can be imported using any of these accepted formats:

        * `projects/{{project}}/locations/{{region}}/instances/{{name}}`

        * `{{project}}/{{region}}/{{name}}`

        * `{{region}}/{{name}}`

        * `{{name}}`

        When using the `pulumi import` command, Instance can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:securitycenter/instanceIamMember:InstanceIamMember default projects/{{project}}/locations/{{region}}/instances/{{name}}
        ```

        ```sh
        $ pulumi import gcp:securitycenter/instanceIamMember:InstanceIamMember default {{project}}/{{region}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:securitycenter/instanceIamMember:InstanceIamMember default {{region}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:securitycenter/instanceIamMember:InstanceIamMember default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: The ID of the instance or a fully qualified identifier for the instance.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: The region of the Data Fusion instance.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: InstanceIamMemberArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Represents a Data Fusion instance.

        To get more information about Instance, see:

        * [API documentation](https://cloud.google.com/data-fusion/docs/reference/rest/v1beta1/projects.locations.instances)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/data-fusion/docs/)

        ## Example Usage

        ### Data Fusion Instance Basic

        ```python
        import pulumi
        import pulumi_gcp as gcp

        basic_instance = gcp.datafusion.Instance("basic_instance",
            name="my-instance",
            region="us-central1",
            type="BASIC")
        ```
        ### Data Fusion Instance Full

        ```python
        import pulumi
        import pulumi_gcp as gcp

        default = gcp.appengine.get_default_service_account()
        network = gcp.compute.Network("network", name="datafusion-full-network")
        private_ip_alloc = gcp.compute.GlobalAddress("private_ip_alloc",
            name="datafusion-ip-alloc",
            address_type="INTERNAL",
            purpose="VPC_PEERING",
            prefix_length=22,
            network=network.id)
        extended_instance = gcp.datafusion.Instance("extended_instance",
            name="my-instance",
            description="My Data Fusion instance",
            display_name="My Data Fusion instance",
            region="us-central1",
            type="BASIC",
            enable_stackdriver_logging=True,
            enable_stackdriver_monitoring=True,
            private_instance=True,
            dataproc_service_account=default.email,
            labels={
                "example_key": "example_value",
            },
            network_config=gcp.datafusion.InstanceNetworkConfigArgs(
                network="default",
                ip_allocation=pulumi.Output.all(private_ip_alloc.address, private_ip_alloc.prefix_length).apply(lambda address, prefix_length: f"{address}/{prefix_length}"),
            ),
            accelerators=[gcp.datafusion.InstanceAcceleratorArgs(
                accelerator_type="CDC",
                state="ENABLED",
            )])
        ```
        ### Data Fusion Instance Cmek

        ```python
        import pulumi
        import pulumi_gcp as gcp

        key_ring = gcp.kms.KeyRing("key_ring",
            name="my-instance",
            location="us-central1")
        crypto_key = gcp.kms.CryptoKey("crypto_key",
            name="my-instance",
            key_ring=key_ring.id)
        project = gcp.organizations.get_project()
        crypto_key_member = gcp.kms.CryptoKeyIAMMember("crypto_key_member",
            crypto_key_id=crypto_key.id,
            role="roles/cloudkms.cryptoKeyEncrypterDecrypter",
            member=f"serviceAccount:service-{project.number}@gcp-sa-datafusion.iam.gserviceaccount.com")
        cmek = gcp.datafusion.Instance("cmek",
            name="my-instance",
            region="us-central1",
            type="BASIC",
            crypto_key_config=gcp.datafusion.InstanceCryptoKeyConfigArgs(
                key_reference=crypto_key.id,
            ),
            opts=pulumi.ResourceOptions(depends_on=[crypto_key_member]))
        ```
        ### Data Fusion Instance Enterprise

        ```python
        import pulumi
        import pulumi_gcp as gcp

        enterprise_instance = gcp.datafusion.Instance("enterprise_instance",
            name="my-instance",
            region="us-central1",
            type="ENTERPRISE",
            enable_rbac=True)
        ```
        ### Data Fusion Instance Event

        ```python
        import pulumi
        import pulumi_gcp as gcp

        event_topic = gcp.pubsub.Topic("event", name="my-instance")
        event = gcp.datafusion.Instance("event",
            name="my-instance",
            region="us-central1",
            type="BASIC",
            event_publish_config=gcp.datafusion.InstanceEventPublishConfigArgs(
                enabled=True,
                topic=event_topic.id,
            ))
        ```
        ### Data Fusion Instance Zone

        ```python
        import pulumi
        import pulumi_gcp as gcp

        zone = gcp.datafusion.Instance("zone",
            name="my-instance",
            region="us-central1",
            zone="us-central1-a",
            type="DEVELOPER")
        ```

        ## Import

        Instance can be imported using any of these accepted formats:

        * `projects/{{project}}/locations/{{region}}/instances/{{name}}`

        * `{{project}}/{{region}}/{{name}}`

        * `{{region}}/{{name}}`

        * `{{name}}`

        When using the `pulumi import` command, Instance can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:securitycenter/instanceIamMember:InstanceIamMember default projects/{{project}}/locations/{{region}}/instances/{{name}}
        ```

        ```sh
        $ pulumi import gcp:securitycenter/instanceIamMember:InstanceIamMember default {{project}}/{{region}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:securitycenter/instanceIamMember:InstanceIamMember default {{region}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:securitycenter/instanceIamMember:InstanceIamMember default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param InstanceIamMemberArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(InstanceIamMemberArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 condition: Optional[pulumi.Input[pulumi.InputType['InstanceIamMemberConditionArgs']]] = None,
                 member: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = InstanceIamMemberArgs.__new__(InstanceIamMemberArgs)

            __props__.__dict__["condition"] = condition
            if member is None and not opts.urn:
                raise TypeError("Missing required property 'member'")
            __props__.__dict__["member"] = member
            __props__.__dict__["name"] = name
            __props__.__dict__["project"] = project
            __props__.__dict__["region"] = region
            if role is None and not opts.urn:
                raise TypeError("Missing required property 'role'")
            __props__.__dict__["role"] = role
            __props__.__dict__["etag"] = None
        super(InstanceIamMember, __self__).__init__(
            'gcp:securitycenter/instanceIamMember:InstanceIamMember',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            condition: Optional[pulumi.Input[pulumi.InputType['InstanceIamMemberConditionArgs']]] = None,
            etag: Optional[pulumi.Input[str]] = None,
            member: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None,
            region: Optional[pulumi.Input[str]] = None,
            role: Optional[pulumi.Input[str]] = None) -> 'InstanceIamMember':
        """
        Get an existing InstanceIamMember resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: The ID of the instance or a fully qualified identifier for the instance.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: The region of the Data Fusion instance.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _InstanceIamMemberState.__new__(_InstanceIamMemberState)

        __props__.__dict__["condition"] = condition
        __props__.__dict__["etag"] = etag
        __props__.__dict__["member"] = member
        __props__.__dict__["name"] = name
        __props__.__dict__["project"] = project
        __props__.__dict__["region"] = region
        __props__.__dict__["role"] = role
        return InstanceIamMember(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def condition(self) -> pulumi.Output[Optional['outputs.InstanceIamMemberCondition']]:
        return pulumi.get(self, "condition")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def member(self) -> pulumi.Output[str]:
        return pulumi.get(self, "member")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The ID of the instance or a fully qualified identifier for the instance.
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

    @property
    @pulumi.getter
    def region(self) -> pulumi.Output[str]:
        """
        The region of the Data Fusion instance.
        """
        return pulumi.get(self, "region")

    @property
    @pulumi.getter
    def role(self) -> pulumi.Output[str]:
        return pulumi.get(self, "role")

