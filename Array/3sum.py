"""
Problem Link: https://leetcode.com/problems/3sum/

Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.

Notice that the solution set must not contain duplicate triplets.

 
Example 1:


Input: nums = [-1,0,1,2,-1,-4]
Output: [[-1,-1,2],[-1,0,1]]
Explanation: 
nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0.
nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0.
nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0.
The distinct triplets are [-1,0,1] and [-1,-1,2].
Notice that the order of the output and the order of the triplets does not matter.


Example 2:


Input: nums = [0,1,1]
Output: []
Explanation: The only possible triplet does not sum up to 0.


Example 3:


Input: nums = [0,0,0]
Output: [[0,0,0]]
Explanation: The only possible triplet sums up to 0.


 
Constraints:


	3 <= nums.length <= 3000
	-105 <= nums[i] <= 105
"""

class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        #return self.bruteForce(nums)
        return self.twoSum(nums)

    def twoSum(self, nums: List[int]) -> List[List[int]]:
        result = []
        nums.sort()
        size = len(nums)
        i = 0
        while i < size:
            anchor = nums[i]
            left = i + 1
            right = size - 1
            while left < right:
                sum = anchor + nums[left] + nums[right]
                if sum == 0:
                    result.append([anchor, nums[left], nums[right]])
                    left += 1
                    right -= 1
                    while left < right and nums[left] == nums[left - 1]:
                        left += 1
                    while right > left and nums[right] == nums[right + 1]:
                        right -= 1
                elif sum < 0:
                    left += 1
                else:
                    right -= 1
            i += 1
            while i < size and nums[i] == nums[i - 1]:
                i += 1
        return result

    def bruteForce(self, nums: List[int]) -> List[List[int]]:
        result = []
        size = len(nums)
        for i in range(size):
            for j in range(i + 1, size):
                for k in range(j + 1, size):
                    if nums[i] + nums[j] + nums[k] == 0:
                        r = sorted([nums[i], nums[j], nums[k]])
                        if r not in result:
                            result.append([nums[i], nums[j], nums[k]])
        return result
