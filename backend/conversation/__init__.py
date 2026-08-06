"""Conversation Management subsystem for NeuroFlow AI."""

from backend.conversation.adapters import (
    InMemoryConversationRepository,
    SQLiteConversationRepository,
)
from backend.conversation.conversation import Conversation
from backend.conversation.exceptions import (
    ConversationError,
    ConversationNotFoundError,
    InvalidMessageError,
)
from backend.conversation.message import Message
from backend.conversation.models import MessageRole
from backend.conversation.repository import IConversationRepository
from backend.conversation.repository_factory import ConversationRepositoryFactory
from backend.conversation.service import ConversationService

__all__ = [
    "Conversation",
    "ConversationError",
    "ConversationNotFoundError",
    "ConversationRepositoryFactory",
    "ConversationService",
    "IConversationRepository",
    "InMemoryConversationRepository",
    "InvalidMessageError",
    "Message",
    "MessageRole",
    "SQLiteConversationRepository",
]
