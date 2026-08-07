import logging
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

import kopf
from kubernetes import client
from kubernetes.client.api_client import ApiClient

from hello_configmap_operator.common import (
    CreateStatus,
    call_model_dump_on_model,
    create_configmap_data_from_spec_meta,
)

logger = logging.getLogger(__name__)


@kopf.on.create("hello")
@call_model_dump_on_model
async def create_fn(meta: kopf.Meta, spec: kopf.Spec, **_: Any) -> CreateStatus:
    logger.info(f"{meta.name} is created.")

    config_map_data = create_configmap_data_from_spec_meta(meta, spec)
    kopf.adopt(config_map_data)

    with ApiClient() as api:
        v1 = client.CoreV1Api(api)
        v1.create_namespaced_config_map(body=config_map_data, namespace=meta.namespace)
    return CreateStatus(create_at=datetime.now(tz=ZoneInfo("Asia/Tehran")))
