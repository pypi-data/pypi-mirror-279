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

__all__ = ['MetastoreFederationArgs', 'MetastoreFederation']

@pulumi.input_type
class MetastoreFederationArgs:
    def __init__(__self__, *,
                 backend_metastores: pulumi.Input[Sequence[pulumi.Input['MetastoreFederationBackendMetastoreArgs']]],
                 federation_id: pulumi.Input[str],
                 version: pulumi.Input[str],
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a MetastoreFederation resource.
        :param pulumi.Input[Sequence[pulumi.Input['MetastoreFederationBackendMetastoreArgs']]] backend_metastores: A map from BackendMetastore rank to BackendMetastores from which the federation service serves metadata at query time. The map key represents the order in which BackendMetastores should be evaluated to resolve database names at query time and should be greater than or equal to zero. A BackendMetastore with a lower number will be evaluated before a BackendMetastore with a higher number.
               Structure is documented below.
        :param pulumi.Input[str] federation_id: The ID of the metastore federation. The id must contain only letters (a-z, A-Z), numbers (0-9), underscores (_),
               and hyphens (-). Cannot begin or end with underscore or hyphen. Must consist of between
               3 and 63 characters.
        :param pulumi.Input[str] version: The Apache Hive metastore version of the federation. All backend metastore versions must be compatible with the federation version.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: User-defined labels for the metastore federation. **Note**: This field is non-authoritative, and will only manage the
               labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the
               resource.
        :param pulumi.Input[str] location: The location where the metastore federation should reside.
        """
        pulumi.set(__self__, "backend_metastores", backend_metastores)
        pulumi.set(__self__, "federation_id", federation_id)
        pulumi.set(__self__, "version", version)
        if labels is not None:
            pulumi.set(__self__, "labels", labels)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if project is not None:
            pulumi.set(__self__, "project", project)

    @property
    @pulumi.getter(name="backendMetastores")
    def backend_metastores(self) -> pulumi.Input[Sequence[pulumi.Input['MetastoreFederationBackendMetastoreArgs']]]:
        """
        A map from BackendMetastore rank to BackendMetastores from which the federation service serves metadata at query time. The map key represents the order in which BackendMetastores should be evaluated to resolve database names at query time and should be greater than or equal to zero. A BackendMetastore with a lower number will be evaluated before a BackendMetastore with a higher number.
        Structure is documented below.
        """
        return pulumi.get(self, "backend_metastores")

    @backend_metastores.setter
    def backend_metastores(self, value: pulumi.Input[Sequence[pulumi.Input['MetastoreFederationBackendMetastoreArgs']]]):
        pulumi.set(self, "backend_metastores", value)

    @property
    @pulumi.getter(name="federationId")
    def federation_id(self) -> pulumi.Input[str]:
        """
        The ID of the metastore federation. The id must contain only letters (a-z, A-Z), numbers (0-9), underscores (_),
        and hyphens (-). Cannot begin or end with underscore or hyphen. Must consist of between
        3 and 63 characters.
        """
        return pulumi.get(self, "federation_id")

    @federation_id.setter
    def federation_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "federation_id", value)

    @property
    @pulumi.getter
    def version(self) -> pulumi.Input[str]:
        """
        The Apache Hive metastore version of the federation. All backend metastore versions must be compatible with the federation version.
        """
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: pulumi.Input[str]):
        pulumi.set(self, "version", value)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        User-defined labels for the metastore federation. **Note**: This field is non-authoritative, and will only manage the
        labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the
        resource.
        """
        return pulumi.get(self, "labels")

    @labels.setter
    def labels(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "labels", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The location where the metastore federation should reside.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)


@pulumi.input_type
class _MetastoreFederationState:
    def __init__(__self__, *,
                 backend_metastores: Optional[pulumi.Input[Sequence[pulumi.Input['MetastoreFederationBackendMetastoreArgs']]]] = None,
                 effective_labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 endpoint_uri: Optional[pulumi.Input[str]] = None,
                 federation_id: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 pulumi_labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 state: Optional[pulumi.Input[str]] = None,
                 state_message: Optional[pulumi.Input[str]] = None,
                 uid: Optional[pulumi.Input[str]] = None,
                 version: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering MetastoreFederation resources.
        :param pulumi.Input[Sequence[pulumi.Input['MetastoreFederationBackendMetastoreArgs']]] backend_metastores: A map from BackendMetastore rank to BackendMetastores from which the federation service serves metadata at query time. The map key represents the order in which BackendMetastores should be evaluated to resolve database names at query time and should be greater than or equal to zero. A BackendMetastore with a lower number will be evaluated before a BackendMetastore with a higher number.
               Structure is documented below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] effective_labels: All of labels (key/value pairs) present on the resource in GCP, including the labels configured through Pulumi, other clients and services.
        :param pulumi.Input[str] endpoint_uri: The URI of the endpoint used to access the metastore federation.
        :param pulumi.Input[str] federation_id: The ID of the metastore federation. The id must contain only letters (a-z, A-Z), numbers (0-9), underscores (_),
               and hyphens (-). Cannot begin or end with underscore or hyphen. Must consist of between
               3 and 63 characters.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: User-defined labels for the metastore federation. **Note**: This field is non-authoritative, and will only manage the
               labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the
               resource.
        :param pulumi.Input[str] location: The location where the metastore federation should reside.
        :param pulumi.Input[str] name: The relative resource name of the metastore federation.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] pulumi_labels: The combination of labels configured directly on the resource
               and default labels configured on the provider.
        :param pulumi.Input[str] state: The current state of the metastore federation.
        :param pulumi.Input[str] state_message: Additional information about the current state of the metastore federation, if available.
        :param pulumi.Input[str] uid: The globally unique resource identifier of the metastore federation.
        :param pulumi.Input[str] version: The Apache Hive metastore version of the federation. All backend metastore versions must be compatible with the federation version.
        """
        if backend_metastores is not None:
            pulumi.set(__self__, "backend_metastores", backend_metastores)
        if effective_labels is not None:
            pulumi.set(__self__, "effective_labels", effective_labels)
        if endpoint_uri is not None:
            pulumi.set(__self__, "endpoint_uri", endpoint_uri)
        if federation_id is not None:
            pulumi.set(__self__, "federation_id", federation_id)
        if labels is not None:
            pulumi.set(__self__, "labels", labels)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if pulumi_labels is not None:
            pulumi.set(__self__, "pulumi_labels", pulumi_labels)
        if state is not None:
            pulumi.set(__self__, "state", state)
        if state_message is not None:
            pulumi.set(__self__, "state_message", state_message)
        if uid is not None:
            pulumi.set(__self__, "uid", uid)
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter(name="backendMetastores")
    def backend_metastores(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['MetastoreFederationBackendMetastoreArgs']]]]:
        """
        A map from BackendMetastore rank to BackendMetastores from which the federation service serves metadata at query time. The map key represents the order in which BackendMetastores should be evaluated to resolve database names at query time and should be greater than or equal to zero. A BackendMetastore with a lower number will be evaluated before a BackendMetastore with a higher number.
        Structure is documented below.
        """
        return pulumi.get(self, "backend_metastores")

    @backend_metastores.setter
    def backend_metastores(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['MetastoreFederationBackendMetastoreArgs']]]]):
        pulumi.set(self, "backend_metastores", value)

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
    @pulumi.getter(name="endpointUri")
    def endpoint_uri(self) -> Optional[pulumi.Input[str]]:
        """
        The URI of the endpoint used to access the metastore federation.
        """
        return pulumi.get(self, "endpoint_uri")

    @endpoint_uri.setter
    def endpoint_uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "endpoint_uri", value)

    @property
    @pulumi.getter(name="federationId")
    def federation_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the metastore federation. The id must contain only letters (a-z, A-Z), numbers (0-9), underscores (_),
        and hyphens (-). Cannot begin or end with underscore or hyphen. Must consist of between
        3 and 63 characters.
        """
        return pulumi.get(self, "federation_id")

    @federation_id.setter
    def federation_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "federation_id", value)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        User-defined labels for the metastore federation. **Note**: This field is non-authoritative, and will only manage the
        labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the
        resource.
        """
        return pulumi.get(self, "labels")

    @labels.setter
    def labels(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "labels", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The location where the metastore federation should reside.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The relative resource name of the metastore federation.
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
        The current state of the metastore federation.
        """
        return pulumi.get(self, "state")

    @state.setter
    def state(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "state", value)

    @property
    @pulumi.getter(name="stateMessage")
    def state_message(self) -> Optional[pulumi.Input[str]]:
        """
        Additional information about the current state of the metastore federation, if available.
        """
        return pulumi.get(self, "state_message")

    @state_message.setter
    def state_message(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "state_message", value)

    @property
    @pulumi.getter
    def uid(self) -> Optional[pulumi.Input[str]]:
        """
        The globally unique resource identifier of the metastore federation.
        """
        return pulumi.get(self, "uid")

    @uid.setter
    def uid(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "uid", value)

    @property
    @pulumi.getter
    def version(self) -> Optional[pulumi.Input[str]]:
        """
        The Apache Hive metastore version of the federation. All backend metastore versions must be compatible with the federation version.
        """
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "version", value)


class MetastoreFederation(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 backend_metastores: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['MetastoreFederationBackendMetastoreArgs']]]]] = None,
                 federation_id: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 version: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        A managed metastore federation.

        ## Example Usage

        ### Dataproc Metastore Federation Basic

        ```python
        import pulumi
        import pulumi_gcp as gcp

        default_metastore_service = gcp.dataproc.MetastoreService("default",
            service_id="",
            location="us-central1",
            tier="DEVELOPER",
            hive_metastore_config=gcp.dataproc.MetastoreServiceHiveMetastoreConfigArgs(
                version="3.1.2",
                endpoint_protocol="GRPC",
            ))
        default = gcp.dataproc.MetastoreFederation("default",
            location="us-central1",
            federation_id="",
            version="3.1.2",
            backend_metastores=[gcp.dataproc.MetastoreFederationBackendMetastoreArgs(
                rank="1",
                name=default_metastore_service.id,
                metastore_type="DATAPROC_METASTORE",
            )])
        ```
        ### Dataproc Metastore Federation Bigquery

        ```python
        import pulumi
        import pulumi_gcp as gcp

        default_metastore_service = gcp.dataproc.MetastoreService("default",
            service_id="",
            location="us-central1",
            tier="DEVELOPER",
            hive_metastore_config=gcp.dataproc.MetastoreServiceHiveMetastoreConfigArgs(
                version="3.1.2",
                endpoint_protocol="GRPC",
            ))
        project = gcp.organizations.get_project()
        default = gcp.dataproc.MetastoreFederation("default",
            location="us-central1",
            federation_id="",
            version="3.1.2",
            backend_metastores=[
                gcp.dataproc.MetastoreFederationBackendMetastoreArgs(
                    rank="2",
                    name=project.id,
                    metastore_type="BIGQUERY",
                ),
                gcp.dataproc.MetastoreFederationBackendMetastoreArgs(
                    rank="1",
                    name=default_metastore_service.id,
                    metastore_type="DATAPROC_METASTORE",
                ),
            ])
        ```

        ## Import

        Federation can be imported using any of these accepted formats:

        * `projects/{{project}}/locations/{{location}}/federations/{{federation_id}}`

        * `{{project}}/{{location}}/{{federation_id}}`

        * `{{location}}/{{federation_id}}`

        When using the `pulumi import` command, Federation can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:dataproc/metastoreFederation:MetastoreFederation default projects/{{project}}/locations/{{location}}/federations/{{federation_id}}
        ```

        ```sh
        $ pulumi import gcp:dataproc/metastoreFederation:MetastoreFederation default {{project}}/{{location}}/{{federation_id}}
        ```

        ```sh
        $ pulumi import gcp:dataproc/metastoreFederation:MetastoreFederation default {{location}}/{{federation_id}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['MetastoreFederationBackendMetastoreArgs']]]] backend_metastores: A map from BackendMetastore rank to BackendMetastores from which the federation service serves metadata at query time. The map key represents the order in which BackendMetastores should be evaluated to resolve database names at query time and should be greater than or equal to zero. A BackendMetastore with a lower number will be evaluated before a BackendMetastore with a higher number.
               Structure is documented below.
        :param pulumi.Input[str] federation_id: The ID of the metastore federation. The id must contain only letters (a-z, A-Z), numbers (0-9), underscores (_),
               and hyphens (-). Cannot begin or end with underscore or hyphen. Must consist of between
               3 and 63 characters.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: User-defined labels for the metastore federation. **Note**: This field is non-authoritative, and will only manage the
               labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the
               resource.
        :param pulumi.Input[str] location: The location where the metastore federation should reside.
        :param pulumi.Input[str] version: The Apache Hive metastore version of the federation. All backend metastore versions must be compatible with the federation version.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: MetastoreFederationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A managed metastore federation.

        ## Example Usage

        ### Dataproc Metastore Federation Basic

        ```python
        import pulumi
        import pulumi_gcp as gcp

        default_metastore_service = gcp.dataproc.MetastoreService("default",
            service_id="",
            location="us-central1",
            tier="DEVELOPER",
            hive_metastore_config=gcp.dataproc.MetastoreServiceHiveMetastoreConfigArgs(
                version="3.1.2",
                endpoint_protocol="GRPC",
            ))
        default = gcp.dataproc.MetastoreFederation("default",
            location="us-central1",
            federation_id="",
            version="3.1.2",
            backend_metastores=[gcp.dataproc.MetastoreFederationBackendMetastoreArgs(
                rank="1",
                name=default_metastore_service.id,
                metastore_type="DATAPROC_METASTORE",
            )])
        ```
        ### Dataproc Metastore Federation Bigquery

        ```python
        import pulumi
        import pulumi_gcp as gcp

        default_metastore_service = gcp.dataproc.MetastoreService("default",
            service_id="",
            location="us-central1",
            tier="DEVELOPER",
            hive_metastore_config=gcp.dataproc.MetastoreServiceHiveMetastoreConfigArgs(
                version="3.1.2",
                endpoint_protocol="GRPC",
            ))
        project = gcp.organizations.get_project()
        default = gcp.dataproc.MetastoreFederation("default",
            location="us-central1",
            federation_id="",
            version="3.1.2",
            backend_metastores=[
                gcp.dataproc.MetastoreFederationBackendMetastoreArgs(
                    rank="2",
                    name=project.id,
                    metastore_type="BIGQUERY",
                ),
                gcp.dataproc.MetastoreFederationBackendMetastoreArgs(
                    rank="1",
                    name=default_metastore_service.id,
                    metastore_type="DATAPROC_METASTORE",
                ),
            ])
        ```

        ## Import

        Federation can be imported using any of these accepted formats:

        * `projects/{{project}}/locations/{{location}}/federations/{{federation_id}}`

        * `{{project}}/{{location}}/{{federation_id}}`

        * `{{location}}/{{federation_id}}`

        When using the `pulumi import` command, Federation can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:dataproc/metastoreFederation:MetastoreFederation default projects/{{project}}/locations/{{location}}/federations/{{federation_id}}
        ```

        ```sh
        $ pulumi import gcp:dataproc/metastoreFederation:MetastoreFederation default {{project}}/{{location}}/{{federation_id}}
        ```

        ```sh
        $ pulumi import gcp:dataproc/metastoreFederation:MetastoreFederation default {{location}}/{{federation_id}}
        ```

        :param str resource_name: The name of the resource.
        :param MetastoreFederationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(MetastoreFederationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 backend_metastores: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['MetastoreFederationBackendMetastoreArgs']]]]] = None,
                 federation_id: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 version: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = MetastoreFederationArgs.__new__(MetastoreFederationArgs)

            if backend_metastores is None and not opts.urn:
                raise TypeError("Missing required property 'backend_metastores'")
            __props__.__dict__["backend_metastores"] = backend_metastores
            if federation_id is None and not opts.urn:
                raise TypeError("Missing required property 'federation_id'")
            __props__.__dict__["federation_id"] = federation_id
            __props__.__dict__["labels"] = labels
            __props__.__dict__["location"] = location
            __props__.__dict__["project"] = project
            if version is None and not opts.urn:
                raise TypeError("Missing required property 'version'")
            __props__.__dict__["version"] = version
            __props__.__dict__["effective_labels"] = None
            __props__.__dict__["endpoint_uri"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["pulumi_labels"] = None
            __props__.__dict__["state"] = None
            __props__.__dict__["state_message"] = None
            __props__.__dict__["uid"] = None
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["effectiveLabels", "pulumiLabels"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(MetastoreFederation, __self__).__init__(
            'gcp:dataproc/metastoreFederation:MetastoreFederation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            backend_metastores: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['MetastoreFederationBackendMetastoreArgs']]]]] = None,
            effective_labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            endpoint_uri: Optional[pulumi.Input[str]] = None,
            federation_id: Optional[pulumi.Input[str]] = None,
            labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            location: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None,
            pulumi_labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            state: Optional[pulumi.Input[str]] = None,
            state_message: Optional[pulumi.Input[str]] = None,
            uid: Optional[pulumi.Input[str]] = None,
            version: Optional[pulumi.Input[str]] = None) -> 'MetastoreFederation':
        """
        Get an existing MetastoreFederation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['MetastoreFederationBackendMetastoreArgs']]]] backend_metastores: A map from BackendMetastore rank to BackendMetastores from which the federation service serves metadata at query time. The map key represents the order in which BackendMetastores should be evaluated to resolve database names at query time and should be greater than or equal to zero. A BackendMetastore with a lower number will be evaluated before a BackendMetastore with a higher number.
               Structure is documented below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] effective_labels: All of labels (key/value pairs) present on the resource in GCP, including the labels configured through Pulumi, other clients and services.
        :param pulumi.Input[str] endpoint_uri: The URI of the endpoint used to access the metastore federation.
        :param pulumi.Input[str] federation_id: The ID of the metastore federation. The id must contain only letters (a-z, A-Z), numbers (0-9), underscores (_),
               and hyphens (-). Cannot begin or end with underscore or hyphen. Must consist of between
               3 and 63 characters.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: User-defined labels for the metastore federation. **Note**: This field is non-authoritative, and will only manage the
               labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the
               resource.
        :param pulumi.Input[str] location: The location where the metastore federation should reside.
        :param pulumi.Input[str] name: The relative resource name of the metastore federation.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] pulumi_labels: The combination of labels configured directly on the resource
               and default labels configured on the provider.
        :param pulumi.Input[str] state: The current state of the metastore federation.
        :param pulumi.Input[str] state_message: Additional information about the current state of the metastore federation, if available.
        :param pulumi.Input[str] uid: The globally unique resource identifier of the metastore federation.
        :param pulumi.Input[str] version: The Apache Hive metastore version of the federation. All backend metastore versions must be compatible with the federation version.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _MetastoreFederationState.__new__(_MetastoreFederationState)

        __props__.__dict__["backend_metastores"] = backend_metastores
        __props__.__dict__["effective_labels"] = effective_labels
        __props__.__dict__["endpoint_uri"] = endpoint_uri
        __props__.__dict__["federation_id"] = federation_id
        __props__.__dict__["labels"] = labels
        __props__.__dict__["location"] = location
        __props__.__dict__["name"] = name
        __props__.__dict__["project"] = project
        __props__.__dict__["pulumi_labels"] = pulumi_labels
        __props__.__dict__["state"] = state
        __props__.__dict__["state_message"] = state_message
        __props__.__dict__["uid"] = uid
        __props__.__dict__["version"] = version
        return MetastoreFederation(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="backendMetastores")
    def backend_metastores(self) -> pulumi.Output[Sequence['outputs.MetastoreFederationBackendMetastore']]:
        """
        A map from BackendMetastore rank to BackendMetastores from which the federation service serves metadata at query time. The map key represents the order in which BackendMetastores should be evaluated to resolve database names at query time and should be greater than or equal to zero. A BackendMetastore with a lower number will be evaluated before a BackendMetastore with a higher number.
        Structure is documented below.
        """
        return pulumi.get(self, "backend_metastores")

    @property
    @pulumi.getter(name="effectiveLabels")
    def effective_labels(self) -> pulumi.Output[Mapping[str, str]]:
        """
        All of labels (key/value pairs) present on the resource in GCP, including the labels configured through Pulumi, other clients and services.
        """
        return pulumi.get(self, "effective_labels")

    @property
    @pulumi.getter(name="endpointUri")
    def endpoint_uri(self) -> pulumi.Output[str]:
        """
        The URI of the endpoint used to access the metastore federation.
        """
        return pulumi.get(self, "endpoint_uri")

    @property
    @pulumi.getter(name="federationId")
    def federation_id(self) -> pulumi.Output[str]:
        """
        The ID of the metastore federation. The id must contain only letters (a-z, A-Z), numbers (0-9), underscores (_),
        and hyphens (-). Cannot begin or end with underscore or hyphen. Must consist of between
        3 and 63 characters.
        """
        return pulumi.get(self, "federation_id")

    @property
    @pulumi.getter
    def labels(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        User-defined labels for the metastore federation. **Note**: This field is non-authoritative, and will only manage the
        labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the
        resource.
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        The location where the metastore federation should reside.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The relative resource name of the metastore federation.
        """
        return pulumi.get(self, "name")

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
        The current state of the metastore federation.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter(name="stateMessage")
    def state_message(self) -> pulumi.Output[str]:
        """
        Additional information about the current state of the metastore federation, if available.
        """
        return pulumi.get(self, "state_message")

    @property
    @pulumi.getter
    def uid(self) -> pulumi.Output[str]:
        """
        The globally unique resource identifier of the metastore federation.
        """
        return pulumi.get(self, "uid")

    @property
    @pulumi.getter
    def version(self) -> pulumi.Output[str]:
        """
        The Apache Hive metastore version of the federation. All backend metastore versions must be compatible with the federation version.
        """
        return pulumi.get(self, "version")

