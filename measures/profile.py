import io
import os
import tempfile
import subprocess
from types import FunctionType
from line_profiler import LineProfiler

from utils.logger import get_logger
from models import CodeRequest, ProfileResults, AdvancedProfileResults

logger = get_logger(__name__)


class ProfileAnalysis:
    """
    Class for performing code profiling and analysis.
    """

    @staticmethod
    def action(request: CodeRequest) -> ProfileResults:
        """
        Perform code profiling and return the results.

        Args:
            request (CodeRequest): The code request object.

        Returns:
            ProfileResults: The profile results.
        """
        try:
            profile = ProfileAnalysis.profile_code(request)
            return ProfileResults(profile=profile)
        except Exception as e:
            logger.error(f"[ProfileAnalysis] Error occurred during execution: {e}")
            raise

    @staticmethod
    def advanced_action(request: CodeRequest) -> AdvancedProfileResults:
        """
        Perform advanced code profiling and return the results.

        Args:
            request (CodeRequest): The code request object.

        Returns:
            AdvancedProfileResults: The advanced profile results.
        """
        profile: str = ProfileAnalysis.profile_code(request)
        try:
            line_profile: str = ProfileAnalysis.line_profiler(request)
        except Exception as e:
            logger.error(f"[ProfileAnalysis] Error occurred during execution: {e}")
            line_profile = "Unable to generate line-by-line profile."
            
        return AdvancedProfileResults(profile=profile, line_profile=line_profile)

    @staticmethod
    def profile_code(request: CodeRequest) -> str:
        """
        Profile the code and return the profiling results.

        Note: The subprocess includes and returns its own profiling results to avoid interference with subprocess profiling.

        Args:
            request (CodeRequest): The code request object.

        Returns:
            str: The profiling results.
        """
        with tempfile.NamedTemporaryFile(
            suffix=".py", mode="w", delete=False
        ) as temp_file:
            # Write a wrapper script that includes profiling
            script = (
                "import cProfile, pstats, io\n"
                "profiler = cProfile.Profile()\n"
                "profiler.enable()\n"
                f"{request.code}\n"
                "profiler.disable()\n"
                "s = io.StringIO()\n"
                "stats = pstats.Stats(profiler, stream=s).sort_stats('cumulative')\n"
                "stats.print_stats()\n"
                "print(s.getvalue())"
            )
            temp_file.write(script)
            temp_file_path = temp_file.name

        try:
            result = subprocess.run(
                ["python", temp_file_path], capture_output=True, text=True, check=True
            )
            return result.stdout
        finally:
            os.remove(temp_file_path)

    @staticmethod
    def line_profiler(request: CodeRequest) -> str:
        """
        Perform line-by-line code profiling and return the profiling results.

        Args:
            request (CodeRequest): The code request object.

        Returns:
            str: The line-by-line profiling results.
        """
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
