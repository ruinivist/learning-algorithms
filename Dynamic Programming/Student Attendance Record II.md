---
leetcode_url: https://leetcode.com/problems/student-attendance-record-ii/
---

# Student Attendance Record II

Find number of strings with count of As <=1 and no more than 2 consectutive Ls.
P's can be any.

If you map it to say ints.
You can have any number of 0s, <=1 1s in total, and no more than 2 consecutive 2s.

## Solution

The problem is really trivial for a dp one, state is just count of 1s and the running count
of 2s and how far in the contruction are we.

this was the recursion, note that

```python
class Solution:
    def checkRecord(self, n: int) -> int:
        # f is count we can make from suffix

        mod = int(1e9 + 7)
        @cache
        def f(i, c1, c2):
            if i == n:
                return 1

            ans = 0
            pick = [0] + ([1] if c1 < 1 else []) + ([2] if c2 < 2 else [])

            for x in pick:
                # IMP: precedence of + > precedence of x == 1
                # so this bracket is NEEDED
                nc1 = c1 + (x == 1)
                nc2 = 0 if x != 2 else c2 + 1
                ans += f(i + 1, nc1, nc2)
                # a mod at each step is needed else python is caching large
                # numbers in f, this otherwise gets MLEd
                ans %= mod
            return ans

        return f(0, 0, 0)
```

They really want the interative version here as this gets TLEd.

```python
class Solution:
    def checkRecord(self, n: int) -> int:
        MOD = int(1e9 + 7)

        # dp[c1][c2]
        dp = [[0] * 3 for _ in range(2)]
        dp[0][0] = 1

        for i in range(n):
            ndp = [[0] * 3 for _ in range(2)]

            for c1 in range(2):
                for c2 in range(3):
                    if dp[c1][c2] == 0:
                        continue

                    pick = [0] + ([1] if c1 < 1 else []) + ([2] if c2 < 2 else [])

                    for x in pick:
                        nc1 = c1 + (x == 1)
                        nc2 = 0 if x != 2 else c2 + 1

                        ndp[nc1][nc2] += dp[c1][c2]
                        ndp[nc1][nc2] %= MOD

            dp = ndp

        return sum(sum(row) for row in dp) % MOD
```

Note that there is a matrix-exponentiation version possible but this is a good problem to
practice that, something for later.
