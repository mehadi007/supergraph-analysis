# 2014.06.19 01:17:49 EDT

class Graph:
    numNodes = 0
    numEdges = 0
    edges = []

    def __init__(self):
        self.numNodes = 0
        self.numEdges = 0
        self.edges = [frozenset()]



    def hasEdge(self, i, j):
        return max(i, j) - 1 in self.edges[(min(i, j) - 1)]



    def load(self, fullpath):
        fg = open(fullpath)
        self.edges = []
        edgeList = []
        for line in fg:
            tmp = line.strip().split(',')
            if len(tmp) < 2:
                continue
            i = int(tmp[0])
            j = int(tmp[1])
            if i > self.numNodes:
                self.numNodes = i
            if j > self.numNodes:
                self.numNodes = j
            edgeList.append((min(i, j), max(i, j)))

        tmpAdj = [ set() for i in range(self.numNodes) ]
        for edge in edgeList:
            (i, j,) = edge
            if j - 1 not in tmpAdj[(i - 1)]:
                tmpAdj[(i - 1)].add(j - 1)
                self.numEdges += 1

        self.edges = [ frozenset(x) for x in tmpAdj ]
        return edgeList



    def plot(self):
        for idx in range(len(self.edges)):
            mystr = ''.join([ '.' for x in range(0, idx + 1) ])
            for idy in range(idx + 1, len(self.edges)):
                if idy in self.edges[idx]:
                    mystr += '1'
                else:
                    mystr += '0'

            print mystr





