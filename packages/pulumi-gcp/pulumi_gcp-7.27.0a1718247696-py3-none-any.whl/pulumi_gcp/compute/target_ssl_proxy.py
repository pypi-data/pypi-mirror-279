# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['TargetSSLProxyArgs', 'TargetSSLProxy']

@pulumi.input_type
class TargetSSLProxyArgs:
    def __init__(__self__, *,
                 backend_service: pulumi.Input[str],
                 certificate_map: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 proxy_header: Optional[pulumi.Input[str]] = None,
                 ssl_certificates: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 ssl_policy: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a TargetSSLProxy resource.
        :param pulumi.Input[str] backend_service: A reference to the BackendService resource.
               
               
               - - -
        :param pulumi.Input[str] certificate_map: A reference to the CertificateMap resource uri that identifies a certificate map
               associated with the given target proxy. This field can only be set for global target proxies.
               Accepted format is `//certificatemanager.googleapis.com/projects/{project}/locations/{location}/certificateMaps/{resourceName}`.
        :param pulumi.Input[str] description: An optional description of this resource.
        :param pulumi.Input[str] name: Name of the resource. Provided by the client when the resource is
               created. The name must be 1-63 characters long, and comply with
               RFC1035. Specifically, the name must be 1-63 characters long and match
               the regular expression `a-z?` which means the
               first character must be a lowercase letter, and all following
               characters must be a dash, lowercase letter, or digit, except the last
               character, which cannot be a dash.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] proxy_header: Specifies the type of proxy header to append before sending data to
               the backend.
               Default value is `NONE`.
               Possible values are: `NONE`, `PROXY_V1`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] ssl_certificates: A list of SslCertificate resources that are used to authenticate
               connections between users and the load balancer. At least one
               SSL certificate must be specified.
        :param pulumi.Input[str] ssl_policy: A reference to the SslPolicy resource that will be associated with
               the TargetSslProxy resource. If not set, the TargetSslProxy
               resource will not have any SSL policy configured.
        """
        pulumi.set(__self__, "backend_service", backend_service)
        if certificate_map is not None:
            pulumi.set(__self__, "certificate_map", certificate_map)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if proxy_header is not None:
            pulumi.set(__self__, "proxy_header", proxy_header)
        if ssl_certificates is not None:
            pulumi.set(__self__, "ssl_certificates", ssl_certificates)
        if ssl_policy is not None:
            pulumi.set(__self__, "ssl_policy", ssl_policy)

    @property
    @pulumi.getter(name="backendService")
    def backend_service(self) -> pulumi.Input[str]:
        """
        A reference to the BackendService resource.


        - - -
        """
        return pulumi.get(self, "backend_service")

    @backend_service.setter
    def backend_service(self, value: pulumi.Input[str]):
        pulumi.set(self, "backend_service", value)

    @property
    @pulumi.getter(name="certificateMap")
    def certificate_map(self) -> Optional[pulumi.Input[str]]:
        """
        A reference to the CertificateMap resource uri that identifies a certificate map
        associated with the given target proxy. This field can only be set for global target proxies.
        Accepted format is `//certificatemanager.googleapis.com/projects/{project}/locations/{location}/certificateMaps/{resourceName}`.
        """
        return pulumi.get(self, "certificate_map")

    @certificate_map.setter
    def certificate_map(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "certificate_map", value)

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
        Name of the resource. Provided by the client when the resource is
        created. The name must be 1-63 characters long, and comply with
        RFC1035. Specifically, the name must be 1-63 characters long and match
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
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter(name="proxyHeader")
    def proxy_header(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the type of proxy header to append before sending data to
        the backend.
        Default value is `NONE`.
        Possible values are: `NONE`, `PROXY_V1`.
        """
        return pulumi.get(self, "proxy_header")

    @proxy_header.setter
    def proxy_header(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "proxy_header", value)

    @property
    @pulumi.getter(name="sslCertificates")
    def ssl_certificates(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of SslCertificate resources that are used to authenticate
        connections between users and the load balancer. At least one
        SSL certificate must be specified.
        """
        return pulumi.get(self, "ssl_certificates")

    @ssl_certificates.setter
    def ssl_certificates(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "ssl_certificates", value)

    @property
    @pulumi.getter(name="sslPolicy")
    def ssl_policy(self) -> Optional[pulumi.Input[str]]:
        """
        A reference to the SslPolicy resource that will be associated with
        the TargetSslProxy resource. If not set, the TargetSslProxy
        resource will not have any SSL policy configured.
        """
        return pulumi.get(self, "ssl_policy")

    @ssl_policy.setter
    def ssl_policy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ssl_policy", value)


@pulumi.input_type
class _TargetSSLProxyState:
    def __init__(__self__, *,
                 backend_service: Optional[pulumi.Input[str]] = None,
                 certificate_map: Optional[pulumi.Input[str]] = None,
                 creation_timestamp: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 proxy_header: Optional[pulumi.Input[str]] = None,
                 proxy_id: Optional[pulumi.Input[int]] = None,
                 self_link: Optional[pulumi.Input[str]] = None,
                 ssl_certificates: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 ssl_policy: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering TargetSSLProxy resources.
        :param pulumi.Input[str] backend_service: A reference to the BackendService resource.
               
               
               - - -
        :param pulumi.Input[str] certificate_map: A reference to the CertificateMap resource uri that identifies a certificate map
               associated with the given target proxy. This field can only be set for global target proxies.
               Accepted format is `//certificatemanager.googleapis.com/projects/{project}/locations/{location}/certificateMaps/{resourceName}`.
        :param pulumi.Input[str] creation_timestamp: Creation timestamp in RFC3339 text format.
        :param pulumi.Input[str] description: An optional description of this resource.
        :param pulumi.Input[str] name: Name of the resource. Provided by the client when the resource is
               created. The name must be 1-63 characters long, and comply with
               RFC1035. Specifically, the name must be 1-63 characters long and match
               the regular expression `a-z?` which means the
               first character must be a lowercase letter, and all following
               characters must be a dash, lowercase letter, or digit, except the last
               character, which cannot be a dash.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] proxy_header: Specifies the type of proxy header to append before sending data to
               the backend.
               Default value is `NONE`.
               Possible values are: `NONE`, `PROXY_V1`.
        :param pulumi.Input[int] proxy_id: The unique identifier for the resource.
        :param pulumi.Input[str] self_link: The URI of the created resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] ssl_certificates: A list of SslCertificate resources that are used to authenticate
               connections between users and the load balancer. At least one
               SSL certificate must be specified.
        :param pulumi.Input[str] ssl_policy: A reference to the SslPolicy resource that will be associated with
               the TargetSslProxy resource. If not set, the TargetSslProxy
               resource will not have any SSL policy configured.
        """
        if backend_service is not None:
            pulumi.set(__self__, "backend_service", backend_service)
        if certificate_map is not None:
            pulumi.set(__self__, "certificate_map", certificate_map)
        if creation_timestamp is not None:
            pulumi.set(__self__, "creation_timestamp", creation_timestamp)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if proxy_header is not None:
            pulumi.set(__self__, "proxy_header", proxy_header)
        if proxy_id is not None:
            pulumi.set(__self__, "proxy_id", proxy_id)
        if self_link is not None:
            pulumi.set(__self__, "self_link", self_link)
        if ssl_certificates is not None:
            pulumi.set(__self__, "ssl_certificates", ssl_certificates)
        if ssl_policy is not None:
            pulumi.set(__self__, "ssl_policy", ssl_policy)

    @property
    @pulumi.getter(name="backendService")
    def backend_service(self) -> Optional[pulumi.Input[str]]:
        """
        A reference to the BackendService resource.


        - - -
        """
        return pulumi.get(self, "backend_service")

    @backend_service.setter
    def backend_service(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "backend_service", value)

    @property
    @pulumi.getter(name="certificateMap")
    def certificate_map(self) -> Optional[pulumi.Input[str]]:
        """
        A reference to the CertificateMap resource uri that identifies a certificate map
        associated with the given target proxy. This field can only be set for global target proxies.
        Accepted format is `//certificatemanager.googleapis.com/projects/{project}/locations/{location}/certificateMaps/{resourceName}`.
        """
        return pulumi.get(self, "certificate_map")

    @certificate_map.setter
    def certificate_map(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "certificate_map", value)

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
        Name of the resource. Provided by the client when the resource is
        created. The name must be 1-63 characters long, and comply with
        RFC1035. Specifically, the name must be 1-63 characters long and match
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
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter(name="proxyHeader")
    def proxy_header(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the type of proxy header to append before sending data to
        the backend.
        Default value is `NONE`.
        Possible values are: `NONE`, `PROXY_V1`.
        """
        return pulumi.get(self, "proxy_header")

    @proxy_header.setter
    def proxy_header(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "proxy_header", value)

    @property
    @pulumi.getter(name="proxyId")
    def proxy_id(self) -> Optional[pulumi.Input[int]]:
        """
        The unique identifier for the resource.
        """
        return pulumi.get(self, "proxy_id")

    @proxy_id.setter
    def proxy_id(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "proxy_id", value)

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
    @pulumi.getter(name="sslCertificates")
    def ssl_certificates(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of SslCertificate resources that are used to authenticate
        connections between users and the load balancer. At least one
        SSL certificate must be specified.
        """
        return pulumi.get(self, "ssl_certificates")

    @ssl_certificates.setter
    def ssl_certificates(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "ssl_certificates", value)

    @property
    @pulumi.getter(name="sslPolicy")
    def ssl_policy(self) -> Optional[pulumi.Input[str]]:
        """
        A reference to the SslPolicy resource that will be associated with
        the TargetSslProxy resource. If not set, the TargetSslProxy
        resource will not have any SSL policy configured.
        """
        return pulumi.get(self, "ssl_policy")

    @ssl_policy.setter
    def ssl_policy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ssl_policy", value)


class TargetSSLProxy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 backend_service: Optional[pulumi.Input[str]] = None,
                 certificate_map: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 proxy_header: Optional[pulumi.Input[str]] = None,
                 ssl_certificates: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 ssl_policy: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Represents a TargetSslProxy resource, which is used by one or more
        global forwarding rule to route incoming SSL requests to a backend
        service.

        To get more information about TargetSslProxy, see:

        * [API documentation](https://cloud.google.com/compute/docs/reference/v1/targetSslProxies)
        * How-to Guides
            * [Setting Up SSL proxy for Google Cloud Load Balancing](https://cloud.google.com/compute/docs/load-balancing/tcp-ssl/)

        ## Example Usage

        ### Target Ssl Proxy Basic

        ```python
        import pulumi
        import pulumi_gcp as gcp
        import pulumi_std as std

        default_ssl_certificate = gcp.compute.SSLCertificate("default",
            name="default-cert",
            private_key=std.file(input="path/to/private.key").result,
            certificate=std.file(input="path/to/certificate.crt").result)
        default_health_check = gcp.compute.HealthCheck("default",
            name="health-check",
            check_interval_sec=1,
            timeout_sec=1,
            tcp_health_check=gcp.compute.HealthCheckTcpHealthCheckArgs(
                port=443,
            ))
        default_backend_service = gcp.compute.BackendService("default",
            name="backend-service",
            protocol="SSL",
            health_checks=default_health_check.id)
        default = gcp.compute.TargetSSLProxy("default",
            name="test-proxy",
            backend_service=default_backend_service.id,
            ssl_certificates=[default_ssl_certificate.id])
        ```

        ## Import

        TargetSslProxy can be imported using any of these accepted formats:

        * `projects/{{project}}/global/targetSslProxies/{{name}}`

        * `{{project}}/{{name}}`

        * `{{name}}`

        When using the `pulumi import` command, TargetSslProxy can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:compute/targetSSLProxy:TargetSSLProxy default projects/{{project}}/global/targetSslProxies/{{name}}
        ```

        ```sh
        $ pulumi import gcp:compute/targetSSLProxy:TargetSSLProxy default {{project}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:compute/targetSSLProxy:TargetSSLProxy default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] backend_service: A reference to the BackendService resource.
               
               
               - - -
        :param pulumi.Input[str] certificate_map: A reference to the CertificateMap resource uri that identifies a certificate map
               associated with the given target proxy. This field can only be set for global target proxies.
               Accepted format is `//certificatemanager.googleapis.com/projects/{project}/locations/{location}/certificateMaps/{resourceName}`.
        :param pulumi.Input[str] description: An optional description of this resource.
        :param pulumi.Input[str] name: Name of the resource. Provided by the client when the resource is
               created. The name must be 1-63 characters long, and comply with
               RFC1035. Specifically, the name must be 1-63 characters long and match
               the regular expression `a-z?` which means the
               first character must be a lowercase letter, and all following
               characters must be a dash, lowercase letter, or digit, except the last
               character, which cannot be a dash.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] proxy_header: Specifies the type of proxy header to append before sending data to
               the backend.
               Default value is `NONE`.
               Possible values are: `NONE`, `PROXY_V1`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] ssl_certificates: A list of SslCertificate resources that are used to authenticate
               connections between users and the load balancer. At least one
               SSL certificate must be specified.
        :param pulumi.Input[str] ssl_policy: A reference to the SslPolicy resource that will be associated with
               the TargetSslProxy resource. If not set, the TargetSslProxy
               resource will not have any SSL policy configured.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: TargetSSLProxyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Represents a TargetSslProxy resource, which is used by one or more
        global forwarding rule to route incoming SSL requests to a backend
        service.

        To get more information about TargetSslProxy, see:

        * [API documentation](https://cloud.google.com/compute/docs/reference/v1/targetSslProxies)
        * How-to Guides
            * [Setting Up SSL proxy for Google Cloud Load Balancing](https://cloud.google.com/compute/docs/load-balancing/tcp-ssl/)

        ## Example Usage

        ### Target Ssl Proxy Basic

        ```python
        import pulumi
        import pulumi_gcp as gcp
        import pulumi_std as std

        default_ssl_certificate = gcp.compute.SSLCertificate("default",
            name="default-cert",
            private_key=std.file(input="path/to/private.key").result,
            certificate=std.file(input="path/to/certificate.crt").result)
        default_health_check = gcp.compute.HealthCheck("default",
            name="health-check",
            check_interval_sec=1,
            timeout_sec=1,
            tcp_health_check=gcp.compute.HealthCheckTcpHealthCheckArgs(
                port=443,
            ))
        default_backend_service = gcp.compute.BackendService("default",
            name="backend-service",
            protocol="SSL",
            health_checks=default_health_check.id)
        default = gcp.compute.TargetSSLProxy("default",
            name="test-proxy",
            backend_service=default_backend_service.id,
            ssl_certificates=[default_ssl_certificate.id])
        ```

        ## Import

        TargetSslProxy can be imported using any of these accepted formats:

        * `projects/{{project}}/global/targetSslProxies/{{name}}`

        * `{{project}}/{{name}}`

        * `{{name}}`

        When using the `pulumi import` command, TargetSslProxy can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:compute/targetSSLProxy:TargetSSLProxy default projects/{{project}}/global/targetSslProxies/{{name}}
        ```

        ```sh
        $ pulumi import gcp:compute/targetSSLProxy:TargetSSLProxy default {{project}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:compute/targetSSLProxy:TargetSSLProxy default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param TargetSSLProxyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(TargetSSLProxyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 backend_service: Optional[pulumi.Input[str]] = None,
                 certificate_map: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 proxy_header: Optional[pulumi.Input[str]] = None,
                 ssl_certificates: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 ssl_policy: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = TargetSSLProxyArgs.__new__(TargetSSLProxyArgs)

            if backend_service is None and not opts.urn:
                raise TypeError("Missing required property 'backend_service'")
            __props__.__dict__["backend_service"] = backend_service
            __props__.__dict__["certificate_map"] = certificate_map
            __props__.__dict__["description"] = description
            __props__.__dict__["name"] = name
            __props__.__dict__["project"] = project
            __props__.__dict__["proxy_header"] = proxy_header
            __props__.__dict__["ssl_certificates"] = ssl_certificates
            __props__.__dict__["ssl_policy"] = ssl_policy
            __props__.__dict__["creation_timestamp"] = None
            __props__.__dict__["proxy_id"] = None
            __props__.__dict__["self_link"] = None
        super(TargetSSLProxy, __self__).__init__(
            'gcp:compute/targetSSLProxy:TargetSSLProxy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            backend_service: Optional[pulumi.Input[str]] = None,
            certificate_map: Optional[pulumi.Input[str]] = None,
            creation_timestamp: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None,
            proxy_header: Optional[pulumi.Input[str]] = None,
            proxy_id: Optional[pulumi.Input[int]] = None,
            self_link: Optional[pulumi.Input[str]] = None,
            ssl_certificates: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            ssl_policy: Optional[pulumi.Input[str]] = None) -> 'TargetSSLProxy':
        """
        Get an existing TargetSSLProxy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] backend_service: A reference to the BackendService resource.
               
               
               - - -
        :param pulumi.Input[str] certificate_map: A reference to the CertificateMap resource uri that identifies a certificate map
               associated with the given target proxy. This field can only be set for global target proxies.
               Accepted format is `//certificatemanager.googleapis.com/projects/{project}/locations/{location}/certificateMaps/{resourceName}`.
        :param pulumi.Input[str] creation_timestamp: Creation timestamp in RFC3339 text format.
        :param pulumi.Input[str] description: An optional description of this resource.
        :param pulumi.Input[str] name: Name of the resource. Provided by the client when the resource is
               created. The name must be 1-63 characters long, and comply with
               RFC1035. Specifically, the name must be 1-63 characters long and match
               the regular expression `a-z?` which means the
               first character must be a lowercase letter, and all following
               characters must be a dash, lowercase letter, or digit, except the last
               character, which cannot be a dash.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] proxy_header: Specifies the type of proxy header to append before sending data to
               the backend.
               Default value is `NONE`.
               Possible values are: `NONE`, `PROXY_V1`.
        :param pulumi.Input[int] proxy_id: The unique identifier for the resource.
        :param pulumi.Input[str] self_link: The URI of the created resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] ssl_certificates: A list of SslCertificate resources that are used to authenticate
               connections between users and the load balancer. At least one
               SSL certificate must be specified.
        :param pulumi.Input[str] ssl_policy: A reference to the SslPolicy resource that will be associated with
               the TargetSslProxy resource. If not set, the TargetSslProxy
               resource will not have any SSL policy configured.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _TargetSSLProxyState.__new__(_TargetSSLProxyState)

        __props__.__dict__["backend_service"] = backend_service
        __props__.__dict__["certificate_map"] = certificate_map
        __props__.__dict__["creation_timestamp"] = creation_timestamp
        __props__.__dict__["description"] = description
        __props__.__dict__["name"] = name
        __props__.__dict__["project"] = project
        __props__.__dict__["proxy_header"] = proxy_header
        __props__.__dict__["proxy_id"] = proxy_id
        __props__.__dict__["self_link"] = self_link
        __props__.__dict__["ssl_certificates"] = ssl_certificates
        __props__.__dict__["ssl_policy"] = ssl_policy
        return TargetSSLProxy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="backendService")
    def backend_service(self) -> pulumi.Output[str]:
        """
        A reference to the BackendService resource.


        - - -
        """
        return pulumi.get(self, "backend_service")

    @property
    @pulumi.getter(name="certificateMap")
    def certificate_map(self) -> pulumi.Output[Optional[str]]:
        """
        A reference to the CertificateMap resource uri that identifies a certificate map
        associated with the given target proxy. This field can only be set for global target proxies.
        Accepted format is `//certificatemanager.googleapis.com/projects/{project}/locations/{location}/certificateMaps/{resourceName}`.
        """
        return pulumi.get(self, "certificate_map")

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
        Name of the resource. Provided by the client when the resource is
        created. The name must be 1-63 characters long, and comply with
        RFC1035. Specifically, the name must be 1-63 characters long and match
        the regular expression `a-z?` which means the
        first character must be a lowercase letter, and all following
        characters must be a dash, lowercase letter, or digit, except the last
        character, which cannot be a dash.
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
    @pulumi.getter(name="proxyHeader")
    def proxy_header(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the type of proxy header to append before sending data to
        the backend.
        Default value is `NONE`.
        Possible values are: `NONE`, `PROXY_V1`.
        """
        return pulumi.get(self, "proxy_header")

    @property
    @pulumi.getter(name="proxyId")
    def proxy_id(self) -> pulumi.Output[int]:
        """
        The unique identifier for the resource.
        """
        return pulumi.get(self, "proxy_id")

    @property
    @pulumi.getter(name="selfLink")
    def self_link(self) -> pulumi.Output[str]:
        """
        The URI of the created resource.
        """
        return pulumi.get(self, "self_link")

    @property
    @pulumi.getter(name="sslCertificates")
    def ssl_certificates(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        A list of SslCertificate resources that are used to authenticate
        connections between users and the load balancer. At least one
        SSL certificate must be specified.
        """
        return pulumi.get(self, "ssl_certificates")

    @property
    @pulumi.getter(name="sslPolicy")
    def ssl_policy(self) -> pulumi.Output[Optional[str]]:
        """
        A reference to the SslPolicy resource that will be associated with
        the TargetSslProxy resource. If not set, the TargetSslProxy
        resource will not have any SSL policy configured.
        """
        return pulumi.get(self, "ssl_policy")

