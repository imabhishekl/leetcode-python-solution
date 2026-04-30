"""
Problem Link: https://leetcode.com/problems/rotate-array/

Given an integer array nums, rotate the array to the right by k steps, where k is non-negative.

 
Example 1:


Input: nums = [1,2,3,4,5,6,7], k = 3
Output: [5,6,7,1,2,3,4]
Explanation:
rotate 1 steps to the right: [7,1,2,3,4,5,6]
rotate 2 steps to the right: [6,7,1,2,3,4,5]
rotate 3 steps to the right: [5,6,7,1,2,3,4]


Example 2:


Input: nums = [-1,-100,3,99], k = 2
Output: [3,99,-1,-100]
Explanation: 
rotate 1 steps to the right: [99,-1,-100,3]
rotate 2 steps to the right: [3,99,-1,-100]


 
Constraints:


	1 <= nums.length <= 105
	-231 <= nums[i] <= 231 - 1
	0 <= k <= 105


 
Follow up:


	Try to come up with as many solutions as you can. There are at least three different ways to solve this problem.
	Could you do it in-place with O(1) extra space?
"""

class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        #self.approach1(nums, k)
        self.cyclicApproach(nums, k)

    def approach1(self, nums: List[int], k: int) -> None:
        for i in range(k):
            prev = nums[0]
            for j in range(1, len(nums)):
                temp = nums[j]
                nums[j] = prev
                prev = temp
            nums[0] = prev

    def cyclicApproach(self, nums: List[int], k: int) -> None:
        processed = 0
        n = len(nums)
        k = k%n
        if k == 0:
            return
        id, processed = 0, 0
        while processed < n:
            start, v = id, nums[id]
            while True:
                next = (start + k) % n
                processed += 1
                nums[next], v = v, nums[next]
                start = next
                if id == start:
                    break
            id += 1

    #def tripleReversalApproach(self, nums: List[int], k: int) -> None: