# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ManagedZoneArgs', 'ManagedZone']

@pulumi.input_type
class ManagedZoneArgs:
    def __init__(__self__, *,
                 dns: pulumi.Input[str],
                 target_project: pulumi.Input[str],
                 target_vpc: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ManagedZone resource.
        :param pulumi.Input[str] dns: DNS Name of the resource.
        :param pulumi.Input[str] target_project: The name of the Target Project.
        :param pulumi.Input[str] target_vpc: The name of the Target Project VPC Network.
        :param pulumi.Input[str] description: Description of the resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Resource labels to represent user provided metadata.
               
               **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
               Please refer to the field `effective_labels` for all of the labels present on the resource.
        :param pulumi.Input[str] name: Name of Managed Zone needs to be created.
               
               
               - - -
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        """
        pulumi.set(__self__, "dns", dns)
        pulumi.set(__self__, "target_project", target_project)
        pulumi.set(__self__, "target_vpc", target_vpc)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if labels is not None:
            pulumi.set(__self__, "labels", labels)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)

    @property
    @pulumi.getter
    def dns(self) -> pulumi.Input[str]:
        """
        DNS Name of the resource.
        """
        return pulumi.get(self, "dns")

    @dns.setter
    def dns(self, value: pulumi.Input[str]):
        pulumi.set(self, "dns", value)

    @property
    @pulumi.getter(name="targetProject")
    def target_project(self) -> pulumi.Input[str]:
        """
        The name of the Target Project.
        """
        return pulumi.get(self, "target_project")

    @target_project.setter
    def target_project(self, value: pulumi.Input[str]):
        pulumi.set(self, "target_project", value)

    @property
    @pulumi.getter(name="targetVpc")
    def target_vpc(self) -> pulumi.Input[str]:
        """
        The name of the Target Project VPC Network.
        """
        return pulumi.get(self, "target_vpc")

    @target_vpc.setter
    def target_vpc(self, value: pulumi.Input[str]):
        pulumi.set(self, "target_vpc", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of the resource.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource labels to represent user provided metadata.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field `effective_labels` for all of the labels present on the resource.
        """
        return pulumi.get(self, "labels")

    @labels.setter
    def labels(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "labels", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of Managed Zone needs to be created.


        - - -
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


@pulumi.input_type
class _ManagedZoneState:
    def __init__(__self__, *,
                 create_time: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 dns: Optional[pulumi.Input[str]] = None,
                 effective_labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 pulumi_labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 target_project: Optional[pulumi.Input[str]] = None,
                 target_vpc: Optional[pulumi.Input[str]] = None,
                 update_time: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ManagedZone resources.
        :param pulumi.Input[str] create_time: Time the Namespace was created in UTC.
        :param pulumi.Input[str] description: Description of the resource.
        :param pulumi.Input[str] dns: DNS Name of the resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] effective_labels: All of labels (key/value pairs) present on the resource in GCP, including the labels configured through Pulumi, other clients and services.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Resource labels to represent user provided metadata.
               
               **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
               Please refer to the field `effective_labels` for all of the labels present on the resource.
        :param pulumi.Input[str] name: Name of Managed Zone needs to be created.
               
               
               - - -
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] pulumi_labels: The combination of labels configured directly on the resource
               and default labels configured on the provider.
        :param pulumi.Input[str] target_project: The name of the Target Project.
        :param pulumi.Input[str] target_vpc: The name of the Target Project VPC Network.
        :param pulumi.Input[str] update_time: Time the Namespace was updated in UTC.
        """
        if create_time is not None:
            pulumi.set(__self__, "create_time", create_time)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if dns is not None:
            pulumi.set(__self__, "dns", dns)
        if effective_labels is not None:
            pulumi.set(__self__, "effective_labels", effective_labels)
        if labels is not None:
            pulumi.set(__self__, "labels", labels)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if pulumi_labels is not None:
            pulumi.set(__self__, "pulumi_labels", pulumi_labels)
        if target_project is not None:
            pulumi.set(__self__, "target_project", target_project)
        if target_vpc is not None:
            pulumi.set(__self__, "target_vpc", target_vpc)
        if update_time is not None:
            pulumi.set(__self__, "update_time", update_time)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> Optional[pulumi.Input[str]]:
        """
        Time the Namespace was created in UTC.
        """
        return pulumi.get(self, "create_time")

    @create_time.setter
    def create_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "create_time", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of the resource.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def dns(self) -> Optional[pulumi.Input[str]]:
        """
        DNS Name of the resource.
        """
        return pulumi.get(self, "dns")

    @dns.setter
    def dns(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "dns", value)

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
    def labels(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource labels to represent user provided metadata.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field `effective_labels` for all of the labels present on the resource.
        """
        return pulumi.get(self, "labels")

    @labels.setter
    def labels(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "labels", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of Managed Zone needs to be created.


        - - -
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
    @pulumi.getter(name="targetProject")
    def target_project(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Target Project.
        """
        return pulumi.get(self, "target_project")

    @target_project.setter
    def target_project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "target_project", value)

    @property
    @pulumi.getter(name="targetVpc")
    def target_vpc(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Target Project VPC Network.
        """
        return pulumi.get(self, "target_vpc")

    @target_vpc.setter
    def target_vpc(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "target_vpc", value)

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> Optional[pulumi.Input[str]]:
        """
        Time the Namespace was updated in UTC.
        """
        return pulumi.get(self, "update_time")

    @update_time.setter
    def update_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "update_time", value)


class ManagedZone(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 dns: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 target_project: Optional[pulumi.Input[str]] = None,
                 target_vpc: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        An Integration connectors Managed Zone.

        To get more information about ManagedZone, see:

        * [API documentation](https://cloud.google.com/integration-connectors/docs/reference/rest/v1/projects.locations.global.managedZones)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/integration-connectors/docs)

        ## Example Usage

        ### Integration Connectors Managed Zone

        ```python
        import pulumi
        import pulumi_gcp as gcp

        target_project = gcp.organizations.Project("target_project",
            project_id="tf-test_34535",
            name="tf-test_22375",
            org_id="123456789",
            billing_account="000000-0000000-0000000-000000")
        test_project = gcp.organizations.get_project()
        dns_peer_binding = gcp.projects.IAMMember("dns_peer_binding",
            project=target_project.project_id,
            role="roles/dns.peer",
            member=f"serviceAccount:service-{test_project.number}@gcp-sa-connectors.iam.gserviceaccount.com")
        dns = gcp.projects.Service("dns",
            project=target_project.project_id,
            service="dns.googleapis.com")
        compute = gcp.projects.Service("compute",
            project=target_project.project_id,
            service="compute.googleapis.com")
        network = gcp.compute.Network("network",
            project=target_project.project_id,
            name="test",
            auto_create_subnetworks=False,
            opts=pulumi.ResourceOptions(depends_on=[compute]))
        zone = gcp.dns.ManagedZone("zone",
            name="tf-test-dns_29439",
            dns_name="private_87786.example.com.",
            visibility="private",
            private_visibility_config=gcp.dns.ManagedZonePrivateVisibilityConfigArgs(
                networks=[gcp.dns.ManagedZonePrivateVisibilityConfigNetworkArgs(
                    network_url=network.id,
                )],
            ),
            opts=pulumi.ResourceOptions(depends_on=[dns]))
        testmanagedzone = gcp.integrationconnectors.ManagedZone("testmanagedzone",
            name="test",
            description="tf created description",
            labels={
                "intent": "example",
            },
            target_project=target_project.project_id,
            target_vpc="test",
            dns=zone.dns_name,
            opts=pulumi.ResourceOptions(depends_on=[
                    dns_peer_binding,
                    zone,
                ]))
        ```

        ## Import

        ManagedZone can be imported using any of these accepted formats:

        * `projects/{{project}}/locations/global/managedZones/{{name}}`

        * `{{project}}/{{name}}`

        * `{{name}}`

        When using the `pulumi import` command, ManagedZone can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:integrationconnectors/managedZone:ManagedZone default projects/{{project}}/locations/global/managedZones/{{name}}
        ```

        ```sh
        $ pulumi import gcp:integrationconnectors/managedZone:ManagedZone default {{project}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:integrationconnectors/managedZone:ManagedZone default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: Description of the resource.
        :param pulumi.Input[str] dns: DNS Name of the resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Resource labels to represent user provided metadata.
               
               **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
               Please refer to the field `effective_labels` for all of the labels present on the resource.
        :param pulumi.Input[str] name: Name of Managed Zone needs to be created.
               
               
               - - -
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] target_project: The name of the Target Project.
        :param pulumi.Input[str] target_vpc: The name of the Target Project VPC Network.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ManagedZoneArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        An Integration connectors Managed Zone.

        To get more information about ManagedZone, see:

        * [API documentation](https://cloud.google.com/integration-connectors/docs/reference/rest/v1/projects.locations.global.managedZones)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/integration-connectors/docs)

        ## Example Usage

        ### Integration Connectors Managed Zone

        ```python
        import pulumi
        import pulumi_gcp as gcp

        target_project = gcp.organizations.Project("target_project",
            project_id="tf-test_34535",
            name="tf-test_22375",
            org_id="123456789",
            billing_account="000000-0000000-0000000-000000")
        test_project = gcp.organizations.get_project()
        dns_peer_binding = gcp.projects.IAMMember("dns_peer_binding",
            project=target_project.project_id,
            role="roles/dns.peer",
            member=f"serviceAccount:service-{test_project.number}@gcp-sa-connectors.iam.gserviceaccount.com")
        dns = gcp.projects.Service("dns",
            project=target_project.project_id,
            service="dns.googleapis.com")
        compute = gcp.projects.Service("compute",
            project=target_project.project_id,
            service="compute.googleapis.com")
        network = gcp.compute.Network("network",
            project=target_project.project_id,
            name="test",
            auto_create_subnetworks=False,
            opts=pulumi.ResourceOptions(depends_on=[compute]))
        zone = gcp.dns.ManagedZone("zone",
            name="tf-test-dns_29439",
            dns_name="private_87786.example.com.",
            visibility="private",
            private_visibility_config=gcp.dns.ManagedZonePrivateVisibilityConfigArgs(
                networks=[gcp.dns.ManagedZonePrivateVisibilityConfigNetworkArgs(
                    network_url=network.id,
                )],
            ),
            opts=pulumi.ResourceOptions(depends_on=[dns]))
        testmanagedzone = gcp.integrationconnectors.ManagedZone("testmanagedzone",
            name="test",
            description="tf created description",
            labels={
                "intent": "example",
            },
            target_project=target_project.project_id,
            target_vpc="test",
            dns=zone.dns_name,
            opts=pulumi.ResourceOptions(depends_on=[
                    dns_peer_binding,
                    zone,
                ]))
        ```

        ## Import

        ManagedZone can be imported using any of these accepted formats:

        * `projects/{{project}}/locations/global/managedZones/{{name}}`

        * `{{project}}/{{name}}`

        * `{{name}}`

        When using the `pulumi import` command, ManagedZone can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:integrationconnectors/managedZone:ManagedZone default projects/{{project}}/locations/global/managedZones/{{name}}
        ```

        ```sh
        $ pulumi import gcp:integrationconnectors/managedZone:ManagedZone default {{project}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:integrationconnectors/managedZone:ManagedZone default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param ManagedZoneArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ManagedZoneArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 dns: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 target_project: Optional[pulumi.Input[str]] = None,
                 target_vpc: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ManagedZoneArgs.__new__(ManagedZoneArgs)

            __props__.__dict__["description"] = description
            if dns is None and not opts.urn:
                raise TypeError("Missing required property 'dns'")
            __props__.__dict__["dns"] = dns
            __props__.__dict__["labels"] = labels
            __props__.__dict__["name"] = name
            __props__.__dict__["project"] = project
            if target_project is None and not opts.urn:
                raise TypeError("Missing required property 'target_project'")
            __props__.__dict__["target_project"] = target_project
            if target_vpc is None and not opts.urn:
                raise TypeError("Missing required property 'target_vpc'")
            __props__.__dict__["target_vpc"] = target_vpc
            __props__.__dict__["create_time"] = None
            __props__.__dict__["effective_labels"] = None
            __props__.__dict__["pulumi_labels"] = None
            __props__.__dict__["update_time"] = None
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["effectiveLabels", "pulumiLabels"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(ManagedZone, __self__).__init__(
            'gcp:integrationconnectors/managedZone:ManagedZone',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            create_time: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            dns: Optional[pulumi.Input[str]] = None,
            effective_labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            name: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None,
            pulumi_labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            target_project: Optional[pulumi.Input[str]] = None,
            target_vpc: Optional[pulumi.Input[str]] = None,
            update_time: Optional[pulumi.Input[str]] = None) -> 'ManagedZone':
        """
        Get an existing ManagedZone resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] create_time: Time the Namespace was created in UTC.
        :param pulumi.Input[str] description: Description of the resource.
        :param pulumi.Input[str] dns: DNS Name of the resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] effective_labels: All of labels (key/value pairs) present on the resource in GCP, including the labels configured through Pulumi, other clients and services.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Resource labels to represent user provided metadata.
               
               **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
               Please refer to the field `effective_labels` for all of the labels present on the resource.
        :param pulumi.Input[str] name: Name of Managed Zone needs to be created.
               
               
               - - -
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] pulumi_labels: The combination of labels configured directly on the resource
               and default labels configured on the provider.
        :param pulumi.Input[str] target_project: The name of the Target Project.
        :param pulumi.Input[str] target_vpc: The name of the Target Project VPC Network.
        :param pulumi.Input[str] update_time: Time the Namespace was updated in UTC.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ManagedZoneState.__new__(_ManagedZoneState)

        __props__.__dict__["create_time"] = create_time
        __props__.__dict__["description"] = description
        __props__.__dict__["dns"] = dns
        __props__.__dict__["effective_labels"] = effective_labels
        __props__.__dict__["labels"] = labels
        __props__.__dict__["name"] = name
        __props__.__dict__["project"] = project
        __props__.__dict__["pulumi_labels"] = pulumi_labels
        __props__.__dict__["target_project"] = target_project
        __props__.__dict__["target_vpc"] = target_vpc
        __props__.__dict__["update_time"] = update_time
        return ManagedZone(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> pulumi.Output[str]:
        """
        Time the Namespace was created in UTC.
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Description of the resource.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def dns(self) -> pulumi.Output[str]:
        """
        DNS Name of the resource.
        """
        return pulumi.get(self, "dns")

    @property
    @pulumi.getter(name="effectiveLabels")
    def effective_labels(self) -> pulumi.Output[Mapping[str, str]]:
        """
        All of labels (key/value pairs) present on the resource in GCP, including the labels configured through Pulumi, other clients and services.
        """
        return pulumi.get(self, "effective_labels")

    @property
    @pulumi.getter
    def labels(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource labels to represent user provided metadata.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field `effective_labels` for all of the labels present on the resource.
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of Managed Zone needs to be created.


        - - -
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
    @pulumi.getter(name="pulumiLabels")
    def pulumi_labels(self) -> pulumi.Output[Mapping[str, str]]:
        """
        The combination of labels configured directly on the resource
        and default labels configured on the provider.
        """
        return pulumi.get(self, "pulumi_labels")

    @property
    @pulumi.getter(name="targetProject")
    def target_project(self) -> pulumi.Output[str]:
        """
        The name of the Target Project.
        """
        return pulumi.get(self, "target_project")

    @property
    @pulumi.getter(name="targetVpc")
    def target_vpc(self) -> pulumi.Output[str]:
        """
        The name of the Target Project VPC Network.
        """
        return pulumi.get(self, "target_vpc")

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> pulumi.Output[str]:
        """
        Time the Namespace was updated in UTC.
        """
        return pulumi.get(self, "update_time")

