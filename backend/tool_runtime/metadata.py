"""Tool metadata specifications."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ToolParameter:
    """Descriptor for a single tool argument parameter.

    Attributes:
        name: Parameter name key.
        type: Expected data type string (e.g. 'str', 'int', 'float').
        description: Human-readable parameter description.
        required: Whether parameter is mandatory.
    """

    name: str
    type: str
    description: str
    required: bool = True


@dataclass(frozen=True)
class ToolMetadata:
    """Metadata specification describing a tool interface.

    Attributes:
        name: Unique canonical tool name identifier.
        description: Functional description of tool capabilities.
        parameters: List of ToolParameter descriptors.
        version: Tool version string.
    """

    name: str
    description: str
    parameters: list[ToolParameter] = field(default_factory=list)
    version: str = "1.0.0"
