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
    'GetOrganizationPolicyResult',
    'AwaitableGetOrganizationPolicyResult',
    'get_organization_policy',
    'get_organization_policy_output',
]

@pulumi.output_type
class GetOrganizationPolicyResult:
    """
    A collection of values returned by getOrganizationPolicy.
    """
    def __init__(__self__, boolean_policies=None, constraint=None, etag=None, folder=None, id=None, list_policies=None, restore_policies=None, update_time=None, version=None):
        if boolean_policies and not isinstance(boolean_policies, list):
            raise TypeError("Expected argument 'boolean_policies' to be a list")
        pulumi.set(__self__, "boolean_policies", boolean_policies)
        if constraint and not isinstance(constraint, str):
            raise TypeError("Expected argument 'constraint' to be a str")
        pulumi.set(__self__, "constraint", constraint)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if folder and not isinstance(folder, str):
            raise TypeError("Expected argument 'folder' to be a str")
        pulumi.set(__self__, "folder", folder)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if list_policies and not isinstance(list_policies, list):
            raise TypeError("Expected argument 'list_policies' to be a list")
        pulumi.set(__self__, "list_policies", list_policies)
        if restore_policies and not isinstance(restore_policies, list):
            raise TypeError("Expected argument 'restore_policies' to be a list")
        pulumi.set(__self__, "restore_policies", restore_policies)
        if update_time and not isinstance(update_time, str):
            raise TypeError("Expected argument 'update_time' to be a str")
        pulumi.set(__self__, "update_time", update_time)
        if version and not isinstance(version, int):
            raise TypeError("Expected argument 'version' to be a int")
        pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter(name="booleanPolicies")
    def boolean_policies(self) -> Sequence['outputs.GetOrganizationPolicyBooleanPolicyResult']:
        return pulumi.get(self, "boolean_policies")

    @property
    @pulumi.getter
    def constraint(self) -> str:
        return pulumi.get(self, "constraint")

    @property
    @pulumi.getter
    def etag(self) -> str:
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def folder(self) -> str:
        return pulumi.get(self, "folder")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="listPolicies")
    def list_policies(self) -> Sequence['outputs.GetOrganizationPolicyListPolicyResult']:
        return pulumi.get(self, "list_policies")

    @property
    @pulumi.getter(name="restorePolicies")
    def restore_policies(self) -> Sequence['outputs.GetOrganizationPolicyRestorePolicyResult']:
        return pulumi.get(self, "restore_policies")

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> str:
        return pulumi.get(self, "update_time")

    @property
    @pulumi.getter
    def version(self) -> int:
        return pulumi.get(self, "version")


class AwaitableGetOrganizationPolicyResult(GetOrganizationPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetOrganizationPolicyResult(
            boolean_policies=self.boolean_policies,
            constraint=self.constraint,
            etag=self.etag,
            folder=self.folder,
            id=self.id,
            list_policies=self.list_policies,
            restore_policies=self.restore_policies,
            update_time=self.update_time,
            version=self.version)


def get_organization_policy(constraint: Optional[str] = None,
                            folder: Optional[str] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetOrganizationPolicyResult:
    """
    Allows management of Organization policies for a Google Folder. For more information see
    [the official
    documentation](https://cloud.google.com/resource-manager/docs/organization-policy/overview)

    ## Example Usage

    ```python
    import pulumi
    import pulumi_gcp as gcp

    policy = gcp.folder.get_organization_policy(folder="folders/folderid",
        constraint="constraints/compute.trustedImageProjects")
    pulumi.export("version", policy.version)
    ```


    :param str constraint: (Required) The name of the Constraint the Policy is configuring, for example, `serviceuser.services`. Check out the [complete list of available constraints](https://cloud.google.com/resource-manager/docs/organization-policy/understanding-constraints#available_constraints).
    :param str folder: The resource name of the folder to set the policy for. Its format is folders/{folder_id}.
    """
    __args__ = dict()
    __args__['constraint'] = constraint
    __args__['folder'] = folder
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('gcp:folder/getOrganizationPolicy:getOrganizationPolicy', __args__, opts=opts, typ=GetOrganizationPolicyResult).value

    return AwaitableGetOrganizationPolicyResult(
        boolean_policies=pulumi.get(__ret__, 'boolean_policies'),
        constraint=pulumi.get(__ret__, 'constraint'),
        etag=pulumi.get(__ret__, 'etag'),
        folder=pulumi.get(__ret__, 'folder'),
        id=pulumi.get(__ret__, 'id'),
        list_policies=pulumi.get(__ret__, 'list_policies'),
        restore_policies=pulumi.get(__ret__, 'restore_policies'),
        update_time=pulumi.get(__ret__, 'update_time'),
        version=pulumi.get(__ret__, 'version'))


@_utilities.lift_output_func(get_organization_policy)
def get_organization_policy_output(constraint: Optional[pulumi.Input[str]] = None,
                                   folder: Optional[pulumi.Input[str]] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetOrganizationPolicyResult]:
    """
    Allows management of Organization policies for a Google Folder. For more information see
    [the official
    documentation](https://cloud.google.com/resource-manager/docs/organization-policy/overview)

    ## Example Usage

    ```python
    import pulumi
    import pulumi_gcp as gcp

    policy = gcp.folder.get_organization_policy(folder="folders/folderid",
        constraint="constraints/compute.trustedImageProjects")
    pulumi.export("version", policy.version)
    ```


    :param str constraint: (Required) The name of the Constraint the Policy is configuring, for example, `serviceuser.services`. Check out the [complete list of available constraints](https://cloud.google.com/resource-manager/docs/organization-policy/understanding-constraints#available_constraints).
    :param str folder: The resource name of the folder to set the policy for. Its format is folders/{folder_id}.
    """
    ...
