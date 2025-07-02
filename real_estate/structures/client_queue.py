class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class ClientQueue:
    def __init__(self):
        self.front = None
        self.rear = None
        self._size = 0

    def enqueue(self, client):
        # 检查队列中是否已经存在相同的客户端
        current = self.front
        while current:
            if current.data.client_ID == client.client_ID:
                return  # 如果存在相同的客户端，不添加
            current = current.next

        new_node = Node(client)
        if not self.rear:
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        self._size += 1

    def size(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def dequeue(self):
        if self.is_empty():
            return None
        data = self.front.data
        self.front = self.front.next
        if not self.front:
            self.rear = None
        self._size -= 1
        return data

    def __contains__(self, client):
        current = self.front
        while current:
            if current.data.client_ID == client.client_ID:
                return True
            current = current.next
        return False
    
    def move_front_to_rear(self):
        if self.is_empty():
            return
        node = self.dequeue()
        self.enqueue(node)

    
    def peek(self):
        if not self.is_empty():
            return self.front.data
        return None
    
    def to_list(self):
        """将队列中的所有客户转换为列表"""
        clients = []
        current = self.front
        while current:
            clients.append(current.data)
            current = current.next
        return clients
    