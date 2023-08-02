from abc import ABC, abstractmethod


class MediaProcessor(ABC):
    """Abstract base class for media processors."""

    @abstractmethod
    def process(self) -> dict:
        pass
