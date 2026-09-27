# Maximum Vacation Days

`flights[i][j] = 1` means you can fly from city `i` to city `j`, and `days[i][week]` gives the vacation days available in city `i` that week.  
You start in city 0.  
At the beginning of each week, you can either stay in the current city or fly to another city if a direct flight exists.

> note that same city will have different vacation days depending on the week

Goal is to max the total vacationd days.

## Solution

Flights is just a graph, we can ignore that, it's basically something to max over when we
consider choices of where to go in the next week.

It cannot be greedy because you might go to a bad city if it has connecting flight to a good
one for the subsequent weeks.

Define `f(i, week)` as the number of vacation days if I start in city i for week `week`.
Then I can just `max over j = {i, flight to j}: days(j, week) + f(j,week+1)`

## Solution

```python
from functools import cache

class Solution:
    def maxVacationDays(self, flights: list[list[int]], days: list[list[int]]) -> int:
        n, k = len(flights), len(days[0])

        @cache
        def f(city: int, week: int) -> int:
            if week == k:
                return 0

            return max(
                days[nxt][week] + f(nxt, week + 1)
                for nxt in range(n)
                if nxt == city or flights[city][nxt]
            )

        return f(0, 0)
```
