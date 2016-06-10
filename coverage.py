from graph import Graph;

import collections

class Coverage :
    numNodes = 0;
    numEdges = 0;

    # number of edges covered by M
    numCellsCovered = 0;
    covered = [];

    
    def __init__(self, graph):
        self.numNodes = graph.numNodes;
        self.numEdges = graph.numEdges;

        # i want to compute number of edges that are covered multiple times
        self.covered = [list() for i in range(self.numNodes)];
        self.numCellsCovered = 0;

        
    # annotates edge (i,j) as covered
    # ! (i,j) does not have to be in E of G(V,E)
    def cover(self, i, j) :
        self.covered[min(i,j)-1].append(max(i,j)-1);
        self.numCellsCovered += 1;
        return;
 

    # return how many times each edge is covered
    def printCoverage(self):
       print "covered / total: %.0f / %.0f" % (self.numCellsCovered, self.numEdges);
       for i in range(0, self.numNodes-1):
           counter = collections.Counter(self.covered[i])
           if len(list(counter)) > 0:
               z = (counter.most_common(1))[0]; # get the counter of the most common element
               (x, y) = z
               if y > 1:
                   print "%.0f: %s" % (i,counter.most_common(10));
