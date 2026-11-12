# Reverse Bits 笔记（2026-09-09）

从 n 的右边一位一位取 bit，然后从左到右重新构造答案。

```
for _ in range(32):
    bit = n & 1                  # 取 n 最右边一位
    result = (result << 1) | bit # result 左移腾位，把这一位塞到最右边
    n >>= 1                      # n 丢掉最右边一位
```

固定跑 32 轮（不是 while n），否则高位的 0 不会被补齐。
