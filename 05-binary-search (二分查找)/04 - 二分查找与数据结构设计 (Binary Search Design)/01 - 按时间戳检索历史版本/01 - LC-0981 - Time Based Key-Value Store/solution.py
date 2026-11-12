import bisect

class TimeMap:
    def __init__(self):
        self.dict = {}

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.dict.setdefault(key, []).append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        if key not in self.dict:
            return ""

        arr = self.dict[key]
        i = bisect.bisect_right(arr, (timestamp, "")) - 1  # include all values at same ts safely

        return arr[i][1] if i >= 0 else ""
