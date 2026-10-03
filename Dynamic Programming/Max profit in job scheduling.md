# Max profit in job scheduling

(start,end,profit). You cannot do simultaneous work, find maximum profit.

## Solution

A trivial recurrence would be f(i) = max profit if I do the ith task.
Then f(i) = p(i) + max over f(j) s.t. end of job <= start of job i.
This way you also cleanly avoid storing any time info too. But you would then need a correct
ordering to things then. The prefix MUST contain all jobs that have ended prior to my
job. My iteration order on i, must then be on end times of jobs.

Let me be coherent.
Sort by end times.
f(i) = p(i) + max over f(j) s.t. j end <= i start
Note that I CAN be processing an i that is like this => i start...last j end...i end
So I only need the max from a certain prefix ( which I can bin search over ).

Note that for the final answer we need a max across, so I can let the dp incorportate
that max as well. Making the recurrence just

f(i) = max f(i-1), profit i + f(pred)
where pred = max j in prefix st end j < start i

```python
class Solution:
    def jobScheduling(self, startTime, endTime, profit):
        jobs = sorted(zip(endTime, startTime, profit))
        dp = [0] * (len(jobs) + 1)

        for i, (_, start, profit) in enumerate(jobs, 1):
            prev = bisect_right(jobs, (start, math.inf, math.inf))
            dp[i] = max(dp[i - 1], profit + dp[prev])

        return dp[-1]
```
