import os
import tempfile
import cProfile
import subprocess

from models import CodeRequest, FileLink


class DotGraphGenerator:
    @staticmethod
    def action(request: CodeRequest) -> FileLink:
        return FileLink.from_path(DotGraphGenerator.generate_dot_graph(request))

    @staticmethod
    def generate_dot_graph(request: CodeRequest) -> str:
        profiler = cProfile.Profile(subcalls=True, builtins=True)
        profiler.enable()
        exec(request.code)
        profiler.disable()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".prof") as temp_profile:
            profiler.dump_stats(temp_profile.name)

            # Set up the output file for the dot graph
            SAVE_FILE = "./static/dotgraph.png"

            # Set up the pipeline: gprof2dot | dot
            with open(SAVE_FILE, "wb") as output_file:
                gprof2dot_process = subprocess.Popen(
                    ["gprof2dot.py", "-f", "pstats", temp_profile.name],
                    stdout=subprocess.PIPE
                )
                subprocess.run(
                    ["dot", "-Tpng", "-o", output_file.name],
                    stdin=gprof2dot_process.stdout,
                    stdout=output_file
                )
                if gprof2dot_process.stdout:
                    gprof2dot_process.stdout.close()

        os.remove(temp_profile.name)  # Clean up the temporary profile file

        return SAVE_FILE
