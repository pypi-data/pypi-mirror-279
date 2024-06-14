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
    'RulesetMetadataArgs',
    'RulesetSourceArgs',
    'RulesetSourceFileArgs',
]

@pulumi.input_type
class RulesetMetadataArgs:
    def __init__(__self__, *,
                 services: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        :param pulumi.Input[Sequence[pulumi.Input[str]]] services: Services that this ruleset has declarations for (e.g., "cloud.firestore"). There may be 0+ of these.
        """
        if services is not None:
            pulumi.set(__self__, "services", services)

    @property
    @pulumi.getter
    def services(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Services that this ruleset has declarations for (e.g., "cloud.firestore"). There may be 0+ of these.
        """
        return pulumi.get(self, "services")

    @services.setter
    def services(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "services", value)


@pulumi.input_type
class RulesetSourceArgs:
    def __init__(__self__, *,
                 files: pulumi.Input[Sequence[pulumi.Input['RulesetSourceFileArgs']]],
                 language: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[Sequence[pulumi.Input['RulesetSourceFileArgs']]] files: `File` set constituting the `Source` bundle.
        :param pulumi.Input[str] language: `Language` of the `Source` bundle. If unspecified, the language will default to `FIREBASE_RULES`. Possible values: LANGUAGE_UNSPECIFIED, FIREBASE_RULES, EVENT_FLOW_TRIGGERS
        """
        pulumi.set(__self__, "files", files)
        if language is not None:
            pulumi.set(__self__, "language", language)

    @property
    @pulumi.getter
    def files(self) -> pulumi.Input[Sequence[pulumi.Input['RulesetSourceFileArgs']]]:
        """
        `File` set constituting the `Source` bundle.
        """
        return pulumi.get(self, "files")

    @files.setter
    def files(self, value: pulumi.Input[Sequence[pulumi.Input['RulesetSourceFileArgs']]]):
        pulumi.set(self, "files", value)

    @property
    @pulumi.getter
    def language(self) -> Optional[pulumi.Input[str]]:
        """
        `Language` of the `Source` bundle. If unspecified, the language will default to `FIREBASE_RULES`. Possible values: LANGUAGE_UNSPECIFIED, FIREBASE_RULES, EVENT_FLOW_TRIGGERS
        """
        return pulumi.get(self, "language")

    @language.setter
    def language(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "language", value)


@pulumi.input_type
class RulesetSourceFileArgs:
    def __init__(__self__, *,
                 content: pulumi.Input[str],
                 name: pulumi.Input[str],
                 fingerprint: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] content: Textual Content.
        :param pulumi.Input[str] name: File name.
               
               - - -
        :param pulumi.Input[str] fingerprint: Fingerprint (e.g. github sha) associated with the `File`.
        """
        pulumi.set(__self__, "content", content)
        pulumi.set(__self__, "name", name)
        if fingerprint is not None:
            pulumi.set(__self__, "fingerprint", fingerprint)

    @property
    @pulumi.getter
    def content(self) -> pulumi.Input[str]:
        """
        Textual Content.
        """
        return pulumi.get(self, "content")

    @content.setter
    def content(self, value: pulumi.Input[str]):
        pulumi.set(self, "content", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        File name.

        - - -
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def fingerprint(self) -> Optional[pulumi.Input[str]]:
        """
        Fingerprint (e.g. github sha) associated with the `File`.
        """
        return pulumi.get(self, "fingerprint")

    @fingerprint.setter
    def fingerprint(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "fingerprint", value)


