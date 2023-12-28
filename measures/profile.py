import cProfile
import io
import pstats
from line_profiler import LineProfiler

from models import Code, ProfileResults, AdvancedProfileResults


class ProfileAnalysis:
    @staticmethod
    def action(code: Code) -> ProfileResults:
        profile = ProfileAnalysis.profile_code(code)
        return ProfileResults(profile=profile)

    @staticmethod
    def advanced_action(code: Code) -> AdvancedProfileResults:
        profile = ProfileAnalysis.profile_code(code)
        line_profile = ProfileAnalysis.line_profiler(code)
        return AdvancedProfileResults(profile=profile, line_profile=line_profile)

    @staticmethod
    def profile_code(code: Code) -> str:
        profiler = cProfile.Profile()
        profiler.enable()
        exec(code.code_str)
        profiler.disable()

        s = io.StringIO()
        stats = pstats.Stats(profiler, stream=s).sort_stats("cumulative")
        stats.print_stats()
        return s.getvalue()

    @staticmethod
    def line_profiler(code: Code) -> str:
        # Define a wrapper function to execute the code
        def exec_wrapper():
            exec(code.code_str, globals(), locals())

        # Initialize LineProfiler with the wrapper function
        lp = LineProfiler()
        lp_wrapper = lp(exec_wrapper)

        # Execute the wrapper function under the profiler
        lp_wrapper()

        # Capture the profiling result as a string
        output = io.StringIO()
        lp.print_stats(output)
        return output.getvalue()