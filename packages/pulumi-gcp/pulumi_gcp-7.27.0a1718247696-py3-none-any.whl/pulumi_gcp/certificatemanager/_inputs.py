# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'CertificateIssuanceConfigCertificateAuthorityConfigArgs',
    'CertificateIssuanceConfigCertificateAuthorityConfigCertificateAuthorityServiceConfigArgs',
    'CertificateManagedArgs',
    'CertificateManagedAuthorizationAttemptInfoArgs',
    'CertificateManagedProvisioningIssueArgs',
    'CertificateMapGclbTargetArgs',
    'CertificateMapGclbTargetIpConfigArgs',
    'CertificateSelfManagedArgs',
    'DnsAuthorizationDnsResourceRecordArgs',
    'TrustConfigTrustStoreArgs',
    'TrustConfigTrustStoreIntermediateCaArgs',
    'TrustConfigTrustStoreTrustAnchorArgs',
]

@pulumi.input_type
class CertificateIssuanceConfigCertificateAuthorityConfigArgs:
    def __init__(__self__, *,
                 certificate_authority_service_config: Optional[pulumi.Input['CertificateIssuanceConfigCertificateAuthorityConfigCertificateAuthorityServiceConfigArgs']] = None):
        """
        :param pulumi.Input['CertificateIssuanceConfigCertificateAuthorityConfigCertificateAuthorityServiceConfigArgs'] certificate_authority_service_config: Defines a CertificateAuthorityServiceConfig.
               Structure is documented below.
        """
        if certificate_authority_service_config is not None:
            pulumi.set(__self__, "certificate_authority_service_config", certificate_authority_service_config)

    @property
    @pulumi.getter(name="certificateAuthorityServiceConfig")
    def certificate_authority_service_config(self) -> Optional[pulumi.Input['CertificateIssuanceConfigCertificateAuthorityConfigCertificateAuthorityServiceConfigArgs']]:
        """
        Defines a CertificateAuthorityServiceConfig.
        Structure is documented below.
        """
        return pulumi.get(self, "certificate_authority_service_config")

    @certificate_authority_service_config.setter
    def certificate_authority_service_config(self, value: Optional[pulumi.Input['CertificateIssuanceConfigCertificateAuthorityConfigCertificateAuthorityServiceConfigArgs']]):
        pulumi.set(self, "certificate_authority_service_config", value)


@pulumi.input_type
class CertificateIssuanceConfigCertificateAuthorityConfigCertificateAuthorityServiceConfigArgs:
    def __init__(__self__, *,
                 ca_pool: pulumi.Input[str]):
        """
        :param pulumi.Input[str] ca_pool: A CA pool resource used to issue a certificate.
               The CA pool string has a relative resource path following the form
               "projects/{project}/locations/{location}/caPools/{caPool}".
               
               - - -
        """
        pulumi.set(__self__, "ca_pool", ca_pool)

    @property
    @pulumi.getter(name="caPool")
    def ca_pool(self) -> pulumi.Input[str]:
        """
        A CA pool resource used to issue a certificate.
        The CA pool string has a relative resource path following the form
        "projects/{project}/locations/{location}/caPools/{caPool}".

        - - -
        """
        return pulumi.get(self, "ca_pool")

    @ca_pool.setter
    def ca_pool(self, value: pulumi.Input[str]):
        pulumi.set(self, "ca_pool", value)


@pulumi.input_type
class CertificateManagedArgs:
    def __init__(__self__, *,
                 authorization_attempt_infos: Optional[pulumi.Input[Sequence[pulumi.Input['CertificateManagedAuthorizationAttemptInfoArgs']]]] = None,
                 dns_authorizations: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 domains: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 issuance_config: Optional[pulumi.Input[str]] = None,
                 provisioning_issues: Optional[pulumi.Input[Sequence[pulumi.Input['CertificateManagedProvisioningIssueArgs']]]] = None,
                 state: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[Sequence[pulumi.Input['CertificateManagedAuthorizationAttemptInfoArgs']]] authorization_attempt_infos: (Output)
               Detailed state of the latest authorization attempt for each domain
               specified for this Managed Certificate.
               Structure is documented below.
               
               
               <a name="nested_provisioning_issue"></a>The `provisioning_issue` block contains:
        :param pulumi.Input[Sequence[pulumi.Input[str]]] dns_authorizations: Authorizations that will be used for performing domain authorization. Either issuanceConfig or dnsAuthorizations should be specificed, but not both.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] domains: The domains for which a managed SSL certificate will be generated.
               Wildcard domains are only supported with DNS challenge resolution
        :param pulumi.Input[str] issuance_config: The resource name for a CertificateIssuanceConfig used to configure private PKI certificates in the format projects/*/locations/*/certificateIssuanceConfigs/*.
               If this field is not set, the certificates will instead be publicly signed as documented at https://cloud.google.com/load-balancing/docs/ssl-certificates/google-managed-certs#caa.
               Either issuanceConfig or dnsAuthorizations should be specificed, but not both.
        :param pulumi.Input[Sequence[pulumi.Input['CertificateManagedProvisioningIssueArgs']]] provisioning_issues: (Output)
               Information about issues with provisioning this Managed Certificate.
               Structure is documented below.
        :param pulumi.Input[str] state: (Output)
               State of the domain for managed certificate issuance.
        """
        if authorization_attempt_infos is not None:
            pulumi.set(__self__, "authorization_attempt_infos", authorization_attempt_infos)
        if dns_authorizations is not None:
            pulumi.set(__self__, "dns_authorizations", dns_authorizations)
        if domains is not None:
            pulumi.set(__self__, "domains", domains)
        if issuance_config is not None:
            pulumi.set(__self__, "issuance_config", issuance_config)
        if provisioning_issues is not None:
            pulumi.set(__self__, "provisioning_issues", provisioning_issues)
        if state is not None:
            pulumi.set(__self__, "state", state)

    @property
    @pulumi.getter(name="authorizationAttemptInfos")
    def authorization_attempt_infos(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['CertificateManagedAuthorizationAttemptInfoArgs']]]]:
        """
        (Output)
        Detailed state of the latest authorization attempt for each domain
        specified for this Managed Certificate.
        Structure is documented below.


        <a name="nested_provisioning_issue"></a>The `provisioning_issue` block contains:
        """
        return pulumi.get(self, "authorization_attempt_infos")

    @authorization_attempt_infos.setter
    def authorization_attempt_infos(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['CertificateManagedAuthorizationAttemptInfoArgs']]]]):
        pulumi.set(self, "authorization_attempt_infos", value)

    @property
    @pulumi.getter(name="dnsAuthorizations")
    def dns_authorizations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Authorizations that will be used for performing domain authorization. Either issuanceConfig or dnsAuthorizations should be specificed, but not both.
        """
        return pulumi.get(self, "dns_authorizations")

    @dns_authorizations.setter
    def dns_authorizations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "dns_authorizations", value)

    @property
    @pulumi.getter
    def domains(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The domains for which a managed SSL certificate will be generated.
        Wildcard domains are only supported with DNS challenge resolution
        """
        return pulumi.get(self, "domains")

    @domains.setter
    def domains(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "domains", value)

    @property
    @pulumi.getter(name="issuanceConfig")
    def issuance_config(self) -> Optional[pulumi.Input[str]]:
        """
        The resource name for a CertificateIssuanceConfig used to configure private PKI certificates in the format projects/*/locations/*/certificateIssuanceConfigs/*.
        If this field is not set, the certificates will instead be publicly signed as documented at https://cloud.google.com/load-balancing/docs/ssl-certificates/google-managed-certs#caa.
        Either issuanceConfig or dnsAuthorizations should be specificed, but not both.
        """
        return pulumi.get(self, "issuance_config")

    @issuance_config.setter
    def issuance_config(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "issuance_config", value)

    @property
    @pulumi.getter(name="provisioningIssues")
    def provisioning_issues(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['CertificateManagedProvisioningIssueArgs']]]]:
        """
        (Output)
        Information about issues with provisioning this Managed Certificate.
        Structure is documented below.
        """
        return pulumi.get(self, "provisioning_issues")

    @provisioning_issues.setter
    def provisioning_issues(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['CertificateManagedProvisioningIssueArgs']]]]):
        pulumi.set(self, "provisioning_issues", value)

    @property
    @pulumi.getter
    def state(self) -> Optional[pulumi.Input[str]]:
        """
        (Output)
        State of the domain for managed certificate issuance.
        """
        return pulumi.get(self, "state")

    @state.setter
    def state(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "state", value)


@pulumi.input_type
class CertificateManagedAuthorizationAttemptInfoArgs:
    def __init__(__self__, *,
                 details: Optional[pulumi.Input[str]] = None,
                 domain: Optional[pulumi.Input[str]] = None,
                 failure_reason: Optional[pulumi.Input[str]] = None,
                 state: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] details: Human readable explanation for reaching the state. Provided to help
               address the configuration issues.
               Not guaranteed to be stable. For programmatic access use 'failure_reason' field.
        :param pulumi.Input[str] domain: Domain name of the authorization attempt.
        :param pulumi.Input[str] failure_reason: Reason for failure of the authorization attempt for the domain.
        :param pulumi.Input[str] state: State of the domain for managed certificate issuance.
        """
        if details is not None:
            pulumi.set(__self__, "details", details)
        if domain is not None:
            pulumi.set(__self__, "domain", domain)
        if failure_reason is not None:
            pulumi.set(__self__, "failure_reason", failure_reason)
        if state is not None:
            pulumi.set(__self__, "state", state)

    @property
    @pulumi.getter
    def details(self) -> Optional[pulumi.Input[str]]:
        """
        Human readable explanation for reaching the state. Provided to help
        address the configuration issues.
        Not guaranteed to be stable. For programmatic access use 'failure_reason' field.
        """
        return pulumi.get(self, "details")

    @details.setter
    def details(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "details", value)

    @property
    @pulumi.getter
    def domain(self) -> Optional[pulumi.Input[str]]:
        """
        Domain name of the authorization attempt.
        """
        return pulumi.get(self, "domain")

    @domain.setter
    def domain(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "domain", value)

    @property
    @pulumi.getter(name="failureReason")
    def failure_reason(self) -> Optional[pulumi.Input[str]]:
        """
        Reason for failure of the authorization attempt for the domain.
        """
        return pulumi.get(self, "failure_reason")

    @failure_reason.setter
    def failure_reason(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "failure_reason", value)

    @property
    @pulumi.getter
    def state(self) -> Optional[pulumi.Input[str]]:
        """
        State of the domain for managed certificate issuance.
        """
        return pulumi.get(self, "state")

    @state.setter
    def state(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "state", value)


@pulumi.input_type
class CertificateManagedProvisioningIssueArgs:
    def __init__(__self__, *,
                 details: Optional[pulumi.Input[str]] = None,
                 reason: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] details: Human readable explanation about the issue. Provided to help address
               the configuration issues.
               Not guaranteed to be stable. For programmatic access use 'reason' field.
        :param pulumi.Input[str] reason: Reason for provisioning failures.
        """
        if details is not None:
            pulumi.set(__self__, "details", details)
        if reason is not None:
            pulumi.set(__self__, "reason", reason)

    @property
    @pulumi.getter
    def details(self) -> Optional[pulumi.Input[str]]:
        """
        Human readable explanation about the issue. Provided to help address
        the configuration issues.
        Not guaranteed to be stable. For programmatic access use 'reason' field.
        """
        return pulumi.get(self, "details")

    @details.setter
    def details(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "details", value)

    @property
    @pulumi.getter
    def reason(self) -> Optional[pulumi.Input[str]]:
        """
        Reason for provisioning failures.
        """
        return pulumi.get(self, "reason")

    @reason.setter
    def reason(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "reason", value)


@pulumi.input_type
class CertificateMapGclbTargetArgs:
    def __init__(__self__, *,
                 ip_configs: Optional[pulumi.Input[Sequence[pulumi.Input['CertificateMapGclbTargetIpConfigArgs']]]] = None,
                 target_https_proxy: Optional[pulumi.Input[str]] = None,
                 target_ssl_proxy: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[Sequence[pulumi.Input['CertificateMapGclbTargetIpConfigArgs']]] ip_configs: An IP configuration where this Certificate Map is serving
               Structure is documented below.
        :param pulumi.Input[str] target_https_proxy: Proxy name must be in the format projects/*/locations/*/targetHttpsProxies/*.
               This field is part of a union field `target_proxy`: Only one of `targetHttpsProxy` or
               `targetSslProxy` may be set.
        :param pulumi.Input[str] target_ssl_proxy: Proxy name must be in the format projects/*/locations/*/targetSslProxies/*.
               This field is part of a union field `target_proxy`: Only one of `targetHttpsProxy` or
               `targetSslProxy` may be set.
        """
        if ip_configs is not None:
            pulumi.set(__self__, "ip_configs", ip_configs)
        if target_https_proxy is not None:
            pulumi.set(__self__, "target_https_proxy", target_https_proxy)
        if target_ssl_proxy is not None:
            pulumi.set(__self__, "target_ssl_proxy", target_ssl_proxy)

    @property
    @pulumi.getter(name="ipConfigs")
    def ip_configs(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['CertificateMapGclbTargetIpConfigArgs']]]]:
        """
        An IP configuration where this Certificate Map is serving
        Structure is documented below.
        """
        return pulumi.get(self, "ip_configs")

    @ip_configs.setter
    def ip_configs(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['CertificateMapGclbTargetIpConfigArgs']]]]):
        pulumi.set(self, "ip_configs", value)

    @property
    @pulumi.getter(name="targetHttpsProxy")
    def target_https_proxy(self) -> Optional[pulumi.Input[str]]:
        """
        Proxy name must be in the format projects/*/locations/*/targetHttpsProxies/*.
        This field is part of a union field `target_proxy`: Only one of `targetHttpsProxy` or
        `targetSslProxy` may be set.
        """
        return pulumi.get(self, "target_https_proxy")

    @target_https_proxy.setter
    def target_https_proxy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "target_https_proxy", value)

    @property
    @pulumi.getter(name="targetSslProxy")
    def target_ssl_proxy(self) -> Optional[pulumi.Input[str]]:
        """
        Proxy name must be in the format projects/*/locations/*/targetSslProxies/*.
        This field is part of a union field `target_proxy`: Only one of `targetHttpsProxy` or
        `targetSslProxy` may be set.
        """
        return pulumi.get(self, "target_ssl_proxy")

    @target_ssl_proxy.setter
    def target_ssl_proxy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "target_ssl_proxy", value)


@pulumi.input_type
class CertificateMapGclbTargetIpConfigArgs:
    def __init__(__self__, *,
                 ip_address: Optional[pulumi.Input[str]] = None,
                 ports: Optional[pulumi.Input[Sequence[pulumi.Input[int]]]] = None):
        """
        :param pulumi.Input[str] ip_address: An external IP address
        :param pulumi.Input[Sequence[pulumi.Input[int]]] ports: A list of ports
        """
        if ip_address is not None:
            pulumi.set(__self__, "ip_address", ip_address)
        if ports is not None:
            pulumi.set(__self__, "ports", ports)

    @property
    @pulumi.getter(name="ipAddress")
    def ip_address(self) -> Optional[pulumi.Input[str]]:
        """
        An external IP address
        """
        return pulumi.get(self, "ip_address")

    @ip_address.setter
    def ip_address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ip_address", value)

    @property
    @pulumi.getter
    def ports(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[int]]]]:
        """
        A list of ports
        """
        return pulumi.get(self, "ports")

    @ports.setter
    def ports(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[int]]]]):
        pulumi.set(self, "ports", value)


@pulumi.input_type
class CertificateSelfManagedArgs:
    def __init__(__self__, *,
                 certificate_pem: Optional[pulumi.Input[str]] = None,
                 pem_certificate: Optional[pulumi.Input[str]] = None,
                 pem_private_key: Optional[pulumi.Input[str]] = None,
                 private_key_pem: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] certificate_pem: (Optional, Deprecated)
               The certificate chain in PEM-encoded form.
               Leaf certificate comes first, followed by intermediate ones if any.
               **Note**: This property is sensitive and will not be displayed in the plan.
               
               > **Warning:** `certificate_pem` is deprecated and will be removed in a future major release. Use `pem_certificate` instead.
        :param pulumi.Input[str] pem_certificate: The certificate chain in PEM-encoded form.
               Leaf certificate comes first, followed by intermediate ones if any.
               **Note**: This property is sensitive and will not be displayed in the plan.
        :param pulumi.Input[str] pem_private_key: The private key of the leaf certificate in PEM-encoded form.
               **Note**: This property is sensitive and will not be displayed in the plan.
        :param pulumi.Input[str] private_key_pem: (Optional, Deprecated)
               The private key of the leaf certificate in PEM-encoded form.
               **Note**: This property is sensitive and will not be displayed in the plan.
               
               > **Warning:** `private_key_pem` is deprecated and will be removed in a future major release. Use `pem_private_key` instead.
        """
        if certificate_pem is not None:
            warnings.warn("""`certificate_pem` is deprecated and will be removed in a future major release. Use `pem_certificate` instead.""", DeprecationWarning)
            pulumi.log.warn("""certificate_pem is deprecated: `certificate_pem` is deprecated and will be removed in a future major release. Use `pem_certificate` instead.""")
        if certificate_pem is not None:
            pulumi.set(__self__, "certificate_pem", certificate_pem)
        if pem_certificate is not None:
            pulumi.set(__self__, "pem_certificate", pem_certificate)
        if pem_private_key is not None:
            pulumi.set(__self__, "pem_private_key", pem_private_key)
        if private_key_pem is not None:
            warnings.warn("""`private_key_pem` is deprecated and will be removed in a future major release. Use `pem_private_key` instead.""", DeprecationWarning)
            pulumi.log.warn("""private_key_pem is deprecated: `private_key_pem` is deprecated and will be removed in a future major release. Use `pem_private_key` instead.""")
        if private_key_pem is not None:
            pulumi.set(__self__, "private_key_pem", private_key_pem)

    @property
    @pulumi.getter(name="certificatePem")
    def certificate_pem(self) -> Optional[pulumi.Input[str]]:
        """
        (Optional, Deprecated)
        The certificate chain in PEM-encoded form.
        Leaf certificate comes first, followed by intermediate ones if any.
        **Note**: This property is sensitive and will not be displayed in the plan.

        > **Warning:** `certificate_pem` is deprecated and will be removed in a future major release. Use `pem_certificate` instead.
        """
        warnings.warn("""`certificate_pem` is deprecated and will be removed in a future major release. Use `pem_certificate` instead.""", DeprecationWarning)
        pulumi.log.warn("""certificate_pem is deprecated: `certificate_pem` is deprecated and will be removed in a future major release. Use `pem_certificate` instead.""")

        return pulumi.get(self, "certificate_pem")

    @certificate_pem.setter
    def certificate_pem(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "certificate_pem", value)

    @property
    @pulumi.getter(name="pemCertificate")
    def pem_certificate(self) -> Optional[pulumi.Input[str]]:
        """
        The certificate chain in PEM-encoded form.
        Leaf certificate comes first, followed by intermediate ones if any.
        **Note**: This property is sensitive and will not be displayed in the plan.
        """
        return pulumi.get(self, "pem_certificate")

    @pem_certificate.setter
    def pem_certificate(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "pem_certificate", value)

    @property
    @pulumi.getter(name="pemPrivateKey")
    def pem_private_key(self) -> Optional[pulumi.Input[str]]:
        """
        The private key of the leaf certificate in PEM-encoded form.
        **Note**: This property is sensitive and will not be displayed in the plan.
        """
        return pulumi.get(self, "pem_private_key")

    @pem_private_key.setter
    def pem_private_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "pem_private_key", value)

    @property
    @pulumi.getter(name="privateKeyPem")
    def private_key_pem(self) -> Optional[pulumi.Input[str]]:
        """
        (Optional, Deprecated)
        The private key of the leaf certificate in PEM-encoded form.
        **Note**: This property is sensitive and will not be displayed in the plan.

        > **Warning:** `private_key_pem` is deprecated and will be removed in a future major release. Use `pem_private_key` instead.
        """
        warnings.warn("""`private_key_pem` is deprecated and will be removed in a future major release. Use `pem_private_key` instead.""", DeprecationWarning)
        pulumi.log.warn("""private_key_pem is deprecated: `private_key_pem` is deprecated and will be removed in a future major release. Use `pem_private_key` instead.""")

        return pulumi.get(self, "private_key_pem")

    @private_key_pem.setter
    def private_key_pem(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "private_key_pem", value)


@pulumi.input_type
class DnsAuthorizationDnsResourceRecordArgs:
    def __init__(__self__, *,
                 data: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] data: (Output)
               Data of the DNS Resource Record.
        :param pulumi.Input[str] name: Name of the resource; provided by the client when the resource is created.
               The name must be 1-64 characters long, and match the regular expression [a-zA-Z][a-zA-Z0-9_-]* which means the first character must be a letter,
               and all following characters must be a dash, underscore, letter or digit.
               
               
               - - -
        :param pulumi.Input[str] type: type of DNS authorization. If unset during the resource creation, FIXED_RECORD will
               be used for global resources, and PER_PROJECT_RECORD will be used for other locations.
               FIXED_RECORD DNS authorization uses DNS-01 validation method
               PER_PROJECT_RECORD DNS authorization allows for independent management
               of Google-managed certificates with DNS authorization across multiple
               projects.
               Possible values are: `FIXED_RECORD`, `PER_PROJECT_RECORD`.
        """
        if data is not None:
            pulumi.set(__self__, "data", data)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def data(self) -> Optional[pulumi.Input[str]]:
        """
        (Output)
        Data of the DNS Resource Record.
        """
        return pulumi.get(self, "data")

    @data.setter
    def data(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "data", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the resource; provided by the client when the resource is created.
        The name must be 1-64 characters long, and match the regular expression [a-zA-Z][a-zA-Z0-9_-]* which means the first character must be a letter,
        and all following characters must be a dash, underscore, letter or digit.


        - - -
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        type of DNS authorization. If unset during the resource creation, FIXED_RECORD will
        be used for global resources, and PER_PROJECT_RECORD will be used for other locations.
        FIXED_RECORD DNS authorization uses DNS-01 validation method
        PER_PROJECT_RECORD DNS authorization allows for independent management
        of Google-managed certificates with DNS authorization across multiple
        projects.
        Possible values are: `FIXED_RECORD`, `PER_PROJECT_RECORD`.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)


@pulumi.input_type
class TrustConfigTrustStoreArgs:
    def __init__(__self__, *,
                 intermediate_cas: Optional[pulumi.Input[Sequence[pulumi.Input['TrustConfigTrustStoreIntermediateCaArgs']]]] = None,
                 trust_anchors: Optional[pulumi.Input[Sequence[pulumi.Input['TrustConfigTrustStoreTrustAnchorArgs']]]] = None):
        """
        :param pulumi.Input[Sequence[pulumi.Input['TrustConfigTrustStoreIntermediateCaArgs']]] intermediate_cas: Set of intermediate CA certificates used for the path building phase of chain validation.
               The field is currently not supported if trust config is used for the workload certificate feature.
               Structure is documented below.
        :param pulumi.Input[Sequence[pulumi.Input['TrustConfigTrustStoreTrustAnchorArgs']]] trust_anchors: List of Trust Anchors to be used while performing validation against a given TrustStore.
               Structure is documented below.
        """
        if intermediate_cas is not None:
            pulumi.set(__self__, "intermediate_cas", intermediate_cas)
        if trust_anchors is not None:
            pulumi.set(__self__, "trust_anchors", trust_anchors)

    @property
    @pulumi.getter(name="intermediateCas")
    def intermediate_cas(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['TrustConfigTrustStoreIntermediateCaArgs']]]]:
        """
        Set of intermediate CA certificates used for the path building phase of chain validation.
        The field is currently not supported if trust config is used for the workload certificate feature.
        Structure is documented below.
        """
        return pulumi.get(self, "intermediate_cas")

    @intermediate_cas.setter
    def intermediate_cas(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['TrustConfigTrustStoreIntermediateCaArgs']]]]):
        pulumi.set(self, "intermediate_cas", value)

    @property
    @pulumi.getter(name="trustAnchors")
    def trust_anchors(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['TrustConfigTrustStoreTrustAnchorArgs']]]]:
        """
        List of Trust Anchors to be used while performing validation against a given TrustStore.
        Structure is documented below.
        """
        return pulumi.get(self, "trust_anchors")

    @trust_anchors.setter
    def trust_anchors(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['TrustConfigTrustStoreTrustAnchorArgs']]]]):
        pulumi.set(self, "trust_anchors", value)


@pulumi.input_type
class TrustConfigTrustStoreIntermediateCaArgs:
    def __init__(__self__, *,
                 pem_certificate: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] pem_certificate: PEM intermediate certificate used for building up paths for validation.
               Each certificate provided in PEM format may occupy up to 5kB.
               **Note**: This property is sensitive and will not be displayed in the plan.
        """
        if pem_certificate is not None:
            pulumi.set(__self__, "pem_certificate", pem_certificate)

    @property
    @pulumi.getter(name="pemCertificate")
    def pem_certificate(self) -> Optional[pulumi.Input[str]]:
        """
        PEM intermediate certificate used for building up paths for validation.
        Each certificate provided in PEM format may occupy up to 5kB.
        **Note**: This property is sensitive and will not be displayed in the plan.
        """
        return pulumi.get(self, "pem_certificate")

    @pem_certificate.setter
    def pem_certificate(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "pem_certificate", value)


@pulumi.input_type
class TrustConfigTrustStoreTrustAnchorArgs:
    def __init__(__self__, *,
                 pem_certificate: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] pem_certificate: PEM root certificate of the PKI used for validation.
               Each certificate provided in PEM format may occupy up to 5kB.
               **Note**: This property is sensitive and will not be displayed in the plan.
        """
        if pem_certificate is not None:
            pulumi.set(__self__, "pem_certificate", pem_certificate)

    @property
    @pulumi.getter(name="pemCertificate")
    def pem_certificate(self) -> Optional[pulumi.Input[str]]:
        """
        PEM root certificate of the PKI used for validation.
        Each certificate provided in PEM format may occupy up to 5kB.
        **Note**: This property is sensitive and will not be displayed in the plan.
        """
        return pulumi.get(self, "pem_certificate")

    @pem_certificate.setter
    def pem_certificate(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "pem_certificate", value)


