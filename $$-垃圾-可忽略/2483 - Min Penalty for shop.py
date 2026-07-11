class Solution_One_Pass:
    def bestClosingTime(self, customers: str) -> int:
        cur_penalty = min_penalty = 0
        earliest_hour = 0
        
        for i, ch in enumerate(customers):
            if ch == 'Y':
                cur_penalty -= 1
            else:
                cur_penalty += 1
            if cur_penalty < min_penalty:
                earliest_hour = i + 1
                min_penalty = cur_penalty
                
        return earliest_hour


class Solution_Two_Passes:
    def bestClosingTime(self, customers: str) -> int:
        arr = [1 if x == "Y" else 0 for x in customers]
        min_penalty = penalty = sum(arr)
        min_index = 0
        for index, char in enumerate(customers):
            if char == "Y":
                penalty -= 1
            else:
                penalty += 1
            if penalty < min_penalty:
                min_penalty = penalty
                min_index = index + 1

        return min_index
