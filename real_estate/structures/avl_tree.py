class AVLNode:
    def __init__(self, key):
        self.key = key  # 节点的键值
        self.left = None  # 左子节点
        self.right = None  # 右子节点
        self.height = 1  # 节点的高度，默认为1

class AVLTree:
    def __init__(self):
        self.root = None  # 树的根节点

    def height(self, node):
        if not node:
            return 0  # 如果节点为空，返回高度0
        return node.height  # 返回节点的高度

    def balance_factor(self, node):
        if not node:
            return 0  # 如果节点为空，返回平衡因子0
        return self.height(node.left) - self.height(node.right)  # 计算平衡因子

    def update_height(self, node):
        if not node:
            return  # 如果节点为空，直接返回
        node.height = max(self.height(node.left), self.height(node.right)) + 1  # 更新节点的高度

    def right_rotate(self, y):
        x = y.left  # x是y的左子节点
        T2 = x.right  # T2是x的右子节点
        x.right = y  # 将y设置为x的右子节点
        y.left = T2  # 将T2设置为y的左子节点
        self.update_height(y)  # 更新y的高度
        self.update_height(x)  # 更新x的高度
        return x  # 返回新的根节点x

    def left_rotate(self, x):
        y = x.right  # y是x的右子节点
        T2 = y.left  # T2是y的左子节点
        y.left = x  # 将x设置为y的左子节点
        x.right = T2  # 将T2设置为x的右子节点
        self.update_height(x)  # 更新x的高度
        self.update_height(y)  # 更新y的高度
        return y  # 返回新的根节点y

    def insert(self, root, key):
        if not root:
            return AVLNode(key)  # 如果根节点为空，创建一个新节点

        if key < root.key:
            root.left = self.insert(root.left, key)  # 在左子树中插入
        elif key > root.key:
            root.right = self.insert(root.right, key)  # 在右子树中插入
        else:
            return root  # 不允许插入重复的键值

        self.update_height(root)  # 更新根节点的高度
        balance = self.balance_factor(root)  # 计算根节点的平衡因子

        # 左左情况
        if balance > 1 and key < root.left.key:
            return self.right_rotate(root)

        # 右右情况
        if balance < -1 and key > root.right.key:
            return self.left_rotate(root)

        # 左右情况
        if balance > 1 and key > root.left.key:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # 右左情况
        if balance < -1 and key < root.right.key:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root  # 返回根节点

    def insert_key(self, key):
        self.root = self.insert(self.root, key)  # 插入键值并更新根节点

    def in_order(self, root):
        if not root:
            return []  # 如果根节点为空，返回空列表
        return self.in_order(root.left) + [root.key] + self.in_order(root.right)  # 中序遍历

    def get_keys(self):
        return self.in_order(self.root)  # 获取所有键值

    def print_tree(self, node, level=0):
        if node is not None:
            self.print_tree(node.left, level + 1)  # 打印左子树
            print(' ' * 4 * level + '->', node.key)  # 打印当前节点
            self.print_tree(node.right, level + 1)  # 打印右子树

    def display(self):
        self.print_tree(self.root)  # 打印整棵树

    def delete_key(self, key):
        def _delete(node, key):
            if not node:
                return None  # 如果节点为空，直接返回None

            if key < node.key:
                node.left = _delete(node.left, key)  # 在左子树中删除
            elif key > node.key:
                node.right = _delete(node.right, key)  # 在右子树中删除
            else:
                # 节点只有一个子节点或没有子节点
                if not node.left:
                    return node.right
                elif not node.right:
                    return node.left
                # 节点有两个子节点
                else:
                    # 获取中序后继节点（右子树中的最小节点）
                    successor = self._get_min_value_node(node.right)
                    node.key = successor.key  # 将后继节点的键值赋给当前节点
                    node.right = _delete(node.right, successor.key)  # 删除后继节点

            if not node:
                return None

            # 更新高度
            self.update_height(node)
            balance = self.balance_factor(node)  # 计算平衡因子

            # 平衡树
            if balance > 1:
                if self.balance_factor(node.left) >= 0:
                    return self.right_rotate(node)
                else:
                    node.left = self.left_rotate(node.left)
                    return self.right_rotate(node)
            if balance < -1:
                if self.balance_factor(node.right) <= 0:
                    return self.left_rotate(node)
                else:
                    node.right = self.right_rotate(node.right)
                    return self.left_rotate(node)

            return node

        self.root = _delete(self.root, key)  # 删除键值并更新根节点

    def _get_min_value_node(self, node):
        current = node
        while current.left:
            current = current.left  # 找到最左边的节点
        return current  # 返回最小值节点