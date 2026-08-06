"""Abstract port contracts for Layer 3 platform runtimes and plugins."""

from abc import ABC, abstractmethod
from typing import Any

from backend.core.types import ErrorInfo, Result
from backend.core.value_objects import EntityId, TenantId, Uri


class IWorkflowRuntime(ABC):
    """Abstract port interface for DAG Workflow Engine runtime."""

    @abstractmethod
    async def execute_workflow(
        self,
        workflow_id: EntityId,
        inputs: dict[str, Any],
        tenant_id: TenantId,
    ) -> Result[dict[str, Any], ErrorInfo]:
        """Execute a workflow DAG instance with inputs for tenant."""


class IAgentRuntime(ABC):
    """Abstract port interface for Autonomous Agent reasoning runtime."""

    @abstractmethod
    async def run_agent(
        self,
        agent_id: EntityId,
        goal: str,
        tenant_id: TenantId,
    ) -> Result[dict[str, Any], ErrorInfo]:
        """Run multi-turn agent reasoning loop towards goal for tenant."""


class IToolRuntime(ABC):
    """Abstract port interface for Tool verification and sandboxed execution."""

    @abstractmethod
    async def execute_tool(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        tenant_id: TenantId,
    ) -> Result[Any, ErrorInfo]:
        """Execute tool by name inside sandbox with validated arguments."""


class IPromptRuntime(ABC):
    """Abstract port interface for Prompt compilation and context building."""

    @abstractmethod
    async def compile_prompt(
        self,
        template_id: str,
        variables: dict[str, Any],
    ) -> Result[str, ErrorInfo]:
        """Compile parameterized prompt template with dynamic variables."""


class IRagRuntime(ABC):
    """Abstract port interface for Hybrid RAG retrieval runtime."""

    @abstractmethod
    async def retrieve_context(
        self,
        query: str,
        tenant_id: TenantId,
        top_k: int = 5,
    ) -> Result[list[dict[str, Any]], ErrorInfo]:
        """Retrieve hybrid vector/graph contextual passages for query."""


class IIntegrationRuntime(ABC):
    """Abstract port interface for external API integration transport."""

    @abstractmethod
    async def invoke_endpoint(
        self,
        target_uri: Uri,
        payload: dict[str, Any],
        headers: dict[str, str] | None = None,
    ) -> Result[dict[str, Any], ErrorInfo]:
        """Invoke external HTTP/gRPC REST integration endpoint."""


class IPluginManager(ABC):
    """Abstract port interface for domain plugin lifecycle management."""

    @abstractmethod
    async def register_plugin(
        self,
        plugin_name: str,
        config: dict[str, Any],
    ) -> Result[bool, ErrorInfo]:
        """Register domain plugin module with configuration."""

    @abstractmethod
    async def execute_plugin_hook(
        self,
        hook_name: str,
        payload: dict[str, Any],
    ) -> Result[dict[str, Any], ErrorInfo]:
        """Execute extension hook across registered domain plugins."""
