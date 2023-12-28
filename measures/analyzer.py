from models import CodeRequest, Results
from .time import TimeAnalysis
from .dotgraph import DotGraphGenerator
from .memory import MemoryAnalysis
from .flamegraph import FlameGraphGenerator
from .profile import ProfileAnalysis

from utils.logger import get_logger

logger = get_logger(__name__)


class PerformanceAnalyzer:
    strategies = {
        "time": TimeAnalysis.action,
        "memory": MemoryAnalysis.action,
        "advanced_memory": MemoryAnalysis.advanced_action,
        "profile": ProfileAnalysis.action,
        "advanced_profile": ProfileAnalysis.advanced_action,
        "dotgraph": DotGraphGenerator.action,
        "flamegraph": FlameGraphGenerator.action,
    }

    @classmethod
    def measure(cls, request: CodeRequest) -> Results:
        results = Results(request=request)

        try:
            request.generate_code_file()
            
            for option in request.options:
                strategy_fn = cls.strategies.get(option)
                if not strategy_fn:
                    logger.warning(f"Strategy for '{option}' not found.")
                    continue

                try:
                    if option == "time":
                        result = strategy_fn(request)
                    else:
                        result = strategy_fn(request)
                    results[option] = result
                except Exception as e:
                    logger.error(f"Error in '{option}' analysis: {e}")
                    results[option] = None
        finally:
            request.delete_code_file()

        return results
