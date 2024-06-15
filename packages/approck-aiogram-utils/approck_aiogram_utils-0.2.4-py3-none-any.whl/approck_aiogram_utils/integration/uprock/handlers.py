from typing import Optional

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from approck_messaging.models.message import TransportMessage
from faststream import Context
from faststream.exceptions import NackMessage
from uprock_sdk import terms

from approck_aiogram_utils.callback import CallbackType
from approck_aiogram_utils.message import send_message


async def send_message_handler(
    message: TransportMessage,
    bot: Bot = Context(),
    on_success_callback: Optional[CallbackType] = None,
    on_forbidden_callback: Optional[CallbackType] = None,
):
    if message.caption:
        message.caption = terms.sanitize(message.caption)

    try:
        await send_message(
            bot=bot,
            chat_id=message.recipient.telegram_id,
            message=message,
            on_success_callback=on_success_callback,
            on_forbidden_callback=on_forbidden_callback,
        )
    except TelegramBadRequest:
        # Ack to skip a broken message
        pass
    except Exception as exc:
        raise NackMessage() from exc
