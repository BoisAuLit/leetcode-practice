from typing import List

"""
Time complexity: O()
Space complexity: O()
"""

class Solution:
    def averageWaitingTime(self, customers: List[List[int]]) -> float:
        total_waiting_time = customers[0][1]
        last_order_end_time = customers[0][0] + customers[0][1]
        for arrival_time, duration in customers[1:]:
            if last_order_end_time < arrival_time:
                total_waiting_time += duration
                last_order_end_time = arrival_time + duration
            else:
                total_waiting_time += last_order_end_time - arrival_time + duration
                last_order_end_time = last_order_end_time + duration
        return total_waiting_time / len(customers)


# class Solution:
#     def averageWaitingTime(self, customers: List[List[int]]) -> float:
#         next_idle_time = 0
#         net_wait_time = 0

#         for customer in customers:
#             # The next idle time for the chef is given by the time of delivery
#             # of current customer's order.
#             next_idle_time = max(customer[0], next_idle_time) + customer[1]

#             # The wait time for the current customer is the difference between
#             # his delivery time and arrival time.
#             net_wait_time += next_idle_time - customer[0]

#         # Divide by total customers to get average.
#         average_wait_time = net_wait_time / len(customers)
#         return average_wait_time


s = Solution()
input_ = [[1, 2], [2, 5], [4, 3]]
result = s.averageWaitingTime(input_)
print(result)
