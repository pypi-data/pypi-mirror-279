from typing import Literal

import numpy as np

def format_message(message: str) -> str: ...
def convert_time(
    time: int | float | np.ndarray | list,
    from_units: Literal["ns", "us", "ms", "s", "m", "h", "d"],
    to_units: Literal["ns", "us", "ms", "s", "m", "h", "d"],
) -> float | np.ndarray | list: ...
def get_timestamp(time_separator: str = "-") -> str: ...
