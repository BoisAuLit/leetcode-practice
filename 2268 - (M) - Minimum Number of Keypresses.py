import collections


class Solution:
    def minimumKeypresses(self, s: str) -> int:
        c = collections.Counter(s)
        print(c)
        ans = cnt = 0
        for i, freq in enumerate(
            sorted(c.values(), reverse=True)
        ):  # sort reversely
            if i % 9 == 0:
                cnt += 1
            ans += (
                cnt * freq
            )  # add `num_of_time_to_press_the_key * frequency` to result
        return ans

s = Solution()
input_ = "abcdefghijkl"
result = s.minimumKeypresses(input_)
print(result)
