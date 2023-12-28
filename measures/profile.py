import io
import pstats
import cProfile
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
        temp_code_file: str = request.get_code_file()

        # Load the code from the file
        namespace = {}
        with open(temp_code_file) as f:
            code = compile(f.read(), temp_code_file, "exec")
            exec(code, namespace)

        lp = LineProfiler()

        # Add all functions in the namespace to the profiler
        for name, obj in namespace.items():
            if isinstance(obj, FunctionType):
                lp.add_function(obj)

        # Run each function under the profiler
        for name, func in namespace.items():
            if isinstance(func, FunctionType):
                lp.runctx(f"{name}()", globals(), namespace)

        output = io.StringIO()
        lp.print_stats(output)
        return output.getvalue()
