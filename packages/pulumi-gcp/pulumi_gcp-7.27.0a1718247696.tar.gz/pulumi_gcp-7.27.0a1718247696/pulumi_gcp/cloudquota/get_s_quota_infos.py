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

__all__ = [
    'GetSQuotaInfosResult',
    'AwaitableGetSQuotaInfosResult',
    'get_s_quota_infos',
    'get_s_quota_infos_output',
]

@pulumi.output_type
class GetSQuotaInfosResult:
    """
    A collection of values returned by getSQuotaInfos.
    """
    def __init__(__self__, id=None, parent=None, quota_infos=None, service=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if parent and not isinstance(parent, str):
            raise TypeError("Expected argument 'parent' to be a str")
        pulumi.set(__self__, "parent", parent)
        if quota_infos and not isinstance(quota_infos, list):
            raise TypeError("Expected argument 'quota_infos' to be a list")
        pulumi.set(__self__, "quota_infos", quota_infos)
        if service and not isinstance(service, str):
            raise TypeError("Expected argument 'service' to be a str")
        pulumi.set(__self__, "service", service)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def parent(self) -> str:
        return pulumi.get(self, "parent")

    @property
    @pulumi.getter(name="quotaInfos")
    def quota_infos(self) -> Sequence['outputs.GetSQuotaInfosQuotaInfoResult']:
        """
        (Output) The list of QuotaInfo.
        """
        return pulumi.get(self, "quota_infos")

    @property
    @pulumi.getter
    def service(self) -> str:
        return pulumi.get(self, "service")


class AwaitableGetSQuotaInfosResult(GetSQuotaInfosResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSQuotaInfosResult(
            id=self.id,
            parent=self.parent,
            quota_infos=self.quota_infos,
            service=self.service)


def get_s_quota_infos(parent: Optional[str] = None,
                      service: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSQuotaInfosResult:
    """
    Provides information about all quotas for a given project, folder or organization.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_gcp as gcp

    my_quota_infos = gcp.cloudquota.get_s_quota_infos(parent="projects/my-project",
        service="compute.googleapis.com")
    ```


    :param str parent: Parent value of QuotaInfo resources. Listing across different resource containers (such as 'projects/-') is not allowed. Allowed parents are "projects/[project-id / number]" or "folders/[folder-id / number]" or "organizations/[org-id / number].
    :param str service: The name of the service in which the quotas are defined.
    """
    __args__ = dict()
    __args__['parent'] = parent
    __args__['service'] = service
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('gcp:cloudquota/getSQuotaInfos:getSQuotaInfos', __args__, opts=opts, typ=GetSQuotaInfosResult).value

    return AwaitableGetSQuotaInfosResult(
        id=pulumi.get(__ret__, 'id'),
        parent=pulumi.get(__ret__, 'parent'),
        quota_infos=pulumi.get(__ret__, 'quota_infos'),
        service=pulumi.get(__ret__, 'service'))


@_utilities.lift_output_func(get_s_quota_infos)
def get_s_quota_infos_output(parent: Optional[pulumi.Input[str]] = None,
                             service: Optional[pulumi.Input[str]] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSQuotaInfosResult]:
    """
    Provides information about all quotas for a given project, folder or organization.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_gcp as gcp

    my_quota_infos = gcp.cloudquota.get_s_quota_infos(parent="projects/my-project",
        service="compute.googleapis.com")
    ```


    :param str parent: Parent value of QuotaInfo resources. Listing across different resource containers (such as 'projects/-') is not allowed. Allowed parents are "projects/[project-id / number]" or "folders/[folder-id / number]" or "organizations/[org-id / number].
    :param str service: The name of the service in which the quotas are defined.
    """
    ...
