for clus_exluded in SL K L M SP BI H
do
#    python2.7 parse_graph.py DATA_ABLATION/chocolate/chocMediaWiki.sentenceEdges.graph DATA_ABLATION/chocolate/chocMediaWiki.sentenceEdges$clus_exluded\_orderedALL.model DATA_ABLATION/chocolate/result DATA_ABLATION/chocolate/optGreedySelection_nStop_simple_chocMediaWiki.sentenceEdges$clus_exluded\_orderedALL.model DATA_ABLATION/chocolate/optGreedySelection_costs_simple_chocMediaWiki.sentenceEdges$clus_exluded\_orderedALL.model > DATA_ABLATION/chocolate/result/OUTPUT_chocMediaWiki.sentenceEdges$clus_exluded.txt &
    python2.7 parse_graph.py DATA_ABLATION/oregon/as-oregon.graph DATA_ABLATION/oregon/as-oregon$clus_exluded\_orderedALL.model DATA_ABLATION/oregon/result DATA_ABLATION/oregon/optGreedySelection_nStop_simple_as-oregon$clus_exluded\_orderedALL.model DATA_ABLATION/oregon/optGreedySelection_costs_simple_as-oregon$clus_exluded\_orderedALL.model > DATA_ABLATION/oregon/result/OUTPUT_as-oregon$clus_exluded.txt &
done
