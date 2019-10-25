import numpy as np

from entities import Lesson


class State:

    def __init__(self, sumTmimata):
        self.array = np.zeros((sumTmimata, 5, 7), dtype=object)

    def setXYZ(self, x, y, z, data):
        self.array[x][y][z] = data

    def out(self):
        print(self.array)

    def specificOut(self, x, y, z):
        return self.array[x][y][z]


class Node:

    def __init__(self, state, parent):
        self.children = []
        self.parent = parent
        self.state = state

    def addChild(self, node):
        self.children.append(node)

    def calculateWeights(self):
        for child in self.children:
            print(':)')
