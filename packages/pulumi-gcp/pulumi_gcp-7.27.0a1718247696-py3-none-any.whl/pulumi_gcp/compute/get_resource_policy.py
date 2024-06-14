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
    'GetResourcePolicyResult',
    'AwaitableGetResourcePolicyResult',
    'get_resource_policy',
    'get_resource_policy_output',
]

@pulumi.output_type
class GetResourcePolicyResult:
    """
    A collection of values returned by getResourcePolicy.
    """
    def __init__(__self__, description=None, disk_consistency_group_policies=None, group_placement_policies=None, id=None, instance_schedule_policies=None, name=None, project=None, region=None, self_link=None, snapshot_schedule_policies=None):
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if disk_consistency_group_policies and not isinstance(disk_consistency_group_policies, list):
            raise TypeError("Expected argument 'disk_consistency_group_policies' to be a list")
        pulumi.set(__self__, "disk_consistency_group_policies", disk_consistency_group_policies)
        if group_placement_policies and not isinstance(group_placement_policies, list):
            raise TypeError("Expected argument 'group_placement_policies' to be a list")
        pulumi.set(__self__, "group_placement_policies", group_placement_policies)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if instance_schedule_policies and not isinstance(instance_schedule_policies, list):
            raise TypeError("Expected argument 'instance_schedule_policies' to be a list")
        pulumi.set(__self__, "instance_schedule_policies", instance_schedule_policies)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if project and not isinstance(project, str):
            raise TypeError("Expected argument 'project' to be a str")
        pulumi.set(__self__, "project", project)
        if region and not isinstance(region, str):
            raise TypeError("Expected argument 'region' to be a str")
        pulumi.set(__self__, "region", region)
        if self_link and not isinstance(self_link, str):
            raise TypeError("Expected argument 'self_link' to be a str")
        pulumi.set(__self__, "self_link", self_link)
        if snapshot_schedule_policies and not isinstance(snapshot_schedule_policies, list):
            raise TypeError("Expected argument 'snapshot_schedule_policies' to be a list")
        pulumi.set(__self__, "snapshot_schedule_policies", snapshot_schedule_policies)

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        Description of this Resource Policy.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="diskConsistencyGroupPolicies")
    def disk_consistency_group_policies(self) -> Sequence['outputs.GetResourcePolicyDiskConsistencyGroupPolicyResult']:
        return pulumi.get(self, "disk_consistency_group_policies")

    @property
    @pulumi.getter(name="groupPlacementPolicies")
    def group_placement_policies(self) -> Sequence['outputs.GetResourcePolicyGroupPlacementPolicyResult']:
        return pulumi.get(self, "group_placement_policies")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="instanceSchedulePolicies")
    def instance_schedule_policies(self) -> Sequence['outputs.GetResourcePolicyInstanceSchedulePolicyResult']:
        return pulumi.get(self, "instance_schedule_policies")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def project(self) -> Optional[str]:
        return pulumi.get(self, "project")

    @property
    @pulumi.getter
    def region(self) -> Optional[str]:
        return pulumi.get(self, "region")

    @property
    @pulumi.getter(name="selfLink")
    def self_link(self) -> str:
        """
        The URI of the resource.
        """
        return pulumi.get(self, "self_link")

    @property
    @pulumi.getter(name="snapshotSchedulePolicies")
    def snapshot_schedule_policies(self) -> Sequence['outputs.GetResourcePolicySnapshotSchedulePolicyResult']:
        return pulumi.get(self, "snapshot_schedule_policies")


class AwaitableGetResourcePolicyResult(GetResourcePolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetResourcePolicyResult(
            description=self.description,
            disk_consistency_group_policies=self.disk_consistency_group_policies,
            group_placement_policies=self.group_placement_policies,
            id=self.id,
            instance_schedule_policies=self.instance_schedule_policies,
            name=self.name,
            project=self.project,
            region=self.region,
            self_link=self.self_link,
            snapshot_schedule_policies=self.snapshot_schedule_policies)


def get_resource_policy(name: Optional[str] = None,
                        project: Optional[str] = None,
                        region: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetResourcePolicyResult:
    """
    Provide access to a Resource Policy's attributes. For more information see [the official documentation](https://cloud.google.com/compute/docs/disks/scheduled-snapshots) or the [API](https://cloud.google.com/compute/docs/reference/rest/beta/resourcePolicies).

    ```python
    import pulumi
    import pulumi_gcp as gcp

    daily = gcp.compute.get_resource_policy(name="daily",
        region="us-central1")
    ```


    :param str name: The name of the Resource Policy.
    :param str project: Project from which to list the Resource Policy. Defaults to project declared in the provider.
    :param str region: Region where the Resource Policy resides.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['project'] = project
    __args__['region'] = region
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('gcp:compute/getResourcePolicy:getResourcePolicy', __args__, opts=opts, typ=GetResourcePolicyResult).value

    return AwaitableGetResourcePolicyResult(
        description=pulumi.get(__ret__, 'description'),
        disk_consistency_group_policies=pulumi.get(__ret__, 'disk_consistency_group_policies'),
        group_placement_policies=pulumi.get(__ret__, 'group_placement_policies'),
        id=pulumi.get(__ret__, 'id'),
        instance_schedule_policies=pulumi.get(__ret__, 'instance_schedule_policies'),
        name=pulumi.get(__ret__, 'name'),
        project=pulumi.get(__ret__, 'project'),
        region=pulumi.get(__ret__, 'region'),
        self_link=pulumi.get(__ret__, 'self_link'),
        snapshot_schedule_policies=pulumi.get(__ret__, 'snapshot_schedule_policies'))


@_utilities.lift_output_func(get_resource_policy)
def get_resource_policy_output(name: Optional[pulumi.Input[str]] = None,
                               project: Optional[pulumi.Input[Optional[str]]] = None,
                               region: Optional[pulumi.Input[Optional[str]]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetResourcePolicyResult]:
    """
    Provide access to a Resource Policy's attributes. For more information see [the official documentation](https://cloud.google.com/compute/docs/disks/scheduled-snapshots) or the [API](https://cloud.google.com/compute/docs/reference/rest/beta/resourcePolicies).

    ```python
    import pulumi
    import pulumi_gcp as gcp

    daily = gcp.compute.get_resource_policy(name="daily",
        region="us-central1")
    ```


    :param str name: The name of the Resource Policy.
    :param str project: Project from which to list the Resource Policy. Defaults to project declared in the provider.
    :param str region: Region where the Resource Policy resides.
    """
    ...
