#!/bin/bash

# This files generate model analysis and supergraphs
# input:
#   data: chocolate, oregon, caida, enron, euemail
#   method: vog, gnf, marg, step, stepa, kstep

data=$1
method=$2

filename=$(case "$data" in
    (chocolate) echo chocMediaWiki.sentenceEdges;;
    (oregon) echo as-oregon;;
    (caida) echo as-caida;;
    (enron) echo enron;;
    (euemail) echo email-EuAll
esac)

targetFolder=$(case "$method" in
    (vog) echo vog_orig_results;;
    (gnf) echo gnf_results;;
    (marg) echo marg_results;;
    (step) echo parallel_results/plain;;
    (stepa) echo parallel_results/active;;
    (kstep) echo parallel_results/topK
esac)

if [ "$method" = "vog" ] || [ "$method" = "gnf" ]; then
    python2.7 parse_graph.py DATA_FOR_SUPERGRAPH/graphs/$filename.graph DATA_FOR_SUPERGRAPH/$targetFolder/$filename\_orderedALL.model DATA_FOR_SUPERGRAPH/$targetFolder DATA_FOR_SUPERGRAPH/$targetFolder/heuristicSelection_nStop_ALL_$filename\_orderedALL.model DATA_FOR_SUPERGRAPH/$targetFolder/heuristic_Selection_costs_ALL_$filename\_orderedALL.model > DATA_FOR_SUPERGRAPH/$targetFolder/OUTPUT_$filename.txt &
elif [ "$method" = "marg" ]; then
    python2.7 parse_graph.py DATA_FOR_SUPERGRAPH/graphs/$filename.graph DATA_FOR_SUPERGRAPH/$targetFolder/$filename\_orderedALL.model DATA_FOR_SUPERGRAPH/$targetFolder DATA_FOR_SUPERGRAPH/$targetFolder/greedySelectionMargin_nStop_$filename\_orderedALL.model DATA_FOR_SUPERGRAPH/$targetFolder/greedySelectionMargin_costs_$filename\_orderedALL.model > DATA_FOR_SUPERGRAPH/$targetFolder/OUTPUT_$filename.txt &
elif [ "$method" = "step" ] || [ "$method" = "stepa" ] || [ "$method" = "kstep" ]; then
    #python2.7 parse_graph.py DATA_FOR_SUPERGRAPH/graphs/$filename.graph DATA_FOR_SUPERGRAPH/$targetFolder/$filename\_orderedALL.model DATA_FOR_SUPERGRAPH/$targetFolder DATA_FOR_SUPERGRAPH/$targetFolder/$filename\_structures_1 DATA_FOR_SUPERGRAPH/$targetFolder/$filename\_encoding_1 > DATA_FOR_SUPERGRAPH/$targetFolder/OUTPUT_$filename.txt &
    python2.7 parse_graph.py DATA_FOR_SUPERGRAPH/graphs/$filename.graph DATA_FOR_SUPERGRAPH/gnf_results/$filename\_orderedALL.model DATA_FOR_SUPERGRAPH/$targetFolder DATA_FOR_SUPERGRAPH/$targetFolder/$filename\_structures_1 > DATA_FOR_SUPERGRAPH/$targetFolder/OUTPUT_$filename.txt &
else
    echo 'Wrong input.'
fi
echo ''
echo 'Analysis completed.'
