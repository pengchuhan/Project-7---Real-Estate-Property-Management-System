class AVLNode:
    def __init__(self, key, property_obj):
        self.key = key  # (price, property_id)
        self.property = property_obj
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None

    def height(self, node):
        return node.height if node else 0

    def balance_factor(self, node):
        return self.height(node.left) - self.height(node.right) if node else 0

    def update_height(self, node):
        node.height = max(self.height(node.left), self.height(node.right)) + 1

    def right_rotate(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        self.update_height(y)
        self.update_height(x)
        return x

    def left_rotate(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        self.update_height(x)
        self.update_height(y)
        return y

    def insert(self, node, key, property_obj):
        if not node:
            return AVLNode(key, property_obj)

        if key < node.key:
            node.left = self.insert(node.left, key, property_obj)
        elif key > node.key:
            node.right = self.insert(node.right, key, property_obj)
        else:
            # 已有完全相同key，不允许插入，或者根据需求处理
            return node

        self.update_height(node)

        balance = self.balance_factor(node)

        # 左左
        if balance > 1 and key < node.left.key:
            return self.right_rotate(node)

        # 右右
        if balance < -1 and key > node.right.key:
            return self.left_rotate(node)

        # 左右
        if balance > 1 and key > node.left.key:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # 右左
        if balance < -1 and key < node.right.key:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def insert_key(self, key, property_obj):
        self.root = self.insert(self.root, key, property_obj)

    def _get_min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def delete(self, node, key):
        if not node:
            return node

        if key < node.key:
            node.left = self.delete(node.left, key)
        elif key > node.key:
            node.right = self.delete(node.right, key)
        else:
            # 找到节点，删除
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            else:
                successor = self._get_min_value_node(node.right)
                node.key = successor.key
                node.property = successor.property
                node.right = self.delete(node.right, successor.key)

        self.update_height(node)
        balance = self.balance_factor(node)

        # 平衡调整
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

    def delete_key(self, key):
        self.root = self.delete(self.root, key)

    # 按 property_id 查找节点 (递归遍历)
    def find_by_id(self, property_id):
        return self._find_by_id(self.root, property_id)

    def _find_by_id(self, node, property_id):
        if not node:
            return None
        if node.property.property_ID == property_id:
            return node
        left_res = self._find_by_id(node.left, property_id)
        if left_res:
            return left_res
        return self._find_by_id(node.right, property_id)

    # 根据 price 范围搜索
    def search_by_price_range(self, min_price, max_price):
        results = []
        self._search_inorder(self.root, min_price, max_price, results)
        return results

    def _search_inorder(self, node, min_price, max_price, results):
        if not node:
            return
        price = node.key
        if price >= min_price:
            self._search_inorder(node.left, min_price, max_price, results)
        if min_price <= price <= max_price:
            results.append(node.property)
        if price <= max_price:
            self._search_inorder(node.right, min_price, max_price, results)
    
    def display_horizontal(self, node=None, level=0):
        if node is None:
            node = self.root
            if node is None:
                print("(Empty Tree)")
                return

        if node.right:
            self.display_horizontal(node.right, level + 1)

        print('    ' * level + f'-> {node.key}')

        if node.left:
            self.display_horizontal(node.left, level + 1)
    
    def size(self):
        def count_nodes(node):
            if not node:
                return 0
            return 1 + count_nodes(node.left) + count_nodes(node.right)
        return count_nodes(self.root)

    def get_keys(self):
        keys = []
        def inorder(node):
            if not node:
                return
            inorder(node.left)
            keys.append(node.property.property_ID)
            inorder(node.right)
        inorder(self.root)
        return keys