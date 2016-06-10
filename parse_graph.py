#!/usr/local/bin/python2.6

#########################################################################
#                                                                       #
# Supergraph creation:                                                  #
#  -each vog structure becomes a supernode                              #
#  -the number of nodes between nodes withing a supernode corresponds   #
#   to the weight of the superedges                                     #
#                                                                       #
#  Author: Danai Kouta                                                  #
#                                                                       #
# --------------------------------------------------------------------- #
# Based on the method:                                                  #
# VOG: Summarizing and Understanding Large Graphs                       #
# by Danai Koutra, U Kang, Jilles Vreeken, Christos Faloutsos           #
# http://www.cs.cmu.edu/~dkoutra/papers/VoG.pdf                         #
#                                                                       #
#########################################################################


import sys
import os
import config

from time import time

from graph import Graph;
from supergraph import SuperGraph;
from model import Model;
from coverage import Coverage;
import evaluation as entropy

print len(sys.argv)

if len(sys.argv) <= 1 :
    print 'at least: <graph.graph> <model.model> <output folder> [selected_lines_from_model.txt] [costs of models]';
    print ' optional argument selected_lines = file with the model structures (line numbers) in the created summary. Otherwise all the structures in the given model are considered.';
    print ' optional argument model_costs = file with the (iterative) costs of the created summary.';
    print ' optional argument -vX    = verbosity (1, 2, or 3)';
    print ' optional argument -pG    = plot Graph adjacency matrix';
    exit();

if (len(sys.argv) > 2 and ("-v1" in sys.argv)) :
    config.optVerbosity = 1;
elif (len(sys.argv) > 2 and ("-v2" in sys.argv)) :
    config.optVerbosity = 2;
if (len(sys.argv) > 2 and ("-v3" in sys.argv)) :
    config.optVerbosity = 3;

t0 = time()

gFilename = sys.argv[1];
g = Graph();
edgeList = g.load(gFilename);
if config.optVerbosity > 1 : print "- graph loaded."

m = Model(g.numNodes);

c = Coverage(g);

if len(sys.argv) > 2 and sys.argv[2][0] != '-' :
    mFilename = sys.argv[2];
    mOutFolder = sys.argv[3];
    mFilename_list = mFilename.split('/');
    mFilename_main = mFilename_list[len(mFilename_list) - 1];
    mFilename_mainNameList = mFilename_main.split('.');
    mFilename_mainName = mFilename_mainNameList[0];
    mAttrpath = mOutFolder + '/superNodes_attributes_' + mFilename_main;
    gdfpath =  mOutFolder + '/gephi_' + mFilename_mainName + '.gdf';
    gdfhandle = open(gdfpath, 'w');
    gmlpath =  mOutFolder + '/gml_' + mFilename_mainName + '.gml';
    gmlhandle = open(gmlpath, 'w');
    augmentedModelpath =  mOutFolder + '/augmentedModel_' + mFilename_mainName + '.model';
    augmentedModelhandle = open(augmentedModelpath, 'w');
    
    gmlhandle.write('graph [\n');
    gmlhandle.write('\tcomment "This is the %s graph"\n' % mFilename_mainName);
    gmlhandle.write('\tdirected 0\n');

    linesSelected = [];
    # node header for gdf file
    gdfhandle.write("nodedef>name INT,type VARCHAR,size INT\n")
    #if len(sys.argv) > 3 :
    if len(sys.argv) == 3 :
       m.load(mFilename, mAttrpath, gdfhandle, gmlhandle,c,g, augmentedModelhandle);
    else :  # 4, we have to select the structures that belong to the model
       linesFilename = sys.argv[4];
       with open(linesFilename) as f:
          linesSelected = [int(line.rstrip()) for line in f]
      # print linesSelected
       if linesSelected :   # if the list of structures is non-empty
          m.loadLines(mFilename, linesSelected, mAttrpath, gdfhandle, gmlhandle,c,g, augmentedModelhandle)
    print "Number of structures in the model: %.0f" % m.numStructs;
    if config.optVerbosity > 1 : print "- M_x loaded."
    
    if m.numStructs < 100000 :
       mOverlappath =  mOutFolder + '/superNodes_overlap_' + mFilename_main;
       mFullInfopath =  mOutFolder + '/superNodes_fullOverlapInfo_' + mFilename_main;
       m.findOverlaps(mOverlappath, mFullInfopath, gdfhandle, augmentedModelhandle);
    
       # edge header for gdf file
       gdfhandle.write("edgedef>source INT,target INT,weight INT,type VARCHAR\n")
       sg = SuperGraph(m.numStructs);
       sg.createSuperEdges(edgeList, m.memberships);
       mGraphpath = mOutFolder + '/superGraph_' + mFilename_main;
       sg.plot(mGraphpath, gdfhandle, gmlhandle, m.overlapsList);

       gmlhandle.write(']\n');

    # Read the encoding costs
    emptyModelCost = -1;
    finalModelCost = -1;
    if linesSelected:  # obtain the costs only if the model file is not empty
       if len(sys.argv) > 4:
          costsFilename = sys.argv[5];
          with open(costsFilename, "rb") as f:
             first = f.readline()     # Read the first line.
             f.seek(-2, 2)            # Jump to the second last byte.
             while f.read(1) != "\n": # Until EOL is found...
                f.seek(-2, 1)        # ...jump back the read byte plus one more.
             last = f.readline()      # Read last line.
          if first:  # if not empty string
             emptyModelCost = int(first.split(' ')[-1].rstrip()); # Get the cost of the empty model from the first line
          if last:   # if not empty string
             finalModelCost = int(last.split('\t')[-1].rstrip());  # Get the final cost of the selected model
       

    # Find statistics about the summaries
    print "Total\tfc\tst\tbc\tch\tnc\tnb\tEmpty\tModel\tPercent"
    print "%.0f\t%.0f\t%.0f\t%.0f\t%.0f\t%.0f\t%.0f\t%.0f\t%.0f\t%.2f%%\n" % (m.numStructs, m.numFullCliques, m.numStars, m.numBiPartiteCores, m.numChains, m.numNearCliques, m.numNearBiPartiteCores, emptyModelCost, finalModelCost, 100.0*finalModelCost/emptyModelCost)

# Compute print entropy
structEntropy = entropy.entropy_single([m.numStructs, m.numFullCliques, m.numStars, m.numBiPartiteCores, m.numChains])
print 'Entropy over structure type: ' + str(structEntropy)

print time()-t0    
print "Total running time %.2f" % (time()-t0);

gdfhandle.close()
gmlhandle.close()

c.printCoverage();
