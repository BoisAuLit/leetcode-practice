from collections import defaultdict

class TimeMap:
    def __init__(self):
        self.map = dict()

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.map[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        # ! 这一步很重要，一定要检查 key 是不是已经存在
        if key not in self.map:
            return ""
    
        arr = self.map[key]
        if timestamp < arr[0][0]:
            return ""
        l, r = 0, len(arr) - 1
        
        while l <= r:
            m = (l + r) // 2
            if arr[m][0] <= timestamp and (m + 1 == len(arr) or arr[m + 1][0] > timestamp):
                return arr[m][1]
            if arr[m][0] < timestamp:
                l += 1
            elif arr[m][0] > timestamp:
                r -= 1
            else:
                return arr[m][1]
        return ""
