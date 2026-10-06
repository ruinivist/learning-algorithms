# Min time to finish all jobs

n jobs, jobs(i) = time to finish it
k workers that I can assign to.
working time = sum of all working times
min the max working time across all

## Solution

let's simplify, parition n into k subsets, such that the max sum across any subset is
minimised.

that minmax suggest a binary search.
if I ask, can I make an assignemnt, such that sum on any <= W and all are assigned.
We need to iterate over one end, what needs to be collision free, it's job as I can't
assign same to two workers, so f(i, mask) seems to be some direction.

I mean, isn't this like a k part knapack or something?
This can definitely work
f(i, mask)
assign a submask of tasks to i, and then min over f(i+1, remaining mask)

You would need to do a submask iteration.

```python
class Solution:
    def minimumTimeRequired(self, jobs: list[int], k: int) -> int:
        n = len(jobs)

        @cache
        def maskjobsum(mask):
            return sum(jobs[i] for i in range(n) if (mask >> i) & 1)

        # mask = 1 for where job is available
        @cache
        def f(i, mask):
            # if it's the last worker, has to do all jobs
            if i == k - 1:
                return maskjobsum(mask)

            ans = math.inf

            sub = mask
            while sub:
                # this worker does submask tasks
                this_worker = maskjobsum(sub)
                nmask = mask ^ sub
                rem_workers = f(i + 1, nmask)
                ans = min(ans, max(this_worker, rem_workers))
                sub = (sub - 1) & mask

            return ans

        return f(0, (1 << n) - 1)
```
