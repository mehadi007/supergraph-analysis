import csv
import pickle
import numpy as np
import math


def conductance(links, attributes , assignments , n , K):
    # print "Clustering Conductance..."
    cluster_conductances = []
    for k in range(K):
        current_members = set(np.where(assignments==k)[0])
        cut_edge_count = 0.0
        total_edge_count = 0.0
        for i in current_members:
            for j in np.where(links[i,:] == 1)[0]:
                if j not in current_members:
                    cut_edge_count+= 1
                total_edge_count += 1
        total_edge_count_bar = np.sum(links) - total_edge_count

        if total_edge_count == 0:
            cluster_conductances.append(0)
            continue            
        if total_edge_count > total_edge_count_bar:
            cluster_conductances.append(cut_edge_count/total_edge_count_bar)            
        else:
            cluster_conductances.append(cut_edge_count/total_edge_count)

    return cluster_conductances

def get_assignments(n):
    assignments = np.zeros((n),dtype='int64')
    with open('DATA/cluster_assignments.csv') as cluster_file:
        cluster_csv = csv.reader(cluster_file)
        for row in cluster_csv:
            assignments[int(row[0])-1] = int(row[1])-1
    return assignments

def modularity(links , assignments):
    n = links.shape[0]
    K = len(assignments)
    S = np.zeros((n,K) , dtype='float')
    m = np.count_nonzero(links)
    for k in range(K):
        for assgn in assignments[k]:
            S[assgn][k] = 1.

    links = (links + links.transpose())/2
    degrees = np.sum(links , axis = 0)
    B = np.empty(links.shape , dtype='float')
    for i in range(n):
        for j in range(n):
            B[i][j] = links[i][j] - degrees[i]*degrees[j] / (2*m)

    Q = 1. / (2*m) * np.trace(np.dot(np.dot(S.transpose() , B), S))
    return Q




def entropy_single( attributes_single ):
    # attributes_single contains a single attribute value for all nodes
    #counts = {}
    #total = 0
    #for att in attributes_single:
    #    if att == ():
    #        continue
    #    if att in counts: 
    #        counts[att] += 1.0
    #    else:
    #        counts[att] = 1.0
    #    total += 1
    ##total = len(attributes_single)
    ## number of possible values
    ##numVal = len(set(attributes_single))
    ##print counts
    #numVal = len(counts)
    ##print numVal, total
    #entropy = 0.0
    #for count in counts.values():
    #    prob  = count / total
    #    # print prob
    #    entropy +=  - prob * math.log(prob,2)
    # normalize entropy
    #maxEntropy = math.log(numVal, 2)
    #if numVal > 1:
    #    entropy /= maxEntropy
    total = sum(attributes_single)
    entropy = 0.0
    for count in attributes_single:
        prob = count / total
        if prob != 0:
            entropy += -prob * math.log(prob, 2)

    #print entropy

    return entropy

def entropy_multiple(attributes_multiple):
    # change this function to calculate entropy for each category of
    # attributes, min, max, avg (done), std, median
    # attributes_multiple contains a list of list for the attributes of each node. 
    attr_len = len(attributes_multiple[0])

    min_entropy = 100
    max_entropy = -1.0
    std_entropy = 0.0
    med_entropy = 0.0
    avg_entropy = 0.0
    sum_entropy = 0.0
    all_entropy = [0] * attr_len
    for i in range(attr_len):
        curr_attr_list = [a[i] for a in attributes_multiple]
        curr_entropy = entropy_single(curr_attr_list)
        sum_entropy += curr_entropy
        all_entropy[i] = curr_entropy

        if all_entropy[i] < min_entropy:
            min_entropy = all_entropy[i]
        if all_entropy[i] > max_entropy:
            max_entropy = all_entropy[i]

    avg_entropy = sum_entropy / attr_len
    std_entropy = np.std(np.array(all_entropy))
    med_entropy = np.median(np.array(all_entropy))
    """
    if max_entropy != 0:
        all_entropy = [x / max_entropy for x in all_entropy]
        avg_entropy /= max_entropy
        std_entropy /= max_entropy
        med_entropy /= max_entropy
        min_entropy /= max_entropy
        max_entropy /= max_entropy
    """

    print 'min entropy: ' + str(min_entropy)
    print 'max entropy: ' + str(max_entropy)
    print 'avg entropy: ' + str(avg_entropy)
    print 'std entropy: ' + str(std_entropy)
    print 'med entropy: ' + str(med_entropy)
    return all_entropy


def entropy( attributes , assignments , n , K):
    entropies = []
    print "Cluster Information"
    for k in range(K):
        current_members = np.where(assignments==k)[0]
        total_members = len(current_members)
        pos = len(np.where(attributes[current_members]==1)[0])
        pos_p = float(pos)/total_members
        neg_p = 1. - pos_p
        print "Cluster , Nodes , PositiveMembers" , k , total_members , pos
        if not pos_p or not neg_p:
            entropies.append(0)
        else:
            entropies.append(-pos_p*math.log(pos_p,2)-neg_p*math.log(neg_p,2))
    print
    return entropies


if __name__ == "__main__":
    a = [1,1,1,1,2]
    print 'single attribute value: ' + str(entropy_single(a))

    b = [[1,1,3,4,1,2,3,4], # lists have to be of same length
         [1,2,1,1,1,1,1,1],
         [1,3,3,1,3,1,4,1],
         [1,4,1,4,2,4,1,2]   
        ]

#    print entropy_multiple(b)
    #print 'list of attribute values: ' + str(entropy_multiple(b))
# attribute_links = pickle.load(open('methods/cluster-distance/pol_data.p','rb'))
# links = attribute_links['links']
# attributes = attribute_links['attributes']
# n , temp = links.shape
# assignments = get_assignments(n)
# k = np.max(assignments)
# conductance(links,attributes,assignments,n,k)
