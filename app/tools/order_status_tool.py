"""Tool that looks up an order's status and estimated delivery date."""

import json
from pathlib import Path

from app.core.config import get_settings
from app.core.logging_config import get_logger
from app.tools.base import Tool

logger = get_logger(__name__)


class OrderStatusTool(Tool):
    """Looks up an order's status and estimated delivery date by order ID."""

    name = "order_status"
    description = "Look up an order's status and estimated delivery date using its order ID."

    def __init__(self) -> None:
        settings = get_settings()
        self._orders_path = Path(settings.orders_data_path)
        self._orders = self._load_orders()

    def _load_orders(self) -> dict[str, dict]:
        """Load orders.json into a dict keyed by order_id."""
        if not self._orders_path.exists():
            logger.warning("Orders data file not found at '%s'", self._orders_path)
            return {}

        with open(self._orders_path, encoding="utf-8") as f:
            orders_list = json.load(f)

        logger.info("Loaded %d orders from '%s'", len(orders_list), self._orders_path)
        return {order["order_id"]: order for order in orders_list}

    def run(self, **kwargs) -> str:
        """Look up an order by order_id and return its status and delivery date."""
        order_id = str(kwargs.get("order_id", "")).strip()

        if not order_id:
            return "Please provide an order ID."

        order = self._orders.get(order_id)

        if order is None:
            logger.info("Order ID '%s' not found", order_id)
            return f"No order found with ID '{order_id}'. Please check the order ID and try again."

        return (
            f"Order {order_id} status: {order['status']}. "
            f"Estimated delivery: {order['estimated_delivery']}."
        )