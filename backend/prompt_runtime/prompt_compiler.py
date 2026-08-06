"""Prompt compiler validating required variables and template integrity."""

from dataclasses import dataclass

from backend.prompt_runtime.exceptions import PromptValidationError
from backend.prompt_runtime.prompt_context import PromptContext
from backend.prompt_runtime.prompt_template import PromptTemplate


@dataclass(frozen=True)
class CompiledPrompt:
    """Compiled prompt structure ready for rendering.

    Attributes:
        template: Original PromptTemplate instance.
        context: Active PromptContext container.
    """

    template: PromptTemplate
    context: PromptContext


class PromptCompiler:
    """Compiler validating prompt templates against execution contexts."""

    def compile(
        self, template: PromptTemplate, context: PromptContext
    ) -> CompiledPrompt:
        """Validate template requirements against context variables.

        Args:
            template: Target PromptTemplate.
            context: Active PromptContext.

        Returns:
            CompiledPrompt instance.

        Raises:
            PromptValidationError: If required variables are missing.
        """
        missing_vars = [
            var
            for var in template.required_variables
            if not context.variables.contains(var)
        ]

        if missing_vars:
            raise PromptValidationError(
                f"Missing required variables for template '{template.name}': "
                f"{', '.join(missing_vars)}"
            )

        return CompiledPrompt(template=template, context=context)
