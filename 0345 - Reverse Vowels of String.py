class Solution:
    def reverseVowels(self, s: str) -> str:
        list_ = list(s)
        p1 = 0
        p2 = len(list_) - 1
        vowels = set("aeiouAEIOU")

        while True:
            while p1 < len(list_) and list_[p1] not in vowels:
                p1 += 1
            while p2 >= 0 and list_[p2] not in vowels:
                p2 -= 1
            if p1 >= p2:
                break
            list_[p1], list_[p2] = list_[p2], list_[p1]
            p1 += 1
            p2 -= 1
        return "".join(list_)
