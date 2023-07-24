from datetime import datetime


class Solution:
    def daysBetweenDates(self, date1: str, date2: str) -> int:
        d1 = datetime.strptime(date1, "%Y-%m-%d")
        d2 = datetime.strptime(date2, "%Y-%m-%d")
        delta = d2 - d1
        return abs(delta.days)


"""
Runtime
- 41ms
- Beats 90.57%

Memory
16.50mb
- Beats 24.91%
"""
