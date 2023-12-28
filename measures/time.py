import time

from utils.logger import get_logger
from models import CodeRequest, TimeResults

logger = get_logger(__name__)


class TimeAnalysis:
    @staticmethod
    def action(request: CodeRequest) -> TimeResults:
        try:
            execution_time: float = TimeAnalysis.test_execution_time(request)
            return TimeResults.from_nano_seconds(execution_time)
        except Exception as e:
            logger.error(f"[TimeAnalysis] Error occurred during execution: {e}")
            raise

    @staticmethod
    def test_execution_time(request: CodeRequest) -> float:
        iterations: list[float] = []
        for _ in range(request.iterations):
            iterations.append(TimeAnalysis.__single_execution_time(request.code))
        return sum(iterations) / len(iterations)

    @staticmethod
    def __single_execution_time(code: str) -> float:
        start_time: float = time.perf_counter_ns()
        exec(code)
        end_time: float = time.perf_counter_ns()
        return end_time - start_time
