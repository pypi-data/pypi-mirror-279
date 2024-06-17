from typing import Any, Dict, Optional

import approck_events_sdk
from approck_events_sdk.event import Event
from approck_messaging.models.message import Message


async def on_success_callback(
    message: Message,
    message_channel: Optional[str] = None,
    exc: Optional[Exception] = None,
    extra: Optional[Dict[str, Any]] = None,
):
    if "mass-message" not in message_channel or "":
        return

    extra = extra or {}

    approck_events_sdk.capture_event(
        Event(
            event_name="mass_message_sent",
            event_json={
                "id": extra.get("id"),
                "send_at": extra.get("send_at"),
            },
            user_id=extra.get("user_id"),
        )
    )


async def on_forbidden_callback(
    message: Message,
    message_channel: Optional[str],
    exc: Optional[Exception] = None,
    extra: Optional[Dict[str, Any]] = None,
):
    if "mass-message" not in message_channel or "":
        return

    extra = extra or {}

    approck_events_sdk.capture_event(
        Event(
            event_name="mass_message_forbidden",
            event_json={
                "id": extra.get("id"),
                "send_at": extra.get("send_at"),
            },
            user_id=extra.get("user_id"),
        )
    )
