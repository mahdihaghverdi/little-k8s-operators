import functools
import inspect
from typing import Any

import kopf
from pydantic import BaseModel

__all__ = ["call_model_dump_on_model", "create_configmap_data_from_spec_meta"]

from hello_configmap_operator.common import Metadata
from hello_configmap_operator.manifests import ConfigMap


def call_model_dump_on_model(fun):
    """Thread and Coroutine decorator to call .model_dump on model"""

    @functools.wraps(fun)
    async def async_wrapper(*args, **kwargs):
        instance: BaseModel = await fun(*args, **kwargs)
        return instance.model_dump(mode="json")

    @functools.wraps(fun)
    def sync_wrapper(*args, **kwargs):
        instance: BaseModel = fun(*args, **kwargs)
        return instance.model_dump(mode="json")

    if inspect.iscoroutinefunction(fun):
        return async_wrapper
    return sync_wrapper


def create_configmap_data_from_spec_meta(
    meta: kopf.Meta, spec: kopf.Spec
) -> dict[str, Any]:
    config_map = ConfigMap(
        metadata=Metadata(
            name=f"{meta.name}-configmap",
            labels=meta.labels,
        ),
        immutable=spec["immutable"],
    )
    config_map_data = config_map.model_dump(mode="json")
    config_map_data["data"] = {"message": spec["message"]}
    return config_map_data
