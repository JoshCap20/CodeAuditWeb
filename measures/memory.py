import os
import tempfile
import subprocess

from memory_profiler import memory_usage

from models import CodeRequest, MemoryResults, AdvancedMemoryResults, FileLink


class MemoryAnalysis:
    @staticmethod
    def action(request: CodeRequest) -> MemoryResults:
        peak_memory_usage: float = MemoryAnalysis.test_memory_usage(request)
        return MemoryResults.from_mebibyte(peak_memory_usage)

    @staticmethod
    def advanced_action(request: CodeRequest) -> AdvancedMemoryResults:
        # Detailed memory usage and profiling
        detailed_usage: str = MemoryAnalysis.line_by_line_memory_usage(request)
        peak_memory_usage: float = MemoryAnalysis.test_memory_usage(request)

        # Generate memory usage charts
        chart_file: FileLink = FileLink.from_path(
            file_path=MemoryAnalysis.generate_memory_chart(request)
        )

        return AdvancedMemoryResults(
            detailed_usage=detailed_usage,
            peak_memory_usage=MemoryResults.from_mebibyte(peak_memory_usage),
            memory_chart=chart_file,
        )

    @staticmethod
    def test_memory_usage(request: CodeRequest) -> float:
        def wrapper():
            exec(request.code)

        mem_usage = memory_usage(wrapper)  # type: ignore
        peak_memory_usage = max(mem_usage)
        return peak_memory_usage

    @staticmethod
    def line_by_line_memory_usage(request: CodeRequest) -> str:
        with tempfile.NamedTemporaryFile(
            suffix=".py", mode="w", delete=False
        ) as temp_file:
            temp_file.write(f"@profile\n{request.code}")
            temp_file_path = temp_file.name

        try:
            profile_output = subprocess.check_output(
                ["python", "-m", "memory_profiler", temp_file_path], text=True
            )
        finally:
            os.remove(temp_file_path)

        return profile_output

    @staticmethod
    def generate_memory_chart(request: CodeRequest) -> str:
        chart_file = "./static/memory_chart.png"

        temp_file = request.get_code_file()

        subprocess.run(["mprof", "run", "--python", temp_file], check=False)
        subprocess.run(["mprof", "plot", "--output", chart_file], check=False)

        return chart_file
