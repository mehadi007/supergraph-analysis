# 2014.06.19 01:19:46 EDT
import os
import sys
from graph import *
from collections import namedtuple
from mdl_structs import *

class Model:
    strucTypes = []
    numStrucTypes = 0
    structs = []
    numStructs = 0
    structSizeList = []
    uncoveredNodes = []
    coveredNodes = []
    graphNodes = 0
    overlapsList = []
    memberships = []
    numFullCliques = 0
    numNearCliques = 0
    numFullOffDiagonals = 0
    numNearOffDiagonals = 0
    numChains = 0
    numStars = 0
    numBiPartiteCores = 0
    numNearBiPartiteCores = 0
    numCorePeripheries = 0
    numJellyFishes = 0

    def __init__(self, graphNodes):
        self.strucTypes = ['fc',
         'nc',
         'ch',
         'st',
         'bc',
         'nb']
        self.numStrucTypes = len(self.strucTypes)
        self.structs = []
        self.numStructs = 0
        self.graphNodes = graphNodes
        self.structSizeList = [ set() for i in range(graphNodes) ]
        self.uncoveredNodes = [ i for i in range(graphNodes) ]
        self.coveredNodes = []
        self.memberships = [ set() for i in range(graphNodes) ]
        self.overlapsList = [];



    def findUncoveredNodes(self):
        allNodes = [ i + 1 for i in range(self.graphNodes) ]
        setUncovered = set(allNodes).difference(set(self.coveredNodes))
        self.uncoveredNodes = list(setUncovered)



    def createNoiseSuperNode(self, idx):
        self.findUncoveredNodes()
        print 'total nodes: %.0f' % self.graphNodes
        print 'uncovered nodes: %.0f' % len(self.uncoveredNodes)
        for i in self.uncoveredNodes:
            self.memberships[(i - 1)].add(idx)




    def findOverlaps(self, outpath, fullInfopath, gdfHandle, augmented_model):
        mHandle = open(outpath, 'w')
        mHandleFull = open(fullInfopath, 'w')
        OV = namedtuple('OV', ['s1', 's2', 'nodeOverlap'])
        mHandle.write('Supernode_1,Supernode_2,Overall_Node_Overlap\n')
        mHandleFull.write('SuperNode_1\t\tSuperNode_2\t\tNode Overlap Breakdown\t\tNormalized Overlap\n')
        mHandleFull.write('Type Index (size)\tType Index (size)\n')
        for struc1 in self.structs:
            for struc2 in self.structs:
                if struc1.idx < struc2.idx:
                    overlap = self.computeOverlaps(struc1, struc2)
                    ov = OV(s1=struc1.idx, s2=struc2.idx, nodeOverlap=overlap)
                    # create tuples of the form (source, 
                    #                            destination, 
                    #                            weight=0, 
                    #                            normalized_weight = 1/( (struct1.numNodes) * (struct2.numNodes-overall_overlap)), 
                    #                            overlap_overall, 
                    #                            normalized_overlap = overlap_overall / (struct1.numNodes + struct2.numNodes)
                    #                           )
                    if (struc1.numNodes-overlap[0]) * (struc2.numNodes-overlap[0]) != 0 :
                        #self.overlapsList.append((struc1.idx, struc2.idx, 0, 1.0/((struc1.numNodes) * (struc2.numNodes-overlap[0])), overlap[0], float(overlap[0])/min(struc1.numNodes, struc2.numNodes)));
                        # change to jaccard similarity
                        self.overlapsList.append((struc1.idx, struc2.idx, 0, 1.0/((struc1.numNodes) * (struc2.numNodes-overlap[0])), overlap[0], float(overlap[0])/(struc1.numNodes + struc2.numNodes - overlap[0])));
                    else :
                        #self.overlapsList.append((struc1.idx, struc2.idx, 0, 1.0, overlap[0], float(overlap[0])/min(struc1.numNodes, struc2.numNodes)));
                        # change to jaccard similarity
                        self.overlapsList.append((struc1.idx, struc2.idx, 0, 1.0, overlap[0], float(overlap[0])/(struc1.numNodes + struc2.numNodes - overlap[0])));
                    #print self.overlapsList
                    if ov.nodeOverlap[0] > 0:
                        stringOverlap = ','.join(map(str, ov.nodeOverlap))
                        #mHandleFull.write('%s' % struc1.typeS + ' %.0f' % (struc1.idx + 1) + ' (%.0f)' % struc1.numNodes + '\t\t%s' % struc2.typeS + ' %.0f' % (struc2.idx + 1) + ' (%.0f)' % struc2.numNodes + '\t\t%s' % stringOverlap + '\t\t\t\t%.3f' % (float(overlap[0])/(min(struc1.numNodes,struc2.numNodes))))
                        # change to jaccard similarity
                        mHandleFull.write('%s' % struc1.typeS + ' %.0f' % (struc1.idx + 1) + ' (%.0f)' % struc1.numNodes + '\t\t%s' % struc2.typeS + ' %.0f' % (struc2.idx + 1) + ' (%.0f)' % struc2.numNodes + '\t\t%s' % stringOverlap + '\t\t\t\t%.3f' % (float(overlap[0])/((struc1.numNodes + struc2.numNodes - overlap[0]))))
                        mHandleFull.write('\n')
                        mHandle.write('%.0f,' % (struc1.idx + 1) + '%.0f' % (struc2.idx + 1) + ',%.0f' % ov.nodeOverlap[0] + '\n')
                        gdfHandle.write('%.0f,' % (struc1.idx + 1) + '%.0f' % (struc2.idx + 1) + ',%.0f' % ov.nodeOverlap[0] + ',nodeOverlap\n')
                    #if (float(overlap[0])/(min(struc1.numNodes,struc2.numNodes))) > 0.1:
                    # change to jaccard similarity
                    if (float(overlap[0])/((struc1.numNodes + struc2.numNodes - overlap[0]))) > 0.1:
                        self.outputMoreCandidates(struc1, struc2, augmented_model);

        mHandle.close()
        mHandleFull.close()


    def computeOverlaps(self, struct1, struct2):
        if struct1.typeS in [FullClique.getType(), NearClique.getType(), Chain.getType()] and struct2.typeS in [FullClique.getType(), NearClique.getType(), Chain.getType()]:
            overlap = [len(list(set(struct1.nodes) & set(struct2.nodes)))]
        elif struct1.typeS == Star.getType():
            if struct2.typeS in [FullClique.getType(), NearClique.getType(), Chain.getType()]:
                overlap_total = len(list(set(struct1.nodes) & set(struct2.nodes)))
                overlap_hub_nodes = len(list(set([struct1.cNode]) & set(struct2.nodes)))
                overlap = [overlap_total, overlap_hub_nodes]
            elif struct2.typeS == Star.getType():
                overlap_total = len(list(set(struct1.nodes) & set(struct2.nodes)))
                overlap_hub_spokes = len(list(set([struct1.cNode]) & set(struct2.sNodes)))
                overlap_spokes_hub = len(list(set(struct1.sNodes) & set([struct2.cNode])))
                overlap = [overlap_total, overlap_hub_spokes, overlap_spokes_hub]
            elif struct2.typeS in [BiPartiteCore.getType(), NearBiPartiteCore.getType()]:
                overlap_total = len(list(set(struct1.nodes) & set(struct2.nodes)))
                overlap_hub_left = len(list(set([struct1.cNode]) & set(struct2.lNodes)))
                overlap_hub_right = len(list(set([struct1.cNode]) & set(struct2.rNodes)))
                overlap_spokes_left = len(list(set(struct1.sNodes) & set(struct2.lNodes)))
                overlap_spokes_right = len(list(set(struct1.sNodes) & set(struct2.rNodes)))
                overlap = [overlap_total,
                 overlap_hub_left,
                 overlap_hub_right,
                 overlap_spokes_left,
                 overlap_spokes_right]
        elif struct2.typeS == Star.getType():
            if struct1.typeS in [FullClique.getType(), NearClique.getType(), Chain.getType()]:
                overlap_total = len(list(set(struct2.nodes) & set(struct1.nodes)))
                overlap_hub_nodes = len(list(set([struct2.cNode]) & set(struct1.nodes)))
                overlap = [overlap_total, overlap_hub_nodes]
            elif struct1.typeS in [BiPartiteCore.getType(), NearBiPartiteCore.getType()]:
                overlap_total = len(list(set(struct2.nodes) & set(struct1.nodes)))
                overlap_hub_left = len(list(set([struct2.cNode]) & set(struct1.lNodes)))
                overlap_hub_right = len(list(set([struct2.cNode]) & set(struct1.rNodes)))
                overlap_spokes_left = len(list(set(struct2.sNodes) & set(struct1.lNodes)))
                overlap_spokes_right = len(list(set(struct2.sNodes) & set(struct1.rNodes)))
                overlap = [overlap_total,
                 overlap_hub_left,
                 overlap_hub_right,
                 overlap_spokes_left,
                 overlap_spokes_right]
        elif struct1.typeS in [BiPartiteCore.getType(), NearBiPartiteCore.getType()] and struct2.typeS in [FullClique.getType(), NearClique.getType(), Chain.getType()]:
            overlap_total = len(list(set(struct1.nodes) & set(struct2.nodes)))
            overlap_left_nodes = len(list(set(struct1.lNodes) & set(struct2.nodes)))
            overlap_right_nodes = len(list(set(struct1.rNodes) & set(struct2.nodes)))
            overlap = [overlap_total, overlap_left_nodes, overlap_right_nodes]
        elif struct2.typeS in [BiPartiteCore.getType(), NearBiPartiteCore.getType()] and struct1.typeS in [FullClique.getType(), NearClique.getType(), Chain.getType()]:
            overlap_total = len(list(set(struct1.nodes) & set(struct2.nodes)))
            overlap_left_nodes = len(list(set(struct2.lNodes) & set(struct1.nodes)))
            overlap_right_nodes = len(list(set(struct2.rNodes) & set(struct1.nodes)))
            overlap = [overlap_total, overlap_left_nodes, overlap_right_nodes]
        elif struct1.typeS in [BiPartiteCore.getType(), NearBiPartiteCore.getType()] and struct2.typeS in [BiPartiteCore.getType(), NearBiPartiteCore.getType()]:
            overlap_total = len(list(set(struct1.nodes) & set(struct2.nodes)))
            overlap_left_left = len(list(set(struct1.lNodes) & set(struct2.lNodes)))
            overlap_left_right = len(list(set(struct1.lNodes) & set(struct2.rNodes)))
            overlap_right_left = len(list(set(struct1.rNodes) & set(struct2.lNodes)))
            overlap_right_right = len(list(set(struct1.rNodes) & set(struct2.rNodes)))
            overlap = [overlap_total,
             overlap_left_left,
             overlap_left_right,
             overlap_right_left,
             overlap_right_right]
        return overlap

    def outputMoreCandidates(self, struct1, struct2, augmented_model):
        # reorder the structures
        if struct2.typeS == FullClique.getType():
            if struct1.typeS != FullClique.getType():
                temp = struct1;
                struct1 = struct2;
                struct2 = temp;
        elif struct2.typeS == Star.getType():
            if struct1.typeS != Star.getType():
                temp = struct1;
                struct1 = struct2;
                struct2 = temp;
        elif struct2.typeS == BiPartiteCore.getType():
            if struct1.typeS != BiPartiteCore.getType():
                temp = struct1;
                struct1 = struct2;
                struct2 = temp;

        if struct1.typeS == FullClique.getType() and struct2.typeS == FullClique.getType():
            # print out the minimal envelope: AUB
            #augmented_model.write("fc-fc 1: AUB\n");
            augmented_model.write("fc ");
            for s in sorted(list(set(struct1.nodes) | set(struct2.nodes))):
                augmented_model.write("%.0f " % s); 
            augmented_model.write("\n");
            
           # print out A-B
            #augmented_model.write("fc-fc 2: A-B\n");
            aList = sorted(list(set(struct1.nodes) - set(struct2.nodes)));
            if len(aList) > 2:
                augmented_model.write("fc ");
                for s in aList:
                    augmented_model.write("%.0f " % s); 
                augmented_model.write("\n");

            # print out B-A
            #augmented_model.write("fc-fc 3: B-A\n");
            aList = sorted(list(set(struct2.nodes) - set(struct1.nodes)));
            if len(aList) > 2:
               augmented_model.write("fc ");
               for s in aList:
                   augmented_model.write("%.0f " % s); 
               augmented_model.write("\n");

            # print out A and B
            #augmented_model.write("fc-fc 4: A and B\n");
            augmented_model.write("fc ");
            for s in sorted(list(set(struct1.nodes) & set(struct2.nodes))):
                augmented_model.write("%.0f " % s); 
            augmented_model.write("\n");

        elif struct1.typeS == FullClique.getType() and struct2.typeS == BiPartiteCore.getType():
            # print out the minimal envelope: AUB
            #augmented_model.write("fc-bc 1: AUB\n");
            augmented_model.write("fc ");
            for s in sorted(list(set(struct1.nodes) | set(struct2.lNodes) | set(struct2.rNodes) )):
                augmented_model.write("%.0f " % s); 
            augmented_model.write("\n");

            # print A and B as fc
            #augmented_model.write("fc-bc 2: A and B as fc\n");
            augmented_model.write("fc ");
            for s in sorted(list(set(struct1.nodes) & (set(struct2.lNodes) | set(struct2.rNodes)) )):
                augmented_model.write("%.0f " % s); 
            augmented_model.write("\n");

            # print A-B as fc
            #augmented_model.write("fc-bc 3: A-B as fc\n");
            augmented_model.write("fc ");
            for s in sorted(list(set(struct1.nodes) & (set(struct2.lNodes) | set(struct2.rNodes)) )):
                augmented_model.write("%.0f " % s); 
            augmented_model.write("\n");

            # print B-A as bc
            #augmented_model.write("fc-bc 4: B-A as fc\n");
            aList =  sorted(list(set(struct2.lNodes) - set(struct1.nodes)));
            bList = sorted(list(set(struct2.rNodes) - set(struct1.nodes)));
            if len(aList) > 1 and len(bList) > 1:
                augmented_model.write("bc ");
                for s in aList:
                    augmented_model.write("%.0f " % s); 
                augmented_model.write(",");
                for s in bList:
                    augmented_model.write("%.0f " % s); 
                augmented_model.write("\n");

        elif struct1.typeS == FullClique.getType() and struct2.typeS == Star.getType():
            # remove the spokes in the clique from the star
            #augmented_model.write("fc-st 1: remove the spokes in the clique from the star\n");
            aList = sorted(list(set(struct2.sNodes) - set(struct1.nodes)));
            if len(aList) > 1:
                augmented_model.write("st ");
                augmented_model.write("%.0f" % struct2.cNode);
                augmented_model.write(",");
                for s in aList:
                    augmented_model.write("%.0f " % s); 
                augmented_model.write("\n");

            # remove the spokes of the star from the clique
            #augmented_model.write("fc-st 2: remove the spokes of the star from the clique\n");
            aList = list(set(struct1.nodes) - set(struct2.sNodes));
            if struct2.cNode in aList:
                aList.remove(struct2.cNode);
            if len(aList) > 2:
                augmented_model.write("fc ");
                for s in sorted(aList):
                    augmented_model.write("%.0f " % s); 
                augmented_model.write("\n");

        elif struct1.typeS == FullClique.getType() and struct2.typeS == Chain.getType():
            # remove the fc nodes from the chain
            #augmented_model.write("fc-ch: remove the fc nodes from the chain\n");
            augmented_model.write("ch ");
            for x in struct2.nodes:
                if x not in struct1.nodes:
                    augmented_model.write("%.0f " % x);
            augmented_model.write('\n');

        elif struct1.typeS == Star.getType() and struct2.typeS == BiPartiteCore.getType():
            # bc without the star
            #augmented_model.write("st-bc 1: bc without the star\n");
       
            aList = list(set(struct2.lNodes) - set(struct1.sNodes));
            if struct1.cNode in aList:
                aList.remove(struct1.cNode);
            if len(aList) > 1 :
                augmented_model.write("bc ");
                for s in sorted(aList):
                    augmented_model.write("%.0f " % s); 
                augmented_model.write(",");
                bList = sorted(list(set(struct2.rNodes) - set(struct1.sNodes)));
                if struct1.cNode in bList: 
                    bList.remove(struct1.cNode);
                for s in sorted(bList):
                    augmented_model.write("%.0f " % s); 
                augmented_model.write("\n");

        elif struct1.typeS == FullClique.getType() and struct2.typeS == Star.getType():
            # minimal envelope as bc
            if len(list(set(struct1.sNodes) & set(struct2.lNodes))) > 1:
                #augmented_model.write("st-bc 2: minimal envelope as bc\n");
                augmented_model.write("bc ");
                for s in sorted(list(set(struct2.lNodes) | set(struct1.sNodes))):
                    augmented_model.write("%.0f " % s); 
                augmented_model.write(",");
                for s in sorted(list(set(struct2.rNodes) | set(struct1.cNode) )):
                    augmented_model.write("%.0f " % s); 
                augmented_model.write("\n");

            if len(list(set(struct1.sNodes) & set(struct2.rNodes))) > 1:
                #augmented_model.write("st-bc 3: minimal envelope as bc\n");
                augmented_model.write("bc ");
                for s in  sorted(list(set(struct2.lNodes) | set(struct1.cNode))):
                    augmented_model.write("%.0f " % s); 
                augmented_model.write(",");
                for s in sorted(list(set(struct2.rNodes) | set(struct1.sNodes) )):
                    augmented_model.write("%.0f " % s); 
                augmented_model.write("\n");

        elif struct1.typeS == Star.getType() and struct2.typeS == Star.getType():
            # first star without the common spokes
            aList = sorted(list(set(struct1.sNodes) - set(struct2.sNodes) ));
            if len(aList) > 2:
                #augmented_model.write("st-st: first star without the common spokes\n");
                augmented_model.write("st %.0f," % struct1.cNode);
                for s in sorted(list(set(struct1.sNodes) - set(struct2.sNodes) )):
                    augmented_model.write("%.0f " % s); 
                augmented_model.write("\n");

            # second star without the common spokes
            #augmented_model.write("st-st: second star without the common spokes\n");
            aList = sorted(list(set(struct2.sNodes) - set(struct1.sNodes) ));
            if len(aList) > 1:
                augmented_model.write("st %.0f," % struct2.cNode);
                for s in aList:
                    augmented_model.write("%.0f " % s); 
                augmented_model.write("\n");

            # common spokes and hubs as a fc
            #augmented_model.write("st-st: common spokes and hubs as a fc\n");
            if len(list(set(struct1.sNodes) &  set(struct2.sNodes))) > 1:
                aList = list(set(struct1.sNodes) &  set(struct2.sNodes)) + [struct1.cNode, struct2.cNode];
                if len(aList) > 2:
                    augmented_model.write("fc ");
                    for s in sorted(list(set(aList))):
                        augmented_model.write("%.0f " % s); 
                    augmented_model.write("\n");

            # common spokes and hubs as a bc
            #augmented_model.write("st-st: common spokes and hubs as a bc\n");
            if len(set([struct1.cNode, struct2.cNode])) == 1:
                 augmented_model.write("st %.0f," % struct1.cNode);
            else: 
                 augmented_model.write("bc");
                 for s in sorted([struct1.cNode, struct2.cNode]):
                    augmented_model.write(" %.0f" % s); 
                 augmented_model.write(",");
            for s in sorted(list(set(struct1.sNodes) | set(struct2.sNodes) )):
                augmented_model.write("%.0f " % s); 
            augmented_model.write("\n");

        elif struct1.typeS == Star.getType() and struct2.typeS == Chain.getType():
            return;
        # nothing for now
        elif struct1.typeS == BiPartiteCore.getType() and struct2.typeS == BiPartiteCore.getType():
            return;
        elif struct1.typeS == BiPartiteCore.getType() and  struct2.typeS == Chain.getType():
           # remove the bc nodes from the chain
            #augmented_model.write("bc-ch: remove the bc nodes from the chain\n");
            augmented_model.write("ch ");
            for x in struct2.nodes:
                if x not in list(set(struct1.lNodes) | set(struct1.rNodes)):
                    augmented_model.write("%.0f " % x);
            augmented_model.write('\n');
        # let's ignore this for now. We need to reorder the chains somehow...
        elif struct1.typeS == Chain.getType() and struct2.typeS == Chain.getType():
            return;
            


    def setStrucTypes(self, st):
        self.strucTypes = st
        self.numStrucTypes = len(self.strucTypes)



    def addStructure(self, struct):
        self.structs.append(struct)
        self.numStructs += 1
        if struct.getType() not in self.strucTypes:
            print 'structure type not declared'
        if struct.isFullClique():
            self.numFullCliques += 1
        elif struct.isNearClique():
            self.numNearCliques += 1
        elif struct.isChain():
            self.numChains += 1
        elif struct.isStar():
            self.numStars += 1
        elif struct.isBiPartiteCore():
            self.numBiPartiteCores += 1
        elif struct.isNearBiPartiteCore():
            self.numNearBiPartiteCores += 1
        elif struct.isCorePeriphery():
            self.numCorePeripheries += 1
        elif struct.isJellyFish():
            self.numJellyFishes += 1



    def load(self, fullpath, attrpath, gdfHandle, gmlHandle,C,G, model_augmented):
        fg = open(fullpath)
        mHandle = open(attrpath, 'w')
        idx = 0
        mHandle.write('ID,TYPE,SIZE\n')
        for line in fg:
            if len(line) < 4 or line[0] == '#':
                continue
            struct = Structure.load(line, idx, self.memberships)
            model_augmented.write(line); # printing out the input model, which will later be augmented with more structures (based on the overlaps)
            if struct != 0:
                self.addStructure(struct)
                self.coveredNodes.extend(struct.nodes)
                self.structSizeList[idx].add(struct.numNodes)
                mHandle.write('%.0f' % (idx + 1) + ',%s' % struct.typeS + ',%.0f' % struct.numNodes + '\n')
                gdfHandle.write('%.0f' % (idx + 1) + ',%s' % struct.typeS + ',%.0f' % struct.numNodes + '\n')
                gmlHandle.write('\tnode [\n\t  id %.0f' % (idx + 1) + '\n\t  label "%.0f"'  % (idx + 1)  + '\n\t  type "%s"' % struct.typeS + '\n\t  image "%s.png"' % struct.typeS + "\n\t  size %.0f\n\t]\n" % struct.numNodes); 
                if struct.isFullClique() :
                   LfullClique(struct,G,C);
                elif struct.isChain() :
                   Lchain(struct,G,C);
                elif struct.isStar() :
                   Lstar(struct,G,C);
                elif struct.isBiPartiteCore() :
                   LbiPartiteCore(struct,G,C);
            idx += 1

        self.createNoiseSuperNode(idx)
        # add the noise node
        gdfHandle.write('%.0f' % (idx + 1) + ',noise,%.0f' % len(self.uncoveredNodes) + '\n')
        gmlHandle.write('\tnode [\n\t  id %.0f' % (idx + 1) + '\n\t  label "%.0f"'  % (idx + 1)  + '\n\t  type "noise"' + '\n\t  image noise.png' + '\n\t  size %.0f\n\t]\n' % len(self.uncoveredNodes)); 
        mHandle.close()



    def loadLines(self, fullpath, lineList, attrpath, gdfHandle, gmlHandle, C,G, model_augmented):
        fg = open(fullpath)
        allStructs = [line.rstrip('/n') for line in fg]
        mHandle = open(attrpath, 'w')
        idx = 0 
        mHandle.write('ID,TYPE,SIZE\n')
        lineNo = 0
        for i in lineList:
            #lineNo = lineNo + 1
            #if lineNo > lineList[(len(lineList) - 1)]:
            #    break
            #if lineNo in lineList:
            #    if len(line) < 4 or line[0] == '#':
            #        continue
            #    struct = Structure.load(line, idx, self.memberships)
                struct = Structure.load(allStructs[i-1], idx, self.memberships)
                if struct != 0:
                    model_augmented.write(allStructs[i-1]); # printing out the input model, which will later be augmented with more structures (based on the overlaps)
                    #print allStructs[i-1]
                    self.addStructure(struct)
                    self.coveredNodes.extend(struct.nodes)
                    self.structSizeList[idx].add(struct.numNodes)
                    mHandle.write('%.0f' % (idx + 1) + ',%s' % struct.typeS + ',%.0f' % struct.numNodes + '\n')
                    gdfHandle.write('%.0f' % (idx + 1) + ',%s' % struct.typeS + ',%.0f' % struct.numNodes + '\n')
                    gmlHandle.write('\tnode [\n\t  id %.0f' % (idx + 1) + '\n\t  label "%.0f"'  % (idx + 1)  + '\n\t  type "%s"' % struct.typeS + '\n\t  image "%s.png"' % struct.typeS + "\n\t  size %.0f\n\t]\n" % struct.numNodes); 
                if struct.isFullClique() :
                   LfullClique(struct,G,C);
                elif struct.isChain() :
                   Lchain(struct,G,C);
                elif struct.isStar() :
                   Lstar(struct,G,C);
                elif struct.isBiPartiteCore() :
                   LbiPartiteCore(struct,G,C);

                idx += 1; 

        self.createNoiseSuperNode(idx)
        # add the noise node
        gdfHandle.write('%.0f' % (idx + 1) + ',noise,%.0f' % len(self.uncoveredNodes) + '\n')
        gmlHandle.write('\tnode [\n\t  id %.0f' % (idx + 1) + '\n\t  label "%.0f"'  % (idx + 1)  + '\n\t  type "noise"' + '\n\t  image noise.png' + '\n\t  size %.0f\n\t]\n' % len(self.uncoveredNodes)); 
        mHandle.close()





class Structure:

    def getType(self):
        return '?'


    getType = staticmethod(getType)

    def isFullClique(self):
        return False



    def isNearClique(self):
        return False



    def isFullOffDiagonal(self):
        return False



    def isNearOffDiagonal(self):
        return False



    def isChain(self):
        return False



    def isStar(self):
        return False



    def isBiPartiteCore(self):
        return False



    def isNearBiPartiteCore(self):
        return False



    def isCorePeriphery(self):
        return False



    def isJellyFish(self):
        return False



    def load(line, idx, memberships):
        if line[:2] == FullClique.getType():
            return FullClique.load(line, idx, memberships)
        if line[:2] == NearClique.getType():
            return NearClique.load(line, idx, memberships)
        if line[:2] == Chain.getType():
            return Chain.load(line, idx, memberships)
        if line[:2] == Star.getType():
            return Star.load(line, idx, memberships)
        if line[:2] == BiPartiteCore.getType():
            return BiPartiteCore.load(line, idx, memberships)
        if line[:2] == NearBiPartiteCore.getType():
            return NearBiPartiteCore.load(line, idx, memberships)
        if line[:2] == CorePeriphery.getType():
            return CorePeriphery.load(line, idx, memberships)
        if line[:2] == JellyFish.getType():
            return JellyFish.load(line, idx, memberships)


    load = staticmethod(load)


class Clique(Structure):
    nodes = []
    numNodes = 0
    idx = -1
    typeS = ''


class FullClique(Clique):

    def __init__(self, nodes, idx):
        self.nodes = nodes
        self.numNodes = len(nodes)
        self.idx = idx
        self.typeS = self.getType()



    def getType():
        return 'fc'


    getType = staticmethod(getType)

    def isFullClique(self):
        return True



    def load(line, idx, memberships):
        if line[:2] != FullClique.getType():
            return 0
        parts = line[3:].strip().split(' ')
        nodes = []
        for x in parts:
            if x.find('-') > 0:
                y = x.strip().split('-')
                nodes.extend([ z for z in range(int(y[0]), int(y[1]) + 1) ])
            else:
                xint = int(x)
                nodes.append(xint)
                memberships[(xint - 1)].add(idx)

        return FullClique(sorted(nodes), idx)


    load = staticmethod(load)


class NearClique(Clique):
    numEdges = 0
    nodes = []
    idx = -1
    typeS = ''

    def __init__(self, nodes, numEdges, idx):
        self.nodes = nodes
        self.numNodes = len(nodes)
        self.numEdges = numEdges
        self.idx = idx
        self.typeS = self.getType()



    def getType():
        return 'nc'


    getType = staticmethod(getType)

    def isNearClique(self):
        return True



    def load(line, idx, memberships):
        if line[:2] != NearClique.getType():
            return 0
        cParts = line[3:].strip().split(',')
        numEdges = int(float(cParts[0].strip()))
        sParts = cParts[1].strip().split(' ')
        nodes = []
        for x in sParts:
            if x.find('-') > 0:
                y = x.strip().split('-')
                nodes.extend([ x for x in range(int(y[0]), int(y[1]) + 1) ])
            else:
                xint = int(x)
                nodes.append(xint)
                memberships[(xint - 1)].add(idx)

        return NearClique(sorted(nodes), numEdges, idx)


    load = staticmethod(load)


class Rectangle(Structure):
    lNodeList = []
    rNodeList = []
    numNodesLeft = 0
    numNodesRight = 0
    nodes = []
    numNodes = 0
    idx = -1

    def __init__(self, left, right, idx):
        self.lNodeList = left
        self.rNodeList = right
        self.numNodesLeft = len(left)
        self.numNodesRight = len(right)
        self.numNodes = self.numNodesLeft + self.numNodesRight
        self.nodes = left + right
        self.idx = idx
        self.type = getType()




class Chain(Structure):
    nodes = []
    numNodes = 0
    idx = -1
    typeS = ''

    def __init__(self, nodes, idx):
        self.nodes = nodes
        self.numNodes = len(nodes)
        #print 'nodes number: %.0f' % self.numNodes
        self.idx = idx
        self.typeS = self.getType()



    def getType():
        return 'ch'


    getType = staticmethod(getType)

    def isChain(self):
        return True



    def load(line, idx, memberships):
        if line[:2] != Chain.getType():
            return 0
        parts = line[3:].strip().split(' ')
        nodes = []
        for x in parts:
            if x.find('-') > 0:
                y = x.strip().split('-')
                nodes.extend([ x for x in range(int(y[0]), int(y[1]) + 1) ])
            else:
                xint = int(x)
                nodes.append(xint)
                memberships[(xint - 1)].add(idx)

        return Chain(nodes, idx)


    load = staticmethod(load)


class Star(Structure):
    cNode = -1
    sNodes = []
    numSpokes = 0
    numNodes = 0
    nodes = []
    idx = -1
    typeS = ''

    def __init__(self, hub, spokes, idx):
        self.cNode = hub
        self.sNodes = spokes
        self.numSpokes = len(spokes)
        self.nodes = [hub] + spokes
        self.numNodes = 1 + len(spokes)
        self.idx = idx
        self.typeS = self.getType()



    def getType():
        return 'st'


    getType = staticmethod(getType)

    def isStar(self):
        return True



    def load(line, idx, memberships):
        if line[:2] != Star.getType():
            return 0
        parts = line[3:].strip().split(',')
        cParts = parts[0].strip().split(' ')
        cNodes = []
        for x in cParts:
            if x.find('-') > 0:
                y = x.split('-')
                cNodes.extend([ x for x in range(int(y[0]), int(y[1]) + 1) ])
            else:
                xint = int(x)
                cNodes.append(xint)
                memberships[(xint - 1)].add(idx)

        sParts = parts[1].strip().split(' ')
        sNodes = []
        for x in sParts:
            if x.find('-') > 0:
                y = x.split('-')
                sNodes.extend([ x for x in range(int(y[0]), int(y[1]) + 1) ])
            else:
                xint = int(x)
                sNodes.append(xint)
                memberships[(xint - 1)].add(idx)

        return Star(cNodes[0], sorted(sNodes), idx)


    load = staticmethod(load)


class BiPartiteCore(Structure):
    lNodes = []
    numNodesLeft = 0
    rNodes = []
    numNodesRight = 0
    numNodes = 0
    nodes = []
    idx = -1
    typeS = ''

    def __init__(self, left, right, idx):
        self.lNodes = left
        self.numNodesLeft = len(left)
        self.rNodes = right
        self.numNodesRight = len(right)
        self.nodes = left + right
        self.numNodes = len(left) + len(right)
        self.idx = idx
        self.typeS = self.getType()



    def getType():
        return 'bc'


    getType = staticmethod(getType)

    def isBiPartiteCore(self):
        return True



    def load(line, idx, memberships):
        if line[:2] != BiPartiteCore.getType():
            return 0
        parts = line[3:].strip().split(',')
        lParts = parts[0].strip().split(' ')
        lNodes = []
        for x in lParts:
            if x.find('-') > 0:
                y = x.strip().split('-')
                lNodes.extend([ z for z in range(int(y[0]), int(y[1]) + 1) ])
            else:
                xint = int(x)
                lNodes.append(xint)
                memberships[(xint - 1)].add(idx)

        rParts = parts[1].strip().split(' ')
        rNodes = []
        for x in rParts:
            if x.find('-') > 0:
                y = x.strip().split('-')
                rNodes.extend([ z for z in range(int(y[0]), int(y[1]) + 1) ])
            else:
                xint = int(x)
                rNodes.append(xint)
                memberships[(xint - 1)].add(idx)

        return BiPartiteCore(sorted(lNodes), sorted(rNodes), idx)


    load = staticmethod(load)


class NearBiPartiteCore(Structure):
    lNodes = []
    numNodesLeft = 0
    rNodes = []
    numNodesRight = 0
    nodes = []
    numNodes = 0
    idx = -1
    typeS = ''

    def __init__(self, left, right, idx):
        self.lNodes = left
        self.numNodesLeft = len(left)
        self.rNodes = right
        self.numRightNodes = len(right)
        self.nodes = left + right
        self.numNodes = len(left) + len(right)
        self.idx = idx
        self.typeS = self.getType()



    def getType():
        return 'nb'


    getType = staticmethod(getType)

    def isNearBiPartiteCore(self):
        return True



    def load(line, idx, memberships):
        if line[:2] != NearBiPartiteCore.getType():
            return 0
        parts = line[3:].strip().split(',')
        lParts = parts[0].strip().split(' ')
        lNodes = []
        for x in lParts:
            if x.find('-') > 0:
                y = x.strip().split('-')
                lNodes.extend([ z for z in range(int(y[0]), int(y[1]) + 1) ])
            else:
                xint = int(x)
                lNodes.append(xint)
                memberships[(xint - 1)].add(idx)

        rParts = parts[1].strip().split(' ')
        rNodes = []
        for x in rParts:
            if x.find('-') > 0:
                y = x.strip().split('-')
                rNodes.extend([ z for z in range(int(y[0]), int(y[1]) + 1) ])
            else:
                xint = int(x)
                rNodes.append(xint)
                memberships[(xint - 1)].add(idx)

        return NearBiPartiteCore(sorted(lNodes), sorted(rNodes), idx)


    load = staticmethod(load)


class CorePeriphery(Structure):
    cNodes = []
    numCores = 0
    sNodes = []
    numSpokes = 0
    numNodes = 0
    nodes = []
    idx = -1
    typeS = ''

    def __init__(self, cores, spokes, idx):
        self.cNodes = cores
        self.numCores = len(cores)
        self.sNodes = spokes
        self.numSpokes = len(spokes)
        self.nodes = cores + spokes
        self.numNodes = len(cores) + len(spokes)
        self.idx = idx
        self.typeS = self.getType()



    def getType():
        return 'cp'


    getType = staticmethod(getType)

    def isCorePeriphery(self):
        return True



    def load(line, idx, memberships):
        if line[:2] != CorePeriphery.getType():
            return 0
        parts = line[3:].strip().split(',')
        cParts = parts[0].strip().split(' ')
        cNodes = []
        for x in cParts:
            if x.find('-') > 0:
                y = x.strip().split('-')
                cNodes.extend([ z for z in range(int(y[0]), int(y[1]) + 1) ])
            else:
                xint = int(x)
                cNodes.append(xint)
                memberships[(xint - 1)].add(idx)

        sParts = parts[1].strip().split(' ')
        sNodes = []
        for x in sParts:
            if x.find('-') > 0:
                y = x.strip().split('-')
                sNodes.extend([ z for z in range(int(y[0]), int(y[1]) + 1) ])
            else:
                xint = int(x)
                sNodes.append(xint)
                memberships[(xint - 1)].add(idx)

        return CorePeriphery(sorted(cNodes), sorted(sNodes), idx)


    load = staticmethod(load)


class JellyFish(Structure):
    cNodes = []
    numCores = 0
    sNodes = [[]]
    numSpokes = []
    numSpokeSum = 0
    numNodes = 0
    nodes = []
    idx = -1
    typeS = ''

    def __init__(self, cores, spokes, idx):
        self.cNodes = cores
        self.numCores = len(cores)
        self.sNodes = spokes
        self.numSpokes = [ len(s) for s in spokes ]
        self.numSpokeSum = sum(self.numSpokes)
        self.nodes = cores + spokes
        self.numNodes = len(cores) + self.numSpokeSum
        self.idx = idx
        self.typeS = self.getType()



    def getType():
        return 'jf'


    getType = staticmethod(getType)

    def isJellyFish(self):
        return True



    def load(line, idx, memberships):
        if line[:2] != JellyFish.getType():
            return 0
        parts = line[3:].strip().split(',')
        cParts = parts[0].strip().split(' ')
        cNodes = []
        for x in cParts:
            if x.find('-') > 0:
                y = x.strip().split('-')
                cNodes.extend([ z for z in range(int(y[0]), int(y[1]) + 1) ])
            else:
                xint = int(x)
                cNodes.append(xint)
                memberships[(xint - 1)].add(idx)

        sNodes = [ [] for x in range(len(cNodes)) ]
        for i in range(len(cNodes)):
            sParts = parts[(i + 1)].strip().split(' ')
            for x in sParts:
                if x.find('-') > 0:
                    y = x.strip().split('-')
                    sNodes[i].extend([ z for z in range(int(y[0]), int(y[1]) + 1) ])
                else:
                    xint = int(x)
                    sNodes[i].append(xint)
                    memberships[(xint - 1)].add(idx)

            sNodes[i] = sorted(sNodes[i])

        return JellyFish(sorted(cNodes), sNodes, idx)


    load = staticmethod(load)


