import cProfile
import pstats
import flameprof

from models import FileLink, CodeRequest


class FlameGraphGenerator:
    @staticmethod
    def action(request: CodeRequest) -> FileLink:
        return FileLink.from_path(FlameGraphGenerator.generate_flamegraph(request))

    @staticmethod
    def generate_flamegraph(request: CodeRequest) -> str:
        profiler = cProfile.Profile(subcalls=True, builtins=True)
        profiler.enable()
        exec(request.code)
        profiler.disable()
        stats: pstats.Stats = pstats.Stats(profiler)

        SAVE_FILE: str = "./static/flamegraph.svg"

        with open(SAVE_FILE, "w") as f:
            flameprof.render(stats.stats, f)  # type: ignore

        return SAVE_FILE
