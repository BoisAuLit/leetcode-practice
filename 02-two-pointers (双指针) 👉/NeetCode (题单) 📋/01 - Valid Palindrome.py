"""
📌 信号→模式: 回文判定忽略非字母数字 → 首尾相向双指针 + isalnum 跳过
📅 首次: 2026-09-04 | 卡点: （待补） | 守卫: （待补）
🔁 复习: 下次: 2026-09-05
"""
class Solution:
    def isPalindrome(self, s: str) -> bool:
        l = 0
        r = len(s) - 1
        while l < r:
            while l < r and not s[l].isalnum():
                l += 1
            while r > l and not s[r].isalnum():
                r -= 1
            if s[l].lower() != s[r].lower():
                return False
            l += 1
            r -= 1
        return True
