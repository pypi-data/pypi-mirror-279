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
    'GetManagedZonesResult',
    'AwaitableGetManagedZonesResult',
    'get_managed_zones',
    'get_managed_zones_output',
]

@pulumi.output_type
class GetManagedZonesResult:
    """
    A collection of values returned by getManagedZones.
    """
    def __init__(__self__, id=None, managed_zones=None, project=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if managed_zones and not isinstance(managed_zones, list):
            raise TypeError("Expected argument 'managed_zones' to be a list")
        pulumi.set(__self__, "managed_zones", managed_zones)
        if project and not isinstance(project, str):
            raise TypeError("Expected argument 'project' to be a str")
        pulumi.set(__self__, "project", project)

    @property
    @pulumi.getter
    def id(self) -> str:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="managedZones")
    def managed_zones(self) -> Sequence['outputs.GetManagedZonesManagedZoneResult']:
        """
        A list of managed zones.
        """
        return pulumi.get(self, "managed_zones")

    @property
    @pulumi.getter
    def project(self) -> Optional[str]:
        return pulumi.get(self, "project")


class AwaitableGetManagedZonesResult(GetManagedZonesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetManagedZonesResult(
            id=self.id,
            managed_zones=self.managed_zones,
            project=self.project)


def get_managed_zones(project: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetManagedZonesResult:
    """
    Provides access to a list of zones within Google Cloud DNS.
    For more information see
    [the official documentation](https://cloud.google.com/dns/zones/)
    and
    [API](https://cloud.google.com/dns/api/v1/managedZones).

    ```python
    import pulumi
    import pulumi_gcp as gcp

    zones = gcp.dns.get_managed_zones(project="my-project-id")
    ```


    :param str project: The ID of the project containing Google Cloud DNS zones. If this is not provided the default project will be used.
    """
    __args__ = dict()
    __args__['project'] = project
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('gcp:dns/getManagedZones:getManagedZones', __args__, opts=opts, typ=GetManagedZonesResult).value

    return AwaitableGetManagedZonesResult(
        id=pulumi.get(__ret__, 'id'),
        managed_zones=pulumi.get(__ret__, 'managed_zones'),
        project=pulumi.get(__ret__, 'project'))


@_utilities.lift_output_func(get_managed_zones)
def get_managed_zones_output(project: Optional[pulumi.Input[Optional[str]]] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetManagedZonesResult]:
    """
    Provides access to a list of zones within Google Cloud DNS.
    For more information see
    [the official documentation](https://cloud.google.com/dns/zones/)
    and
    [API](https://cloud.google.com/dns/api/v1/managedZones).

    ```python
    import pulumi
    import pulumi_gcp as gcp

    zones = gcp.dns.get_managed_zones(project="my-project-id")
    ```


    :param str project: The ID of the project containing Google Cloud DNS zones. If this is not provided the default project will be used.
    """
    ...
