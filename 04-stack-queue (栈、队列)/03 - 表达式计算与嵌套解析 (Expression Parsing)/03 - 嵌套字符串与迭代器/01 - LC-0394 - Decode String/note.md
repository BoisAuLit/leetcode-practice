# Decode String 笔记

### 📝 2026-10-02 - retry 1

```python
class Solution:
    def decodeString(self, s: str) -> str:
        stack = []
        for ch in s:
            if ch == "]":
                letters = []
                while stack[-1] != "[":
                    letters.append(stack.pop())
                stack.pop()  # Pop the "["
                numbers = []
                while stack and stack[-1].isdigit():
                    numbers.append(stack.pop())
                for _ in range(int("".join(numbers[::-1]))):
                    for i in range(len(letters)-1, -1, -1):
                        stack.append(letters[i])
            else:
                stack.append(ch)
        return "".join(stack)
```
