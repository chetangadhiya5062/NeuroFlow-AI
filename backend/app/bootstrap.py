"""Platform bootstrap logic for initializing settings, logging, and container."""

import logging

import structlog

from backend.config import (
    PydanticConfigurationProvider,
    ServiceContainer,
    Settings,
    get_container,
    get_settings,
)
from backend.conversation import (
    ConversationRepositoryFactory,
    ConversationService,
    IConversationRepository,
)
from backend.core.ports import IConfigurationProvider, ILLMGateway
from backend.llm_gateway import LLMGatewayService, ProviderFactory
from backend.pipeline import AIRequestPipeline
from backend.pipeline.processor import (
    ContextCreationProcessor,
    ConversationLoadingProcessor,
    ConversationUpdateProcessor,
    FinalResponseProcessor,
    LLMInvocationProcessor,
    PromptPlaceholderProcessor,
    ProviderResolutionProcessor,
    RequestValidationProcessor,
    ResponseProcessingProcessor,
)
from backend.prompt_runtime import (
    PromptBuilder,
    PromptRegistry,
    PromptService,
)
from backend.services import ChatService


def configure_logging(settings: Settings) -> None:
    """Configure structlog and standard library logging based on settings.

    Args:
        settings: Root platform settings instance.
    """
    log_level = getattr(logging, settings.logging.level.upper(), logging.INFO)

    renderer: structlog.types.Processor
    if settings.logging.format == "json":
        renderer = structlog.processors.JSONRenderer()
    else:
        renderer = structlog.dev.ConsoleRenderer(colors=True)

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            renderer,
        ],
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def register_foundation_services(
    container: ServiceContainer, settings: Settings
) -> None:
    """Register platform configuration and foundation ports in container.

    Args:
        container: Target ServiceContainer instance.
        settings: Root platform settings instance.
    """
    # Register Configuration Provider
    config_provider = PydanticConfigurationProvider(settings)
    container.register_singleton(
        IConfigurationProvider, instance=config_provider  # type: ignore[type-abstract]
    )

    # Instantiate Provider Factory and target configured LLM provider
    factory = ProviderFactory(settings=settings)
    target_provider_name = settings.llm.provider.lower()
    active_provider = factory.create_provider(target_provider_name)

    gateway_service = LLMGatewayService()
    gateway_service.router.register_provider(active_provider)

    # Ensure Mock provider is also registered if target provider is not mock
    if target_provider_name != "mock":
        mock_provider = factory.create_provider("mock")
        gateway_service.router.register_provider(mock_provider)

    container.register_singleton(
        ILLMGateway, instance=gateway_service  # type: ignore[type-abstract]
    )

    # Register Conversation Repository via Factory
    conv_repo = ConversationRepositoryFactory.create_repository(
        storage_type=settings.conversation.storage,
        sqlite_db_path=settings.conversation.sqlite_db_path,
    )
    container.register_singleton(
        IConversationRepository, instance=conv_repo  # type: ignore[type-abstract]
    )
    conv_service = ConversationService(repository=conv_repo)
    container.register_singleton(ConversationService, instance=conv_service)

    # Register Prompt Registry and Service
    prompt_registry = PromptRegistry()
    default_template = (
        PromptBuilder("default-chat")
        .with_system("You are NeuroFlow AI, an enterprise intelligent agent assistant.")
        .with_user("{prompt}")
        .build()
    )
    prompt_registry.register_template(default_template)
    prompt_service = PromptService(registry=prompt_registry)

    container.register_singleton(PromptRegistry, instance=prompt_registry)
    container.register_singleton(PromptService, instance=prompt_service)

    # Register AI Request Pipeline
    pipeline = AIRequestPipeline(
        gateway=gateway_service,
        conversation_service=conv_service,
        processors=[
            RequestValidationProcessor(),
            ContextCreationProcessor(),
            ConversationLoadingProcessor(conv_service),
            ProviderResolutionProcessor(),
            PromptPlaceholderProcessor(prompt_service),
            LLMInvocationProcessor(gateway_service),
            ResponseProcessingProcessor(),
            ConversationUpdateProcessor(conv_service),
            FinalResponseProcessor(),
        ],
    )
    container.register_singleton(AIRequestPipeline, instance=pipeline)

    # Register Application ChatService delegating to pipeline
    chat_service = ChatService(pipeline=pipeline)
    container.register_singleton(ChatService, instance=chat_service)


def register_infrastructure_adapters(container: ServiceContainer) -> None:
    """Placeholder hook for future infrastructure adapter registrations.

    Args:
        container: Target ServiceContainer instance.
    """
    pass


def register_runtime_engines(container: ServiceContainer) -> None:
    """Placeholder hook for future Layer 3 platform runtime engine registrations.

    Args:
        container: Target ServiceContainer instance.
    """
    pass


def bootstrap_platform(
    container: ServiceContainer | None = None,
    settings: Settings | None = None,
) -> tuple[ServiceContainer, Settings]:
    """Bootstrap platform configuration, logging, and dependency container.

    Args:
        container: Optional explicit ServiceContainer instance.
        settings: Optional explicit Settings instance.

    Returns:
        Tuple of (initialized ServiceContainer, active Settings).
    """
    active_settings = settings or get_settings()
    active_container = container or get_container()

    # 1. Configure structured logging
    configure_logging(active_settings)

    # 2. Register foundation services and services
    register_foundation_services(active_container, active_settings)

    # 3. Register infrastructure adapters (placeholder hook)
    register_infrastructure_adapters(active_container)

    # 4. Register runtime engines (placeholder hook)
    register_runtime_engines(active_container)

    return active_container, active_settings
