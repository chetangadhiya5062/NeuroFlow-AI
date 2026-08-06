"""Stage processors orchestrating individual AI request pipeline steps."""

from abc import ABC, abstractmethod
from typing import Any

from backend.conversation import ConversationService, MessageRole
from backend.core.exceptions import ValidationError
from backend.core.ports import ILLMGateway
from backend.core.value_objects import ModelIdentifier
from backend.llm_gateway import ChatMessage, CompletionRequest
from backend.pipeline.context import PipelineContext
from backend.pipeline.response import PipelineResponse
from backend.prompt_runtime import PromptService


class IPipelineProcessor(ABC):
    """Abstract interface contract for pipeline stage processors."""

    @abstractmethod
    async def process(self, context: PipelineContext) -> None:
        """Process pipeline context state for this stage.

        Args:
            context: Mutable PipelineContext object.
        """


class RequestValidationProcessor(IPipelineProcessor):
    """Stage 1: Validates incoming request prompt content."""

    async def process(self, context: PipelineContext) -> None:
        """Validate request prompt is non-empty."""
        if not context.request.prompt or not context.request.prompt.strip():
            raise ValidationError("Chat message prompt cannot be empty.")


class ContextCreationProcessor(IPipelineProcessor):
    """Stage 2: Initializes execution metadata and tracking flags."""

    async def process(self, context: PipelineContext) -> None:
        """Initialize metadata context values."""
        context.metadata["stage"] = "initialized"
        context.metadata["sources"] = []


class ConversationLoadingProcessor(IPipelineProcessor):
    """Stage 3: Loads or creates Conversation aggregate via ConversationService."""

    def __init__(self, conversation_service: ConversationService) -> None:
        """Initialize with ConversationService."""
        self._conversation_service = conversation_service

    async def process(self, context: PipelineContext) -> None:
        """Load target conversation or create new conversation aggregate."""
        cid = context.request.conversation_id
        if cid:
            res = await self._conversation_service.get_conversation(cid)
            if res.is_success:
                context.conversation = res.unwrap()
                return

        context.conversation = (
            await self._conversation_service.create_conversation(
                title="Chat Session"
            )
        )


class ProviderResolutionProcessor(IPipelineProcessor):
    """Stage 4: Resolves target model identifier and provider adapter."""

    async def process(self, context: PipelineContext) -> None:
        """Resolve ModelIdentifier for execution."""
        provider = context.request.provider_name or "mock"
        model_name = context.request.model_name or "mock-model"
        context.model_id = ModelIdentifier(name=model_name, provider=provider)


class PromptPlaceholderProcessor(IPipelineProcessor):
    """Stage 5: Formats prompt text using PromptService, RAG, and Tool Runtime."""

    def __init__(
        self,
        prompt_service: PromptService | None = None,
        rag_service: Any = None,
        tool_service: Any = None,
    ) -> None:
        """Initialize with optional PromptService, RAGService, and ToolService."""
        self._prompt_service = prompt_service
        self._rag_service = rag_service
        self._tool_service = tool_service

    async def process(self, context: PipelineContext) -> None:
        """Format prompt text and inject retrieved RAG / Tool execution results."""
        base_prompt = context.request.prompt.strip()

        # 1. Check Tool Runtime execution intent if ToolService is present
        tool_block = ""
        if self._tool_service is not None:
            tool_res = await self._tool_service.process_prompt_tool_intent(base_prompt)
            if tool_res and tool_res.success:
                context.metadata["tool_result"] = tool_res.result
                tool_block = f"\n\nTool Result: {tool_res.result}"

        # 2. Retrieve RAG context chunks if RAGService is active
        retrieved_sources: list[dict[str, Any]] = []
        context_block = ""
        if self._rag_service is not None:
            rag_res = await self._rag_service.retrieve_context(base_prompt, top_k=3)
            if rag_res.is_success:
                matches = rag_res.unwrap()
                if matches and any(m.score > 0.001 for m in matches):
                    retrieved_sources = self._rag_service.format_sources(matches)
                    chunk_texts = [
                        f"[Source: {m['filename']}]\n{m['text']}"
                        for m in retrieved_sources
                    ]
                    context_block = (
                        "\n\nContext Information:\n" + "\n---\n".join(chunk_texts)
                    )

        context.metadata["sources"] = retrieved_sources

        # 3. Format final augmented prompt
        raw_full_prompt = f"{base_prompt}{tool_block}{context_block}"

        if self._prompt_service is not None:
            context.formatted_prompt = (
                await self._prompt_service.format_user_prompt(raw_full_prompt)
            )
        else:
            context.formatted_prompt = raw_full_prompt


class LLMInvocationProcessor(IPipelineProcessor):
    """Stage 6: Prepares completion payload and invokes LLM Gateway."""

    def __init__(self, gateway: ILLMGateway) -> None:
        """Initialize with ILLMGateway."""
        self._gateway = gateway

    async def process(self, context: PipelineContext) -> None:
        """Invoke LLM Gateway for generation."""
        if context.model_id is None or context.formatted_prompt is None:
            raise ValidationError("Missing model_id or formatted_prompt.")

        # Prepare messages
        messages = [
            ChatMessage(role="user", content=context.formatted_prompt)
        ]
        request = CompletionRequest(
            messages=messages,
            model=context.model_id,
        )
        context.llm_request = request

        # Invoke gateway generate_completion if available
        if hasattr(self._gateway, "generate_completion"):
            generate_fn = getattr(self._gateway, "generate_completion")  # noqa: B009
            result = await generate_fn(request)
            if result.is_success:
                context.llm_response = result.unwrap()
                return
            err = result.unwrap_err()
            raise ValidationError(err.message)

        # Fallback to generate_text port method
        res = await self._gateway.generate_text(
            prompt=context.formatted_prompt, model=context.model_id
        )
        if res.is_success:
            content = res.unwrap()
            from backend.llm_gateway.models import CompletionResponse, UsageInfo

            context.llm_response = CompletionResponse(
                id="comp-text",
                model=context.model_id,
                content=content,
                usage=UsageInfo(
                    prompt_tokens=10, completion_tokens=10, total_tokens=20
                ),
            )
        else:
            raise ValidationError(res.unwrap_err().message)


class ResponseProcessingProcessor(IPipelineProcessor):
    """Stage 7: Extracts generated text and token metrics."""

    async def process(self, context: PipelineContext) -> None:
        """Process LLM completion response."""
        if context.llm_response is None:
            raise ValidationError("No LLM response payload generated.")


class ConversationUpdateProcessor(IPipelineProcessor):
    """Stage 8: Records user and assistant messages in Conversation aggregate."""

    def __init__(self, conversation_service: ConversationService) -> None:
        """Initialize with ConversationService."""
        self._conversation_service = conversation_service

    async def process(self, context: PipelineContext) -> None:
        """Append user and assistant messages to conversation."""
        if (
            context.conversation is not None
            and context.llm_response is not None
        ):
            cid = context.conversation.id
            # 1. Append user message
            await self._conversation_service.add_message(
                conversation_id=cid,
                role=MessageRole.USER,
                content=context.request.prompt,
            )
            # 2. Append assistant response message
            await self._conversation_service.add_message(
                conversation_id=cid,
                role=MessageRole.ASSISTANT,
                content=context.llm_response.content,
            )


class FinalResponseProcessor(IPipelineProcessor):
    """Stage 9: Constructs final PipelineResponse output payload."""

    async def process(self, context: PipelineContext) -> None:
        """Construct final PipelineResponse object."""
        if (
            context.llm_response is None
            or context.conversation is None
            or context.model_id is None
        ):
            raise ValidationError("Incomplete pipeline state for response.")

        context.final_response = PipelineResponse(
            content=context.llm_response.content,
            conversation_id=context.conversation.id.value,
            model_used=context.model_id.canonical_name,
            provider_used=context.model_id.provider,
            tokens_used=context.llm_response.usage.total_tokens,
            estimated_cost=context.llm_response.usage.estimated_cost,
            metadata=dict(context.metadata),
        )
