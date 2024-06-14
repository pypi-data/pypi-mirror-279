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
    'GetTunnelDestGroupIamPolicyResult',
    'AwaitableGetTunnelDestGroupIamPolicyResult',
    'get_tunnel_dest_group_iam_policy',
    'get_tunnel_dest_group_iam_policy_output',
]

@pulumi.output_type
class GetTunnelDestGroupIamPolicyResult:
    """
    A collection of values returned by getTunnelDestGroupIamPolicy.
    """
    def __init__(__self__, dest_group=None, etag=None, id=None, policy_data=None, project=None, region=None):
        if dest_group and not isinstance(dest_group, str):
            raise TypeError("Expected argument 'dest_group' to be a str")
        pulumi.set(__self__, "dest_group", dest_group)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if policy_data and not isinstance(policy_data, str):
            raise TypeError("Expected argument 'policy_data' to be a str")
        pulumi.set(__self__, "policy_data", policy_data)
        if project and not isinstance(project, str):
            raise TypeError("Expected argument 'project' to be a str")
        pulumi.set(__self__, "project", project)
        if region and not isinstance(region, str):
            raise TypeError("Expected argument 'region' to be a str")
        pulumi.set(__self__, "region", region)

    @property
    @pulumi.getter(name="destGroup")
    def dest_group(self) -> str:
        return pulumi.get(self, "dest_group")

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
    @pulumi.getter(name="policyData")
    def policy_data(self) -> str:
        """
        (Required only by `iap.TunnelDestGroupIamPolicy`) The policy data generated by
        a `organizations_get_iam_policy` data source.
        """
        return pulumi.get(self, "policy_data")

    @property
    @pulumi.getter
    def project(self) -> str:
        return pulumi.get(self, "project")

    @property
    @pulumi.getter
    def region(self) -> str:
        return pulumi.get(self, "region")


class AwaitableGetTunnelDestGroupIamPolicyResult(GetTunnelDestGroupIamPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTunnelDestGroupIamPolicyResult(
            dest_group=self.dest_group,
            etag=self.etag,
            id=self.id,
            policy_data=self.policy_data,
            project=self.project,
            region=self.region)


def get_tunnel_dest_group_iam_policy(dest_group: Optional[str] = None,
                                     project: Optional[str] = None,
                                     region: Optional[str] = None,
                                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetTunnelDestGroupIamPolicyResult:
    """
    Retrieves the current IAM policy data for tunneldestgroup

    ## example

    ```python
    import pulumi
    import pulumi_gcp as gcp

    policy = gcp.iap.get_tunnel_dest_group_iam_policy(project=dest_group["project"],
        region=dest_group["region"],
        dest_group=dest_group["groupName"])
    ```


    :param str project: The ID of the project in which the resource belongs.
           If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
    :param str region: The region of the tunnel group. Must be the same as the network resources in the group.
           Used to find the parent resource to bind the IAM policy to. If not specified,
           the value will be parsed from the identifier of the parent resource. If no region is provided in the parent identifier and no
           region is specified, it is taken from the provider configuration.
    """
    __args__ = dict()
    __args__['destGroup'] = dest_group
    __args__['project'] = project
    __args__['region'] = region
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('gcp:iap/getTunnelDestGroupIamPolicy:getTunnelDestGroupIamPolicy', __args__, opts=opts, typ=GetTunnelDestGroupIamPolicyResult).value

    return AwaitableGetTunnelDestGroupIamPolicyResult(
        dest_group=pulumi.get(__ret__, 'dest_group'),
        etag=pulumi.get(__ret__, 'etag'),
        id=pulumi.get(__ret__, 'id'),
        policy_data=pulumi.get(__ret__, 'policy_data'),
        project=pulumi.get(__ret__, 'project'),
        region=pulumi.get(__ret__, 'region'))


@_utilities.lift_output_func(get_tunnel_dest_group_iam_policy)
def get_tunnel_dest_group_iam_policy_output(dest_group: Optional[pulumi.Input[str]] = None,
                                            project: Optional[pulumi.Input[Optional[str]]] = None,
                                            region: Optional[pulumi.Input[Optional[str]]] = None,
                                            opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetTunnelDestGroupIamPolicyResult]:
    """
    Retrieves the current IAM policy data for tunneldestgroup

    ## example

    ```python
    import pulumi
    import pulumi_gcp as gcp

    policy = gcp.iap.get_tunnel_dest_group_iam_policy(project=dest_group["project"],
        region=dest_group["region"],
        dest_group=dest_group["groupName"])
    ```


    :param str project: The ID of the project in which the resource belongs.
           If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
    :param str region: The region of the tunnel group. Must be the same as the network resources in the group.
           Used to find the parent resource to bind the IAM policy to. If not specified,
           the value will be parsed from the identifier of the parent resource. If no region is provided in the parent identifier and no
           region is specified, it is taken from the provider configuration.
    """
    ...
