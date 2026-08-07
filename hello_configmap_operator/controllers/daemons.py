import asyncio
import logging
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

import kopf
from kubernetes import client
from kubernetes.client import ApiClient, ApiException

from hello_configmap_operator.common import (
    DaemonCancelled,
    call_model_dump_on_model,
    create_configmap_data_from_spec_meta,
)

logger = logging.getLogger(__name__)


@kopf.daemon(
    "hellos",
    initial_delay=3,
    cancellation_timeout=10,
)
@call_model_dump_on_model
async def check_configmap_exists(
    stopped: kopf.DaemonStopped,
    meta: kopf.Meta,
    patch: kopf.Patch,
    spec: kopf.Spec,
    **_: Any,
) -> DaemonCancelled:
    logger.info("Daemon check_configmap_exists runs")
    with ApiClient() as api:
        v1 = client.CoreV1Api(api)
        try:
            while True:
                try:
                    v1.read_namespaced_config_map(
                        namespace=meta.namespace,
                        name=f"{meta.name}-configmap",
                    )
                except ApiException as e:
                    match e.status:
                        case 404:
                            config_map_data = create_configmap_data_from_spec_meta(
                                meta, spec
                            )
                            kopf.adopt(config_map_data)

                            v1.create_namespaced_config_map(
                                body=config_map_data, namespace=meta.namespace
                            )

                            patch.status["created_by_daemon_at"] = datetime.now(
                                tz=ZoneInfo("Asia/Tehran")
                            ).isoformat()
                            raise kopf.TemporaryError(
                                "Deleted ConfigMap detected, creating another one.",
                                delay=3,
                            )
                        case _:
                            # unexpected error
                            patch.status["unexpected_error_body"] = repr(e.body)
                            raise kopf.TemporaryError(
                                "Unexpected error in `check_configmap_exists` daemon. "
                                f"Details are stored in .status[unexpected_error_body] of {meta.name!r}",
                                delay=10,
                            )
                else:
                    await stopped.wait(5)
        except asyncio.CancelledError:
            return DaemonCancelled()
