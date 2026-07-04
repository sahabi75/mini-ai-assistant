from abc import ABC, abstractmethod


class Tool(ABC):
    """Interface for a callable tool the assistant can use."""

    name: str
    description: str

    @abstractmethod
    def run(self, **kwargs) -> str:
        """Execute the tool and return its result as a string."""
        raise NotImplementedError