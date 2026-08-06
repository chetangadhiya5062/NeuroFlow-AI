"""Master prompt service managing compilation, rendering, and template lookup."""

from typing import Any

from backend.llm_gateway.models import ChatMessage
from backend.prompt_runtime.prompt_compiler import PromptCompiler
from backend.prompt_runtime.prompt_context import PromptContext
from backend.prompt_runtime.prompt_registry import PromptRegistry
from backend.prompt_runtime.prompt_renderer import PromptRenderer
from backend.prompt_runtime.prompt_template import PromptTemplate
from backend.prompt_runtime.prompt_variables import PromptVariables


class PromptService:
    """Service providing high-level interface for prompt rendering and registration."""

    def __init__(
        self,
        registry: PromptRegistry | None = None,
        compiler: PromptCompiler | None = None,
        renderer: PromptRenderer | None = None,
    ) -> None:
        """Initialize PromptService with registry, compiler, and renderer."""
        self.registry = registry or PromptRegistry()
        self.compiler = compiler or PromptCompiler()
        self.renderer = renderer or PromptRenderer()

    async def render_prompt(
        self,
        template_name: str,
        context: PromptContext | None = None,
        version: str | None = None,
    ) -> list[ChatMessage]:
        """Render a registered prompt template into ChatMessage payloads.

        Args:
            template_name: Name of registered prompt template.
            context: Optional PromptContext object.
            version: Optional template version string.

        Returns:
            List of ChatMessage objects.
        """
        active_context = context or PromptContext()
        template = self.registry.get_template(template_name, version=version)
        compiled = self.compiler.compile(template, active_context)
        return self.renderer.render(compiled)

    async def format_user_prompt(
        self,
        prompt_text: str,
        variables: dict[str, Any] | None = None,
    ) -> str:
        """Substitute variables into a standalone prompt string.

        Args:
            prompt_text: Text template containing variable placeholders.
            variables: Optional key-value variables dictionary.

        Returns:
            Rendered prompt string value.
        """
        vars_container = PromptVariables(variables=variables or {})
        return vars_container.substitute_in_text(prompt_text)

    def register_template(self, template: PromptTemplate) -> None:
        """Register a prompt template in the registry."""
        self.registry.register_template(template)
