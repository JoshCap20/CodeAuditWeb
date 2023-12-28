import subprocess

from models import FileLink, CodeRequest


class FlameGraphGenerator:
    snakeviz_process = None

    @staticmethod
    def action(request: CodeRequest) -> FileLink:
        input_file: str = request.get_code_file()
        output_file: str = "static/test.profile"
        FlameGraphGenerator.generate_flamegraph(input_file, output_file)
        return FileLink.from_path(output_file)

    @staticmethod
    def generate_flamegraph(input_file: str, output_file: str) -> None:
        subprocess.run(
            ["python", "-m", "cProfile", "-o", output_file, input_file], check=True
        )

        if FlameGraphGenerator.snakeviz_process:
            FlameGraphGenerator.snakeviz_process.terminate()

        FlameGraphGenerator.snakeviz_process = subprocess.Popen(
            ["snakeviz", output_file]
        )
