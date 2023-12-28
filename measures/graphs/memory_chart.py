import subprocess

from models import CodeRequest, FileLink


class MemoryChartGenerator:
    @staticmethod
    def action(request: CodeRequest) -> FileLink:
        output_file: str = "static/memory_chart.png"
        input_file: str = request.get_code_file()
        MemoryChartGenerator.generate_memory_chart(input_file, output_file)
        return FileLink.from_path(output_file)
    
    @staticmethod
    def generate_memory_chart(input_file: str, output_file: str) -> None:
        subprocess.run(["mprof", "run", "--python", input_file], check=True)
        subprocess.run(["mprof", "plot", "--output", output_file], check=True)
