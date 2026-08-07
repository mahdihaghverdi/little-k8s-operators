from datetime import datetime

from pydantic import BaseModel

__all__ = ["CreateStatus"]


class CreateStatus(BaseModel):
    createAt: datetime
    updated: bool = False
