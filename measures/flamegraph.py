import cProfile
import pstats
import flameprof

from models import FileLink, Code


class FlameGraphGenerator:
    @staticmethod
    def action(code: Code) -> FileLink:
        return FileLink.from_path(FlameGraphGenerator.generate_flamegraph(code))

    @staticmethod
    def generate_flamegraph(code: Code) -> str:
        profiler = cProfile.Profile(subcalls=True, builtins=True)
        profiler.enable()
        exec(code.code_str)
        profiler.disable()
        stats: pstats.Stats = pstats.Stats(profiler)

        SAVE_FILE: str = "./static/flamegraph.svg"

        with open(SAVE_FILE, "w") as f:
            flameprof.render(stats.stats, f)  # type: ignore

        return SAVE_FILE
