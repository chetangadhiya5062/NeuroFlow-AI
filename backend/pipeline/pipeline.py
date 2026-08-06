"""AI Request Pipeline orchestrator executing ordered stage processors."""

import structlog

from backend.conversation import ConversationService
from backend.core.exceptions import PlatformError, ValidationError
from backend.core.ports import ILLMGateway
from backend.core.types import Err, ErrorInfo, Ok, Result
from backend.pipeline.context import PipelineContext
from backend.pipeline.middleware import IPipelineMiddleware, LoggingPipelineMiddleware
from backend.pipeline.processor import (
    ContextCreationProcessor,
    ConversationLoadingProcessor,
    ConversationUpdateProcessor,
    FinalResponseProcessor,
    IPipelineProcessor,
    LLMInvocationProcessor,
    PromptPlaceholderProcessor,
    ProviderResolutionProcessor,
    RequestValidationProcessor,
    ResponseProcessingProcessor,
)
from backend.pipeline.request import PipelineRequest
from backend.pipeline.response import PipelineResponse

logger = structlog.get_logger(__name__)


class AIRequestPipeline:
    """Orchestrator managing sequence execution of AI Request Pipeline stages."""

    def __init__(
        self,
        gateway: ILLMGateway,
        conversation_service: ConversationService,
        processors: list[IPipelineProcessor] | None = None,
        middlewares: list[IPipelineMiddleware] | None = None,
    ) -> None:
        """Initialize AIRequestPipeline with dependencies and stage processors.

        Args:
            gateway: ILLMGateway port implementation.
            conversation_service: ConversationService instance.
            processors: Optional custom list of stage processors.
            middlewares: Optional list of pipeline middlewares.
        """
        self._gateway = gateway
        self._conversation_service = conversation_service
        self._middlewares = middlewares or [LoggingPipelineMiddleware()]

        # Initialize standard 9-stage processors if not explicitly passed
        self._processors = processors or [
            RequestValidationProcessor(),
            ContextCreationProcessor(),
            ConversationLoadingProcessor(conversation_service),
            ProviderResolutionProcessor(),
            PromptPlaceholderProcessor(),
            LLMInvocationProcessor(gateway),
            ResponseProcessingProcessor(),
            ConversationUpdateProcessor(conversation_service),
            FinalResponseProcessor(),
        ]

    async def execute(
        self, request: PipelineRequest
    ) -> Result[PipelineResponse, ErrorInfo]:
        """Execute complete AI request pipeline for incoming request.

        Args:
            request: PipelineRequest payload.

        Returns:
            Result wrapping PipelineResponse or ErrorInfo error payload.
        """
        context = PipelineContext(request=request)
        logger.info("Executing AI Request Pipeline", prompt_len=len(request.prompt))

        try:
            for processor in self._processors:
                await processor.process(context)

            if context.final_response is None:
                return Err(
                    ErrorInfo(
                        message="Pipeline finished without final response.",
                        error_code="PIPELINE_INCOMPLETE_RESPONSE",
                    )
                )

            logger.info(
                "AI Request Pipeline execution succeeded",
                conversation_id=context.final_response.conversation_id,
            )
            return Ok(context.final_response)
        except ValidationError as exc:
            return Err(
                ErrorInfo(
                    message=exc.message,
                    error_code="VALIDATION_ERROR",
                    details=exc.details,
                )
            )
        except PlatformError as exc:
            return Err(
                ErrorInfo(
                    message=exc.message,
                    error_code=exc.error_code,
                    details=exc.details,
                    retryable=exc.retryable,
                )
            )
        except Exception as exc:
            logger.error("Unexpected pipeline failure", exc_info=True)
            return Err(
                ErrorInfo(
                    message=f"Pipeline unexpected execution error: {exc}",
                    error_code="PIPELINE_UNEXPECTED_ERROR",
                )
            )
