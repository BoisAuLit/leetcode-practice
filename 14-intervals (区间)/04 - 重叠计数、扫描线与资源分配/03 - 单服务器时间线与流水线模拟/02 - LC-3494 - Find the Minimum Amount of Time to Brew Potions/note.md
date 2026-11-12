# Find the Minimum Amount of Time to Brew Potions 笔记

### 📝 2026-10-14 - retry 1

```python
class Solution:
    def minTime(self, skill: List[int], mana: List[int]) -> int:
        n = len(skill)

        # 台阶的"形状":base[i] = 前 i 个巫师的 skill 之和(还没乘 m)
        # 这就是你原来的 start 数组去掉 m,所以只需要算一次
        base = [0] * n
        for i in range(1, n):
            base[i] = base[i - 1] + skill[i - 1]

        last_finish = [0] * n
        for m in mana:
            # 量撞深:上一瓶右端 − 我的左端(我的左端 = base[i] * m)
            push = 0
            for i in range(n):
                push = max(push, last_finish[i] - base[i] * m)
            # 整体右推:我的右端 = 左端 + 这一级长度 + push
            for i in range(n):
                last_finish[i] = base[i] * m + skill[i] * m + push

        return last_finish[-1]
```
