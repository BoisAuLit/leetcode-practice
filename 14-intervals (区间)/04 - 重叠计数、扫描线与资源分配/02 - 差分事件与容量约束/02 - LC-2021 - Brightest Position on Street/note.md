# Brightest Position on Street 笔记

### 📝 2026-10-27 - retry 1

```python
class Solution:
    def brightestPosition(self, lights: list[list[int]]) -> int:
        arrL = []
        arrR = []

        # Collect start and end positions
        for pos, radius in lights:
            arrL.append(pos - radius)
            arrR.append(pos + radius)

        arrL.sort()
        arrR.sort()

        p = 0  # Pointer into end positions
        score = 0
        bestScore = 0
        bestL = arrL[0]

        for i in range(len(arrL)):
            # A new light starts at L
            score += 1

            # Remove lights that ended before L
            while p < len(arrR) and arrR[p] < arrL[i]:
                score -= 1
                p += 1


            # Update brightest position
            if score > bestScore:
                bestScore = score
                bestL = arrL[i]

        return bestL
```
