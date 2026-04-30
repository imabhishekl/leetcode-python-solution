"""
Problem Link: https://leetcode.com/problems/meeting-rooms-ii/

Given an array of meeting time intervals intervals where intervals[i] = [starti, endi], return the minimum number of conference rooms required.

 
Example 1:
Input: intervals = [[0,30],[5,10],[15,20]]
Output: 2
Example 2:
Input: intervals = [[7,10],[2,4]]
Output: 1

 
Constraints:


	1 <= intervals.length <= 104
	0 <= starti < endi <= 106
"""

class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        endTime = []
        intervals.sort(key=lambda x: x[0])
        result = 0

        for interval in intervals:
            if not endTime:
                heapq.heappush(endTime, interval[1])
            elif interval[0] < endTime[0]:
                heappush(endTime, interval[1])
            else:
                heappop(endTime)
                heappush(endTime, interval[1])
            result = max(result, len(endTime))
        return result