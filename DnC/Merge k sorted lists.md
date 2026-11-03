# Merge k sorted lists

You have k sorted linked lists, merge them into one sorted.

## Solution ( heapq )

```python
import heapq

class Solution:
    def mergeKLists(self, lists: list[ListNode | None]) -> ListNode | None:
        heap = [
            (node.val, i, node)
            for i, node in enumerate(lists)
            if node
        ]
        heapq.heapify(heap)

        dummy = ListNode()
        tail = dummy

        while heap:
            _, i, node = heapq.heappop(heap)

            if node.next:
                nxt = node.next
                heapq.heappush(heap, (nxt.val, i, nxt))

            tail.next = node
            tail = node

        return dummy.next
```

## DnC one which uses less space

```python
class Solution:
    def mergeKLists(self, lists: list[ListNode | None]) -> ListNode | None:
        if not lists:
            return None

        # merge for 2 kists
        def merge(a, b):
            dummy = ListNode()
            tail = dummy

            while a and b:
                if a.val <= b.val:
                    tail.next = a
                    a = a.next
                else:
                    tail.next = b
                    b = b.next

                tail = tail.next

            tail.next = a or b
            return dummy.next

        while len(lists) > 1:
            merged = []

            for i in range(0, len(lists), 2):
                a = lists[i]
                b = lists[i + 1] if i + 1 < len(lists) else None

                merged.append(merge(a, b))

            lists = merged

        return lists[0]
```
