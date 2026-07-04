

import re

from app.core.logging_config import get_logger
from app.tools.registry import get_tool

logger = get_logger(__name__)

ORDER_ID_PATTERN = re.compile(r"\bORD\d+\b", re.IGNORECASE)
PRODUCT_KEYWORDS = [
    "price of", "stock of", "how much is", "how much does",
    "looking for", "show me", "search for", "do you have", "product",
]


def _try_order_query(message: str) -> str | None:
    """Route to the order_status tool if the message contains an order ID."""
    match = ORDER_ID_PATTERN.search(message)
    if not match:
        return None

    order_id = match.group().upper()
    tool = get_tool("order_status")
    return tool.run(order_id=order_id)


def _extract_product_name(message: str, phrase: str) -> str:
    """Return the text after a matched keyword phrase, cleaned up."""
    lowered = message.lower()
    idx = lowered.index(phrase) + len(phrase)
    extracted = message[idx:].strip(" ?.!")

    for article in ("the ", "a ", "an "):
        if extracted.lower().startswith(article):
            extracted = extracted[len(article):]

    return extracted.strip()


def _try_product_query(message: str) -> str | None:
    """Route to the product_search tool if the message asks about a product."""
    lowered = message.lower()

    for phrase in PRODUCT_KEYWORDS:
        if phrase in lowered:
            product_name = _extract_product_name(message, phrase)
            if not product_name:
                continue
            tool = get_tool("product_search")
            return tool.run(product_name=product_name)

    return None


# Ordered list of route handlers. First one that returns a non-None result wins.
_ROUTE_HANDLERS = [_try_order_query, _try_product_query]


def route(message: str) -> str | None:
    """Try to answer a message using a tool.

    Returns the tool's result string if a route matched, or None if no
    tool matched -- meaning the caller should fall through to retrieval.
    """
    for handler in _ROUTE_HANDLERS:
        result = handler(message)
        if result is not None:
            logger.info("Routed message to tool via '%s'", handler.__name__)
            return result

    logger.info("No tool route matched; falling through to retrieval.")
    return None