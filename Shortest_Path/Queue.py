from env import *

class Queue:
    """
    Queue for BFS
    """
    def __init__(self):
        self.nodes = []
        self.frontier = set()

    def __eq__(self, other):
        return self.nodes == other.nodes
    
    def empty(self):
        return len(self.nodes) == 0

    def add(self, node:Node):
        """
        adding node to queue

        node: node to be added --> Node
        """
        if not isinstance(node, Node):
            raise TypeError("Insert object should be a Node instance")
        self.nodes.append(node)
    
    def remove(self):
        if self.empty():
            raise ValueError("Empty queue")
        node = self.nodes[0]
        self.nodes = self.nodes[1:]
        return node