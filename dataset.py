from collections import deque
import asyncio

class SimpleCAFilter:
    def __init__(self, max_size=30):
        self.max_size = max_size
        self._seen_cas = deque(maxlen=max_size)
        self._lock = asyncio.Lock()

    async def should_skip(self, ca: str) -> bool:
        """Returns True if CA should be skipped (already seen)"""
        async with self._lock:
            if ca in self._seen_cas:
                return True
            self._seen_cas.append(ca)
            return False
