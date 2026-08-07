from pydantic import BaseModel, Field

from hello_configmap_operator.common.dtypes import (
    APIGroup,
    Metadata,
    Version,
    api_version_gen,
)


class Base(BaseModel):
    api_version: str = Field(serialization_alias="apiVersion")
    kind: str
    metadata: Metadata


class ConfigMap(Base):
    api_version: str = api_version_gen(APIGroup.core, Version.v1)
    kind: str = "ConfigMap"
