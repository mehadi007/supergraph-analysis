from model import Model;

# 2014.06.19 01:18:18 EDT

class SuperGraph:
    numNodes = 0
    numEdges = 0
    edges = []

    def __init__(self, numStructs):
        self.numNodes = numStructs
        self.numEdges = 0
        self.edges = []



    def hasEdge(self, i, j):
        return max(i, j) - 1 in self.edges[(min(i, j) - 1)]



    def createSuperEdges(self, edgeList, membership):
        superEdgeList = []
        for edge in edgeList:
            (i, j,) = edge
            for x in membership[(i - 1)]:
                for y in membership[(j - 1)]:
                    if x != y and y not in membership[(i - 1)] and x not in membership[(j - 1)]:
                        superEdgeList.append((min(x, y), max(x, y)))



        self.edges = sorted(superEdgeList)



    def plot(self, outpath, gdfhandle, gmlhandle):

        # in the gml file we need to print the overlaps between structures as attributes
        # Output:
        # 	edge [
	#	   source S
	#	   target T
	#	   interaction 5
	#	   overlap 4
	#	   interactionPercent 0.3
	#	   overlapPercent 0.7
	#	]
        
        fout = open(outpath, 'w')
        (ip, jp,) = (-1, -1)
        (i, j,) = (-1, -1)
        w = 1
        print 'number of edges with duplicates = %.0f' % len(self.edges)
        for e in self.edges:
            (i, j,) = e
            if i == ip and j == jp:
                w += 1
            else:
                if ip != -1:
                    fout.write('%.0f,' % (ip + 1) + '%.0f' % (jp + 1) + ',%.0f\n' % w)
                    gdfhandle.write('%.0f,' % (ip + 1) + '%.0f' % (jp + 1) + ',%.0f,interaction\n' % w)
                    w = 1
                (ip, jp,) = (i, j)

        if i == ip and j == jp:
            fout.write('%.0f' % (ip + 1) + ',%.0f' % (jp + 1) + ',%.0f\n' % w)
            gdfhandle.write('%.0f' % (ip + 1) + ',%.0f' % (jp + 1) + ',%.0f,interaction\n' % w)
        fout.close()
        print 'SuperGraph edges printed out'




