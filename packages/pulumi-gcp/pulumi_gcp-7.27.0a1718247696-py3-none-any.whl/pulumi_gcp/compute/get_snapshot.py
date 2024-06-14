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
    'GetSnapshotResult',
    'AwaitableGetSnapshotResult',
    'get_snapshot',
    'get_snapshot_output',
]

@pulumi.output_type
class GetSnapshotResult:
    """
    A collection of values returned by getSnapshot.
    """
    def __init__(__self__, chain_name=None, creation_timestamp=None, description=None, disk_size_gb=None, effective_labels=None, filter=None, id=None, label_fingerprint=None, labels=None, licenses=None, most_recent=None, name=None, project=None, pulumi_labels=None, self_link=None, snapshot_encryption_keys=None, snapshot_id=None, source_disk=None, source_disk_encryption_keys=None, storage_bytes=None, storage_locations=None, zone=None):
        if chain_name and not isinstance(chain_name, str):
            raise TypeError("Expected argument 'chain_name' to be a str")
        pulumi.set(__self__, "chain_name", chain_name)
        if creation_timestamp and not isinstance(creation_timestamp, str):
            raise TypeError("Expected argument 'creation_timestamp' to be a str")
        pulumi.set(__self__, "creation_timestamp", creation_timestamp)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if disk_size_gb and not isinstance(disk_size_gb, int):
            raise TypeError("Expected argument 'disk_size_gb' to be a int")
        pulumi.set(__self__, "disk_size_gb", disk_size_gb)
        if effective_labels and not isinstance(effective_labels, dict):
            raise TypeError("Expected argument 'effective_labels' to be a dict")
        pulumi.set(__self__, "effective_labels", effective_labels)
        if filter and not isinstance(filter, str):
            raise TypeError("Expected argument 'filter' to be a str")
        pulumi.set(__self__, "filter", filter)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if label_fingerprint and not isinstance(label_fingerprint, str):
            raise TypeError("Expected argument 'label_fingerprint' to be a str")
        pulumi.set(__self__, "label_fingerprint", label_fingerprint)
        if labels and not isinstance(labels, dict):
            raise TypeError("Expected argument 'labels' to be a dict")
        pulumi.set(__self__, "labels", labels)
        if licenses and not isinstance(licenses, list):
            raise TypeError("Expected argument 'licenses' to be a list")
        pulumi.set(__self__, "licenses", licenses)
        if most_recent and not isinstance(most_recent, bool):
            raise TypeError("Expected argument 'most_recent' to be a bool")
        pulumi.set(__self__, "most_recent", most_recent)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if project and not isinstance(project, str):
            raise TypeError("Expected argument 'project' to be a str")
        pulumi.set(__self__, "project", project)
        if pulumi_labels and not isinstance(pulumi_labels, dict):
            raise TypeError("Expected argument 'pulumi_labels' to be a dict")
        pulumi.set(__self__, "pulumi_labels", pulumi_labels)
        if self_link and not isinstance(self_link, str):
            raise TypeError("Expected argument 'self_link' to be a str")
        pulumi.set(__self__, "self_link", self_link)
        if snapshot_encryption_keys and not isinstance(snapshot_encryption_keys, list):
            raise TypeError("Expected argument 'snapshot_encryption_keys' to be a list")
        pulumi.set(__self__, "snapshot_encryption_keys", snapshot_encryption_keys)
        if snapshot_id and not isinstance(snapshot_id, int):
            raise TypeError("Expected argument 'snapshot_id' to be a int")
        pulumi.set(__self__, "snapshot_id", snapshot_id)
        if source_disk and not isinstance(source_disk, str):
            raise TypeError("Expected argument 'source_disk' to be a str")
        pulumi.set(__self__, "source_disk", source_disk)
        if source_disk_encryption_keys and not isinstance(source_disk_encryption_keys, list):
            raise TypeError("Expected argument 'source_disk_encryption_keys' to be a list")
        pulumi.set(__self__, "source_disk_encryption_keys", source_disk_encryption_keys)
        if storage_bytes and not isinstance(storage_bytes, int):
            raise TypeError("Expected argument 'storage_bytes' to be a int")
        pulumi.set(__self__, "storage_bytes", storage_bytes)
        if storage_locations and not isinstance(storage_locations, list):
            raise TypeError("Expected argument 'storage_locations' to be a list")
        pulumi.set(__self__, "storage_locations", storage_locations)
        if zone and not isinstance(zone, str):
            raise TypeError("Expected argument 'zone' to be a str")
        pulumi.set(__self__, "zone", zone)

    @property
    @pulumi.getter(name="chainName")
    def chain_name(self) -> str:
        return pulumi.get(self, "chain_name")

    @property
    @pulumi.getter(name="creationTimestamp")
    def creation_timestamp(self) -> str:
        return pulumi.get(self, "creation_timestamp")

    @property
    @pulumi.getter
    def description(self) -> str:
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="diskSizeGb")
    def disk_size_gb(self) -> int:
        return pulumi.get(self, "disk_size_gb")

    @property
    @pulumi.getter(name="effectiveLabels")
    def effective_labels(self) -> Mapping[str, str]:
        return pulumi.get(self, "effective_labels")

    @property
    @pulumi.getter
    def filter(self) -> Optional[str]:
        return pulumi.get(self, "filter")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="labelFingerprint")
    def label_fingerprint(self) -> str:
        return pulumi.get(self, "label_fingerprint")

    @property
    @pulumi.getter
    def labels(self) -> Mapping[str, str]:
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def licenses(self) -> Sequence[str]:
        return pulumi.get(self, "licenses")

    @property
    @pulumi.getter(name="mostRecent")
    def most_recent(self) -> Optional[bool]:
        return pulumi.get(self, "most_recent")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
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
    @pulumi.getter(name="selfLink")
    def self_link(self) -> str:
        return pulumi.get(self, "self_link")

    @property
    @pulumi.getter(name="snapshotEncryptionKeys")
    def snapshot_encryption_keys(self) -> Sequence['outputs.GetSnapshotSnapshotEncryptionKeyResult']:
        return pulumi.get(self, "snapshot_encryption_keys")

    @property
    @pulumi.getter(name="snapshotId")
    def snapshot_id(self) -> int:
        return pulumi.get(self, "snapshot_id")

    @property
    @pulumi.getter(name="sourceDisk")
    def source_disk(self) -> str:
        return pulumi.get(self, "source_disk")

    @property
    @pulumi.getter(name="sourceDiskEncryptionKeys")
    def source_disk_encryption_keys(self) -> Sequence['outputs.GetSnapshotSourceDiskEncryptionKeyResult']:
        return pulumi.get(self, "source_disk_encryption_keys")

    @property
    @pulumi.getter(name="storageBytes")
    def storage_bytes(self) -> int:
        return pulumi.get(self, "storage_bytes")

    @property
    @pulumi.getter(name="storageLocations")
    def storage_locations(self) -> Sequence[str]:
        return pulumi.get(self, "storage_locations")

    @property
    @pulumi.getter
    def zone(self) -> str:
        return pulumi.get(self, "zone")


class AwaitableGetSnapshotResult(GetSnapshotResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSnapshotResult(
            chain_name=self.chain_name,
            creation_timestamp=self.creation_timestamp,
            description=self.description,
            disk_size_gb=self.disk_size_gb,
            effective_labels=self.effective_labels,
            filter=self.filter,
            id=self.id,
            label_fingerprint=self.label_fingerprint,
            labels=self.labels,
            licenses=self.licenses,
            most_recent=self.most_recent,
            name=self.name,
            project=self.project,
            pulumi_labels=self.pulumi_labels,
            self_link=self.self_link,
            snapshot_encryption_keys=self.snapshot_encryption_keys,
            snapshot_id=self.snapshot_id,
            source_disk=self.source_disk,
            source_disk_encryption_keys=self.source_disk_encryption_keys,
            storage_bytes=self.storage_bytes,
            storage_locations=self.storage_locations,
            zone=self.zone)


def get_snapshot(filter: Optional[str] = None,
                 most_recent: Optional[bool] = None,
                 name: Optional[str] = None,
                 project: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSnapshotResult:
    """
    To get more information about Snapshot, see:

    * [API documentation](https://cloud.google.com/compute/docs/reference/rest/v1/snapshots)
    * How-to Guides
        * [Official Documentation](https://cloud.google.com/compute/docs/disks/create-snapshots)

    ## Example Usage

    ```python
    import pulumi
    import pulumi_gcp as gcp

    #by name 
    snapshot = gcp.compute.get_snapshot(name="my-snapshot")
    # using a filter
    latest_snapshot = gcp.compute.get_snapshot(filter="name != my-snapshot",
        most_recent=True)
    ```


    :param str filter: A filter to retrieve the compute snapshot.
           See [gcloud topic filters](https://cloud.google.com/sdk/gcloud/reference/topic/filters) for reference.
           If multiple compute snapshot match, either adjust the filter or specify `most_recent`. One of `name` or `filter` must be provided.
           If you want to use a regular expression, use the `eq` (equal) or `ne` (not equal) operator against a single un-parenthesized expression with or without quotes or against multiple parenthesized expressions. Example `sourceDisk eq '.*(.*/data-disk$).*'`. More details for golang Snapshots list call filters [here](https://pkg.go.dev/google.golang.org/api/compute/v1#SnapshotsListCall.Filter).
    :param bool most_recent: If `filter` is provided, ensures the most recent snapshot is returned when multiple compute snapshot match. 
           
           - - -
    :param str name: The name of the compute snapshot. One of `name` or `filter` must be provided.
    :param str project: The ID of the project in which the resource belongs.
           If it is not provided, the provider project is used.
    """
    __args__ = dict()
    __args__['filter'] = filter
    __args__['mostRecent'] = most_recent
    __args__['name'] = name
    __args__['project'] = project
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('gcp:compute/getSnapshot:getSnapshot', __args__, opts=opts, typ=GetSnapshotResult).value

    return AwaitableGetSnapshotResult(
        chain_name=pulumi.get(__ret__, 'chain_name'),
        creation_timestamp=pulumi.get(__ret__, 'creation_timestamp'),
        description=pulumi.get(__ret__, 'description'),
        disk_size_gb=pulumi.get(__ret__, 'disk_size_gb'),
        effective_labels=pulumi.get(__ret__, 'effective_labels'),
        filter=pulumi.get(__ret__, 'filter'),
        id=pulumi.get(__ret__, 'id'),
        label_fingerprint=pulumi.get(__ret__, 'label_fingerprint'),
        labels=pulumi.get(__ret__, 'labels'),
        licenses=pulumi.get(__ret__, 'licenses'),
        most_recent=pulumi.get(__ret__, 'most_recent'),
        name=pulumi.get(__ret__, 'name'),
        project=pulumi.get(__ret__, 'project'),
        pulumi_labels=pulumi.get(__ret__, 'pulumi_labels'),
        self_link=pulumi.get(__ret__, 'self_link'),
        snapshot_encryption_keys=pulumi.get(__ret__, 'snapshot_encryption_keys'),
        snapshot_id=pulumi.get(__ret__, 'snapshot_id'),
        source_disk=pulumi.get(__ret__, 'source_disk'),
        source_disk_encryption_keys=pulumi.get(__ret__, 'source_disk_encryption_keys'),
        storage_bytes=pulumi.get(__ret__, 'storage_bytes'),
        storage_locations=pulumi.get(__ret__, 'storage_locations'),
        zone=pulumi.get(__ret__, 'zone'))


@_utilities.lift_output_func(get_snapshot)
def get_snapshot_output(filter: Optional[pulumi.Input[Optional[str]]] = None,
                        most_recent: Optional[pulumi.Input[Optional[bool]]] = None,
                        name: Optional[pulumi.Input[Optional[str]]] = None,
                        project: Optional[pulumi.Input[Optional[str]]] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSnapshotResult]:
    """
    To get more information about Snapshot, see:

    * [API documentation](https://cloud.google.com/compute/docs/reference/rest/v1/snapshots)
    * How-to Guides
        * [Official Documentation](https://cloud.google.com/compute/docs/disks/create-snapshots)

    ## Example Usage

    ```python
    import pulumi
    import pulumi_gcp as gcp

    #by name 
    snapshot = gcp.compute.get_snapshot(name="my-snapshot")
    # using a filter
    latest_snapshot = gcp.compute.get_snapshot(filter="name != my-snapshot",
        most_recent=True)
    ```


    :param str filter: A filter to retrieve the compute snapshot.
           See [gcloud topic filters](https://cloud.google.com/sdk/gcloud/reference/topic/filters) for reference.
           If multiple compute snapshot match, either adjust the filter or specify `most_recent`. One of `name` or `filter` must be provided.
           If you want to use a regular expression, use the `eq` (equal) or `ne` (not equal) operator against a single un-parenthesized expression with or without quotes or against multiple parenthesized expressions. Example `sourceDisk eq '.*(.*/data-disk$).*'`. More details for golang Snapshots list call filters [here](https://pkg.go.dev/google.golang.org/api/compute/v1#SnapshotsListCall.Filter).
    :param bool most_recent: If `filter` is provided, ensures the most recent snapshot is returned when multiple compute snapshot match. 
           
           - - -
    :param str name: The name of the compute snapshot. One of `name` or `filter` must be provided.
    :param str project: The ID of the project in which the resource belongs.
           If it is not provided, the provider project is used.
    """
    ...
