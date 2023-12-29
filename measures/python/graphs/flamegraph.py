import subprocess

import config
from models import FileLink, CodeRequest


class FlameGraphGenerator:
    snakeviz_process = None

    @staticmethod
    def action(request: CodeRequest) -> FileLink:
        input_file: str = request.get_code_file()
        FlameGraphGenerator.generate_flamegraph(input_file, config.FLAMEGRAPH_PROFILE)
        return FileLink.from_path(config.FLAMEGRAPH_PROFILE)

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
