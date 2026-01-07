from abc import ABC, abstractmethod

class Notifier(ABC):
    @abstractmethod
    def send(self, title: str, summary: str, link: str):
        """Send a notification to a specific platform."""
        pass