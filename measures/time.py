import timeit

from models import CodeRequest, TimeResults


class TimeAnalysis:
    @staticmethod
    def action(request: CodeRequest) -> TimeResults:
        execution_time: float = TimeAnalysis.test_execution_time(request)
        return TimeResults.from_seconds(execution_time)

    @staticmethod
    def test_execution_time(request: CodeRequest) -> float:
        timer = timeit.Timer(request.code)
        execution_time = timer.timeit(number=request.iterations)
        return execution_time
