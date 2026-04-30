class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        return self.updatedLogic(nums)

    def updatedLogic(self, nums: List[int]) -> int:
        slow, fast = 0, 0
        for fast in range(len(nums)):
            if fast < 2 or nums[slow - 2] != nums[fast]:
                nums[slow] = nums[fast]
                slow += 1
        return slow

    def dumbLogic(self, nums: List[int]) -> int:
        i, j = 0, 0
        freq = 0
        curr = nums[0]
        for j in range(len(nums)):
            if curr == nums[j]:
                if freq < 2:
                    nums[i] = nums[j]
                    i += 1
                freq += 1
            else:
                curr = nums[j]
                freq = 1
                nums[i] = nums[j]
                i += 1
        return i