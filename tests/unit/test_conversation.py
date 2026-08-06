"""Unit tests for Conversation Management subsystem."""

import pytest

from backend.conversation import (
    Conversation,
    ConversationService,
    InMemoryConversationRepository,
    MessageRole,
)
from backend.llm_gateway import LLMGatewayService
from backend.llm_gateway.providers import MockLLMProviderAdapter
from backend.pipeline import AIRequestPipeline
from backend.services import ChatService


@pytest.mark.asyncio
async def test_conversation_creation_and_message_appending() -> None:
    """Test Conversation aggregate creation and message adding."""
    conv = Conversation.create(title="Test Conversation")
    assert conv.title == "Test Conversation"
    assert len(conv.messages) == 0

    msg = conv.add_message(role=MessageRole.USER, content="Hello")
    assert len(conv.messages) == 1
    assert msg.content == "Hello"
    assert msg.role == MessageRole.USER


@pytest.mark.asyncio
async def test_conversation_service_flow() -> None:
    """Test ConversationService lifecycle (create, add message, get history)."""
    repo = InMemoryConversationRepository()
    service = ConversationService(repository=repo)

    conv = await service.create_conversation(title="Session 1")
    assert conv.id is not None

    add_res = await service.add_message(
        conversation_id=conv.id,
        role=MessageRole.USER,
        content="What is AI?",
    )
    assert add_res.is_success

    hist_res = await service.get_history(conv.id)
    assert hist_res.is_success
    history = hist_res.unwrap()
    assert len(history) == 1
    assert history[0].content == "What is AI?"


@pytest.mark.asyncio
async def test_chat_service_records_conversation_history() -> None:
    """Test ChatService records both user and assistant messages in conversation."""
    gateway = LLMGatewayService()
    gateway.router.register_provider(MockLLMProviderAdapter())

    repo = InMemoryConversationRepository()
    conv_service = ConversationService(repository=repo)
    pipeline = AIRequestPipeline(
        gateway=gateway, conversation_service=conv_service
    )
    chat_service = ChatService(pipeline=pipeline)

    result = await chat_service.process_chat(message="Hello Conversation")
    assert result.is_success
    assert result.unwrap() == "Hello from NeuroFlow AI Mock Provider"

    # Verify conversation was automatically created with user and assistant messages
    conversations = await repo.list_conversations()
    assert len(conversations) == 1
    conv = conversations[0]

    history = conv.get_history()
    assert len(history) == 2
    assert history[0].role == MessageRole.USER
    assert history[0].content == "Hello Conversation"
    assert history[1].role == MessageRole.ASSISTANT
    assert history[1].content == "Hello from NeuroFlow AI Mock Provider"
