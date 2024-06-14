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
    'GetBackupRunResult',
    'AwaitableGetBackupRunResult',
    'get_backup_run',
    'get_backup_run_output',
]

@pulumi.output_type
class GetBackupRunResult:
    """
    A collection of values returned by getBackupRun.
    """
    def __init__(__self__, backup_id=None, id=None, instance=None, location=None, most_recent=None, project=None, start_time=None, status=None):
        if backup_id and not isinstance(backup_id, int):
            raise TypeError("Expected argument 'backup_id' to be a int")
        pulumi.set(__self__, "backup_id", backup_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if instance and not isinstance(instance, str):
            raise TypeError("Expected argument 'instance' to be a str")
        pulumi.set(__self__, "instance", instance)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if most_recent and not isinstance(most_recent, bool):
            raise TypeError("Expected argument 'most_recent' to be a bool")
        pulumi.set(__self__, "most_recent", most_recent)
        if project and not isinstance(project, str):
            raise TypeError("Expected argument 'project' to be a str")
        pulumi.set(__self__, "project", project)
        if start_time and not isinstance(start_time, str):
            raise TypeError("Expected argument 'start_time' to be a str")
        pulumi.set(__self__, "start_time", start_time)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="backupId")
    def backup_id(self) -> int:
        return pulumi.get(self, "backup_id")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def instance(self) -> str:
        return pulumi.get(self, "instance")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Location of the backups.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="mostRecent")
    def most_recent(self) -> Optional[bool]:
        return pulumi.get(self, "most_recent")

    @property
    @pulumi.getter
    def project(self) -> str:
        return pulumi.get(self, "project")

    @property
    @pulumi.getter(name="startTime")
    def start_time(self) -> str:
        """
        The time the backup operation actually started in UTC timezone in RFC 3339 format, for 
        example 2012-11-15T16:19:00.094Z.
        """
        return pulumi.get(self, "start_time")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        The status of this run. Refer to [API reference](https://cloud.google.com/sql/docs/mysql/admin-api/rest/v1beta4/backupRuns#SqlBackupRunStatus) for possible status values.
        """
        return pulumi.get(self, "status")


class AwaitableGetBackupRunResult(GetBackupRunResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetBackupRunResult(
            backup_id=self.backup_id,
            id=self.id,
            instance=self.instance,
            location=self.location,
            most_recent=self.most_recent,
            project=self.project,
            start_time=self.start_time,
            status=self.status)


def get_backup_run(backup_id: Optional[int] = None,
                   instance: Optional[str] = None,
                   most_recent: Optional[bool] = None,
                   project: Optional[str] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetBackupRunResult:
    """
    Use this data source to get information about a Cloud SQL instance backup run.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_gcp as gcp

    backup = gcp.sql.get_backup_run(instance=main["name"],
        most_recent=True)
    ```


    :param int backup_id: The identifier for this backup run. Unique only for a specific Cloud SQL instance.
           If left empty and multiple backups exist for the instance, `most_recent` must be set to `true`.
    :param str instance: The name of the instance the backup is taken from.
    :param bool most_recent: Toggles use of the most recent backup run if multiple backups exist for a 
           Cloud SQL instance.
    :param str project: The project to list instances for. If it
           is not provided, the provider project is used.
    """
    __args__ = dict()
    __args__['backupId'] = backup_id
    __args__['instance'] = instance
    __args__['mostRecent'] = most_recent
    __args__['project'] = project
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('gcp:sql/getBackupRun:getBackupRun', __args__, opts=opts, typ=GetBackupRunResult).value

    return AwaitableGetBackupRunResult(
        backup_id=pulumi.get(__ret__, 'backup_id'),
        id=pulumi.get(__ret__, 'id'),
        instance=pulumi.get(__ret__, 'instance'),
        location=pulumi.get(__ret__, 'location'),
        most_recent=pulumi.get(__ret__, 'most_recent'),
        project=pulumi.get(__ret__, 'project'),
        start_time=pulumi.get(__ret__, 'start_time'),
        status=pulumi.get(__ret__, 'status'))


@_utilities.lift_output_func(get_backup_run)
def get_backup_run_output(backup_id: Optional[pulumi.Input[Optional[int]]] = None,
                          instance: Optional[pulumi.Input[str]] = None,
                          most_recent: Optional[pulumi.Input[Optional[bool]]] = None,
                          project: Optional[pulumi.Input[Optional[str]]] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetBackupRunResult]:
    """
    Use this data source to get information about a Cloud SQL instance backup run.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_gcp as gcp

    backup = gcp.sql.get_backup_run(instance=main["name"],
        most_recent=True)
    ```


    :param int backup_id: The identifier for this backup run. Unique only for a specific Cloud SQL instance.
           If left empty and multiple backups exist for the instance, `most_recent` must be set to `true`.
    :param str instance: The name of the instance the backup is taken from.
    :param bool most_recent: Toggles use of the most recent backup run if multiple backups exist for a 
           Cloud SQL instance.
    :param str project: The project to list instances for. If it
           is not provided, the provider project is used.
    """
    ...
