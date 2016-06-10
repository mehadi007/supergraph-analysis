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
                        superEdgeList.append((min(x, y), max(x, y),1,0,0,0))



        self.edges = sorted(superEdgeList)



    def plot(self, outpath, gdfhandle, gmlhandle, overlapsTuples):

        # in the gml file we need to print the overlaps between structures as attributes
        # Output:
        # 	edge [
	#	   source S
	#	   target T
	#	   interaction 5
	#	   normalized_interaction 0.3
	#	   overlap 4
	#	   normalized_overlap 0.7
	#	]
        
        print "Printing the graph out"
        #print overlapsTuples
        all_tuples = self.edges + overlapsTuples;
        #print all_tuples
        edge_tuples = sorted( all_tuples );
        #print edge_tuples     

        # example: [(0, 1, 0, 0.05, 1, 0.1111111111111111), (0, 2, 0, 0.03333333333333333, 2, 0.18181818181818182), (1, 2, 0, 0.041666666666666664, 0, 0.0), (1, 2, 1, 0, 0, 0), (1, 2, 1, 0, 0, 0)]

        fout = open(outpath, 'w')
        (ip, jp, wp, nwp, ovp, novp) = (-1, -1, 0, 0.0, 0, 0.0)
        (i, j) = (-1, -1)
        time = 0;
        print 'number of edges with duplicates = %.0f' % len(self.edges)
        for e in edge_tuples:
            (i, j, w, nw, ov, nov) = e
            if i == ip and j == jp:
                wp += w;
                nwp += nw;
                ovp += ov;
                novp += nov;
            else:
                if time != 0 :
                    if wp > 0 :
                        fout.write('%.0f,' % (ip + 1) + '%.0f' % (jp + 1) + ',%.0f,' % wp + '%.3f\n' % (wp * nwp))
                        gdfhandle.write('%.0f,' % (ip + 1) + '%.0f' % (jp + 1) + ',%.0f,interaction\n' % wp)
                    gmlhandle.write('\tedge [\n\t   source %.0f\n' % (ip + 1) + '\t   target %.0f\n' % (jp + 1) + '\t   weight %.0f\n' % wp);
                    gmlhandle.write('\t   norm_interaction %.3f\n' % (wp * nwp)  + '\t   overlap %.0f\n' % ovp + '\t   norm_overlap %.3f\n' % float(novp));
                    gmlhandle.write('\t]\n');
                (ip, jp, wp, nwp, ovp, novp) = (i, j, w, nw, ov, nov);
            time += 1;

        if i == ip and j == jp:
            if wp > 0 :
                fout.write('%.0f' % (ip + 1) + ',%.0f' % (jp + 1) + ',%.0f,' % wp + '%.3f\n' % (wp * nwp))
                gdfhandle.write('%.0f' % (ip + 1) + ',%.0f' % (jp + 1) + ',%.0f,interaction\n' % wp)
            gmlhandle.write('\tedge [\n\t   source %.0f\n' % (ip + 1) + '\t   target %.0f\n' % (jp + 1) + '\t   weight %.0f\n' % wp);
            gmlhandle.write('\t   weight %.3f\n' % (wp * nwp)  + '\t   overlap %.0f\n' % ovp + '\t   norm_overlap %.3f\n' % float(novp));
            gmlhandle.write('\t]\n');
        fout.close()
        print 'SuperGraph edges printed out'




    def plotOld(self, outpath, gdfhandle):

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




