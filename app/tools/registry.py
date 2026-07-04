"""Registry for tools.

New tools register themselves here (by name) and can then be looked up
or listed anywhere in the app, without any other code needing to know
about the specific tool classes.
"""

from app.core.exceptions import NotFoundError
from app.core.logging_config import get_logger
from app.tools.base import Tool

logger = get_logger(__name__)

_tools: dict[str, Tool] = {}


def register_tool(tool: Tool) -> None:
    """Register a tool instance so it can be looked up by name."""
    _tools[tool.name] = tool
    logger.info("Registered tool: '%s'", tool.name)


def get_tool(name: str) -> Tool:
    """Look up a registered tool by name. Raises NotFoundError if not found."""
    if name not in _tools:
        raise NotFoundError(f"Tool '{name}' is not registered.")
    return _tools[name]


def list_tools() -> list[Tool]:
    """Return all currently registered tools."""
    return list(_tools.values())