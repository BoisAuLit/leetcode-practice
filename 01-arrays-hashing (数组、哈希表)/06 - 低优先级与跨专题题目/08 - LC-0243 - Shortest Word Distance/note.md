# Shortest Word Distance 笔记

### 📝 2026-09-30 - retry 1

```python
class Solution:
    def shortestDistance(self, words: List[str], word1: str, word2: str) -> int:
        i1 = i2 = -1
        res = len(words)
        for index, word in enumerate(words):
            if word == word1:
                i1 = index
            if word == word2:
                i2 = index
            # ! Don't forget this check plz!!!!
            if i1 != -1 and i2 != -1:
                res = min(res, abs(i1-i2))
        return res
```
