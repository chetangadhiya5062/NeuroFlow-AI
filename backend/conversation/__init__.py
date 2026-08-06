"""Conversation Management subsystem for NeuroFlow AI."""

from backend.conversation.conversation import Conversation
from backend.conversation.exceptions import (
    ConversationError,
    ConversationNotFoundError,
    InvalidMessageError,
)
from backend.conversation.message import Message
from backend.conversation.models import MessageRole
from backend.conversation.repository import (
    IConversationRepository,
    InMemoryConversationRepository,
)
from backend.conversation.service import ConversationService

__all__ = [
    "Conversation",
    "ConversationError",
    "ConversationNotFoundError",
    "ConversationService",
    "IConversationRepository",
    "InMemoryConversationRepository",
    "InvalidMessageError",
    "Message",
    "MessageRole",
]
