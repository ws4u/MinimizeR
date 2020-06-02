import networkx as nx
import math

def min_r_tree(T):
    """Return the minimum r by recursion with optimal substructure.

    Parameters
    ----------
    T : A tree
        The tree for which R is to be computed

    Returns
    -------
    min_r : integer
        The minimum r of T.

    node_seq: list
        The seq of node removals achieving min r
    """
    n=T.number_of_nodes()
    if n==1 or n==2:
        node_seq = [i for i in T.nodes]
        min_r = n-1
        return min_r, node_seq

    min_r=math.inf
    for i in T.nodes:
        if len(T[i])==1:
            continue
        TT = T.copy()
        TT.remove_node(i)
        seq_current = [i]
        r_current = n-1
        cc_list=[TT.subgraph(c).copy() for c in nx.connected_components(TT)]
        # a list of seqs; merging is not fully implemented now
        seq_list=[] 
        for C in cc_list:
            r, seq = min_r_tree(C)
            r_current += r
            seq_current += seq
            seq_list.append(seq)

        if r_current < min_r:
            min_r = r_current
            node_seq = seq_current
        
        del(TT)

    return min_r, node_seq

# a star graph with n leaves; node 0 is the center
n=6
g=nx.star_graph(n)
# construct a path graph with m nodes; connect it with node n
m=17
for i in range(m): 
    g.add_edge(n+i,n+i+1)

if (n+m)%2 == 0:
    print("Centroid: ", (n+m)//2)
else:
    print("Centroids: ", (n+m)//2, (n+m)//2+1)

print("Optimal:", min_r_tree(g))
