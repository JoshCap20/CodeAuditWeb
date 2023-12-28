import os
import tempfile
import subprocess
from typing import Callable

from memory_profiler import memory_usage

from models import CodeRequest, MemoryResults, AdvancedMemoryResults
from utils.logger import get_logger

logger = get_logger(__name__)


class MemoryAnalysis:
    """
    Class for analyzing memory usage in code execution.
    """

    @staticmethod
    def action(request: CodeRequest) -> MemoryResults:
        """
        Perform memory analysis on the given code request.

        Args:
            request (CodeRequest): The code request object.

        Returns:
            MemoryResults: The memory analysis results.
        """
        try:
            peak_memory_usage: float = MemoryAnalysis.test_memory_usage(request)
            return MemoryResults.from_mebibyte(peak_memory_usage)
        except Exception as e:
            logger.error(f"[MemoryAnalysis] Error occurred during execution: {e}")
            raise

    @staticmethod
    def advanced_action(request: CodeRequest) -> AdvancedMemoryResults:
        """
        Perform advanced memory analysis on the given code request.

        Args:
            request (CodeRequest): The code request object.

        Returns:
            AdvancedMemoryResults: The advanced memory analysis results.
        """
        # Detailed memory usage and profiling
        detailed_usage: str = MemoryAnalysis.line_by_line_memory_usage(request)
        peak_memory_usage: float = MemoryAnalysis.test_memory_usage(request)

        return AdvancedMemoryResults(
            detailed_usage=detailed_usage,
            peak_memory_usage=MemoryResults.from_mebibyte(peak_memory_usage),
        )

    @staticmethod
    def test_memory_usage(request: CodeRequest) -> float:
        """
        Test the memory usage of the code execution. Runs the code multiple times as specified in the CodeRequest.iterations and returns the peak memory usage.

        Args:
            request (CodeRequest): The code request object.

        Returns:
            float: The peak memory usage in megabytes.
        """
        filepath = request.get_code_file()
        return max(
            MemoryAnalysis.__single_memory_usage(filepath)
            for _ in range(request.iterations)
        )

    @staticmethod
    def __single_memory_usage(filepath: str) -> float:
        """
        Calculate the maximum memory usage of a subprocess running a given script.

        Args:
            filepath (str): The path to the script file.

        Returns:
            float: The maximum memory usage in bytes.
        """

        def run_script():
            # Run the script in a separate process
            with subprocess.Popen(
                ["python", filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE
            ) as proc:
                try:
                    proc.communicate(timeout=30)  # Adjust timeout as needed
                except subprocess.TimeoutExpired:
                    logger.error(f"Timeout expired while executing {filepath}")
                    proc.kill()
                    proc.communicate()

        # Measure the memory usage of the subprocess
        mem_usage = memory_usage(run_script)  # type: ignore
        return max(mem_usage)

    # TODO: Fix
    @staticmethod
    def line_by_line_memory_usage(request: CodeRequest) -> str:
        """
        Calculate the line-by-line memory usage of the code execution.

        Args:
            request (CodeRequest): The code request object.

        Returns:
            str: The line-by-line memory usage profile.
        """
        with tempfile.NamedTemporaryFile(
            suffix=".py", mode="w", delete=False
        ) as temp_file:
            temp_file.write("from memory_profiler import profile\n\n@profile\n")
            temp_file.write(f"def wrapped_function():\n")

            temp_file.write(
                "\n".join("    " + line for line in request.code.splitlines())
            )
            temp_file_path = temp_file.name

        try:
            profile_output = subprocess.check_output(
                ["python", "-m", "memory_profiler", temp_file_path],
                stderr=subprocess.STDOUT,
                text=True,
            )
        except subprocess.CalledProcessError as e:
            logger.error(
                f"(line_by_line_memory_usage) Error in memory_profiler: {e.output}"
            )
            raise
        finally:
            os.remove(temp_file_path)

        return profile_output
