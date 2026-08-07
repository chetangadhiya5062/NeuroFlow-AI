"""Unit and integration tests for Minimal Agent Runtime."""

import tempfile

import pytest

from backend.agent_runtime import (
    AgentActionType,
    AgentRuntimeService,
    SingleAgent,
)
from backend.conversation import (
    ConversationService,
    InMemoryConversationRepository,
)
from backend.knowledge_base import (
    InMemoryKnowledgeBaseRepository,
    KnowledgeBaseService,
    LocalFileStorage,
)
from backend.llm_gateway import LLMGatewayService
from backend.llm_gateway.providers.mock_provider import MockLLMProviderAdapter
from backend.rag import RAGService
from backend.tool_runtime import ToolService


@pytest.mark.asyncio
async def test_agent_example_1_calculator_tool_reasoning_loop() -> None:
    """Test Agent Example 1: Math calculation goal triggers Tool Execution."""
    gateway = LLMGatewayService()
    gateway.router.register_provider(MockLLMProviderAdapter())
    tool_service = ToolService()
    conv_repo = InMemoryConversationRepository()
    conv_service = ConversationService(repository=conv_repo)

    agent = SingleAgent(
        gateway=gateway,
        tool_service=tool_service,
        conversation_service=conv_service,
    )
    service = AgentRuntimeService(agent=agent)

    # Goal: What is 5432 × 92?  # noqa: RUF003
    result = await service.execute_agent(
        goal="What is 5432 × 92?"  # noqa: RUF001
    )
    assert result.is_success
    response = result.unwrap()

    # Verify Reasoning Trajectory
    assert len(response.trajectory) >= 2
    assert response.trajectory[0]["action"] == AgentActionType.EXECUTE_TOOL.value
    assert response.trajectory[0]["name"] == "calculator"
    assert response.trajectory[1]["action"] == AgentActionType.RESPOND.value

    # Verify Tool Results
    assert len(response.tool_results) == 1
    assert response.tool_results[0]["result"] == 499744


@pytest.mark.asyncio
async def test_agent_example_2_rag_knowledge_retrieval_reasoning_loop() -> None:
    """Test Agent Example 2: Knowledge query triggers Knowledge Retrieval."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        gateway = LLMGatewayService()
        gateway.router.register_provider(MockLLMProviderAdapter())

        rag_service = RAGService()
        kb_repo = InMemoryKnowledgeBaseRepository()
        storage = LocalFileStorage(base_directory=tmp_dir)
        kb_service = KnowledgeBaseService(
            repository=kb_repo, storage=storage, rag_service=rag_service
        )

        doc_content = (
            b"# Telecom Architecture\n"
            b"Radio Resource Control (RRC) Setup establishes initial connection "
            b"between User Equipment (UE) and gNodeB base station in 5G NR."
        )
        ingest_res = await kb_service.ingest_document(
            filename="telecom.pdf",
            content=doc_content,
            content_type="application/pdf",
        )
        assert ingest_res.is_success

        agent = SingleAgent(
            gateway=gateway,
            rag_service=rag_service,
        )
        service = AgentRuntimeService(agent=agent)

        # Goal: What does the uploaded telecom document say about RRC Setup?
        result = await service.execute_agent(
            goal="What does the uploaded telecom document say about RRC Setup?"
        )
        assert result.is_success
        response = result.unwrap()

        # Verify Reasoning Trajectory
        assert len(response.trajectory) >= 2
        ret_val = AgentActionType.RETRIEVE_KNOWLEDGE.value
        assert response.trajectory[0]["action"] == ret_val
        assert response.trajectory[1]["action"] == AgentActionType.RESPOND.value

        # Verify Sources
        assert len(response.sources) >= 1
        assert response.sources[0]["filename"] == "telecom.pdf"
        assert "gNodeB base station" in response.sources[0]["text"]
