# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 13:10:42 2018

@author: WSi
"""

import networkx as nx
import math

def optimal_r(G):
    """Return the minimum R with the optimal substructure of
    MinR. Also, the LC strategy is utilized.

    Parameters
    ----------
    G : Graph
        The graph for which MinR is to be computed

    Returns
    -------
    min_r : integer
        The minimum R of G.
    node_seq: list
        An optimal sequence to achieve MinR. Each element
        in this list is a 2-tuple (node, c_size).
        'node' gives the node id.
        'c_size' gives the max component size before
        'node' is removed.

    """
    
    # terminations in the recursion
    n=len(G)
    if n==1:
        n_list = list(G.nodes)
        return 0, [(n_list[0], 1)] 
    if n==2:
        n_list = list(G.nodes)
        return 1, [(n_list[0], 2), (n_list[1], 1)]

    min_r=math.inf  # An infinitely large value initially
    node_seq = []
    max_c = max(nx.connected_components(G), key=len)
    max_len = len(max_c)
    for i in max_c:
        GG=G.copy()
        GG.remove_node(i)
        c_list = nx.connected_components(GG)
        r = n - 1
        seq_list = []  # a list of lists
        for c in c_list:
            r_c, seq = optimal_r(GG.subgraph(c))
            r += r_c 
            seq_list.append(seq)

        if r<min_r:
            min_r=r
            node_seq.clear()
            node_seq.append((i, max_len))
            for j in range(n-1):
                c_size = 0
                selected = []
                # find the seq for the max component
                for seq in seq_list:
                    if len(seq) == 0:
                        continue
                    if seq[0][1] > c_size:
                        c_size = seq[0][1]
                        selected = seq
                # add the top item to node_seq
                node_seq.append(selected.pop(0))

    return min_r, node_seq

#####################################################################
#####################################################################
    
level = 0
def optimal_r_sym(G, k):
    """Return the minimum R. 
    The difference from optimal_r(G) is that only the first
    k nodes are searched in the highest level if the graph
    is symmetric in some way. This function needs a global variable
    named 'level' that is initialised to 0 before this function
    is called.

    Parameters
    ----------
    G : Graph
        The graph for which MinR is to be computed

    k : integer
        The first k nodes.

    Returns
    -------
    min_r : integer
        The minimum R of G.
    node_seq: list
        An optimal sequence to achieve MinR. Each element
        in this list is a 2-tuple (node, c_size).
        'node' gives the node id.
        'c_size' gives the max component size before
        'node' is removed.

    """
    
    global level

    # terminations in the recursion
    n=len(G)
    if n==1:
        n_list = list(G.nodes)
        return 0, [(n_list[0], 1)] 
    if n==2:
        n_list = list(G.nodes)
        return 1, [(n_list[0], 2), (n_list[1], 1)]

    level +=1

    min_r=math.inf  # An infinitely large value initially
    node_seq = []
    max_c = max(nx.connected_components(G), key=len)
    max_len = len(max_c)
    for i in max_c:
        if level==1 and i>=k:
            continue
        GG=G.copy()
        GG.remove_node(i)
        c_list = nx.connected_components(GG)
        r = n - 1
        seq_list = []  # a list of lists
        for c in c_list:
            r_c, seq = optimal_r(GG.subgraph(c))
            r += r_c 
            seq_list.append(seq)

        if r<min_r:
            min_r=r
            node_seq.clear()
            node_seq.append((i, max_len))
            for j in range(n-1):
                c_size = 0
                selected = []
                # find the seq for the max component
                for seq in seq_list:
                    if len(seq) == 0:
                        continue
                    if seq[0][1] > c_size:
                        c_size = seq[0][1]
                        selected = seq
                # add the top item to node_seq
                node_seq.append(selected.pop(0))

    level -=1
    return min_r, node_seq

