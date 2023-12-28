from .time import TimeAnalysis
from .memory import MemoryAnalysis
from .profile import ProfileAnalysis
from .graphs import DotGraphGenerator, FlameGraphGenerator

from models import CodeRequest, Results

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
                    raise  # TODO: Remove in final version
        finally:
            request.delete_code_file()

        return results
