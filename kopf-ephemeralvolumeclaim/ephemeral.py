import os
from typing import Any

import kopf
import kubernetes
import yaml


@kopf.on.create("ephemeralvolumeclaims")
def create_fn(
    spec: kopf.Spec,
    name: str,
    namespace: str | None,
    logger: kopf.Logger,
    **_: Any,
) -> dict[str, str]:
    size = spec.get("size")
    if not size:
        raise kopf.PermanentError(f"Size must be set. Got {size!r}.")

    path = os.path.join(os.path.dirname(__file__), "pvc-template.yaml")
    with open(path, "rt") as tmpl:
        text = tmpl.read().format(name=name, size=size)
    data = yaml.safe_load(text)

    api = kubernetes.client.CoreV1Api()
    obj = api.create_namespaced_persistent_volume_claim(
        namespace=namespace,
        body=data,
    )

    logger.info(f"PVC child is created: {obj}")
    return {"pvc-name": obj.metadata.name}


@kopf.on.field("ephemeralvolumeclaims", field="metadata.labels")
def relabel(
    diff: kopf.Diff, status: kopf.Status, namespace: str | None, **_: Any
) -> None:
    """
    The old & new kwargs contain the old & new values of the field
    (or of the whole object for the object handlers).

    It will work as expected when the user adds new labels and changes the existing labels,
    but not when the user deletes the labels from the EVC.
    Why? Because of how patching works in Kubernetes API:
    it merges the dictionaries (with some exceptions).
    To delete a field from the object, you need to set it to None in the patch object.

    So, we need to know which fields were deleted from the EVC.
    Kubernetes does not natively provide this information in object events,
    since it notifies operators only with the latest state of the object
    — as seen in the body/meta kwargs.

    Kopf tracks the state of the objects and calculates the diffs.
    The diffs are provided as the diff kwarg;
    the old & new states of the object or field — as the old & new kwargs.

    A diff-object has this structure:
    ((action, n-tuple of object or field path, old, new),)

     (('add', ('metadata', 'labels', 'label1'), None, 'new-value'),
     ('change', ('metadata', 'labels', 'label2'), 'old-value', 'new-value'),
     ('remove', ('metadata', 'labels', 'label3'), 'old-value', None),
     ('change', ('spec', 'size'), '1G', '2G'))
    """

    labels_patch = {field[0]: new for op, field, old, new in diff}
    pvc_name = status["create_fn"]["pvc-name"]
    pvc_patch = {"metadata": {"labels": labels_patch}}

    api = kubernetes.client.CoreV1Api()
    _obj = api.patch_namespaced_persistent_volume_claim(
        namespace=namespace,
        name=pvc_name,
        body=pvc_patch,
    )
