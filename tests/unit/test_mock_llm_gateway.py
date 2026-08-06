"""Unit tests for Mock LLM Provider and LLM Gateway subsystem."""

import pytest

from backend.core.value_objects import ModelIdentifier
from backend.llm_gateway import (
    CompletionRequest,
    LLMGatewayService,
    ModelMetadata,
)
from backend.llm_gateway.models import ChatMessage
from backend.llm_gateway.providers import MockLLMProviderAdapter


@pytest.mark.asyncio
async def test_mock_llm_provider_adapter_generate_completion() -> None:
    """Test MockLLMProviderAdapter returns Ok(CompletionResponse)."""
    provider = MockLLMProviderAdapter(response_text="Test Response")
    model = ModelIdentifier(name="mock-model", provider="mock")

    request = CompletionRequest(
        messages=[ChatMessage(role="user", content="Hello")],
        model=model,
    )

    result = await provider.generate_completion(request)
    assert result.is_success

    res = result.unwrap()
    assert res.content == "Test Response"
    assert res.model.canonical_name == "mock/mock-model"
    assert res.usage.total_tokens == 20


@pytest.mark.asyncio
async def test_mock_llm_provider_adapter_generate_stream() -> None:
    """Test MockLLMProviderAdapter yields StreamChunk."""
    provider = MockLLMProviderAdapter(response_text="Streamed Response")
    model = ModelIdentifier(name="mock-model", provider="mock")

    request = CompletionRequest(
        messages=[ChatMessage(role="user", content="Stream me")],
        model=model,
        stream=True,
    )

    chunks = [chunk async for chunk in provider.generate_stream(request)]
    assert len(chunks) == 1
    assert chunks[0].delta_content == "Streamed Response"


@pytest.mark.asyncio
async def test_llm_gateway_service_generate_text() -> None:
    """Test LLMGatewayService generate_text via MockLLMProviderAdapter."""
    gateway = LLMGatewayService()
    provider = MockLLMProviderAdapter(response_text="Gateway Response")
    gateway.router.register_provider(provider)

    model = ModelIdentifier(name="mock-model", provider="mock")
    result = await gateway.generate_text(prompt="Hello Gateway", model=model)

    assert result.is_success
    assert result.unwrap() == "Gateway Response"


def test_llm_gateway_service_calculate_cost() -> None:
    """Test LLMGatewayService calculate_cost computation."""
    gateway = LLMGatewayService()
    model = ModelIdentifier(name="gpt-4o", provider="openai")

    metadata = ModelMetadata(
        model_id=model,
        provider_name="openai",
        input_cost_per_1k_tokens=0.005,
        output_cost_per_1k_tokens=0.015,
    )
    gateway.registry.register_model(metadata)

    cost = gateway.calculate_cost(
        model_id=model,
        prompt_tokens=1000,
        completion_tokens=1000,
    )
    assert cost == 0.02
