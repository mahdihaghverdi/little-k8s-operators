import logging
from typing import Any

import kopf

logger = logging.getLogger("playground.operator")


@kopf.on.create("playgrounds")
async def create(
    meta: kopf.Meta,
    spec: kopf.Spec,
    status: kopf.Status,
    resource: kopf.Resource,
    **_: Any,
) -> None:
    logger.info(f"{meta=}")
    logger.info(f"{spec=}")
    logger.info(f"{status=}")
    logger.info(f"{resource=}")


@kopf.on.resume("pg")
async def resume(meta: kopf.Meta, **_: Any) -> None:
    logger.info(f"PlayGround: {meta.name} was created before me!")


@kopf.on.field("playground", field="spec.major")
async def major_changed(spec: kopf.Spec, old: Any, new: Any, **_: Any) -> None:
    logger.info(
        f"PlayGround: {spec['name']}.major experienced this change: {old} -> {new}"
    )


@kopf.on.update("pg")
async def pg_update(diff: kopf.Diff, **_: Any) -> None:
    logger.info(f"{diff=}")
