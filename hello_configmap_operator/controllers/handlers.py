import logging
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

import kopf

from hello_configmap_operator.common import CreateStatus, call_model_dump_on_model

logger = logging.getLogger(__name__)


@kopf.on.create("hello")
@call_model_dump_on_model
async def create_fn(meta: kopf.Meta, **_: Any) -> CreateStatus:
    logger.info(f"{meta.name} is created.")
    return CreateStatus(createAt=datetime.now(tz=ZoneInfo("Asia/Tehran")))
