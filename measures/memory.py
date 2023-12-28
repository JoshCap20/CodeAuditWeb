import os
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
        chart_file: FileLink = FileLink.from_path(file=MemoryAnalysis.generate_memory_chart(code))

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
        # Save the code to a temporary file for profiling
        temp_file = "temp_code.py"
        with open(temp_file, "w") as f:
            f.write(f"@profile\n{code.code_str}")

        # Run memory_profiler on the temporary file
        profile_output = subprocess.check_output(
            ["python", "-m", "memory_profiler", temp_file], text=True
        )

        os.remove(temp_file)  # Clean up temporary file
        return profile_output

    @staticmethod
    def generate_memory_chart(code: Code) -> str:
        # Save the code to a temporary file for chart generation
        temp_file = "temp_code.py"
        with open(temp_file, "w") as f:
            f.write(code.code_str)

        chart_file = "memory_chart.png"
        subprocess.run(["mprof", "run", "--python", temp_file], check=False)
        subprocess.run(["mprof", "plot", "--output", chart_file], check=False)

        os.remove(temp_file)  # Clean up temporary file
        return chart_file
