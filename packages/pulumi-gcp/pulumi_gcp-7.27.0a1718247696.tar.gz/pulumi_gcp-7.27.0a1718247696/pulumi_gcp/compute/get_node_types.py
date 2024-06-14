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
    'GetNodeTypesResult',
    'AwaitableGetNodeTypesResult',
    'get_node_types',
    'get_node_types_output',
]

@pulumi.output_type
class GetNodeTypesResult:
    """
    A collection of values returned by getNodeTypes.
    """
    def __init__(__self__, id=None, names=None, project=None, zone=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if names and not isinstance(names, list):
            raise TypeError("Expected argument 'names' to be a list")
        pulumi.set(__self__, "names", names)
        if project and not isinstance(project, str):
            raise TypeError("Expected argument 'project' to be a str")
        pulumi.set(__self__, "project", project)
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
    def names(self) -> Sequence[str]:
        """
        A list of node types available in the given zone and project.
        """
        return pulumi.get(self, "names")

    @property
    @pulumi.getter
    def project(self) -> str:
        return pulumi.get(self, "project")

    @property
    @pulumi.getter
    def zone(self) -> str:
        return pulumi.get(self, "zone")


class AwaitableGetNodeTypesResult(GetNodeTypesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetNodeTypesResult(
            id=self.id,
            names=self.names,
            project=self.project,
            zone=self.zone)


def get_node_types(project: Optional[str] = None,
                   zone: Optional[str] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetNodeTypesResult:
    """
    Provides available node types for Compute Engine sole-tenant nodes in a zone
    for a given project. For more information, see [the official documentation](https://cloud.google.com/compute/docs/nodes/#types) and [API](https://cloud.google.com/compute/docs/reference/rest/v1/nodeTypes).

    ## Example Usage

    ```python
    import pulumi
    import pulumi_gcp as gcp

    central1b = gcp.compute.get_node_types(zone="us-central1-b")
    tmpl = gcp.compute.NodeTemplate("tmpl",
        name="test-tmpl",
        region="us-central1",
        node_type=types["names"])
    ```


    :param str project: ID of the project to list available node types for.
           Should match the project the nodes of this type will be deployed to.
           Defaults to the project that the provider is authenticated with.
    :param str zone: The zone to list node types for. Should be in zone of intended node groups and region of referencing node template. If `zone` is not specified, the provider-level zone must be set and is used
           instead.
    """
    __args__ = dict()
    __args__['project'] = project
    __args__['zone'] = zone
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('gcp:compute/getNodeTypes:getNodeTypes', __args__, opts=opts, typ=GetNodeTypesResult).value

    return AwaitableGetNodeTypesResult(
        id=pulumi.get(__ret__, 'id'),
        names=pulumi.get(__ret__, 'names'),
        project=pulumi.get(__ret__, 'project'),
        zone=pulumi.get(__ret__, 'zone'))


@_utilities.lift_output_func(get_node_types)
def get_node_types_output(project: Optional[pulumi.Input[Optional[str]]] = None,
                          zone: Optional[pulumi.Input[Optional[str]]] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetNodeTypesResult]:
    """
    Provides available node types for Compute Engine sole-tenant nodes in a zone
    for a given project. For more information, see [the official documentation](https://cloud.google.com/compute/docs/nodes/#types) and [API](https://cloud.google.com/compute/docs/reference/rest/v1/nodeTypes).

    ## Example Usage

    ```python
    import pulumi
    import pulumi_gcp as gcp

    central1b = gcp.compute.get_node_types(zone="us-central1-b")
    tmpl = gcp.compute.NodeTemplate("tmpl",
        name="test-tmpl",
        region="us-central1",
        node_type=types["names"])
    ```


    :param str project: ID of the project to list available node types for.
           Should match the project the nodes of this type will be deployed to.
           Defaults to the project that the provider is authenticated with.
    :param str zone: The zone to list node types for. Should be in zone of intended node groups and region of referencing node template. If `zone` is not specified, the provider-level zone must be set and is used
           instead.
    """
    ...
