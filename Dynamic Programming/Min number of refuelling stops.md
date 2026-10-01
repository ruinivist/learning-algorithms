# Min number of refueling stops

(pos, fuel) tuples, you starts with start fuel. If you stop it's one move and you get all the fuel
at that position. Min number of stops to reach ( 1 fuel per pos consumption ).

## Solution

Stops are just 500. For eachs top as you move, you have two choices, stop or not.
If you stop, it's (moves + 1, fuel + stop fuel), else it remains the same.
The args would just be (i, startfuel) returning moves.

I feel like I'm missing something as contraints must be higher but let's see.

```python
class Solution:
    def minRefuelStops(self, t: int, start: int, s: list[list[int]]) -> int:
        s = [[0, 0]] + s + [[t, 0]]
        n = len(s)

        @cache
        def f(i, sf):
            if sf < 0:
                return math.inf
            if i == n - 1:
                return 0

            dist = s[i + 1][0] - s[i][0]
            ans = min(1 + f(i + 1, sf + s[i][1] - dist), f(i + 1, sf - dist))
            return ans

        ret = f(0, start)
        return -1 if ret == math.inf else ret
```

I wrote this which was clearly not enough, problem was that I misjudged complexity.
Look at my "sf", it's a sum of all past binary choices so same as subset sum, the state just
blows up there's no way around it.

The way to go in this one is model it as a knapsack problem. Define value as the fuel it gives,
and wt as 1 for each ( 1 move ). Then you can do a dp(wt) formulation => max fuel in j stops.
Though it's not exactly knapsack as you are accouning for reachability too.

```python
class Solution:
    def minRefuelStops(self, t: int, start: int, s: list[list[int]]) -> int:
        n = len(s)
        # max dist reachable with j stops
        dp = [start] + [0] * n

        for i, (pos, fuel) in enumerate(s):
            for j in range(i, -1, -1):
                # i can reach this one
                if dp[j] >= pos:
                    # push
                    dp[j + 1] = max(dp[j + 1], dp[j] + fuel)

        for j, reach in enumer-ate(dp):
            if reach >= t:
                return j

        return -1
```

you can also do the same thing recursively, the idea was just the same, f(i, j) = max dist I can go
if I choose from the first i stations and can choose atmost j ( same as knapsack )

```python
class Solution:
    def minRefuelStops(self, t, start, s):
        n = len(s)

        @cache
        def f(i, k):
            if k == 0:
                return start
            if k > i:
                return -math.inf

            skip = f(i - 1, k)
            take = -math.inf

            pos, fuel = s[i - 1]
            # where I could reach with one less stop
            prev = f(i - 1, k - 1)
            if prev >= pos:
                # if I can reach this station
                take = prev + fuel

            return max(skip, take)

        for k in range(n + 1):
            if f(n, k) >= t:
                return k
        return -1
```

## Solution 2

This problem is more of a representative one for max heap I would say.
Idea being you only refuel greedily when needed in the sense that when you run out, you consume
the largest one passed in retrospect.

```python
class Solution:
    def minRefuelStops(self, t: int, sf: int, s: list[list[int]]) -> int:
        q = []
        s.append((t, 0))
        myf, myp = sf, 0
        ans = 0
        for pos, fuel in s:
            dist = pos - myp
            myf -= dist

            # pick greedily
            while q and myf < 0:
                ans += 1
                myf += -heappop(q)

            if myf < 0:
                return -1

            heappush(q, -fuel)
            myp = pos

        return ans
```
