from typing import Type

from models import CodeRequest, Results
from measures.interface import AbstractPerformanceAnalyzer
from measures.python import PerformanceAnalyzer as PythonPerformanceAnalyzer


class AnalysisHandler:
    languages: dict[str, Type[AbstractPerformanceAnalyzer]] = {
        "python": PythonPerformanceAnalyzer
    }

    @classmethod
    def measure(cls, request: CodeRequest) -> Results:
        """
        Measure the performance of the given code request using the specified language and strategies.

        Args:
            request (CodeRequest): The code request to be analyzed.

        Returns:
            Results: The results of the performance analysis.
        """
        analyzer: Type[AbstractPerformanceAnalyzer] | None = cls.languages.get(
            request.language
        )
        if analyzer is None:
            raise ValueError(f"Language '{request.language}' not supported.")

        return analyzer.measure(request)
