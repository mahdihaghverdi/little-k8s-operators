import datetime
import importlib
import logging
import random
import sys
from pathlib import Path
from typing import Any

import kopf

sys.path.append(str(Path(__file__).parent.parent))
importlib.import_module("controllers.handlers")
logger = logging.getLogger("hello-configmap")


@kopf.on.startup()
async def startup_fn(**_: Any) -> None:
    logger.info(f"{Path(__file__).parent.name!r} started.")


@kopf.on.cleanup()
async def cleanup_fn(**_: Any) -> None:
    logger.info(f"{Path(__file__).parent.name!r} stopped.")


@kopf.on.probe(id="now")
def get_current_timestamp(**_: Any) -> str:
    return datetime.datetime.now(datetime.UTC).isoformat()


@kopf.on.probe(id="random")
def get_random_value(**_: Any) -> int:
    return random.randint(0, 1_000_000)
