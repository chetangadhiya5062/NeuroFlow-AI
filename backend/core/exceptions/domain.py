"""Domain and subsystem exception categories for NeuroFlow AI."""

from typing import Any

from backend.core.exceptions.base import PlatformError

# ==============================================================================
# Core System Exceptions
# ==============================================================================


class ConfigurationError(PlatformError):
    """Raised when platform configuration or environment settings are invalid."""

    def __init__(
        self,
        message: str,
        error_code: str = "CONFIGURATION_ERROR",
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize ConfigurationError."""
        super().__init__(
            message=message,
            error_code=error_code,
            details=details,
            retryable=False,
        )


class ValidationError(PlatformError):
    """Raised when domain entity, payload, or DSL validation fails."""

    def __init__(
        self,
        message: str,
        error_code: str = "VALIDATION_ERROR",
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize ValidationError."""
        super().__init__(
            message=message,
            error_code=error_code,
            details=details,
            retryable=False,
        )


class AuthenticationError(PlatformError):
    """Raised when user or client identity authentication fails."""

    def __init__(
        self,
        message: str = "Authentication failed",
        error_code: str = "AUTHENTICATION_ERROR",
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize AuthenticationError."""
        super().__init__(
            message=message,
            error_code=error_code,
            details=details,
            retryable=False,
        )


class AuthorizationError(PlatformError):
    """Raised when access is denied due to insufficient permissions."""

    def __init__(
        self,
        message: str = "Permission denied",
        error_code: str = "AUTHORIZATION_ERROR",
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize AuthorizationError."""
        super().__init__(
            message=message,
            error_code=error_code,
            details=details,
            retryable=False,
        )


class NotFoundError(PlatformError):
    """Raised when a requested domain entity or resource does not exist."""

    def __init__(
        self,
        message: str,
        error_code: str = "NOT_FOUND_ERROR",
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize NotFoundError."""
        super().__init__(
            message=message,
            error_code=error_code,
            details=details,
            retryable=False,
        )


class ConflictError(PlatformError):
    """Raised when a resource state conflict or concurrent modification occurs."""

    def __init__(
        self,
        message: str,
        error_code: str = "CONFLICT_ERROR",
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize ConflictError."""
        super().__init__(
            message=message,
            error_code=error_code,
            details=details,
            retryable=True,
        )


class PlatformTimeoutError(PlatformError):
    """Raised when an operation times out before completing."""

    def __init__(
        self,
        message: str = "Operation timed out",
        error_code: str = "TIMEOUT_ERROR",
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize PlatformTimeoutError."""
        super().__init__(
            message=message,
            error_code=error_code,
            details=details,
            retryable=True,
        )


class ResourceExhaustedError(PlatformError):
    """Raised when rate limits, token budgets, or tenant quotas are exceeded."""

    def __init__(
        self,
        message: str = "Resource quota or rate limit exceeded",
        error_code: str = "RESOURCE_EXHAUSTED",
        details: dict[str, Any] | None = None,
        retryable: bool = True,
    ) -> None:
        """Initialize ResourceExhaustedError."""
        super().__init__(
            message=message,
            error_code=error_code,
            details=details,
            retryable=retryable,
        )


# ==============================================================================
# Infrastructure & External Service Exceptions
# ==============================================================================


class InfrastructureError(PlatformError):
    """Raised when a low-level infrastructure adapter operation fails."""

    def __init__(
        self,
        message: str,
        error_code: str = "INFRASTRUCTURE_ERROR",
        details: dict[str, Any] | None = None,
        retryable: bool = True,
    ) -> None:
        """Initialize InfrastructureError."""
        super().__init__(
            message=message,
            error_code=error_code,
            details=details,
            retryable=retryable,
        )


class ExternalServiceError(InfrastructureError):
    """Raised when an external API or network service call fails."""

    def __init__(
        self,
        message: str,
        error_code: str = "EXTERNAL_SERVICE_ERROR",
        details: dict[str, Any] | None = None,
        retryable: bool = True,
    ) -> None:
        """Initialize ExternalServiceError."""
        super().__init__(
            message=message,
            error_code=error_code,
            details=details,
            retryable=retryable,
        )


class VectorStoreError(InfrastructureError):
    """Raised when a vector database operation fails."""

    def __init__(
        self,
        message: str,
        error_code: str = "VECTOR_STORE_ERROR",
        details: dict[str, Any] | None = None,
        retryable: bool = True,
    ) -> None:
        """Initialize VectorStoreError."""
        super().__init__(
            message=message,
            error_code=error_code,
            details=details,
            retryable=retryable,
        )


class GraphStoreError(InfrastructureError):
    """Raised when a graph database operation fails."""

    def __init__(
        self,
        message: str,
        error_code: str = "GRAPH_STORE_ERROR",
        details: dict[str, Any] | None = None,
        retryable: bool = True,
    ) -> None:
        """Initialize GraphStoreError."""
        super().__init__(
            message=message,
            error_code=error_code,
            details=details,
            retryable=retryable,
        )


class LLMProviderError(InfrastructureError):
    """Raised when an LLM provider API call fails."""

    def __init__(
        self,
        message: str,
        error_code: str = "LLM_PROVIDER_ERROR",
        details: dict[str, Any] | None = None,
        retryable: bool = True,
    ) -> None:
        """Initialize LLMProviderError."""
        super().__init__(
            message=message,
            error_code=error_code,
            details=details,
            retryable=retryable,
        )


# ==============================================================================
# Execution Engine Exceptions
# ==============================================================================


class ExecutionError(PlatformError):
    """Raised when a runtime execution engine encounters a processing failure."""

    def __init__(
        self,
        message: str,
        error_code: str = "EXECUTION_ERROR",
        details: dict[str, Any] | None = None,
        retryable: bool = False,
    ) -> None:
        """Initialize ExecutionError."""
        super().__init__(
            message=message,
            error_code=error_code,
            details=details,
            retryable=retryable,
        )


# ==============================================================================
# Plugin Subsystem Exceptions
# ==============================================================================


class PluginError(PlatformError):
    """Base exception for plugin ecosystem failures."""

    def __init__(
        self,
        message: str,
        error_code: str = "PLUGIN_ERROR",
        details: dict[str, Any] | None = None,
        retryable: bool = False,
    ) -> None:
        """Initialize PluginError."""
        super().__init__(
            message=message,
            error_code=error_code,
            details=details,
            retryable=retryable,
        )


class PluginNotFoundError(PluginError, NotFoundError):
    """Raised when a requested domain plugin is not registered."""

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize PluginNotFoundError."""
        super().__init__(
            message=message,
            error_code="PLUGIN_NOT_FOUND",
            details=details,
            retryable=False,
        )


class PluginExecutionError(PluginError, ExecutionError):
    """Raised when a domain plugin hook execution fails."""

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
        retryable: bool = False,
    ) -> None:
        """Initialize PluginExecutionError."""
        super().__init__(
            message=message,
            error_code="PLUGIN_EXECUTION_ERROR",
            details=details,
            retryable=retryable,
        )


class PluginSecurityError(PluginError, AuthorizationError):
    """Raised when a plugin violates sandbox security policies."""

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize PluginSecurityError."""
        super().__init__(
            message=message,
            error_code="PLUGIN_SECURITY_VIOLATION",
            details=details,
            retryable=False,
        )


# ==============================================================================
# Subsystem Specific Exceptions
# ==============================================================================


class WorkflowError(PlatformError):
    """Base exception for Workflow Engine failures."""

    def __init__(
        self,
        message: str,
        error_code: str = "WORKFLOW_ERROR",
        details: dict[str, Any] | None = None,
        retryable: bool = False,
    ) -> None:
        """Initialize WorkflowError."""
        super().__init__(
            message=message,
            error_code=error_code,
            details=details,
            retryable=retryable,
        )


class WorkflowNotFoundError(WorkflowError, NotFoundError):
    """Raised when a workflow definition or instance is not found."""

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize WorkflowNotFoundError."""
        super().__init__(
            message=message,
            error_code="WORKFLOW_NOT_FOUND",
            details=details,
            retryable=False,
        )


class WorkflowExecutionError(WorkflowError, ExecutionError):
    """Raised when a workflow DAG execution or task node fails."""

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
        retryable: bool = False,
    ) -> None:
        """Initialize WorkflowExecutionError."""
        super().__init__(
            message=message,
            error_code="WORKFLOW_EXECUTION_ERROR",
            details=details,
            retryable=retryable,
        )


class WorkflowValidationError(WorkflowError, ValidationError):
    """Raised when workflow DSL structure or validation fails."""

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize WorkflowValidationError."""
        super().__init__(
            message=message,
            error_code="WORKFLOW_VALIDATION_ERROR",
            details=details,
            retryable=False,
        )


class CompensationError(WorkflowError, ExecutionError):
    """Raised when a Saga compensation rollback fails."""

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize CompensationError."""
        super().__init__(
            message=message,
            error_code="COMPENSATION_FAILURE",
            details=details,
            retryable=False,
        )


class AgentError(PlatformError):
    """Base exception for Agent Runtime failures."""

    def __init__(
        self,
        message: str,
        error_code: str = "AGENT_ERROR",
        details: dict[str, Any] | None = None,
        retryable: bool = False,
    ) -> None:
        """Initialize AgentError."""
        super().__init__(
            message=message,
            error_code=error_code,
            details=details,
            retryable=retryable,
        )


class AgentExecutionError(AgentError, ExecutionError):
    """Raised when an agent reasoning cycle or multi-turn execution fails."""

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
        retryable: bool = False,
    ) -> None:
        """Initialize AgentExecutionError."""
        super().__init__(
            message=message,
            error_code="AGENT_EXECUTION_ERROR",
            details=details,
            retryable=retryable,
        )


class AgentPlanningError(AgentError):
    """Raised when agent goal decomposition or plan generation fails."""

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize AgentPlanningError."""
        super().__init__(
            message=message,
            error_code="AGENT_PLANNING_ERROR",
            details=details,
            retryable=False,
        )


class ToolError(PlatformError):
    """Base exception for Tool Runtime failures."""

    def __init__(
        self,
        message: str,
        error_code: str = "TOOL_ERROR",
        details: dict[str, Any] | None = None,
        retryable: bool = False,
    ) -> None:
        """Initialize ToolError."""
        super().__init__(
            message=message,
            error_code=error_code,
            details=details,
            retryable=retryable,
        )


class ToolNotFoundError(ToolError, NotFoundError):
    """Raised when a requested tool definition is not found in the registry."""

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize ToolNotFoundError."""
        super().__init__(
            message=message,
            error_code="TOOL_NOT_FOUND",
            details=details,
            retryable=False,
        )


class ToolExecutionError(ToolError, ExecutionError):
    """Raised when tool execution inside the sandbox fails."""

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
        retryable: bool = False,
    ) -> None:
        """Initialize ToolExecutionError."""
        super().__init__(
            message=message,
            error_code="TOOL_EXECUTION_ERROR",
            details=details,
            retryable=retryable,
        )


class ToolValidationError(ToolError, ValidationError):
    """Raised when tool input arguments fail schema validation."""

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize ToolValidationError."""
        super().__init__(
            message=message,
            error_code="TOOL_VALIDATION_ERROR",
            details=details,
            retryable=False,
        )


class KnowledgeError(PlatformError):
    """Base exception for Knowledge Base and Knowledge Graph failures."""

    def __init__(
        self,
        message: str,
        error_code: str = "KNOWLEDGE_ERROR",
        details: dict[str, Any] | None = None,
        retryable: bool = False,
    ) -> None:
        """Initialize KnowledgeError."""
        super().__init__(
            message=message,
            error_code=error_code,
            details=details,
            retryable=retryable,
        )


class KnowledgeBaseError(KnowledgeError):
    """Raised when document ingestion, parsing, or chunking fails."""

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
        retryable: bool = False,
    ) -> None:
        """Initialize KnowledgeBaseError."""
        super().__init__(
            message=message,
            error_code="KNOWLEDGE_BASE_ERROR",
            details=details,
            retryable=retryable,
        )


class KnowledgeGraphError(KnowledgeError):
    """Raised when entity-relationship resolution or graph traversal fails."""

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
        retryable: bool = False,
    ) -> None:
        """Initialize KnowledgeGraphError."""
        super().__init__(
            message=message,
            error_code="KNOWLEDGE_GRAPH_ERROR",
            details=details,
            retryable=retryable,
        )


class MemoryLayerError(PlatformError):
    """Base exception for AI Memory Layer operation failures."""

    def __init__(
        self,
        message: str,
        error_code: str = "MEMORY_LAYER_ERROR",
        details: dict[str, Any] | None = None,
        retryable: bool = False,
    ) -> None:
        """Initialize MemoryLayerError."""
        super().__init__(
            message=message,
            error_code=error_code,
            details=details,
            retryable=retryable,
        )


class MemoryReadError(MemoryLayerError):
    """Raised when memory retrieval fails."""

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize MemoryReadError."""
        super().__init__(
            message=message,
            error_code="MEMORY_READ_ERROR",
            details=details,
            retryable=True,
        )


class MemoryWriteError(MemoryLayerError):
    """Raised when memory persistence fails."""

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize MemoryWriteError."""
        super().__init__(
            message=message,
            error_code="MEMORY_WRITE_ERROR",
            details=details,
            retryable=True,
        )
