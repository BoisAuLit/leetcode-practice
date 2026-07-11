class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        m_count = [0] * 26
        ascii_a = ord('a')
        for letter in magazine:
            m_count[ord(letter) - ascii_a] += 1
        
        r_count = [0] * 26
        for letter in ransomNote:
            index = ord(letter) - ascii_a
            r_count[index] += 1
            if r_count[index] > m_count[index]:
                return False
        return True

"""
Runtime
- 61ms
- Beats 79.54%

Memory
16.66mb
- Beats 30.10%
"""
