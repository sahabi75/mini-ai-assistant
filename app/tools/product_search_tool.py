

import json
from pathlib import Path

from app.core.config import get_settings
from app.core.logging_config import get_logger
from app.tools.base import Tool

logger = get_logger(__name__)


class ProductSearchTool(Tool):
    """Searches products by name and returns price and stock for matches."""

    name = "product_search"
    description = "Search for a product by name (partial match supported) and get its price and stock."

    def __init__(self) -> None:
        settings = get_settings()
        self._products_path = Path(settings.products_data_path)
        self._products = self._load_products()

    def _load_products(self) -> list[dict]:
        """Load products.json into a list of product dicts."""
        if not self._products_path.exists():
            logger.warning("Products data file not found at '%s'", self._products_path)
            return []

        with open(self._products_path, encoding="utf-8") as f:
            products = json.load(f)

        logger.info("Loaded %d products from '%s'", len(products), self._products_path)
        return products

    def run(self, **kwargs) -> str:
        """Search products by name (case-insensitive, partial match)."""
        query = str(kwargs.get("product_name", "")).strip().lower()

        if not query:
            return "Please provide a product name to search for."

        matches = [p for p in self._products if query in p["name"].lower()]

        if not matches:
            logger.info("No products matched query '%s'", query)
            return f"No products found matching '{query}'."

        lines = [
            f"{p['name']}: price ${p['price']}, stock {p['stock']}"
            for p in matches
        ]
        return "\n".join(lines)