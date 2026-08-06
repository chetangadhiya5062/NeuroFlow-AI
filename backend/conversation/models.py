"""Enumerations and data models for Conversation subsystem."""

from enum import StrEnum


class MessageRole(StrEnum):
    """Supported roles for conversation messages."""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"
