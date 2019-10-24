class Node:

    def __init__(self, data):
        self.children = []
        self.data = data

    def addChild(self, node):
        self.children.append(node)


class Tree:

    def __init__(self):
        self.head = "None"
        self.size = 0

    def add(self, node):
        if self.size == 0:
            self.head = node
        else:
            # magic stuff
            print()

