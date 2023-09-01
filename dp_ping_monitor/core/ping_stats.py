from typing import Optional


class PingStats(object):
    _min: Optional[int]  # to handle uninitialized state
    _max: int  # we don't need it for max because 0 is a correct uninitialized value for it
    _avg: float
    _val_count: int

    def __init__(self):
        self.reset()

    @property
    def min(self) -> int:
        return self._min if self._min else 0

    @property
    def max(self) -> int:
        return self._max

    @property
    def avg(self) -> float:
        return self._avg

    def add(self, value: int):
        if value is None:
            return

        self._min = min(self._min, value) if self._min else value
        self._max = max(self._max, value)

        cur_sum = self._avg * self._val_count + value
        self._val_count += 1
        self._avg = cur_sum / self._val_count

    def reset(self):
        self._min = None
        self._max = 0
        self._avg = 0.0
        self._val_count = 0
