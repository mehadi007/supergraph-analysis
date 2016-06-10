#!/bin/bash

#../models/slashburn_noNearStructs/anon_newsfeed_directed_matlabNumbering_orderedALL.model  ../models/slashburn_noNearStructs/enron_orderedALL.model         ../models/slashburn_noNearStructs/lcrMediaWiki.sentenceEdges_orderedALL.model
#../models/slashburn_noNearStructs/as-oregon_orderedALL.model                               ../models/slashburn_noNearStructs/epinions_sym_orderedALL.model  ../models/slashburn_noNearStructs/wwwbb_sym_orderedALL.model
#../models/slashburn_noNearStructs/chocMediaWiki.wholeEdges_orderedALL.model                ../models/slashburn_noNearStructs/flickr_orderedALL.model

#as-oregon.graph                    chocMediaWiki.wholeEdges.graph  dstarMediaWiki.sentenceEdges.graph  enron.graph         flickr.graph                       kievMediaWiki.wholeEdges.graph    lcrMediaWiki.wholeEdges.graph
#chocMediaWiki.sentenceEdges.graph  cliqueStarClique.graph          dstarMediaWiki.wholeEdges.graph     epinions_sym.graph  kievMediaWiki.sentenceEdges.graph  lcrMediaWiki.sentenceEdges.graph  wwwbb_sym.graph


##### LCR
# Get the supergraph of the augmented model for the faster heuristic (as in the conference paper)
python2.7 parse_graph.py ../Graphs/lcrMediaWiki.sentenceEdges.graph LCR/FASTER/augmentedModel_lcrMediaWiki.model ../MDL_methods/MDL_faster/heuristicSelection_nStop_ALL_augmentedModel_lcrMediaWiki.model ../MDL_methods/MDL_faster/heuristic_Selection_costs_ALL_augmentedModel_lcrMediaWiki.model > OUTPUT_SUPERGRAPH_lcr_faster_for_augmented_model.txt &

# Run the optgreedy method
#python2.7 parse_graph.py ../Graphs/lcrMediaWiki.sentenceEdges.graph ../models/slashburn_noNearStructs/lcrMediaWiki.sentenceEdges_orderedALL.model ../MDL_methods/MDL_faster_optGreedy/NoNearStructs/greedySelection_nStop_lcrMediaWiki.sentenceEdges_orderedALL.model ../MDL_methods/MDL_faster_optGreedy/NoNearStructs/greedySelection_costs_lcrMediaWiki.sentenceEdges_orderedALL.model > OUTPUT_lcrMediaWiki.sentenceEdges_optgreedy.txt &



##### ENRON
# Run faster heuristic (as in the conference paper)
python2.7 parse_graph.py ../Graphs/enron.graph ENRON/FASTER/augmentedModel_enron_orderedALL.model ../MDL_methods/MDL_faster/heuristicSelection_nStop_ALL_augmentedModel_enron_orderedALL.model ../MDL_methods/MDL_faster/heuristic_Selection_costs_ALL_augmentedModel_enron_orderedALL.model > OUTPUT_SUPERGRAPH_enron_faster_for_augmented_model.txt &

# Run the optgreedy method
#python2.7 parse_graph.py ../Graphs/enron.graph ../models/slashburn_noNearStructs/enron_orderedALL.model ../MDL_methods/MDL_faster_optGreedy/NoNearStructs/greedySelection_nStop_enron_orderedALL.model ../MDL_methods/MDL_faster_optGreedy/NoNearStructs/greedySelection_costs_enron_orderedALL.model > OUTPUT_enron_optgreedy.txt &



##### EPINIONS
# Run faster heuristic (as in the conference paper)
python2.7 parse_graph.py ../Graphs/epinions_sym.graph EPINIONS/FASTER/augmentedModel_epinions_sym_orderedALL.model ../MDL_methods/MDL_faster/heuristicSelection_nStop_ALL_augmentedModel_epinions_sym_orderedALL.model ../MDL_methods/MDL_faster/heuristic_Selection_costs_ALL_augmentedModel_epinions_sym_orderedALL.model > OUTPUT_SUPERGRAPH_epinions_sym_faster_for_augmented_model.txt &

# Run the optgreedy method
#python2.7 parse_graph.py ../Graphs/epinions_sym.graph ../models/slashburn_noNearStructs/epinions_sym_orderedALL.model ../MDL_methods/MDL_faster_optGreedy/NoNearStructs/greedySelection_nStop_epinions_sym_orderedALL.model ../MDL_methods/MDL_faster_optGreedy/NoNearStructs/greedySelection_costs_epinions_sym_orderedALL.model > OUTPUT_epinions_sym_optgreedy.txt &


##### EPINIONS
# Run faster heuristic (as in the conference paper)
python2.7 parse_graph.py ../Graphs/wwwbb_sym.graph WWWBB/FASTER/augmentedModel_wwwbb_sym_orderedALL.model ../MDL_methods/MDL_faster/heuristicSelection_nStop_ALL_augmentedModel_wwwbb_sym_orderedALL.model ../MDL_methods/MDL_faster/heuristic_Selection_costs_ALL_augmentedModel_wwwbb_sym_orderedALL.model > OUTPUT_SUPERGRAPH_wwwbb_sym_faster_for_augmented_model.txt &

# Run the optgreedy method
#python2.7 parse_graph.py ../Graphs/wwwbb_sym.graph ../models/slashburn_noNearStructs/wwwbb_sym_orderedALL.model ../MDL_methods/MDL_faster_optGreedy/NoNearStructs/greedySelection_nStop_wwwbb_sym_orderedALL.model ../MDL_methods/MDL_faster_optGreedy/NoNearStructs/greedySelection_costs_wwwbb_sym_orderedALL.model > OUTPUT_wwwbb_sym_optgreedy.txt &


# Get the graph for the optGreedy selection of the augmented model
#python2.7 parse_graph.py ../Graphs/as-oregon.graph CREATING_AUGMENTED_MODELS/augmentedModel_as-oregon_orderedALL.model ../MDL_methods/MDL_faster/NoNearStructs/greedySelection_nStop_augmentedModel_as-oregon_orderedALL.model ../MDL_methods/MDL_faster/NoNearStructs/greedySelection_costs_augmentedModel_as-oregon_orderedALL.model > as_oregon_graph_for_augmented_model.txt &
