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

__all__ = ['AiTensorboardArgs', 'AiTensorboard']

@pulumi.input_type
class AiTensorboardArgs:
    def __init__(__self__, *,
                 display_name: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 encryption_spec: Optional[pulumi.Input['AiTensorboardEncryptionSpecArgs']] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a AiTensorboard resource.
        :param pulumi.Input[str] display_name: User provided name of this Tensorboard.
               
               
               - - -
        :param pulumi.Input[str] description: Description of this Tensorboard.
        :param pulumi.Input['AiTensorboardEncryptionSpecArgs'] encryption_spec: Customer-managed encryption key spec for a Tensorboard. If set, this Tensorboard and all sub-resources of this Tensorboard will be secured by this key.
               Structure is documented below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: The labels with user-defined metadata to organize your Tensorboards.
               
               **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
               Please refer to the field `effective_labels` for all of the labels present on the resource.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: The region of the tensorboard. eg us-central1
        """
        pulumi.set(__self__, "display_name", display_name)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if encryption_spec is not None:
            pulumi.set(__self__, "encryption_spec", encryption_spec)
        if labels is not None:
            pulumi.set(__self__, "labels", labels)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if region is not None:
            pulumi.set(__self__, "region", region)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Input[str]:
        """
        User provided name of this Tensorboard.


        - - -
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of this Tensorboard.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="encryptionSpec")
    def encryption_spec(self) -> Optional[pulumi.Input['AiTensorboardEncryptionSpecArgs']]:
        """
        Customer-managed encryption key spec for a Tensorboard. If set, this Tensorboard and all sub-resources of this Tensorboard will be secured by this key.
        Structure is documented below.
        """
        return pulumi.get(self, "encryption_spec")

    @encryption_spec.setter
    def encryption_spec(self, value: Optional[pulumi.Input['AiTensorboardEncryptionSpecArgs']]):
        pulumi.set(self, "encryption_spec", value)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        The labels with user-defined metadata to organize your Tensorboards.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field `effective_labels` for all of the labels present on the resource.
        """
        return pulumi.get(self, "labels")

    @labels.setter
    def labels(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "labels", value)

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
        The region of the tensorboard. eg us-central1
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "region", value)


@pulumi.input_type
class _AiTensorboardState:
    def __init__(__self__, *,
                 blob_storage_path_prefix: Optional[pulumi.Input[str]] = None,
                 create_time: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 effective_labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 encryption_spec: Optional[pulumi.Input['AiTensorboardEncryptionSpecArgs']] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 pulumi_labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 run_count: Optional[pulumi.Input[str]] = None,
                 update_time: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering AiTensorboard resources.
        :param pulumi.Input[str] blob_storage_path_prefix: Consumer project Cloud Storage path prefix used to store blob data, which can either be a bucket or directory. Does not end with a '/'.
        :param pulumi.Input[str] create_time: The timestamp of when the Tensorboard was created in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits.
        :param pulumi.Input[str] description: Description of this Tensorboard.
        :param pulumi.Input[str] display_name: User provided name of this Tensorboard.
               
               
               - - -
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] effective_labels: All of labels (key/value pairs) present on the resource in GCP, including the labels configured through Pulumi, other clients and services.
        :param pulumi.Input['AiTensorboardEncryptionSpecArgs'] encryption_spec: Customer-managed encryption key spec for a Tensorboard. If set, this Tensorboard and all sub-resources of this Tensorboard will be secured by this key.
               Structure is documented below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: The labels with user-defined metadata to organize your Tensorboards.
               
               **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
               Please refer to the field `effective_labels` for all of the labels present on the resource.
        :param pulumi.Input[str] name: Name of the Tensorboard.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] pulumi_labels: The combination of labels configured directly on the resource
               and default labels configured on the provider.
        :param pulumi.Input[str] region: The region of the tensorboard. eg us-central1
        :param pulumi.Input[str] run_count: The number of Runs stored in this Tensorboard.
        :param pulumi.Input[str] update_time: The timestamp of when the Tensorboard was last updated in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits.
        """
        if blob_storage_path_prefix is not None:
            pulumi.set(__self__, "blob_storage_path_prefix", blob_storage_path_prefix)
        if create_time is not None:
            pulumi.set(__self__, "create_time", create_time)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if effective_labels is not None:
            pulumi.set(__self__, "effective_labels", effective_labels)
        if encryption_spec is not None:
            pulumi.set(__self__, "encryption_spec", encryption_spec)
        if labels is not None:
            pulumi.set(__self__, "labels", labels)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if pulumi_labels is not None:
            pulumi.set(__self__, "pulumi_labels", pulumi_labels)
        if region is not None:
            pulumi.set(__self__, "region", region)
        if run_count is not None:
            pulumi.set(__self__, "run_count", run_count)
        if update_time is not None:
            pulumi.set(__self__, "update_time", update_time)

    @property
    @pulumi.getter(name="blobStoragePathPrefix")
    def blob_storage_path_prefix(self) -> Optional[pulumi.Input[str]]:
        """
        Consumer project Cloud Storage path prefix used to store blob data, which can either be a bucket or directory. Does not end with a '/'.
        """
        return pulumi.get(self, "blob_storage_path_prefix")

    @blob_storage_path_prefix.setter
    def blob_storage_path_prefix(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "blob_storage_path_prefix", value)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> Optional[pulumi.Input[str]]:
        """
        The timestamp of when the Tensorboard was created in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits.
        """
        return pulumi.get(self, "create_time")

    @create_time.setter
    def create_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "create_time", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of this Tensorboard.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        User provided name of this Tensorboard.


        - - -
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
    @pulumi.getter(name="encryptionSpec")
    def encryption_spec(self) -> Optional[pulumi.Input['AiTensorboardEncryptionSpecArgs']]:
        """
        Customer-managed encryption key spec for a Tensorboard. If set, this Tensorboard and all sub-resources of this Tensorboard will be secured by this key.
        Structure is documented below.
        """
        return pulumi.get(self, "encryption_spec")

    @encryption_spec.setter
    def encryption_spec(self, value: Optional[pulumi.Input['AiTensorboardEncryptionSpecArgs']]):
        pulumi.set(self, "encryption_spec", value)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        The labels with user-defined metadata to organize your Tensorboards.

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
        Name of the Tensorboard.
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
    @pulumi.getter
    def region(self) -> Optional[pulumi.Input[str]]:
        """
        The region of the tensorboard. eg us-central1
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "region", value)

    @property
    @pulumi.getter(name="runCount")
    def run_count(self) -> Optional[pulumi.Input[str]]:
        """
        The number of Runs stored in this Tensorboard.
        """
        return pulumi.get(self, "run_count")

    @run_count.setter
    def run_count(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "run_count", value)

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> Optional[pulumi.Input[str]]:
        """
        The timestamp of when the Tensorboard was last updated in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits.
        """
        return pulumi.get(self, "update_time")

    @update_time.setter
    def update_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "update_time", value)


class AiTensorboard(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 encryption_spec: Optional[pulumi.Input[pulumi.InputType['AiTensorboardEncryptionSpecArgs']]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Tensorboard is a physical database that stores users' training metrics. A default Tensorboard is provided in each region of a GCP project. If needed users can also create extra Tensorboards in their projects.

        To get more information about Tensorboard, see:

        * [API documentation](https://cloud.google.com/vertex-ai/docs/reference/rest/v1/projects.locations.tensorboards)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/vertex-ai/docs)

        ## Example Usage

        ### Vertex Ai Tensorboard

        ```python
        import pulumi
        import pulumi_gcp as gcp

        tensorboard = gcp.vertex.AiTensorboard("tensorboard",
            display_name="terraform",
            description="sample description",
            labels={
                "key1": "value1",
                "key2": "value2",
            },
            region="us-central1")
        ```
        ### Vertex Ai Tensorboard Full

        ```python
        import pulumi
        import pulumi_gcp as gcp

        project = gcp.organizations.get_project()
        crypto_key = gcp.kms.CryptoKeyIAMMember("crypto_key",
            crypto_key_id="kms-name",
            role="roles/cloudkms.cryptoKeyEncrypterDecrypter",
            member=f"serviceAccount:service-{project.number}@gcp-sa-aiplatform.iam.gserviceaccount.com")
        tensorboard = gcp.vertex.AiTensorboard("tensorboard",
            display_name="terraform",
            description="sample description",
            labels={
                "key1": "value1",
                "key2": "value2",
            },
            region="us-central1",
            encryption_spec=gcp.vertex.AiTensorboardEncryptionSpecArgs(
                kms_key_name="kms-name",
            ),
            opts=pulumi.ResourceOptions(depends_on=[crypto_key]))
        ```

        ## Import

        Tensorboard can be imported using any of these accepted formats:

        * `projects/{{project}}/locations/{{region}}/tensorboards/{{name}}`

        * `{{project}}/{{region}}/{{name}}`

        * `{{region}}/{{name}}`

        * `{{name}}`

        When using the `pulumi import` command, Tensorboard can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:vertex/aiTensorboard:AiTensorboard default projects/{{project}}/locations/{{region}}/tensorboards/{{name}}
        ```

        ```sh
        $ pulumi import gcp:vertex/aiTensorboard:AiTensorboard default {{project}}/{{region}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:vertex/aiTensorboard:AiTensorboard default {{region}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:vertex/aiTensorboard:AiTensorboard default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: Description of this Tensorboard.
        :param pulumi.Input[str] display_name: User provided name of this Tensorboard.
               
               
               - - -
        :param pulumi.Input[pulumi.InputType['AiTensorboardEncryptionSpecArgs']] encryption_spec: Customer-managed encryption key spec for a Tensorboard. If set, this Tensorboard and all sub-resources of this Tensorboard will be secured by this key.
               Structure is documented below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: The labels with user-defined metadata to organize your Tensorboards.
               
               **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
               Please refer to the field `effective_labels` for all of the labels present on the resource.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: The region of the tensorboard. eg us-central1
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AiTensorboardArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Tensorboard is a physical database that stores users' training metrics. A default Tensorboard is provided in each region of a GCP project. If needed users can also create extra Tensorboards in their projects.

        To get more information about Tensorboard, see:

        * [API documentation](https://cloud.google.com/vertex-ai/docs/reference/rest/v1/projects.locations.tensorboards)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/vertex-ai/docs)

        ## Example Usage

        ### Vertex Ai Tensorboard

        ```python
        import pulumi
        import pulumi_gcp as gcp

        tensorboard = gcp.vertex.AiTensorboard("tensorboard",
            display_name="terraform",
            description="sample description",
            labels={
                "key1": "value1",
                "key2": "value2",
            },
            region="us-central1")
        ```
        ### Vertex Ai Tensorboard Full

        ```python
        import pulumi
        import pulumi_gcp as gcp

        project = gcp.organizations.get_project()
        crypto_key = gcp.kms.CryptoKeyIAMMember("crypto_key",
            crypto_key_id="kms-name",
            role="roles/cloudkms.cryptoKeyEncrypterDecrypter",
            member=f"serviceAccount:service-{project.number}@gcp-sa-aiplatform.iam.gserviceaccount.com")
        tensorboard = gcp.vertex.AiTensorboard("tensorboard",
            display_name="terraform",
            description="sample description",
            labels={
                "key1": "value1",
                "key2": "value2",
            },
            region="us-central1",
            encryption_spec=gcp.vertex.AiTensorboardEncryptionSpecArgs(
                kms_key_name="kms-name",
            ),
            opts=pulumi.ResourceOptions(depends_on=[crypto_key]))
        ```

        ## Import

        Tensorboard can be imported using any of these accepted formats:

        * `projects/{{project}}/locations/{{region}}/tensorboards/{{name}}`

        * `{{project}}/{{region}}/{{name}}`

        * `{{region}}/{{name}}`

        * `{{name}}`

        When using the `pulumi import` command, Tensorboard can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:vertex/aiTensorboard:AiTensorboard default projects/{{project}}/locations/{{region}}/tensorboards/{{name}}
        ```

        ```sh
        $ pulumi import gcp:vertex/aiTensorboard:AiTensorboard default {{project}}/{{region}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:vertex/aiTensorboard:AiTensorboard default {{region}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:vertex/aiTensorboard:AiTensorboard default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param AiTensorboardArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AiTensorboardArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 encryption_spec: Optional[pulumi.Input[pulumi.InputType['AiTensorboardEncryptionSpecArgs']]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AiTensorboardArgs.__new__(AiTensorboardArgs)

            __props__.__dict__["description"] = description
            if display_name is None and not opts.urn:
                raise TypeError("Missing required property 'display_name'")
            __props__.__dict__["display_name"] = display_name
            __props__.__dict__["encryption_spec"] = encryption_spec
            __props__.__dict__["labels"] = labels
            __props__.__dict__["project"] = project
            __props__.__dict__["region"] = region
            __props__.__dict__["blob_storage_path_prefix"] = None
            __props__.__dict__["create_time"] = None
            __props__.__dict__["effective_labels"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["pulumi_labels"] = None
            __props__.__dict__["run_count"] = None
            __props__.__dict__["update_time"] = None
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["effectiveLabels", "pulumiLabels"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(AiTensorboard, __self__).__init__(
            'gcp:vertex/aiTensorboard:AiTensorboard',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            blob_storage_path_prefix: Optional[pulumi.Input[str]] = None,
            create_time: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            display_name: Optional[pulumi.Input[str]] = None,
            effective_labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            encryption_spec: Optional[pulumi.Input[pulumi.InputType['AiTensorboardEncryptionSpecArgs']]] = None,
            labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            name: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None,
            pulumi_labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            region: Optional[pulumi.Input[str]] = None,
            run_count: Optional[pulumi.Input[str]] = None,
            update_time: Optional[pulumi.Input[str]] = None) -> 'AiTensorboard':
        """
        Get an existing AiTensorboard resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] blob_storage_path_prefix: Consumer project Cloud Storage path prefix used to store blob data, which can either be a bucket or directory. Does not end with a '/'.
        :param pulumi.Input[str] create_time: The timestamp of when the Tensorboard was created in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits.
        :param pulumi.Input[str] description: Description of this Tensorboard.
        :param pulumi.Input[str] display_name: User provided name of this Tensorboard.
               
               
               - - -
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] effective_labels: All of labels (key/value pairs) present on the resource in GCP, including the labels configured through Pulumi, other clients and services.
        :param pulumi.Input[pulumi.InputType['AiTensorboardEncryptionSpecArgs']] encryption_spec: Customer-managed encryption key spec for a Tensorboard. If set, this Tensorboard and all sub-resources of this Tensorboard will be secured by this key.
               Structure is documented below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: The labels with user-defined metadata to organize your Tensorboards.
               
               **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
               Please refer to the field `effective_labels` for all of the labels present on the resource.
        :param pulumi.Input[str] name: Name of the Tensorboard.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] pulumi_labels: The combination of labels configured directly on the resource
               and default labels configured on the provider.
        :param pulumi.Input[str] region: The region of the tensorboard. eg us-central1
        :param pulumi.Input[str] run_count: The number of Runs stored in this Tensorboard.
        :param pulumi.Input[str] update_time: The timestamp of when the Tensorboard was last updated in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AiTensorboardState.__new__(_AiTensorboardState)

        __props__.__dict__["blob_storage_path_prefix"] = blob_storage_path_prefix
        __props__.__dict__["create_time"] = create_time
        __props__.__dict__["description"] = description
        __props__.__dict__["display_name"] = display_name
        __props__.__dict__["effective_labels"] = effective_labels
        __props__.__dict__["encryption_spec"] = encryption_spec
        __props__.__dict__["labels"] = labels
        __props__.__dict__["name"] = name
        __props__.__dict__["project"] = project
        __props__.__dict__["pulumi_labels"] = pulumi_labels
        __props__.__dict__["region"] = region
        __props__.__dict__["run_count"] = run_count
        __props__.__dict__["update_time"] = update_time
        return AiTensorboard(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="blobStoragePathPrefix")
    def blob_storage_path_prefix(self) -> pulumi.Output[str]:
        """
        Consumer project Cloud Storage path prefix used to store blob data, which can either be a bucket or directory. Does not end with a '/'.
        """
        return pulumi.get(self, "blob_storage_path_prefix")

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> pulumi.Output[str]:
        """
        The timestamp of when the Tensorboard was created in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits.
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Description of this Tensorboard.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[str]:
        """
        User provided name of this Tensorboard.


        - - -
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
    @pulumi.getter(name="encryptionSpec")
    def encryption_spec(self) -> pulumi.Output[Optional['outputs.AiTensorboardEncryptionSpec']]:
        """
        Customer-managed encryption key spec for a Tensorboard. If set, this Tensorboard and all sub-resources of this Tensorboard will be secured by this key.
        Structure is documented below.
        """
        return pulumi.get(self, "encryption_spec")

    @property
    @pulumi.getter
    def labels(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        The labels with user-defined metadata to organize your Tensorboards.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field `effective_labels` for all of the labels present on the resource.
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the Tensorboard.
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
    @pulumi.getter
    def region(self) -> pulumi.Output[str]:
        """
        The region of the tensorboard. eg us-central1
        """
        return pulumi.get(self, "region")

    @property
    @pulumi.getter(name="runCount")
    def run_count(self) -> pulumi.Output[str]:
        """
        The number of Runs stored in this Tensorboard.
        """
        return pulumi.get(self, "run_count")

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> pulumi.Output[str]:
        """
        The timestamp of when the Tensorboard was last updated in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits.
        """
        return pulumi.get(self, "update_time")

