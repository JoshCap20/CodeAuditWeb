from .base import Base, BaseTimeMeasurement, BaseSizeMeasurement, FileLink


class TimeResults(BaseTimeMeasurement):
    pass


class MemoryResults(BaseSizeMeasurement):
    pass

class AdvancedMemoryResults(Base):
    detailed_usage: str  # String to hold detailed line-by-line memory usage
    peak_memory_usage: MemoryResults  # Peak memory usage statistics
    memory_chart: FileLink | None  # URL to the memory chart image

class ProfileResults(Base):
    profile: str
    
class AdvancedProfileResults(Base):
    profile: str
    line_profile: str

class Results(Base):
    time: TimeResults | None = None
    memory: MemoryResults | None = None
    advanced_memory: AdvancedMemoryResults | None = None
    flamegraph: FileLink | None = None
    dotgraph: FileLink | None = None
    profile: str | None = None

    def __setitem__(self, key, value):
        if key in self.__fields__:
            setattr(self, key, value)
        else:
            raise KeyError(f"Invalid key: {key}")
