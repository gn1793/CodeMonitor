from collections import deque
from typing import Any, Deque, List

class RingBuffer:
    def __init__(self, capacity: int = 128):
        self.capacity = capacity
        self._dq: Deque[Any] = deque(maxlen=capacity)

    def append(self, item: Any) -> None:
        self._dq.append(item)

    def to_list(self) -> List[Any]:
        return list(self._dq)

    def last(self):
        if not self._dq:
            return None
        return self._dq[-1]
