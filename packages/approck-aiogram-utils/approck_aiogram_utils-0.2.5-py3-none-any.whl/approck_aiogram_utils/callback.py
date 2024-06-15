from typing import Optional, Protocol

from approck_messaging.models.message import Message
from loguru import logger


class CallbackType(Protocol):
    async def __call__(
        self,
        message: Message,
        message_channel: Optional[str] = None,
        exc: Optional[Exception] = None,
    ): ...


async def callback_call(
    message: Message,
    message_channel: Optional[str] = None,
    exc: Optional[Exception] = None,
    callback: Optional[CallbackType] = None,
):
    # noinspection PyBroadException
    try:
        if callback is not None:
            await callback(message=message, message_channel=message_channel, exc=exc)
    except Exception:
        logger.exception("Callback exception")
