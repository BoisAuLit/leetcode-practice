# Minimum Number of Valid Strings to Form Target I 笔记

### 📝 2026-09-30 - retry 1

```python
class Solution:
    def minValidStrings(self, words: List[str], target: str) -> int:
        n = len(target)
        trie = {}
        for word in words:
            node = trie
            for ch in word:
                node = node.setdefault(ch, {})
        max_steps = [0] * n
        for i in range(n):
            level = 0
            node = trie
            for j in range(i, n):
                ch = target[j]
                if ch not in node:
                    break
                node = node[ch]
                level += 1
            max_steps[i] = level

        curr_far = curr_end = 0
        steps = 0
        for i in range(n):
            curr_far = max(curr_far, i + max_steps[i])
            if i == curr_end:
                curr_end = curr_far
                steps += 1
                if curr_end >= n:  # 更新之后再判是否够到终点
                    return steps

        return -1
```

### 📝 2026-10-03 - retry 2

```python
class Solution:
    def minValidStrings(self, words: List[str], target: str) -> int:
        n = len(target)
        trie = {}
        # ! 字典树必然建立在一系列 words 之上, 必须要有好几个 words 才可以的
        for word in words:
            node = trie
            for ch in word:
                node = node.setdefault(ch, {})
            # ! 下面这一行纯属浪费, 无用
            node["#"] = word
        max_steps = [0] * n
        for i in range(n):
            level = 0
            node = trie
            for j in range(i, n):
                ch = target[j]
                if ch not in node:
                    break
                node = node[ch]
                level += 1
            max_steps[i] = level

        curr_far = curr_end = 0
        steps = 0
        for i in range(n):
            curr_far = max(curr_far, i + max_steps[i])
            if i == curr_end:
                curr_end = curr_far
                steps += 1
                # ! 更新之后再判是否够到终点
                if curr_end >= n:  
                    return steps

        """
        能走到这一行,说明循环里从来没有 return 过, 也就是 << 中途卡住了 >>
        也就是说, 在某个 i == curr_end 的时刻, curr_far 没有推进,
        curr_end 从此定在那里,后面所有的 i 都比它大,再也不会更新。


        但 curr_far 不一样——curr_far = max(curr_far, i + max_steps[i]) 这一行每个 i 都会执行,不管 i 到底能不能到达。卡住之后,循环继续往右扫,那些根本到不了的位置照样把它们的 i + max_steps[i] 混进了 curr_far。于是出现这种情况:明明从起点走不通,curr_far 却被某个"到不了的位置"推到了 n。
        """
        return steps if curr_end == n else -1
```

### 📝 2026-10-10 - retry 3

```python
class Solution:
    def minValidStrings(self, words: List[str], target: str) -> int:
        n = len(target)
        trie = {}
        # ! This is how we set up a trie
        for word in words:
            node = trie
            for ch in word:
                node = node.setdefault(ch, {})
            node["#"] = word
        max_right = [0] * n
        for i in range(n):
            level = 0
            node = trie
            for j in range(i, n):
                ch = target[j]
                if ch not in node:
                    break
                node = node[ch]
                level += 1
            max_right[i] = level
        curr_end = curr_far = 0
        steps = 0
        # ! This is jump game II
        for i in range(n):
            curr_far = max(curr_far, i + max_right[i])
            if i == curr_end :
                steps += 1
                curr_end = curr_far

        return steps if curr_end == n else -1
```
