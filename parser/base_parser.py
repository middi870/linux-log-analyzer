from abc import ABC, abstractmethod
from typing import Optional

from analyzer.event import Event


class BaseParser(ABC):
    """
    Abstract parser interface.
    All log parsers must implement this.
    """

    @abstractmethod
    def parse(self, line: str) -> Optional[Event]:
        """
        Parse a log line into an Event object.
        Return None if line cannot be parsed.
        """
        pass
