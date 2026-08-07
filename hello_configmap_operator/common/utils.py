import functools
import inspect

from pydantic import BaseModel

__all__ = ["call_model_dump_on_model"]


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
