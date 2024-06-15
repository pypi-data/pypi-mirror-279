from typing import Optional, Protocol

from approck_messaging.models.message import Message
from loguru import logger


class CallbackType(Protocol):
    async def __call__(self, message: Message, exc: Optional[Exception] = None): ...


async def callback_call(message: Message, exc: Optional[Exception] = None, callback: Optional[CallbackType] = None):
    # noinspection PyBroadException
    try:
        if callback is not None:
            await callback(message=message, exc=exc)
    except Exception:
        logger.exception("Callback exception")
