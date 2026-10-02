---
leetcode_url: https://leetcode.com/problems/race-car/
---

# Race Car

In one move, you can do `x += speed, speed *= 2` OR `speed = 1 * flip sign`.
Num moves to go from 0 to some x in [1,1e4]

## Solution

A bfs looks obvious except take the case of going to -inf, that will be one of the steps
contending in our queue.

It's mostly pruning heuristics. Note that a flip nullifies any speed accumulated,
so going to negative direction and then flipping = not only more distance but also starting
with 1 speed, we can prune that.

What about overshooting, a slight overshoot then a reverse correction can be optimal.
But say distance from start to target is T, if you are ever at > 2T, then the same argument of
not only more distance but also starting from 1 speed applies.

```python
class Solution:
    def racecar(self, t: int) -> int:
        q = deque()
        q.append((0, 1, 0))  # pos, speed, moves

        seen = set()
        while q:
            pos, speed, moves = q.popleft()
            # prune
            if pos < 0 or pos > 2 * t or (pos, speed) in seen:
                continue

            seen.add((pos, speed))
            if pos == t:
                return moves

            # A
            q.append((pos + speed, speed * 2, moves + 1))
            # R
            q.append((pos, -1 * speed // abs(speed), moves + 1))

        return math.inf  # should never reach
```
