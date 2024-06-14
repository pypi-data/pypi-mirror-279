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
    'GetWebAppResult',
    'AwaitableGetWebAppResult',
    'get_web_app',
    'get_web_app_output',
]

@pulumi.output_type
class GetWebAppResult:
    """
    A collection of values returned by getWebApp.
    """
    def __init__(__self__, api_key_id=None, app_id=None, app_urls=None, deletion_policy=None, display_name=None, id=None, name=None, project=None):
        if api_key_id and not isinstance(api_key_id, str):
            raise TypeError("Expected argument 'api_key_id' to be a str")
        pulumi.set(__self__, "api_key_id", api_key_id)
        if app_id and not isinstance(app_id, str):
            raise TypeError("Expected argument 'app_id' to be a str")
        pulumi.set(__self__, "app_id", app_id)
        if app_urls and not isinstance(app_urls, list):
            raise TypeError("Expected argument 'app_urls' to be a list")
        pulumi.set(__self__, "app_urls", app_urls)
        if deletion_policy and not isinstance(deletion_policy, str):
            raise TypeError("Expected argument 'deletion_policy' to be a str")
        pulumi.set(__self__, "deletion_policy", deletion_policy)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if project and not isinstance(project, str):
            raise TypeError("Expected argument 'project' to be a str")
        pulumi.set(__self__, "project", project)

    @property
    @pulumi.getter(name="apiKeyId")
    def api_key_id(self) -> str:
        return pulumi.get(self, "api_key_id")

    @property
    @pulumi.getter(name="appId")
    def app_id(self) -> str:
        """
        Immutable. The globally unique, Firebase-assigned identifier of the App.
        This identifier should be treated as an opaque token, as the data format is not specified.
        """
        return pulumi.get(self, "app_id")

    @property
    @pulumi.getter(name="appUrls")
    def app_urls(self) -> Sequence[str]:
        return pulumi.get(self, "app_urls")

    @property
    @pulumi.getter(name="deletionPolicy")
    def deletion_policy(self) -> str:
        return pulumi.get(self, "deletion_policy")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> str:
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The fully qualified resource name of the App, for example:
        projects/projectId/webApps/appId
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def project(self) -> Optional[str]:
        return pulumi.get(self, "project")


class AwaitableGetWebAppResult(GetWebAppResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetWebAppResult(
            api_key_id=self.api_key_id,
            app_id=self.app_id,
            app_urls=self.app_urls,
            deletion_policy=self.deletion_policy,
            display_name=self.display_name,
            id=self.id,
            name=self.name,
            project=self.project)


def get_web_app(app_id: Optional[str] = None,
                project: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetWebAppResult:
    """
    A Google Cloud Firebase web application instance


    :param str app_id: The app_ip of name of the Firebase webApp.
           
           
           - - -
    :param str project: The ID of the project in which the resource belongs.
           If it is not provided, the provider project is used.
    """
    __args__ = dict()
    __args__['appId'] = app_id
    __args__['project'] = project
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('gcp:firebase/getWebApp:getWebApp', __args__, opts=opts, typ=GetWebAppResult).value

    return AwaitableGetWebAppResult(
        api_key_id=pulumi.get(__ret__, 'api_key_id'),
        app_id=pulumi.get(__ret__, 'app_id'),
        app_urls=pulumi.get(__ret__, 'app_urls'),
        deletion_policy=pulumi.get(__ret__, 'deletion_policy'),
        display_name=pulumi.get(__ret__, 'display_name'),
        id=pulumi.get(__ret__, 'id'),
        name=pulumi.get(__ret__, 'name'),
        project=pulumi.get(__ret__, 'project'))


@_utilities.lift_output_func(get_web_app)
def get_web_app_output(app_id: Optional[pulumi.Input[str]] = None,
                       project: Optional[pulumi.Input[Optional[str]]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetWebAppResult]:
    """
    A Google Cloud Firebase web application instance


    :param str app_id: The app_ip of name of the Firebase webApp.
           
           
           - - -
    :param str project: The ID of the project in which the resource belongs.
           If it is not provided, the provider project is used.
    """
    ...
