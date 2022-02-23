import json
import math

ENERGYLIMIT =  287932

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

def worthRevisit(dist, energy, costlist):
  for costpair in costlist:
    if dist >= costpair[0] and energy >= costpair[1]:
      return False
  return True

def astar(coords, cost, dist, g):
  queue = []
  visited = dict()

  startNode = Node("1", coords["1"])
  endNode = Node("50", coords["50"])

  queue.append(startNode)
  visited["1"] = [[0,0]]

  while queue:
    queue.sort(key=lambda x: (x.f))
    currentNode = queue.pop(0)

    if currentNode.idx == '2465' or currentNode.idx == '2369':
      print(currentNode.idx)
      print(currentNode.parent.idx)
      print(currentNode.f)
      print(currentNode.energy)
      print()

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
      #validation
      energycost = float(cost[currentNode.idx + ',' + neighboridx])
      totalenergy = float(currentNode.energy + energycost)
      distcost = float(dist[currentNode.idx + ',' + neighboridx])
      totaldist = float(currentNode.g + distcost)
      if totalenergy > ENERGYLIMIT:
        continue

      if neighboridx in visited:
        visitedcosts = visited[neighboridx]
        if not worthRevisit(distcost, energycost, visitedcosts):
          continue
        visited[neighboridx].append([distcost, energycost])
      else:
        visited[neighboridx] = [[distcost, energycost]]

      #build node
      newNode = Node(neighboridx, coords[neighboridx])
      newNode.parent = currentNode
      newNode.distCost = distcost
      newNode.energyCost = energycost
      newNode.g = totaldist
      newNode.h = 0.0
      newNode.updatef()
      newNode.energy = totalenergy

      queue.append(newNode)
      
path, totalcost, totaldist = astar(coords, cost, dist, g)
print(path)

# print(totalcost)
# print(totaldist)