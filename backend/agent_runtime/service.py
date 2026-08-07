"""Agent Runtime Application Domain Service."""

from backend.agent_runtime.agent import SingleAgent
from backend.agent_runtime.reasoning import AgentResponse
from backend.conversation import ConversationService
from backend.core.ports import ILLMGateway
from backend.core.types import Err, ErrorInfo, Ok, Result
from backend.rag import RAGService
from backend.tool_runtime import ToolService


class AgentRuntimeService:
    """Domain application service exposing agent execution to platform components."""

    def __init__(
        self,
        agent: SingleAgent | None = None,
        gateway: ILLMGateway | None = None,
        tool_service: ToolService | None = None,
        rag_service: RAGService | None = None,
        conversation_service: ConversationService | None = None,
    ) -> None:
        """Initialize AgentRuntimeService with agent instance or dependencies."""
        if agent is not None:
            self._agent = agent
        elif gateway is not None:
            self._agent = SingleAgent(
                gateway=gateway,
                tool_service=tool_service,
                rag_service=rag_service,
                conversation_service=conversation_service,
            )
        else:
            raise ValueError(
                "Either 'agent' or 'gateway' must be provided to AgentRuntimeService."
            )

    async def execute_agent(
        self,
        goal: str,
        conversation_id: str | None = None,
        max_iterations: int = 5,
    ) -> Result[AgentResponse, ErrorInfo]:
        """Execute single-agent reasoning loop for user goal.

        Args:
            goal: User goal prompt string.
            conversation_id: Optional conversation ID string.
            max_iterations: Maximum reasoning iterations.

        Returns:
            Result wrapping AgentResponse or ErrorInfo.
        """
        try:
            response = await self._agent.run(
                goal=goal,
                conversation_id=conversation_id,
                max_iterations=max_iterations,
            )
            return Ok(response)
        except Exception as exc:
            return Err(
                ErrorInfo(
                    message=f"Agent execution failed: {exc}",
                    error_code="AGENT_EXECUTION_ERROR",
                )
            )
