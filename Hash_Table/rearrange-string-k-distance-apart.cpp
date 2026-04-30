/*
Problem Link: https://leetcode.com/problems/rearrange-string-k-distance-apart/

Given a string s and an integer k, rearrange s such that the same characters are at least distance k from each other. If it is not possible to rearrange the string, return an empty string "".

 
Example 1:


Input: s = "aabbcc", k = 3
Output: "abcabc"
Explanation: The same letters are at least a distance of 3 from each other.


Example 2:


Input: s = "aaabc", k = 3
Output: ""
Explanation: It is not possible to rearrange the string.


Example 3:


Input: s = "aaadbbcc", k = 2
Output: "abacabcd"
Explanation: The same letters are at least a distance of 2 from each other.


 
Constraints:


	1 <= s.length <= 3 * 105
	s consists of only lowercase English letters.
	0 <= k <= s.length
*/

class Solution {
public:
    string rearrangeString(string s, int k) {
        vector<int> freq(26);

        for(int i = 0; i < s.size(); i++) {
            freq[s[i] - 'a']++;
        }

        priority_queue<pair<int, int>> free;

        for(int i = 0; i < 26; i++) {
            if(freq[i]) {
                free.push({ freq[i], i });
            }
        }

        string ans;
        queue<pair<int, int>> busy;

        while(ans.size() != s.size()) {
            int index = ans.size();

            if(!busy.empty() && (index - busy.front().first) >= k) {
                auto q = busy.front(); busy.pop();
                free.push({ freq[q.second], q.second });
            }

            if(free.empty()) {
                return "";
            }

            int current = free.top().second; free.pop();
            ans += current + 'a';

            freq[current]--;

            if(freq[current] > 0) {
                busy.push({ index, current });
            }
        }

        return ans;
    }
};