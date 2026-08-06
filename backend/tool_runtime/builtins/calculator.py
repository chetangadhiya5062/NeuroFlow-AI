"""Calculator built-in tool using AST arithmetic evaluation."""

import ast
import operator
from typing import Any, ClassVar

from backend.tool_runtime.metadata import ToolMetadata, ToolParameter
from backend.tool_runtime.tool import ITool, ToolResult


class CalculatorTool(ITool):
    """Built-in tool safely evaluating arithmetic mathematical expressions."""

    OPERATORS: ClassVar[dict[type, Any]] = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    @property
    def metadata(self) -> ToolMetadata:
        """Return Calculator tool metadata."""
        return ToolMetadata(
            name="calculator",
            description="Evaluates mathematical arithmetic expressions safely.",
            parameters=[
                ToolParameter(
                    name="expression",
                    type="str",
                    description="Arithmetic mathematical expression string.",
                    required=True,
                )
            ],
        )

    def _eval_node(self, node: ast.AST) -> float | int:
        """Recursively evaluate AST math node safely."""
        if isinstance(node, ast.Expression):
            return self._eval_node(node.body)
        if isinstance(node, ast.Constant) and isinstance(
            node.value, (int, float)
        ):
            return node.value
        if isinstance(node, ast.BinOp):
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            bin_op_cls = type(node.op)
            if bin_op_cls in self.OPERATORS:
                res = self.OPERATORS[bin_op_cls](left, right)
                return float(res) if isinstance(res, float) else int(res)
            raise ValueError(
                f"Unsupported binary operator '{bin_op_cls.__name__}'"
            )
        if isinstance(node, ast.UnaryOp):
            operand = self._eval_node(node.operand)
            un_op_cls = type(node.op)
            if un_op_cls in self.OPERATORS:
                res = self.OPERATORS[un_op_cls](operand)
                return float(res) if isinstance(res, float) else int(res)
            raise ValueError(
                f"Unsupported unary operator '{un_op_cls.__name__}'"
            )
        raise ValueError(f"Unsupported AST node type '{type(node).__name__}'")

    async def execute(self, **kwargs: Any) -> ToolResult:
        """Execute calculator expression evaluation.

        Args:
            expression: Arithmetic expression string.

        Returns:
            ToolResult containing numeric calculation result.
        """
        expression = kwargs.get("expression")
        if not expression or not str(expression).strip():
            return ToolResult(
                success=False,
                result=None,
                error="Parameter 'expression' is required.",
            )

        # Normalize multiplication/division Unicode symbols
        expr_str = (
            str(expression)
            .replace("×", "*")  # noqa: RUF001
            .replace("x", "*")
            .replace("÷", "/")
            .replace(",", "")
            .strip()
        )

        try:
            parsed = ast.parse(expr_str, mode="eval")
            calc_val = self._eval_node(parsed)
            # Format integer if whole number
            is_int = isinstance(calc_val, float) and calc_val.is_integer()
            final_val = int(calc_val) if is_int else calc_val
            return ToolResult(
                success=True,
                result=final_val,
                metadata={"expression": expr_str},
            )
        except Exception as exc:
            return ToolResult(
                success=False,
                result=None,
                error=f"Invalid arithmetic expression '{expression}': {exc}",
            )
