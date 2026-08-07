import logging
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

import kopf
from kubernetes import client
from kubernetes.client.api_client import ApiClient

from hello_configmap_operator.common import (
    CreateStatus,
    Metadata,
    call_model_dump_on_model,
)
from hello_configmap_operator.manifests import ConfigMap

logger = logging.getLogger(__name__)


@kopf.on.create("hello")
@call_model_dump_on_model
async def create_fn(meta: kopf.Meta, spec: kopf.Spec, **_: Any) -> CreateStatus:
    logger.info(f"{meta.name} is created.")

    config_map = ConfigMap(
        metadata=Metadata(name=f"{meta.name}-configmap", labels=meta.labels)
    )
    config_map_data = config_map.model_dump(mode="json")
    config_map_data["spec"] = {"message": spec["message"]}

    kopf.adopt(config_map_data)

    with ApiClient() as api:
        v1 = client.CoreV1Api(api)
        v1.create_namespaced_config_map(body=config_map_data, namespace=meta.namespace)
    return CreateStatus(createAt=datetime.now(tz=ZoneInfo("Asia/Tehran")))
