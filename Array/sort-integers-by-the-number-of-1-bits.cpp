/*
Problem Link: https://leetcode.com/problems/sort-integers-by-the-number-of-1-bits/

You are given an integer array arr. Sort the integers in the array in ascending order by the number of 1's in their binary representation and in case of two or more integers have the same number of 1's you have to sort them in ascending order.

Return the array after sorting it.

 
Example 1:


Input: arr = [0,1,2,3,4,5,6,7,8]
Output: [0,1,2,4,8,3,5,6,7]
Explantion: [0] is the only integer with 0 bits.
[1,2,4,8] all have 1 bit.
[3,5,6] have 2 bits.
[7] has 3 bits.
The sorted array by bits is [0,1,2,4,8,3,5,6,7]


Example 2:


Input: arr = [1024,512,256,128,64,32,16,8,4,2,1]
Output: [1,2,4,8,16,32,64,128,256,512,1024]
Explantion: All integers have 1 bit in the binary representation, you should just sort them in ascending order.


 
Constraints:


	1 <= arr.length <= 500
	0 <= arr[i] <= 104
*/

class Solution {
public:
    static bool cmpFunc(pair<int, int> &a, pair<int, int> &b) {
        return a.first < b.first ? true : (a.first == b.first ? a.second < b.second : false);
    }
    vector<int> sortByBits(vector<int>& arr) {
        vector<pair<int, int>> vec;

        for(auto val : arr) {
            int count_ones = 0, tmp_val = val;
            while(tmp_val) {
                if(tmp_val % 2) {
                    count_ones++;
                }

                tmp_val /= 2;
            }
            vec.push_back({ count_ones, val });
        }

        sort(vec.begin(), vec.end(), cmpFunc);

        vector<int> res;

        for(auto num : vec) {
            res.push_back(num.second);
        }

        return res;
    }
};