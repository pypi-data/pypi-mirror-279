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
    'GetListingIamPolicyResult',
    'AwaitableGetListingIamPolicyResult',
    'get_listing_iam_policy',
    'get_listing_iam_policy_output',
]

@pulumi.output_type
class GetListingIamPolicyResult:
    """
    A collection of values returned by getListingIamPolicy.
    """
    def __init__(__self__, data_exchange_id=None, etag=None, id=None, listing_id=None, location=None, policy_data=None, project=None):
        if data_exchange_id and not isinstance(data_exchange_id, str):
            raise TypeError("Expected argument 'data_exchange_id' to be a str")
        pulumi.set(__self__, "data_exchange_id", data_exchange_id)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if listing_id and not isinstance(listing_id, str):
            raise TypeError("Expected argument 'listing_id' to be a str")
        pulumi.set(__self__, "listing_id", listing_id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if policy_data and not isinstance(policy_data, str):
            raise TypeError("Expected argument 'policy_data' to be a str")
        pulumi.set(__self__, "policy_data", policy_data)
        if project and not isinstance(project, str):
            raise TypeError("Expected argument 'project' to be a str")
        pulumi.set(__self__, "project", project)

    @property
    @pulumi.getter(name="dataExchangeId")
    def data_exchange_id(self) -> str:
        return pulumi.get(self, "data_exchange_id")

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
    @pulumi.getter(name="listingId")
    def listing_id(self) -> str:
        return pulumi.get(self, "listing_id")

    @property
    @pulumi.getter
    def location(self) -> str:
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="policyData")
    def policy_data(self) -> str:
        """
        (Required only by `bigqueryanalyticshub.ListingIamPolicy`) The policy data generated by
        a `organizations_get_iam_policy` data source.
        """
        return pulumi.get(self, "policy_data")

    @property
    @pulumi.getter
    def project(self) -> str:
        return pulumi.get(self, "project")


class AwaitableGetListingIamPolicyResult(GetListingIamPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetListingIamPolicyResult(
            data_exchange_id=self.data_exchange_id,
            etag=self.etag,
            id=self.id,
            listing_id=self.listing_id,
            location=self.location,
            policy_data=self.policy_data,
            project=self.project)


def get_listing_iam_policy(data_exchange_id: Optional[str] = None,
                           listing_id: Optional[str] = None,
                           location: Optional[str] = None,
                           project: Optional[str] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetListingIamPolicyResult:
    """
    Retrieves the current IAM policy data for listing

    ## example

    ```python
    import pulumi
    import pulumi_gcp as gcp

    policy = gcp.bigqueryanalyticshub.get_listing_iam_policy(project=listing["project"],
        location=listing["location"],
        data_exchange_id=listing["dataExchangeId"],
        listing_id=listing["listingId"])
    ```


    :param str data_exchange_id: The ID of the data exchange. Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces. Used to find the parent resource to bind the IAM policy to
    :param str listing_id: The ID of the listing. Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces. Used to find the parent resource to bind the IAM policy to
    :param str location: The name of the location this data exchange listing.
           Used to find the parent resource to bind the IAM policy to. If not specified,
           the value will be parsed from the identifier of the parent resource. If no location is provided in the parent identifier and no
           location is specified, it is taken from the provider configuration.
    :param str project: The ID of the project in which the resource belongs.
           If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
    """
    __args__ = dict()
    __args__['dataExchangeId'] = data_exchange_id
    __args__['listingId'] = listing_id
    __args__['location'] = location
    __args__['project'] = project
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('gcp:bigqueryanalyticshub/getListingIamPolicy:getListingIamPolicy', __args__, opts=opts, typ=GetListingIamPolicyResult).value

    return AwaitableGetListingIamPolicyResult(
        data_exchange_id=pulumi.get(__ret__, 'data_exchange_id'),
        etag=pulumi.get(__ret__, 'etag'),
        id=pulumi.get(__ret__, 'id'),
        listing_id=pulumi.get(__ret__, 'listing_id'),
        location=pulumi.get(__ret__, 'location'),
        policy_data=pulumi.get(__ret__, 'policy_data'),
        project=pulumi.get(__ret__, 'project'))


@_utilities.lift_output_func(get_listing_iam_policy)
def get_listing_iam_policy_output(data_exchange_id: Optional[pulumi.Input[str]] = None,
                                  listing_id: Optional[pulumi.Input[str]] = None,
                                  location: Optional[pulumi.Input[Optional[str]]] = None,
                                  project: Optional[pulumi.Input[Optional[str]]] = None,
                                  opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetListingIamPolicyResult]:
    """
    Retrieves the current IAM policy data for listing

    ## example

    ```python
    import pulumi
    import pulumi_gcp as gcp

    policy = gcp.bigqueryanalyticshub.get_listing_iam_policy(project=listing["project"],
        location=listing["location"],
        data_exchange_id=listing["dataExchangeId"],
        listing_id=listing["listingId"])
    ```


    :param str data_exchange_id: The ID of the data exchange. Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces. Used to find the parent resource to bind the IAM policy to
    :param str listing_id: The ID of the listing. Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces. Used to find the parent resource to bind the IAM policy to
    :param str location: The name of the location this data exchange listing.
           Used to find the parent resource to bind the IAM policy to. If not specified,
           the value will be parsed from the identifier of the parent resource. If no location is provided in the parent identifier and no
           location is specified, it is taken from the provider configuration.
    :param str project: The ID of the project in which the resource belongs.
           If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
    """
    ...
