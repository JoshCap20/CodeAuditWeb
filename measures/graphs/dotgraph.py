import os
import tempfile
import cProfile
import subprocess

from models import CodeRequest, FileLink


class DotGraphGenerator:
    @staticmethod
    def action(request: CodeRequest) -> FileLink:
        return FileLink.from_path(DotGraphGenerator.generate_graph(request))

    @staticmethod
    def generate_graph(request: CodeRequest) -> str:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".prof") as temp_profile:
            temp_code_file: str = request.get_code_file()
            DotGraphGenerator._profile_code(temp_code_file, temp_profile.name)
            graph_file = "static/dotgraph.png"
            DotGraphGenerator._create_dot_graph(temp_profile.name, graph_file)
            return graph_file

    @staticmethod
    def _profile_code(code_file: str, output_file: str) -> None:
        profiler = cProfile.Profile()
        profiler.enable()
        with open(code_file, "r") as f:
            exec(f.read())
        profiler.disable()
        profiler.dump_stats(output_file)

    @staticmethod
    def _create_dot_graph(profile_file: str, output_file: str) -> None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".dot") as dot_temp_file:
            subprocess.run(
                ["gprof2dot", "-f", "pstats", profile_file, "-o", dot_temp_file.name],
                check=True,
            )
            subprocess.run(
                ["dot", "-Tpng", dot_temp_file.name, "-o", output_file], check=True
            )
            os.remove(dot_temp_file.name)
