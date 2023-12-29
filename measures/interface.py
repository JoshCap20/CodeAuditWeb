from abc import ABC, abstractmethod
from models import CodeRequest, Results


class AbstractPerformanceAnalyzer(ABC):
    """
    Abstract base class for performance analysis of code in different languages.
    """

    strategies = {}  # Used to populate frontend options and map to strategy functions

    @classmethod
    @abstractmethod
    def measure(cls, request: CodeRequest) -> Results:
        """
        Passes a code request to the correct strategy and populates the results.

        Args:
            request (CodeRequest): The code request to be analyzed.

        Returns:
            Results: The results of the performance analysis.
        """
        pass


class AbstractAnalysisStrategy(ABC):
    """
    Abstract base class for a performance analysis strategy.
    """

    @staticmethod
    @abstractmethod
    def action(request: CodeRequest):
        """
        Args:
            request (CodeRequest): The code request object.

        Returns:
            Any: The results of the analysis.
        """
        pass
