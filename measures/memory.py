import os
import tempfile
import subprocess
from typing import Callable

from memory_profiler import memory_usage

from models import CodeRequest, MemoryResults, AdvancedMemoryResults
from utils.logger import get_logger

logger = get_logger(__name__)


class MemoryAnalysis:
    @staticmethod
    def action(request: CodeRequest) -> MemoryResults:
        try:
            peak_memory_usage: float = MemoryAnalysis.test_memory_usage(request)
            return MemoryResults.from_mebibyte(peak_memory_usage)
        except Exception as e:
            logger.error(f"[MemoryAnalysis] Error occurred during execution: {e}")
            raise

    @staticmethod
    def advanced_action(request: CodeRequest) -> AdvancedMemoryResults:
        # Detailed memory usage and profiling
        detailed_usage: str = MemoryAnalysis.line_by_line_memory_usage(request)
        peak_memory_usage: float = MemoryAnalysis.test_memory_usage(request)

        return AdvancedMemoryResults(
            detailed_usage=detailed_usage,
            peak_memory_usage=MemoryResults.from_mebibyte(peak_memory_usage),
        )

    @staticmethod
    def test_memory_usage(request: CodeRequest) -> float:
        iterations: list[float] = []

        def wrapper():
            exec(request.code)

        for _ in range(request.iterations):
            iterations.append(MemoryAnalysis.__single_memory_usage(wrapper))

        return max(iterations)

    @staticmethod
    def __single_memory_usage(func: Callable) -> float:
        mem_usage = memory_usage(func)  # type: ignore
        peak_memory_usage = max(mem_usage)
        return peak_memory_usage

    @staticmethod
    def line_by_line_memory_usage(request: CodeRequest) -> str:
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
