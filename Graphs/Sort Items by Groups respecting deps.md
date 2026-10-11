# Sort items by groups respective dependencies

You have an ordering define on items and then an ordering define on groups. We need a sort
order that respects BOTH orderings.

## Solution

Now one way that works is that you make a union graph, where a cross of all edges are used
to define group dependencies so from every node in group 1 you have an edge to group 2 implying
that 1 comes first then 2. Problem is this can create n^2 edges.

> actually I misread, the groups themselves have no ordering dep, so group 1 can come before group
> 0, the just need to have their elems together.

Group deps are inferred from the item deps.

Idea is a **hierarchical** toposort where you sort the groups first and then the items within
( can also be the other way around ).

So as you iterate the (prev -> i) edges, if they are in the same group, add it to item graph,
else if cross group, add the group numbers to group graphs.

Toposort the groups, then toposort within each group.

```python

class Solution:
    def sortItems(self, n: int, m: int, group: list[int], beforeItems: list[list[int]]) -> list[int]:
        # Each -1 gets its own one-element group
        for i in range(n):
            if group[i] == -1:
                group[i] = m
                m += 1

        g_groups = [[] for _ in range(m)]
        g_items = [[] for _ in range(n)]

        indeg_groups = [0] * m
        indeg_items = [0] * n

        for i, prev in enumerate(beforeItems):
            for p in prev:
                gi, gp = group[i], group[p]

                if gi != gp:
                    # Different groups
                    g_groups[gp].append(gi)
                    indeg_groups[gi] += 1
                else:
                    # Same group
                    g_items[p].append(i)
                    indeg_items[i] += 1

        def topo(gr, indeg, nodes):
            zeros = [i for i in range(nodes) if indeg[i] == 0]

            order = []
            while zeros:
                cur = zeros.pop()
                order.append(cur)

                for to in gr[cur]:
                    indeg[to] -= 1
                    if indeg[to] == 0:
                        zeros.append(to)

            if len(order) != nodes:
                return []
            return order

        group_topo = topo(g_groups, indeg_groups, m)
        item_topo = topo(g_items, indeg_items, n)

        if len(group_topo) != m or len(item_topo) != n:
            return []

        # Bucket items by their group, preserving topo order
        items_by_group = [[] for _ in range(m)]
        for item in item_topo:
            items_by_group[group[item]].append(item)

        # Output groups in topological order
        ans = []
        for g in group_topo:
            ans.extend(items_by_group[g])

        return ans
```

The key is final assembly. Since we know an order for buckets, all that matters is knowing the elements of items in that bucket. Iterating by topo order on items and then collecting them grouped by bucket gives you that.
