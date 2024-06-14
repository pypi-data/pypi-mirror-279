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
    'GetAttachedVersionsResult',
    'AwaitableGetAttachedVersionsResult',
    'get_attached_versions',
    'get_attached_versions_output',
]

@pulumi.output_type
class GetAttachedVersionsResult:
    """
    A collection of values returned by getAttachedVersions.
    """
    def __init__(__self__, id=None, location=None, project=None, valid_versions=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if project and not isinstance(project, str):
            raise TypeError("Expected argument 'project' to be a str")
        pulumi.set(__self__, "project", project)
        if valid_versions and not isinstance(valid_versions, list):
            raise TypeError("Expected argument 'valid_versions' to be a list")
        pulumi.set(__self__, "valid_versions", valid_versions)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> str:
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def project(self) -> str:
        return pulumi.get(self, "project")

    @property
    @pulumi.getter(name="validVersions")
    def valid_versions(self) -> Sequence[str]:
        """
        A list of versions available for use with this project and location.
        """
        return pulumi.get(self, "valid_versions")


class AwaitableGetAttachedVersionsResult(GetAttachedVersionsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAttachedVersionsResult(
            id=self.id,
            location=self.location,
            project=self.project,
            valid_versions=self.valid_versions)


def get_attached_versions(location: Optional[str] = None,
                          project: Optional[str] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAttachedVersionsResult:
    """
    Provides access to available platform versions in a location for a given project.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_gcp as gcp

    uswest = gcp.container.get_attached_versions(location="us-west1",
        project="my-project")
    pulumi.export("firstAvailableVersion", versions["validVersions"])
    ```


    :param str location: The location to list versions for.
    :param str project: ID of the project to list available platform versions for. Should match the project the cluster will be deployed to.
           Defaults to the project that the provider is authenticated with.
    """
    __args__ = dict()
    __args__['location'] = location
    __args__['project'] = project
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('gcp:container/getAttachedVersions:getAttachedVersions', __args__, opts=opts, typ=GetAttachedVersionsResult).value

    return AwaitableGetAttachedVersionsResult(
        id=pulumi.get(__ret__, 'id'),
        location=pulumi.get(__ret__, 'location'),
        project=pulumi.get(__ret__, 'project'),
        valid_versions=pulumi.get(__ret__, 'valid_versions'))


@_utilities.lift_output_func(get_attached_versions)
def get_attached_versions_output(location: Optional[pulumi.Input[str]] = None,
                                 project: Optional[pulumi.Input[str]] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAttachedVersionsResult]:
    """
    Provides access to available platform versions in a location for a given project.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_gcp as gcp

    uswest = gcp.container.get_attached_versions(location="us-west1",
        project="my-project")
    pulumi.export("firstAvailableVersion", versions["validVersions"])
    ```


    :param str location: The location to list versions for.
    :param str project: ID of the project to list available platform versions for. Should match the project the cluster will be deployed to.
           Defaults to the project that the provider is authenticated with.
    """
    ...
