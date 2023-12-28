import subprocess
import cProfile

from models import Code, FileLink


class DotGraphGenerator:
    @staticmethod
    def action(code: Code) -> FileLink:
        return FileLink.from_path(DotGraphGenerator.generate_dot_graph(code))

    @staticmethod
    def generate_dot_graph(code: Code) -> str:
        profiler = cProfile.Profile(subcalls=True, builtins=True)
        profiler.enable()
        exec(code.code_str)
        profiler.disable()

        # Save the profile to a file
        profile_file = "temp_profile.prof"
        profiler.dump_stats(profile_file)

        SAVE_FILE: str = "./static/dotgraph.svg"

        # Generate the dot file using gprof2dot
        with open(SAVE_FILE, "w") as f:
            subprocess.run(["gprof2dot", "-f", "pstats", profile_file], stdout=f)

        # Optionally, remove the temporary profile file
        # os.remove(profile_file)

        return SAVE_FILE
