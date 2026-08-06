"""Unit tests for internal AI Request Pipeline subsystem."""

import pytest

from backend.conversation import (
    ConversationService,
    InMemoryConversationRepository,
)
from backend.llm_gateway import LLMGatewayService
from backend.llm_gateway.providers import MockLLMProviderAdapter
from backend.pipeline import AIRequestPipeline, PipelineRequest


@pytest.mark.asyncio
async def test_ai_request_pipeline_end_to_end() -> None:
    """Test AIRequestPipeline processes 9-stage sequence successfully."""
    gateway = LLMGatewayService()
    gateway.router.register_provider(MockLLMProviderAdapter())

    repo = InMemoryConversationRepository()
    conv_service = ConversationService(repository=repo)

    pipeline = AIRequestPipeline(
        gateway=gateway, conversation_service=conv_service
    )
    request = PipelineRequest(prompt="Hello Pipeline")

    result = await pipeline.execute(request)
    assert result.is_success

    res = result.unwrap()
    assert res.content == "Hello from NeuroFlow AI Mock Provider"
    assert res.provider_used == "mock"
    assert res.model_used == "mock/mock-model"
    assert res.conversation_id is not None

    # Verify conversation was updated in repo
    conv_res = await conv_service.get_conversation(res.conversation_id)
    assert conv_res.is_success
    history = conv_res.unwrap().get_history()
    assert len(history) == 2


@pytest.mark.asyncio
async def test_ai_request_pipeline_validation_failure() -> None:
    """Test AIRequestPipeline returns error result when prompt is empty."""
    gateway = LLMGatewayService()
    repo = InMemoryConversationRepository()
    conv_service = ConversationService(repository=repo)

    pipeline = AIRequestPipeline(
        gateway=gateway, conversation_service=conv_service
    )
    request = PipelineRequest(prompt="")

    result = await pipeline.execute(request)
    assert not result.is_success

    err = result.unwrap_err()
    assert err.error_code == "VALIDATION_ERROR"
    assert "cannot be empty" in err.message
