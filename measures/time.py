import timeit

from models import Code, TimeResults


class TimeAnalysis:
    @staticmethod
    def action(code: Code, iterations: int) -> TimeResults:
        execution_time: float = TimeAnalysis.test_execution_time(code, iterations)
        return TimeResults.from_seconds(execution_time)

    @staticmethod
    def test_execution_time(code: Code, iterations: int) -> float:
        timer = timeit.Timer(code.code_str)
        execution_time = timer.timeit(number=iterations)
        return execution_time
