"""
Problem Link: https://leetcode.com/problems/merge-intervals/

Given an array of intervals where intervals[i] = [starti, endi], merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.

 
Example 1:


Input: intervals = [[1,3],[2,6],[8,10],[15,18]]
Output: [[1,6],[8,10],[15,18]]
Explanation: Since intervals [1,3] and [2,6] overlap, merge them into [1,6].


Example 2:


Input: intervals = [[1,4],[4,5]]
Output: [[1,5]]
Explanation: Intervals [1,4] and [4,5] are considered overlapping.


Example 3:


Input: intervals = [[4,7],[1,4]]
Output: [[1,7]]
Explanation: Intervals [1,4] and [4,7] are considered overlapping.


 
Constraints:


	1 <= intervals.length <= 104
	intervals[i].length == 2
	0 <= starti <= endi <= 104
"""

class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        result = []
        intervals.sort(key=lambda x: x[0])
        currStart, currEnd = -1, -1
        for s, e in intervals:
            if currEnd == -1:
                currStart = s
                currEnd = e
            elif currEnd < s:
                result.append([currStart, currEnd])
                currStart, currEnd = s, e
            else:
                currEnd = max(currEnd, e)
        result.append([currStart, currEnd])
        return result