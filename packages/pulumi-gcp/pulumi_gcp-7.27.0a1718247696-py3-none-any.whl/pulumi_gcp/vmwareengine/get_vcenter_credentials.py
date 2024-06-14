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
    'GetVcenterCredentialsResult',
    'AwaitableGetVcenterCredentialsResult',
    'get_vcenter_credentials',
    'get_vcenter_credentials_output',
]

@pulumi.output_type
class GetVcenterCredentialsResult:
    """
    A collection of values returned by getVcenterCredentials.
    """
    def __init__(__self__, id=None, parent=None, password=None, username=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if parent and not isinstance(parent, str):
            raise TypeError("Expected argument 'parent' to be a str")
        pulumi.set(__self__, "parent", parent)
        if password and not isinstance(password, str):
            raise TypeError("Expected argument 'password' to be a str")
        pulumi.set(__self__, "password", password)
        if username and not isinstance(username, str):
            raise TypeError("Expected argument 'username' to be a str")
        pulumi.set(__self__, "username", username)

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
    @pulumi.getter
    def password(self) -> str:
        """
        The password of the Vcenter Credential.
        """
        return pulumi.get(self, "password")

    @property
    @pulumi.getter
    def username(self) -> str:
        """
        The username of the Vcenter Credential.
        """
        return pulumi.get(self, "username")


class AwaitableGetVcenterCredentialsResult(GetVcenterCredentialsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVcenterCredentialsResult(
            id=self.id,
            parent=self.parent,
            password=self.password,
            username=self.username)


def get_vcenter_credentials(parent: Optional[str] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVcenterCredentialsResult:
    """
    Use this data source to get Vcenter credentials for a Private Cloud.

    To get more information about private cloud Vcenter credentials, see:
    * [API documentation](https://cloud.google.com/vmware-engine/docs/reference/rest/v1/projects.locations.privateClouds/showVcenterCredentials)

    ## Example Usage

    ```python
    import pulumi
    import pulumi_gcp as gcp

    ds = gcp.vmwareengine.get_vcenter_credentials(parent="projects/my-project/locations/us-west1-a/privateClouds/my-cloud")
    ```


    :param str parent: The resource name of the private cloud which contains the Vcenter.
    """
    __args__ = dict()
    __args__['parent'] = parent
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('gcp:vmwareengine/getVcenterCredentials:getVcenterCredentials', __args__, opts=opts, typ=GetVcenterCredentialsResult).value

    return AwaitableGetVcenterCredentialsResult(
        id=pulumi.get(__ret__, 'id'),
        parent=pulumi.get(__ret__, 'parent'),
        password=pulumi.get(__ret__, 'password'),
        username=pulumi.get(__ret__, 'username'))


@_utilities.lift_output_func(get_vcenter_credentials)
def get_vcenter_credentials_output(parent: Optional[pulumi.Input[str]] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetVcenterCredentialsResult]:
    """
    Use this data source to get Vcenter credentials for a Private Cloud.

    To get more information about private cloud Vcenter credentials, see:
    * [API documentation](https://cloud.google.com/vmware-engine/docs/reference/rest/v1/projects.locations.privateClouds/showVcenterCredentials)

    ## Example Usage

    ```python
    import pulumi
    import pulumi_gcp as gcp

    ds = gcp.vmwareengine.get_vcenter_credentials(parent="projects/my-project/locations/us-west1-a/privateClouds/my-cloud")
    ```


    :param str parent: The resource name of the private cloud which contains the Vcenter.
    """
    ...
