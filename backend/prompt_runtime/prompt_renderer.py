"""Prompt renderer transforming compiled templates into ChatMessage payloads."""

from backend.llm_gateway.models import ChatMessage
from backend.prompt_runtime.prompt_compiler import CompiledPrompt


class PromptRenderer:
    """Renderer converting compiled prompts and contexts into ChatMessage sequences."""

    def render(self, compiled_prompt: CompiledPrompt) -> list[ChatMessage]:
        """Render compiled prompt into list of ChatMessages.

        Args:
            compiled_prompt: CompiledPrompt object.

        Returns:
            List of ChatMessage objects (System, Conversation History, User, Assistant).
        """
        messages: list[ChatMessage] = []
        tmpl = compiled_prompt.template
        ctx = compiled_prompt.context
        vars_container = ctx.variables

        # 1. System Prompt Rendering (System override takes precedence)
        system_text = ctx.system_override or tmpl.system_template
        if system_text:
            rendered_system = vars_container.substitute_in_text(system_text)
            messages.append(ChatMessage(role="system", content=rendered_system))

        # 2. Append Conversation History if present
        if ctx.conversation_history:
            messages.extend(ctx.conversation_history)

        # 3. User Prompt Rendering
        if tmpl.user_template:
            rendered_user = vars_container.substitute_in_text(tmpl.user_template)
            messages.append(ChatMessage(role="user", content=rendered_user))

        # 4. Assistant Pre-fill Prompt Rendering if specified
        if tmpl.assistant_template:
            rendered_assistant = vars_container.substitute_in_text(
                tmpl.assistant_template
            )
            messages.append(
                ChatMessage(role="assistant", content=rendered_assistant)
            )

        return messages
