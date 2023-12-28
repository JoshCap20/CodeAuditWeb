import os
import tempfile
import subprocess

from memory_profiler import memory_usage

from models import Code, MemoryResults, AdvancedMemoryResults, FileLink


class MemoryAnalysis:
    @staticmethod
    def action(code: Code) -> MemoryResults:
        peak_memory_usage: float = MemoryAnalysis.test_memory_usage(code)
        return MemoryResults.from_mebibyte(peak_memory_usage)

    @staticmethod
    def advanced_action(code: Code) -> AdvancedMemoryResults:
        # Detailed memory usage and profiling
        detailed_usage: str = MemoryAnalysis.line_by_line_memory_usage(code)
        peak_memory_usage: float = MemoryAnalysis.test_memory_usage(code)

        # Generate memory usage charts
        chart_file: FileLink = FileLink.from_path(
            file_path=MemoryAnalysis.generate_memory_chart(code)
        )

        return AdvancedMemoryResults(
            detailed_usage=detailed_usage,
            peak_memory_usage=MemoryResults.from_mebibyte(peak_memory_usage),
            memory_chart=chart_file,
        )

    @staticmethod
    def test_memory_usage(code: Code) -> float:
        def wrapper():
            exec(code.code_str)

        mem_usage = memory_usage(wrapper)  # type: ignore
        peak_memory_usage = max(mem_usage)
        return peak_memory_usage

    @staticmethod
    def line_by_line_memory_usage(code: Code) -> str:
        temp_file = "./static/temp_code.py"

        with tempfile.NamedTemporaryFile(
            suffix=".py", mode="w", delete=False
        ) as temp_file:
            temp_file.write(f"@profile\n{code.code_str}")
            temp_file_path = temp_file.name

        try:
            profile_output = subprocess.check_output(
                ["python", "-m", "memory_profiler", temp_file_path], text=True
            )
        finally:
            os.remove(temp_file_path)

        return profile_output

    @staticmethod
    def generate_memory_chart(code: Code) -> str:
        chart_file = "./static/memory_chart.png"

        with tempfile.NamedTemporaryFile(
            suffix=".py", mode="w", delete=False
        ) as temp_file:
            temp_file.write(code.code_str)
            temp_file_path = temp_file.name

        try:
            subprocess.run(["mprof", "run", "--python", temp_file_path], check=False)
            subprocess.run(["mprof", "plot", "--output", chart_file], check=False)
        finally:
            os.remove(temp_file_path)

        return chart_file
