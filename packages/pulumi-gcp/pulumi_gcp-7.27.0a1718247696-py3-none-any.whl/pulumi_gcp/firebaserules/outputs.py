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
    'RulesetMetadata',
    'RulesetSource',
    'RulesetSourceFile',
]

@pulumi.output_type
class RulesetMetadata(dict):
    def __init__(__self__, *,
                 services: Optional[Sequence[str]] = None):
        """
        :param Sequence[str] services: Services that this ruleset has declarations for (e.g., "cloud.firestore"). There may be 0+ of these.
        """
        if services is not None:
            pulumi.set(__self__, "services", services)

    @property
    @pulumi.getter
    def services(self) -> Optional[Sequence[str]]:
        """
        Services that this ruleset has declarations for (e.g., "cloud.firestore"). There may be 0+ of these.
        """
        return pulumi.get(self, "services")


@pulumi.output_type
class RulesetSource(dict):
    def __init__(__self__, *,
                 files: Sequence['outputs.RulesetSourceFile'],
                 language: Optional[str] = None):
        """
        :param Sequence['RulesetSourceFileArgs'] files: `File` set constituting the `Source` bundle.
        :param str language: `Language` of the `Source` bundle. If unspecified, the language will default to `FIREBASE_RULES`. Possible values: LANGUAGE_UNSPECIFIED, FIREBASE_RULES, EVENT_FLOW_TRIGGERS
        """
        pulumi.set(__self__, "files", files)
        if language is not None:
            pulumi.set(__self__, "language", language)

    @property
    @pulumi.getter
    def files(self) -> Sequence['outputs.RulesetSourceFile']:
        """
        `File` set constituting the `Source` bundle.
        """
        return pulumi.get(self, "files")

    @property
    @pulumi.getter
    def language(self) -> Optional[str]:
        """
        `Language` of the `Source` bundle. If unspecified, the language will default to `FIREBASE_RULES`. Possible values: LANGUAGE_UNSPECIFIED, FIREBASE_RULES, EVENT_FLOW_TRIGGERS
        """
        return pulumi.get(self, "language")


@pulumi.output_type
class RulesetSourceFile(dict):
    def __init__(__self__, *,
                 content: str,
                 name: str,
                 fingerprint: Optional[str] = None):
        """
        :param str content: Textual Content.
        :param str name: File name.
               
               - - -
        :param str fingerprint: Fingerprint (e.g. github sha) associated with the `File`.
        """
        pulumi.set(__self__, "content", content)
        pulumi.set(__self__, "name", name)
        if fingerprint is not None:
            pulumi.set(__self__, "fingerprint", fingerprint)

    @property
    @pulumi.getter
    def content(self) -> str:
        """
        Textual Content.
        """
        return pulumi.get(self, "content")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        File name.

        - - -
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def fingerprint(self) -> Optional[str]:
        """
        Fingerprint (e.g. github sha) associated with the `File`.
        """
        return pulumi.get(self, "fingerprint")


