"""Single-agent reasoning loop engine implementation."""

import re

from backend.agent_runtime.action import (
    ActionResult,
    AgentAction,
    AgentActionType,
)
from backend.agent_runtime.exceptions import AgentExecutionError
from backend.agent_runtime.reasoning import (
    AgentContext,
    AgentResponse,
    AgentStep,
)
from backend.conversation import ConversationService, MessageRole
from backend.core.ports import ILLMGateway
from backend.core.value_objects import EntityId, ModelIdentifier
from backend.prompt_runtime import PromptService
from backend.rag import RAGService
from backend.tool_runtime import ToolService


class SingleAgent:
    """Production single-agent executing an iterative reasoning loop."""

    def __init__(
        self,
        gateway: ILLMGateway,
        tool_service: ToolService | None = None,
        rag_service: RAGService | None = None,
        conversation_service: ConversationService | None = None,
        prompt_service: PromptService | None = None,
    ) -> None:
        """Initialize SingleAgent with platform runtime dependencies."""
        self._gateway = gateway
        self._tool_service = tool_service
        self._rag_service = rag_service
        self._conversation_service = conversation_service
        self._prompt_service = prompt_service

    async def _decide_next_action(self, context: AgentContext) -> AgentAction:
        """Decide next action based on context state and query intent."""
        goal = context.goal.strip()
        executed_action_types = {s.action.type for s in context.steps}

        # 1. Check for Calculator Tool Intent if not already executed
        if (
            self._tool_service is not None
            and AgentActionType.EXECUTE_TOOL not in executed_action_types
        ):
            # Look for math arithmetic expressions in prompt
            math_match = re.search(
                r"[\d\s\(\)\+\-\*\/\^\%x×÷,]+[\d\)]", goal  # noqa: RUF001
            )
            if math_match:
                candidate = math_match.group(0).strip()
                if any(
                    char in candidate for char in "+-*%/×÷x"  # noqa: RUF001
                ) and any(c.isdigit() for c in candidate):
                    return AgentAction(
                        type=AgentActionType.EXECUTE_TOOL,
                        name="calculator",
                        arguments={"expression": candidate},
                    )

        # 2. Check for Knowledge Base Retrieval Intent if not already executed
        if (
            self._rag_service is not None
            and AgentActionType.RETRIEVE_KNOWLEDGE not in executed_action_types
        ):
            keywords = [
                "telecom",
                "rrc",
                "document",
                "uploaded",
                "specification",
                "report",
                "according to",
                "knowledge",
            ]
            if any(kw in goal.lower() for kw in keywords):
                return AgentAction(
                    type=AgentActionType.RETRIEVE_KNOWLEDGE,
                    name="vector_retrieval",
                    arguments={"query": goal},
                )

        # 3. Default: Respond via LLM Generation
        return AgentAction(
            type=AgentActionType.RESPOND,
            name="generate_response",
            arguments={},
        )

    async def _execute_tool_action(
        self, action: AgentAction, context: AgentContext
    ) -> ActionResult:
        """Execute registered tool action."""
        if self._tool_service is None:
            return ActionResult(
                action=action,
                success=False,
                output=None,
                error="ToolService is not registered.",
            )
        tool_name = action.name or "calculator"
        tool_res = await self._tool_service.execute_tool_call(
            tool_name, action.arguments
        )
        if tool_res.success:
            context.tool_results.append(
                {
                    "tool": tool_name,
                    "arguments": action.arguments,
                    "result": tool_res.result,
                }
            )
            return ActionResult(
                action=action, success=True, output=tool_res.result
            )
        return ActionResult(
            action=action,
            success=False,
            output=None,
            error=tool_res.error,
        )

    async def _execute_retrieval_action(
        self, action: AgentAction, context: AgentContext
    ) -> ActionResult:
        """Execute RAG knowledge retrieval action."""
        if self._rag_service is None:
            return ActionResult(
                action=action,
                success=False,
                output=None,
                error="RAGService is not registered.",
            )
        query = action.arguments.get("query", context.goal)
        rag_res = await self._rag_service.retrieve_context(query, top_k=3)
        if rag_res.is_success:
            matches = rag_res.unwrap()
            sources = self._rag_service.format_sources(matches)
            context.sources.extend(sources)
            return ActionResult(action=action, success=True, output=sources)
        return ActionResult(
            action=action,
            success=False,
            output=None,
            error=rag_res.unwrap_err().message,
        )

    async def _execute_respond_action(
        self, action: AgentAction, context: AgentContext
    ) -> ActionResult:
        """Execute LLM response generation action."""
        prompt_parts = [f"User Goal: {context.goal}"]

        if context.tool_results:
            for tr in context.tool_results:
                prompt_parts.append(
                    f"Tool Execution Result ({tr['tool']}): {tr['result']}"
                )

        if context.sources:
            src_texts = [
                f"[Source: {s['filename']}]\n{s['text']}"
                for s in context.sources
            ]
            prompt_parts.append(
                "Retrieved Context:\n" + "\n---\n".join(src_texts)
            )

        full_prompt = "\n\n".join(prompt_parts)

        # Format prompt via PromptService if registered
        if self._prompt_service is not None:
            formatted_prompt = await self._prompt_service.format_user_prompt(
                full_prompt
            )
        else:
            formatted_prompt = full_prompt

        model_id = ModelIdentifier(name="mock-model", provider="mock")

        gen_res = await self._gateway.generate_text(
            prompt=formatted_prompt, model=model_id
        )
        if gen_res.is_success:
            answer_text = gen_res.unwrap()
            context.final_answer = answer_text
            context.completed = True
            return ActionResult(action=action, success=True, output=answer_text)
        return ActionResult(
            action=action,
            success=False,
            output=None,
            error=gen_res.unwrap_err().message,
        )

    async def _execute_action(
        self, action: AgentAction, context: AgentContext
    ) -> ActionResult:
        """Execute chosen action against registered platform service."""
        try:
            if action.type == AgentActionType.EXECUTE_TOOL:
                return await self._execute_tool_action(action, context)
            if action.type == AgentActionType.RETRIEVE_KNOWLEDGE:
                return await self._execute_retrieval_action(action, context)
            return await self._execute_respond_action(action, context)
        except Exception as exc:
            return ActionResult(
                action=action, success=False, output=None, error=str(exc)
            )

    async def run(
        self,
        goal: str,
        conversation_id: str | None = None,
        max_iterations: int = 5,
    ) -> AgentResponse:
        """Execute single-agent reasoning loop for a given goal.

        Args:
            goal: User goal or prompt string.
            conversation_id: Optional conversation ID string.
            max_iterations: Maximum loop iteration limit (default 5).

        Returns:
            AgentResponse payload containing final answer, trajectory, and sources.
        """
        if not goal or not goal.strip():
            raise AgentExecutionError("Agent goal prompt cannot be empty.")

        # 1. Load or create conversation aggregate using valid EntityId
        cid = conversation_id or EntityId().value
        if self._conversation_service is not None:
            conv_res = await self._conversation_service.get_conversation(cid)
            if conv_res.is_success:
                cid = conv_res.unwrap().id.value
            else:
                conv = await self._conversation_service.create_conversation(
                    title="Agent Session"
                )
                cid = conv.id.value
                await self._conversation_service.add_message(
                    conv.id, MessageRole.USER, goal
                )

        # 2. Build execution context
        context = AgentContext(goal=goal, conversation_id=cid)
        iteration = 1

        # 3. Iterative Reasoning Loop
        while not context.completed and iteration <= max_iterations:
            action = await self._decide_next_action(context)
            result = await self._execute_action(action, context)

            step = AgentStep(
                iteration=iteration, action=action, result=result
            )
            context.steps.append(step)

            if not result.success:
                context.completed = True
                context.final_answer = (
                    f"Agent execution encountered an error: {result.error}"
                )
                break

            iteration += 1

        if not context.final_answer:
            context.final_answer = "Agent completed execution."

        # Record assistant answer in conversation history
        if self._conversation_service is not None:
            await self._conversation_service.add_message(
                EntityId(cid), MessageRole.ASSISTANT, context.final_answer
            )

        trajectory = [
            {
                "iteration": s.iteration,
                "action": s.action.type.value,
                "name": s.action.name,
                "success": s.result.success if s.result else False,
            }
            for s in context.steps
        ]

        return AgentResponse(
            answer=context.final_answer,
            conversation_id=cid,
            iterations=len(context.steps),
            sources=context.sources,
            tool_results=context.tool_results,
            trajectory=trajectory,
        )
