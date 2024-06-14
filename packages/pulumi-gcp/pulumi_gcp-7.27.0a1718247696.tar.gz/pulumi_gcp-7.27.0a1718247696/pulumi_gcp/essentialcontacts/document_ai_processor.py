# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['DocumentAiProcessorArgs', 'DocumentAiProcessor']

@pulumi.input_type
class DocumentAiProcessorArgs:
    def __init__(__self__, *,
                 display_name: pulumi.Input[str],
                 location: pulumi.Input[str],
                 type: pulumi.Input[str],
                 kms_key_name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a DocumentAiProcessor resource.
        :param pulumi.Input[str] display_name: The display name. Must be unique.
        :param pulumi.Input[str] location: The location of the resource.
               
               
               - - -
        :param pulumi.Input[str] type: The type of processor. For possible types see the [official list](https://cloud.google.com/document-ai/docs/reference/rest/v1/projects.locations/fetchProcessorTypes#google.cloud.documentai.v1.DocumentProcessorService.FetchProcessorTypes)
        :param pulumi.Input[str] kms_key_name: The KMS key used for encryption/decryption in CMEK scenarios. See https://cloud.google.com/security-key-management.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        """
        pulumi.set(__self__, "display_name", display_name)
        pulumi.set(__self__, "location", location)
        pulumi.set(__self__, "type", type)
        if kms_key_name is not None:
            pulumi.set(__self__, "kms_key_name", kms_key_name)
        if project is not None:
            pulumi.set(__self__, "project", project)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Input[str]:
        """
        The display name. Must be unique.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter
    def location(self) -> pulumi.Input[str]:
        """
        The location of the resource.


        - - -
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: pulumi.Input[str]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        The type of processor. For possible types see the [official list](https://cloud.google.com/document-ai/docs/reference/rest/v1/projects.locations/fetchProcessorTypes#google.cloud.documentai.v1.DocumentProcessorService.FetchProcessorTypes)
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="kmsKeyName")
    def kms_key_name(self) -> Optional[pulumi.Input[str]]:
        """
        The KMS key used for encryption/decryption in CMEK scenarios. See https://cloud.google.com/security-key-management.
        """
        return pulumi.get(self, "kms_key_name")

    @kms_key_name.setter
    def kms_key_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kms_key_name", value)

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
class _DocumentAiProcessorState:
    def __init__(__self__, *,
                 display_name: Optional[pulumi.Input[str]] = None,
                 kms_key_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering DocumentAiProcessor resources.
        :param pulumi.Input[str] display_name: The display name. Must be unique.
        :param pulumi.Input[str] kms_key_name: The KMS key used for encryption/decryption in CMEK scenarios. See https://cloud.google.com/security-key-management.
        :param pulumi.Input[str] location: The location of the resource.
               
               
               - - -
        :param pulumi.Input[str] name: The resource name of the processor.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] type: The type of processor. For possible types see the [official list](https://cloud.google.com/document-ai/docs/reference/rest/v1/projects.locations/fetchProcessorTypes#google.cloud.documentai.v1.DocumentProcessorService.FetchProcessorTypes)
        """
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if kms_key_name is not None:
            pulumi.set(__self__, "kms_key_name", kms_key_name)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        The display name. Must be unique.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter(name="kmsKeyName")
    def kms_key_name(self) -> Optional[pulumi.Input[str]]:
        """
        The KMS key used for encryption/decryption in CMEK scenarios. See https://cloud.google.com/security-key-management.
        """
        return pulumi.get(self, "kms_key_name")

    @kms_key_name.setter
    def kms_key_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kms_key_name", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The location of the resource.


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
        The resource name of the processor.
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
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of processor. For possible types see the [official list](https://cloud.google.com/document-ai/docs/reference/rest/v1/projects.locations/fetchProcessorTypes#google.cloud.documentai.v1.DocumentProcessorService.FetchProcessorTypes)
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)


class DocumentAiProcessor(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 kms_key_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        The first-class citizen for Document AI. Each processor defines how to extract structural information from a document.

        To get more information about Processor, see:

        * [API documentation](https://cloud.google.com/document-ai/docs/reference/rest/v1/projects.locations.processors)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/document-ai/docs/overview)

        ## Example Usage

        ### Documentai Processor

        ```python
        import pulumi
        import pulumi_gcp as gcp

        processor = gcp.essentialcontacts.DocumentAiProcessor("processor",
            location="us",
            display_name="test-processor",
            type="OCR_PROCESSOR")
        ```

        ## Import

        Processor can be imported using any of these accepted formats:

        * `projects/{{project}}/locations/{{location}}/processors/{{name}}`

        * `{{project}}/{{location}}/{{name}}`

        * `{{location}}/{{name}}`

        When using the `pulumi import` command, Processor can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:essentialcontacts/documentAiProcessor:DocumentAiProcessor default projects/{{project}}/locations/{{location}}/processors/{{name}}
        ```

        ```sh
        $ pulumi import gcp:essentialcontacts/documentAiProcessor:DocumentAiProcessor default {{project}}/{{location}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:essentialcontacts/documentAiProcessor:DocumentAiProcessor default {{location}}/{{name}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] display_name: The display name. Must be unique.
        :param pulumi.Input[str] kms_key_name: The KMS key used for encryption/decryption in CMEK scenarios. See https://cloud.google.com/security-key-management.
        :param pulumi.Input[str] location: The location of the resource.
               
               
               - - -
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] type: The type of processor. For possible types see the [official list](https://cloud.google.com/document-ai/docs/reference/rest/v1/projects.locations/fetchProcessorTypes#google.cloud.documentai.v1.DocumentProcessorService.FetchProcessorTypes)
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DocumentAiProcessorArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The first-class citizen for Document AI. Each processor defines how to extract structural information from a document.

        To get more information about Processor, see:

        * [API documentation](https://cloud.google.com/document-ai/docs/reference/rest/v1/projects.locations.processors)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/document-ai/docs/overview)

        ## Example Usage

        ### Documentai Processor

        ```python
        import pulumi
        import pulumi_gcp as gcp

        processor = gcp.essentialcontacts.DocumentAiProcessor("processor",
            location="us",
            display_name="test-processor",
            type="OCR_PROCESSOR")
        ```

        ## Import

        Processor can be imported using any of these accepted formats:

        * `projects/{{project}}/locations/{{location}}/processors/{{name}}`

        * `{{project}}/{{location}}/{{name}}`

        * `{{location}}/{{name}}`

        When using the `pulumi import` command, Processor can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:essentialcontacts/documentAiProcessor:DocumentAiProcessor default projects/{{project}}/locations/{{location}}/processors/{{name}}
        ```

        ```sh
        $ pulumi import gcp:essentialcontacts/documentAiProcessor:DocumentAiProcessor default {{project}}/{{location}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:essentialcontacts/documentAiProcessor:DocumentAiProcessor default {{location}}/{{name}}
        ```

        :param str resource_name: The name of the resource.
        :param DocumentAiProcessorArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DocumentAiProcessorArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 kms_key_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DocumentAiProcessorArgs.__new__(DocumentAiProcessorArgs)

            if display_name is None and not opts.urn:
                raise TypeError("Missing required property 'display_name'")
            __props__.__dict__["display_name"] = display_name
            __props__.__dict__["kms_key_name"] = kms_key_name
            if location is None and not opts.urn:
                raise TypeError("Missing required property 'location'")
            __props__.__dict__["location"] = location
            __props__.__dict__["project"] = project
            if type is None and not opts.urn:
                raise TypeError("Missing required property 'type'")
            __props__.__dict__["type"] = type
            __props__.__dict__["name"] = None
        super(DocumentAiProcessor, __self__).__init__(
            'gcp:essentialcontacts/documentAiProcessor:DocumentAiProcessor',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            display_name: Optional[pulumi.Input[str]] = None,
            kms_key_name: Optional[pulumi.Input[str]] = None,
            location: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None,
            type: Optional[pulumi.Input[str]] = None) -> 'DocumentAiProcessor':
        """
        Get an existing DocumentAiProcessor resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] display_name: The display name. Must be unique.
        :param pulumi.Input[str] kms_key_name: The KMS key used for encryption/decryption in CMEK scenarios. See https://cloud.google.com/security-key-management.
        :param pulumi.Input[str] location: The location of the resource.
               
               
               - - -
        :param pulumi.Input[str] name: The resource name of the processor.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] type: The type of processor. For possible types see the [official list](https://cloud.google.com/document-ai/docs/reference/rest/v1/projects.locations/fetchProcessorTypes#google.cloud.documentai.v1.DocumentProcessorService.FetchProcessorTypes)
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _DocumentAiProcessorState.__new__(_DocumentAiProcessorState)

        __props__.__dict__["display_name"] = display_name
        __props__.__dict__["kms_key_name"] = kms_key_name
        __props__.__dict__["location"] = location
        __props__.__dict__["name"] = name
        __props__.__dict__["project"] = project
        __props__.__dict__["type"] = type
        return DocumentAiProcessor(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[str]:
        """
        The display name. Must be unique.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="kmsKeyName")
    def kms_key_name(self) -> pulumi.Output[Optional[str]]:
        """
        The KMS key used for encryption/decryption in CMEK scenarios. See https://cloud.google.com/security-key-management.
        """
        return pulumi.get(self, "kms_key_name")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The location of the resource.


        - - -
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The resource name of the processor.
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
    def type(self) -> pulumi.Output[str]:
        """
        The type of processor. For possible types see the [official list](https://cloud.google.com/document-ai/docs/reference/rest/v1/projects.locations/fetchProcessorTypes#google.cloud.documentai.v1.DocumentProcessorService.FetchProcessorTypes)
        """
        return pulumi.get(self, "type")

