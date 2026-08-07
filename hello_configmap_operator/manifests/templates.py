from pydantic import BaseModel

from hello_configmap_operator.common.dtypes import (
    APIGroup,
    Metadata,
    Version,
    api_version_gen,
)


class Base(BaseModel):
    api_version: str
    kind: str
    metadata: Metadata


class ConfigMap(Base):
    api_version: str = api_version_gen(APIGroup.core, Version.v1)
    kind: str = "ConfigMap"
    immutable: bool = False
