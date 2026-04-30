"""
Problem Link: https://leetcode.com/problems/target-sum/

You are given an integer array nums and an integer target.

You want to build an expression out of nums by adding one of the symbols '+' and '-' before each integer in nums and then concatenate all the integers.


	For example, if nums = [2, 1], you can add a '+' before 2 and a '-' before 1 and concatenate them to build the expression "+2-1".


Return the number of different expressions that you can build, which evaluates to target.

 
Example 1:


Input: nums = [1,1,1,1,1], target = 3
Output: 5
Explanation: There are 5 ways to assign symbols to make the sum of nums be target 3.
-1 + 1 + 1 + 1 + 1 = 3
+1 - 1 + 1 + 1 + 1 = 3
+1 + 1 - 1 + 1 + 1 = 3
+1 + 1 + 1 - 1 + 1 = 3
+1 + 1 + 1 + 1 - 1 = 3


Example 2:


Input: nums = [1], target = 1
Output: 1


 
Constraints:


	1 <= nums.length <= 20
	0 <= nums[i] <= 1000
	0 <= sum(nums[i]) <= 1000
	-1000 <= target <= 1000
"""

class Solution:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        #return self.recurse(0, len(nums), 0, nums, target)
        return self.recurseV2(0, 0, nums, target, {})

    def recurseV2(self, currSum, index, nums, target, memo) -> int:
        if currSum == target and index == len(nums):
            return 1
        elif index == len(nums):
            return 0
        elif (index, currSum) in memo:
            return memo[(index, currSum)]
        else:
            negative = self.recurseV2(currSum - nums[index], index + 1, nums, target, memo)
            positive = self.recurseV2(currSum + nums[index], index + 1, nums, target, memo)
            sum = negative + positive
            memo[(index, currSum)] = sum
            return sum

    def recurse(self, index, size, currSum, nums, target) -> int:
        result = 0
        if currSum == target and index == size:
            #print(f"found:{index}:{currSum}")
            result += 1
        if not index < size:
            return result
        return self.recurse(index + 1, size, currSum + nums[index], nums, target) + self.recurse(index + 1, size, currSum - nums[index], nums, target) + result