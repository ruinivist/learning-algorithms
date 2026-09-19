# Maximal Rectangle ( Histogram )

A very common idea in "binary grid" and finding largest rectangle or square in those.
( the other one being binary search ).

You acumulate the ones row by row and basically treat each row as the histogram of 1s
above it and process just that row in that histogram format.

```python
class Solution:
    def maximalRectangle(self, matrix: list[list[str]]) -> int:
        n, m = len(matrix), len(matrix[0])

        h = [0] * m
        ans = 0

        def smallToLeft(row):
            sml = [-1] * len(row)
            # I want the first smaller to the left so I want to keep
            # popping while it's >= current
            stk = []
            for j in range(len(row)):
                while stk and row[stk[-1]] >= row[j]:
                    stk.pop()

                if stk:
                    sml[j] = stk[-1]

                stk.append(j)
            return sml

        for i in range(n):
            # accumulate in h
            for j in range(m):
                x = matrix[i][j] == "1"
                h[j] = 0 if x == 0 else h[j] + x

            # take each col and make it the height of rect, what can
            # be the ends?
            sml = smallToLeft(h)

            smr = smallToLeft(h[::-1])[::-1]
            smr = [m if pos == -1 else m - 1 - pos for pos in smr]

            for j in range(m):
                a, b = sml[j], smr[j]
                width = b - a - 1
                ans = max(ans, width * h[j])

        return ans
```

Note

- look at how smr is donw, twice reversed and -1 to m
- the line of though "I want the first smaller to left so I can to keep popping while it's
  same or larger is just perfect"
