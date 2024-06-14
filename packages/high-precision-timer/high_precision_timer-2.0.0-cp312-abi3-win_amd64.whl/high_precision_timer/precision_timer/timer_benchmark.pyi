from .timer_class import PrecisionTimer as PrecisionTimer
from .utilities import convert_time as convert_time

def benchmark(interval_cycles: int, interval_delay: float, delay_cycles: tuple, delay_durations: tuple) -> None: ...
