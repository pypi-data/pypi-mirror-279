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
    'GetEnvironmentResult',
    'AwaitableGetEnvironmentResult',
    'get_environment',
    'get_environment_output',
]

@pulumi.output_type
class GetEnvironmentResult:
    """
    A collection of values returned by getEnvironment.
    """
    def __init__(__self__, configs=None, effective_labels=None, id=None, labels=None, name=None, project=None, pulumi_labels=None, region=None, storage_configs=None):
        if configs and not isinstance(configs, list):
            raise TypeError("Expected argument 'configs' to be a list")
        pulumi.set(__self__, "configs", configs)
        if effective_labels and not isinstance(effective_labels, dict):
            raise TypeError("Expected argument 'effective_labels' to be a dict")
        pulumi.set(__self__, "effective_labels", effective_labels)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if labels and not isinstance(labels, dict):
            raise TypeError("Expected argument 'labels' to be a dict")
        pulumi.set(__self__, "labels", labels)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if project and not isinstance(project, str):
            raise TypeError("Expected argument 'project' to be a str")
        pulumi.set(__self__, "project", project)
        if pulumi_labels and not isinstance(pulumi_labels, dict):
            raise TypeError("Expected argument 'pulumi_labels' to be a dict")
        pulumi.set(__self__, "pulumi_labels", pulumi_labels)
        if region and not isinstance(region, str):
            raise TypeError("Expected argument 'region' to be a str")
        pulumi.set(__self__, "region", region)
        if storage_configs and not isinstance(storage_configs, list):
            raise TypeError("Expected argument 'storage_configs' to be a list")
        pulumi.set(__self__, "storage_configs", storage_configs)

    @property
    @pulumi.getter
    def configs(self) -> Sequence['outputs.GetEnvironmentConfigResult']:
        """
        Configuration parameters for the environment.
        """
        return pulumi.get(self, "configs")

    @property
    @pulumi.getter(name="effectiveLabels")
    def effective_labels(self) -> Mapping[str, str]:
        return pulumi.get(self, "effective_labels")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def labels(self) -> Mapping[str, str]:
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def project(self) -> Optional[str]:
        return pulumi.get(self, "project")

    @property
    @pulumi.getter(name="pulumiLabels")
    def pulumi_labels(self) -> Mapping[str, str]:
        return pulumi.get(self, "pulumi_labels")

    @property
    @pulumi.getter
    def region(self) -> Optional[str]:
        return pulumi.get(self, "region")

    @property
    @pulumi.getter(name="storageConfigs")
    def storage_configs(self) -> Sequence['outputs.GetEnvironmentStorageConfigResult']:
        return pulumi.get(self, "storage_configs")


class AwaitableGetEnvironmentResult(GetEnvironmentResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetEnvironmentResult(
            configs=self.configs,
            effective_labels=self.effective_labels,
            id=self.id,
            labels=self.labels,
            name=self.name,
            project=self.project,
            pulumi_labels=self.pulumi_labels,
            region=self.region,
            storage_configs=self.storage_configs)


def get_environment(name: Optional[str] = None,
                    project: Optional[str] = None,
                    region: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetEnvironmentResult:
    """
    Provides access to Cloud Composer environment configuration in a region for a given project.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_gcp as gcp

    composer_env_environment = gcp.composer.Environment("composer_env", name="composer-environment")
    composer_env = gcp.composer.get_environment(name=test["name"])
    pulumi.export("debug", composer_env.configs)
    ```


    :param str name: Name of the environment.
    :param str project: The ID of the project in which the resource belongs.
           If it is not provided, the provider project is used.
    :param str region: The location or Compute Engine region of the environment.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['project'] = project
    __args__['region'] = region
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('gcp:composer/getEnvironment:getEnvironment', __args__, opts=opts, typ=GetEnvironmentResult).value

    return AwaitableGetEnvironmentResult(
        configs=pulumi.get(__ret__, 'configs'),
        effective_labels=pulumi.get(__ret__, 'effective_labels'),
        id=pulumi.get(__ret__, 'id'),
        labels=pulumi.get(__ret__, 'labels'),
        name=pulumi.get(__ret__, 'name'),
        project=pulumi.get(__ret__, 'project'),
        pulumi_labels=pulumi.get(__ret__, 'pulumi_labels'),
        region=pulumi.get(__ret__, 'region'),
        storage_configs=pulumi.get(__ret__, 'storage_configs'))


@_utilities.lift_output_func(get_environment)
def get_environment_output(name: Optional[pulumi.Input[str]] = None,
                           project: Optional[pulumi.Input[Optional[str]]] = None,
                           region: Optional[pulumi.Input[Optional[str]]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetEnvironmentResult]:
    """
    Provides access to Cloud Composer environment configuration in a region for a given project.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_gcp as gcp

    composer_env_environment = gcp.composer.Environment("composer_env", name="composer-environment")
    composer_env = gcp.composer.get_environment(name=test["name"])
    pulumi.export("debug", composer_env.configs)
    ```


    :param str name: Name of the environment.
    :param str project: The ID of the project in which the resource belongs.
           If it is not provided, the provider project is used.
    :param str region: The location or Compute Engine region of the environment.
    """
    ...
