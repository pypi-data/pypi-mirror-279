"""
.. admonition:: API
    :class: hint

    다양한 API를 쉽게 사용할 수 있는 class들
"""

from zhl.api.discord import Discord
from zhl.api.github import GitHub
from zhl.api.koreainvestment import KoreaInvestment
from zhl.api.open_ai import OpenAI
from zhl.api.slack import SlackBot, SlackWebhook

__all__ = ["Discord", "GitHub", "OpenAI", "SlackWebhook", "SlackBot", "KoreaInvestment"]
