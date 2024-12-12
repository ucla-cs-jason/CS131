#include <vector>
#include <algorithm>
#include <iostream>

using namespace std;

int longestRun(const vector<bool>& vec) {
    int maxLength = 0;
    int currLength = 0;
    
    for (bool b : vec) {
        if (b) {
            currLength++;
            maxLength = max(maxLength, currLength);
        } else {
            currLength = 0;
        }
    }

    return maxLength;
}

int main()
{
    vector<bool> vec1 = {true, true, false, true, true, true, false};
    cout << longestRun(vec1) << endl;

    vector<bool> vec2 = {true, false, true, true};
    cout << longestRun(vec2) << endl;

    return 0;
}