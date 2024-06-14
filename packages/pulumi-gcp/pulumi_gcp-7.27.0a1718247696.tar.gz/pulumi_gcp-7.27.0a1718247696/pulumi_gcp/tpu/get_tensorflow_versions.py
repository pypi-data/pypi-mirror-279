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
    'GetTensorflowVersionsResult',
    'AwaitableGetTensorflowVersionsResult',
    'get_tensorflow_versions',
    'get_tensorflow_versions_output',
]

@pulumi.output_type
class GetTensorflowVersionsResult:
    """
    A collection of values returned by getTensorflowVersions.
    """
    def __init__(__self__, id=None, project=None, versions=None, zone=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if project and not isinstance(project, str):
            raise TypeError("Expected argument 'project' to be a str")
        pulumi.set(__self__, "project", project)
        if versions and not isinstance(versions, list):
            raise TypeError("Expected argument 'versions' to be a list")
        pulumi.set(__self__, "versions", versions)
        if zone and not isinstance(zone, str):
            raise TypeError("Expected argument 'zone' to be a str")
        pulumi.set(__self__, "zone", zone)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def project(self) -> str:
        return pulumi.get(self, "project")

    @property
    @pulumi.getter
    def versions(self) -> Sequence[str]:
        """
        The list of TensorFlow versions available for the given project and zone.
        """
        return pulumi.get(self, "versions")

    @property
    @pulumi.getter
    def zone(self) -> str:
        return pulumi.get(self, "zone")


class AwaitableGetTensorflowVersionsResult(GetTensorflowVersionsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTensorflowVersionsResult(
            id=self.id,
            project=self.project,
            versions=self.versions,
            zone=self.zone)


def get_tensorflow_versions(project: Optional[str] = None,
                            zone: Optional[str] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetTensorflowVersionsResult:
    """
    Get TensorFlow versions available for a project. For more information see the [official documentation](https://cloud.google.com/tpu/docs/) and [API](https://cloud.google.com/tpu/docs/reference/rest/v1/projects.locations.tensorflowVersions).

    ## Example Usage

    ```python
    import pulumi
    import pulumi_gcp as gcp

    available = gcp.tpu.get_tensorflow_versions()
    ```

    ### Configure Basic TPU Node With Available Version

    ```python
    import pulumi
    import pulumi_gcp as gcp

    available = gcp.tpu.get_tensorflow_versions()
    tpu = gcp.tpu.Node("tpu",
        name="test-tpu",
        zone="us-central1-b",
        accelerator_type="v3-8",
        tensorflow_version=available.versions[0],
        cidr_block="10.2.0.0/29")
    ```


    :param str project: The project to list versions for. If it
           is not provided, the provider project is used.
    :param str zone: The zone to list versions for. If it
           is not provided, the provider zone is used.
    """
    __args__ = dict()
    __args__['project'] = project
    __args__['zone'] = zone
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('gcp:tpu/getTensorflowVersions:getTensorflowVersions', __args__, opts=opts, typ=GetTensorflowVersionsResult).value

    return AwaitableGetTensorflowVersionsResult(
        id=pulumi.get(__ret__, 'id'),
        project=pulumi.get(__ret__, 'project'),
        versions=pulumi.get(__ret__, 'versions'),
        zone=pulumi.get(__ret__, 'zone'))


@_utilities.lift_output_func(get_tensorflow_versions)
def get_tensorflow_versions_output(project: Optional[pulumi.Input[Optional[str]]] = None,
                                   zone: Optional[pulumi.Input[Optional[str]]] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetTensorflowVersionsResult]:
    """
    Get TensorFlow versions available for a project. For more information see the [official documentation](https://cloud.google.com/tpu/docs/) and [API](https://cloud.google.com/tpu/docs/reference/rest/v1/projects.locations.tensorflowVersions).

    ## Example Usage

    ```python
    import pulumi
    import pulumi_gcp as gcp

    available = gcp.tpu.get_tensorflow_versions()
    ```

    ### Configure Basic TPU Node With Available Version

    ```python
    import pulumi
    import pulumi_gcp as gcp

    available = gcp.tpu.get_tensorflow_versions()
    tpu = gcp.tpu.Node("tpu",
        name="test-tpu",
        zone="us-central1-b",
        accelerator_type="v3-8",
        tensorflow_version=available.versions[0],
        cidr_block="10.2.0.0/29")
    ```


    :param str project: The project to list versions for. If it
           is not provided, the provider project is used.
    :param str zone: The zone to list versions for. If it
           is not provided, the provider zone is used.
    """
    ...
