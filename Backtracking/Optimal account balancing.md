# Optimal account balancing

So you have tuples like (from, to, debt)
and you want to settle them in min transfer of such manner ( from, to, amount )
aka a pairwise settlement.

## Solution

build a net balances array for example [10,5,-15]
where a(i) = net balance right now for person i, then the problem is min number of pairwise
settlements I can do to make it all 0

an exponential backtracking solution is expected, there's no polynomial time one here

something like

```python
from collections import defaultdict

class Solution:
    def minTransfers(self, transactions):
        balance = defaultdict(int)

        for frm, to, amount in transactions:
            balance[frm] -= amount
            balance[to] += amount

        debt = [x for x in balance.values() if x != 0]

        def dfs(start):
            while start < len(debt) and debt[start] == 0:
                start += 1

            if start == len(debt):
                return 0

            ans = float("inf")

            for i in range(start + 1, len(debt)):
                if debt[start] * debt[i] < 0:
                    debt[i] += debt[start]

                    ans = min(ans, 1 + dfs(start + 1))

                    debt[i] -= debt[start]

            return ans

        return dfs(0)
```
