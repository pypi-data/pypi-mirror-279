"""
.. admonition:: Logging
    :class: hint

    Webhook 또는 file에 쉽게 log를 작성할 수 있는 class
"""

from zhl.logging.handler import (
    DiscordHandler,
    SlackBotHandler,
    SlackWebhookHandler,
)
from zhl.logging.logger import Logger

__all__ = ["Logger", "DiscordHandler", "SlackBotHandler", "SlackWebhookHandler"]
