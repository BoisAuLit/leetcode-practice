# Average Waiting Time 笔记

### 📝 2026-10-01 - retry 1

```python
class Solution:
    def averageWaitingTime(self, customers: List[List[int]]) -> float:
        n = len(customers)
        total_wait = customers[0][1]
        curr_end = customers[0][0] + customers[0][1]
        # Simulation
        for i in range(1, n):
            start, wait = customers[i]
            if start <= curr_end:
                total_wait += curr_end - start + wait
                curr_end += wait
            else:
                total_wait += wait
                curr_end = start + wait
        return total_wait / n
```
