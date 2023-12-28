import subprocess
import cProfile
import os

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

        # Temp save the profile to a file
        profile_file: str = "./static/temp_profile.prof"
        with open(profile_file, "w") as f:
            profiler.dump_stats(profile_file)

        # Generate the dot file using gprof2dot
        SAVE_FILE: str = "./static/dotgraph.svg"
        
        with open(SAVE_FILE, "w") as f:
            subprocess.run(["gprof2dot", "-f", "pstats", profile_file], stdout=f)

        # Remove the temp profile file
        os.remove(profile_file)

        return SAVE_FILE
