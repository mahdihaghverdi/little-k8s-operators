from datetime import datetime
from enum import StrEnum
from typing import Any
from uuid import UUID

from pydantic import BaseModel

__all__ = [
    "APIGroup",
    "CreateStatus",
    "DaemonCancelled",
    "Metadata",
    "Version",
    "api_version_gen",
]


class CreateStatus(BaseModel):
    create_at: datetime


class APIGroup(StrEnum):
    core = ""
    admissionregistration = "admissionregistration.k8s.io"
    apiextensions = "apiextensions.k8s.io"
    apiregistration = "apiregistration.k8s.io"
    apps = "apps"
    authentication = "authentication.k8s.io"
    authorization = "authorization.k8s.io"
    autoscaling = "autoscaling"
    batch = "batch"
    certificates = "certificates.k8s.io"
    coordination = "coordination.k8s.io"
    discovery = "discovery.k8s.io"
    events = "events.k8s.io"
    flowcontrol = "flowcontrol.apiserver.k8s.io"
    internal = "internal.apiserver.k8s.io"
    networking = "networking.k8s.io"
    node = "node.k8s.io"
    policy = "policy"
    rbac = "rbac.authorization.k8s.io"
    resource = "resource.k8s.io"
    scheduling = "scheduling.k8s.io"
    storage = "storage.k8s.io"
    storagemigration = "storagemigration.k8s.io"


class Version(StrEnum):
    v1 = "v1"
    v2 = "v2"

    v1alpha1 = "v1alpha1"
    v1alpha2 = "v1alpha2"
    v1alpha3 = "v1alpha3"

    v1beta1 = "v1beta1"
    v1beta2 = "v1beta2"


def api_version_gen(group: APIGroup, version: Version) -> str:
    if group is APIGroup.core:
        return version

    return f"{group}/{version}"


class Metadata(BaseModel):
    name: str
    labels: dict[str, Any]
    namespace: str = "default"
    uid: UUID | None = None


class DaemonCancelled(BaseModel):
    daemon_cancelled: bool = True
