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
    'GetTaskIamPolicyResult',
    'AwaitableGetTaskIamPolicyResult',
    'get_task_iam_policy',
    'get_task_iam_policy_output',
]

@pulumi.output_type
class GetTaskIamPolicyResult:
    """
    A collection of values returned by getTaskIamPolicy.
    """
    def __init__(__self__, etag=None, id=None, lake=None, location=None, policy_data=None, project=None, task_id=None):
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if lake and not isinstance(lake, str):
            raise TypeError("Expected argument 'lake' to be a str")
        pulumi.set(__self__, "lake", lake)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if policy_data and not isinstance(policy_data, str):
            raise TypeError("Expected argument 'policy_data' to be a str")
        pulumi.set(__self__, "policy_data", policy_data)
        if project and not isinstance(project, str):
            raise TypeError("Expected argument 'project' to be a str")
        pulumi.set(__self__, "project", project)
        if task_id and not isinstance(task_id, str):
            raise TypeError("Expected argument 'task_id' to be a str")
        pulumi.set(__self__, "task_id", task_id)

    @property
    @pulumi.getter
    def etag(self) -> str:
        """
        (Computed) The etag of the IAM policy.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def lake(self) -> str:
        return pulumi.get(self, "lake")

    @property
    @pulumi.getter
    def location(self) -> str:
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="policyData")
    def policy_data(self) -> str:
        """
        (Required only by `dataplex.TaskIamPolicy`) The policy data generated by
        a `organizations_get_iam_policy` data source.
        """
        return pulumi.get(self, "policy_data")

    @property
    @pulumi.getter
    def project(self) -> str:
        return pulumi.get(self, "project")

    @property
    @pulumi.getter(name="taskId")
    def task_id(self) -> str:
        return pulumi.get(self, "task_id")


class AwaitableGetTaskIamPolicyResult(GetTaskIamPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTaskIamPolicyResult(
            etag=self.etag,
            id=self.id,
            lake=self.lake,
            location=self.location,
            policy_data=self.policy_data,
            project=self.project,
            task_id=self.task_id)


def get_task_iam_policy(lake: Optional[str] = None,
                        location: Optional[str] = None,
                        project: Optional[str] = None,
                        task_id: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetTaskIamPolicyResult:
    """
    Retrieves the current IAM policy data for task

    ## example

    ```python
    import pulumi
    import pulumi_gcp as gcp

    policy = gcp.dataplex.get_task_iam_policy(project=example["project"],
        location=example["location"],
        lake=example["lake"],
        task_id=example["taskId"])
    ```


    :param str lake: The lake in which the task will be created in.
           Used to find the parent resource to bind the IAM policy to
    :param str location: The location in which the task will be created in.
           Used to find the parent resource to bind the IAM policy to. If not specified,
           the value will be parsed from the identifier of the parent resource. If no location is provided in the parent identifier and no
           location is specified, it is taken from the provider configuration.
    :param str project: The ID of the project in which the resource belongs.
           If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
    """
    __args__ = dict()
    __args__['lake'] = lake
    __args__['location'] = location
    __args__['project'] = project
    __args__['taskId'] = task_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('gcp:dataplex/getTaskIamPolicy:getTaskIamPolicy', __args__, opts=opts, typ=GetTaskIamPolicyResult).value

    return AwaitableGetTaskIamPolicyResult(
        etag=pulumi.get(__ret__, 'etag'),
        id=pulumi.get(__ret__, 'id'),
        lake=pulumi.get(__ret__, 'lake'),
        location=pulumi.get(__ret__, 'location'),
        policy_data=pulumi.get(__ret__, 'policy_data'),
        project=pulumi.get(__ret__, 'project'),
        task_id=pulumi.get(__ret__, 'task_id'))


@_utilities.lift_output_func(get_task_iam_policy)
def get_task_iam_policy_output(lake: Optional[pulumi.Input[str]] = None,
                               location: Optional[pulumi.Input[Optional[str]]] = None,
                               project: Optional[pulumi.Input[Optional[str]]] = None,
                               task_id: Optional[pulumi.Input[str]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetTaskIamPolicyResult]:
    """
    Retrieves the current IAM policy data for task

    ## example

    ```python
    import pulumi
    import pulumi_gcp as gcp

    policy = gcp.dataplex.get_task_iam_policy(project=example["project"],
        location=example["location"],
        lake=example["lake"],
        task_id=example["taskId"])
    ```


    :param str lake: The lake in which the task will be created in.
           Used to find the parent resource to bind the IAM policy to
    :param str location: The location in which the task will be created in.
           Used to find the parent resource to bind the IAM policy to. If not specified,
           the value will be parsed from the identifier of the parent resource. If no location is provided in the parent identifier and no
           location is specified, it is taken from the provider configuration.
    :param str project: The ID of the project in which the resource belongs.
           If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
    """
    ...
