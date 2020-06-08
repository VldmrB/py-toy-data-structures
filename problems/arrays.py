from typing import List


class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        running_sum = 0
        index = 0
        count = 0
        array_len = len(nums) - 1
        while index < array_len:
            cur_num = nums[index]
            if cur_num > k:
                running_sum = cur_num
                index += 1
                count = 0
                continue
            if running_sum + cur_num > k:
                running_sum = cur_num
                index += 1
                count = 1
                continue

            running_sum += cur_num
            index += 1
            count += 1
            if running_sum == k:
                break

        return count


print(Solution().subarraySum(
    [1, 2, 200, 1, 4, 3, 1],
    202
))
