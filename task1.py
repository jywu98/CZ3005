import json
import math
import heapq
import time

with open('Coord.json') as json_file:
    coords = json.load(json_file)
with open('Cost.json') as json_file:
    cost = json.load(json_file)
with open('Dist.json') as json_file:
    dist = json.load(json_file)
with open('G.json') as json_file:
    g = json.load(json_file)


class Node:
    def __init__(self, idx, coord):
        self.parent = None
        self.idx = idx
        self.x = coord[0]
        self.y = coord[1]

        self.distCost = 0.0
        self.energyCost = 0.0

        self.h = 0.0
        self.g = 0.0
        self.f = 0.0
        self.energy = 0.0

    def updatef(self):
        self.f = self.g + self.h

def worthRevisit(dist, costlist):
    for costpair in costlist:
        if dist >= costpair[0]:
            return False
    return True

class MyHeap(object):
    def __init__(self, initial=None, key=lambda x: x.f):
        self.key = key
        self.index = 0
        if initial:
            self._data = [(key(item), i, item)
                          for i, item in enumerate(initial)]
            self.index = len(self._data)
            heapq.heapify(self._data)
        else:
            self._data = []

    def push(self, item):
        heapq.heappush(self._data, (self.key(item), self.index, item))
        self.index += 1

    def pop(self):
        return heapq.heappop(self._data)[2]


def astar(coords, cost, dist, g):
    visited = dict()

    startNode = Node("1", coords["1"])
    endNode = Node("50", coords["50"])

    heap = MyHeap([startNode])
    visited["1"] = [[0]]

    while heap:
        currentNode = heap.pop()

        if currentNode.idx == endNode.idx:
            print("Path found.")
            totalcost = currentNode.energy
            totaldist = currentNode.g
            path = []

            current = currentNode
            while current.parent is not None:
                path.append(current.idx)
                current = current.parent
            path.append(current.idx)
            return path[::-1], totalcost, totaldist

        neighbors = g[currentNode.idx]
        for neighboridx in neighbors:
            # validation
            energycost = float(cost[currentNode.idx + ',' + neighboridx])
            totalenergy = float(currentNode.energy + energycost)
            distcost = float(dist[currentNode.idx + ',' + neighboridx])
            totaldist = float(currentNode.g + distcost)

            if neighboridx in visited:
                visitedcosts = visited[neighboridx]
                if not worthRevisit(totaldist, visitedcosts):
                    continue
                visited[neighboridx].append([totaldist])
            else:
                visited[neighboridx] = [[totaldist]]

            # build node
            newNode = Node(neighboridx, coords[neighboridx])
            newNode.parent = currentNode
            newNode.distCost = distcost
            newNode.energyCost = energycost
            newNode.g = totaldist
            newNode.h = 0.0
            newNode.updatef()
            newNode.energy = totalenergy

            heap.push(newNode)

start = time.time()
path, totalcost, totaldist = astar(coords, cost, dist, g)
end = time.time()
print(path)
print("time taken " + str(end - start))
print("totalcost: " + str(totalcost))
print("totaldist: " + str(totaldist))