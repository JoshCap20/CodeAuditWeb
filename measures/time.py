import time
import subprocess

from utils.logger import get_logger
from models import CodeRequest, TimeResults

logger = get_logger(__name__)


class TimeAnalysis:
    """
    Class for analyzing the execution time of code snippets.
    """

    @staticmethod
    def action(request: CodeRequest) -> TimeResults:
        """
        Executes the code snippet and returns the execution time.

        Args:
            request (CodeRequest): The code request object containing the code snippet and iteration count.

        Returns:
            TimeResults: The execution time results.
        """
        try:
            execution_time: float = TimeAnalysis.test_execution_time(request)
            return TimeResults.from_nano_seconds(execution_time)
        except Exception as e:
            logger.error(f"[TimeAnalysis] Error occurred during execution: {e}")
            raise

    @staticmethod
    def test_execution_time(request: CodeRequest) -> float:
        """
        Tests the execution time of the code snippet. Runs the code multiple times as specified in the CodeRequest.iterations and returns the average execution time.

        Args:
            request (CodeRequest): The code request object containing the code snippet and iteration count.

        Returns:
            float: The average execution time in seconds.
        """
        code_file: str = request.get_code_file()
        return sum(TimeAnalysis.__single_execution_time(code_file) for _ in range(request.iterations)) / request.iterations

    @staticmethod
    def __single_execution_time(code_file: str) -> float:
        """
        Measures the execution time of a single code snippet.

        Args:
            code (str): The code snippet to execute.

        Returns:
            float: The execution time in seconds.
        """
        start_time: float = time.perf_counter_ns()
        subprocess.run(["python", code_file], check=True)
        end_time: float = time.perf_counter_ns()
        return end_time - start_time
