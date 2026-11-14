# Max sum BST in Binary Tree

Fin the max sum across any subtree that is a BST

## Solution

Look at the "info" struct based idea here, once you have info made. Rest is trivial impl.

```cpp
class Solution {
public:
    int maxSumBST(TreeNode* root) {
        const int INF = 1e9;
        int ans = 0;

        struct info{
            bool is_bst;
            int mn;
            int mx;
            int sum;
        };

        auto f = [&](auto&& f, TreeNode* cur) -> info {
            if(!cur) return {1,INF, -INF,0};

            auto l = f(f, cur -> left);
            auto r = f(f, cur -> right);

            // is THIS a bst?
            bool isBST = l.is_bst && r.is_bst && l.mx < cur->val && cur -> val < r.mn;
            if(isBST){
                int sum = l.sum + r.sum + cur->val;
                int mn = min(l.mn,cur->val);
                int mx = max(r.mx,cur->val);
                ans = max(ans, sum);
                return {1, mn, mx, sum};
            }else{
                return {0,0,0,0};
            }
        };
        f(f,root);

        return ans;
    }
};
```
