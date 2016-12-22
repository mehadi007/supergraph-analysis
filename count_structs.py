"""
Count the number of structures of different types.

input:
    dataset (ch - choc, ao - asoregon, ac - ascaida, en - enron, euemail - eu)
    method (v - vog, g - condense + gnf, s - step, sa - steppa, ks - kstep)
    # top structures in consideration
output:
    number of structures per type
"""
import sys

def countStructures(model, idx, n):
    # count number of structures for top n structures and print them out
    structCnt = {}
    for i in idx[:n]:
        i = int(i) - 1
        struct = model[i].split(' ')[0]
        if structCnt.has_key(struct):
            structCnt[struct] += 1
        else: structCnt[struct] = 1
    return structCnt

if __name__ == '__main__':
    dataset, method, n = sys.argv[1], sys.argv[2], int(sys.argv[3])
    if method == 'v':
        path = 'DATA_FOR_SUPERGRAPH/vog_orig_results/'
    elif method == 'g':
        path = 'DATA_FOR_SUPERGRAPH/gnf_results/'
    elif method == 's':
        path = 'DATA_FOR_SUPERGRAPH/parallel_results/plain/'
    elif method == 'sa':
        path = 'DATA_FOR_SUPERGRAPH/parallel_results/active/'
    elif method == 'ks':
        path = 'DATA_FOR_SUPERGRAPH/parallel_results/topK/'
    if dataset == 'en':
        modelFile = path + 'enron_orderedALL.model'
        idxFile = path + 'heuristicSelection_nStop_ALL_enron_orderedALL.model'
    fModel = open(modelFile, 'r')
    fIdx = open(idxFile, 'r')
    model = fModel.read().splitlines()
    idx = fIdx.read().splitlines()
    countStructures(model, idx, n)
    print countStructures(model, idx, n)
