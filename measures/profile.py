import cProfile
import io
import pstats
from types import FunctionType
from line_profiler import LineProfiler

from models import CodeRequest, ProfileResults, AdvancedProfileResults


class ProfileAnalysis:
    @staticmethod
    def action(request: CodeRequest) -> ProfileResults:
        profile = ProfileAnalysis.profile_code(request)
        return ProfileResults(profile=profile)

    @staticmethod
    def advanced_action(request: CodeRequest) -> AdvancedProfileResults:
        profile = ProfileAnalysis.profile_code(request)
        line_profile = ProfileAnalysis.line_profiler(request)
        return AdvancedProfileResults(profile=profile, line_profile=line_profile)

    @staticmethod
    def profile_code(request: CodeRequest) -> str:
        profiler = cProfile.Profile()
        profiler.enable()
        exec(request.code)
        profiler.disable()

        s = io.StringIO()
        stats = pstats.Stats(profiler, stream=s).sort_stats("cumulative")
        stats.print_stats()
        return s.getvalue()

    @staticmethod
    def line_profiler(request: CodeRequest) -> str:
        # Compile the code string into a function
        compiled_code = compile(request.code, "<string>", "exec")
        namespace = {}
        exec(compiled_code, namespace)

        # Find the first function in the namespace
        func_to_profile = None
        for name, obj in namespace.items():
            if isinstance(obj, FunctionType):
                func_to_profile = obj
                break

        if not func_to_profile:
            return "No function found in provided code to profile."

        # Initialize LineProfiler with the found function
        lp = LineProfiler()
        lp.add_function(func_to_profile)

        # Execute the function under the profiler
        lp.runctx("func_to_profile()", globals(), locals())

        # Capture the profiling result as a string
        output = io.StringIO()
        lp.print_stats(output)
        return output.getvalue()
