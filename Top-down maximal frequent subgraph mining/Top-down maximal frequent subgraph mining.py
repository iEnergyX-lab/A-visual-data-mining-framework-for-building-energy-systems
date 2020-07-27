"""
Created on Wed Jul 22 17:09:59 2020

@author: Chaobo Zhang
"""

import numpy as np
from copy import deepcopy
import time
from itertools import combinations
import gc
import pandas as pd

#####A top-down maximal frequent subgraph mining algorithm.
#####It is proposed for mining frequent subgraphs from undirected graphs.
#####It is based on an assumption that a node in a graph have a unique label.

def Graph_transform(RawGraph):
    """
    Convert raw data of graphs (list) into a dict.
    
    Raw data of graphs are stored in a list:
    RawGraph =  ["t # 1",
                 "v 0 2",
                 "v 1 6",
                 "v 7 9",
                 "v 8 10",
                 "v 9 20",
                 "e 0 1 2",
                 "e 0 7 2",
                 "e 7 8 2",
                 "e 7 9 2",
                 ...
                 "t # -1"]
    where, "t # n" means the nth graph, "v i m" means that the label of the ith vertex is m, "e j k p" means that the label of the edge between the jth vertex and the kth vertex is p.
    The label of each vertex should be assigned a unique identification number in {1, 2, …, q}, where q is the number of all non-redundant labels of nodes in all graphs.
    
    The transmofred data of graphs are stored in a dict:
    G_tr[n]["vec"][i] is the label of the ith vertex of the nth graph.
    G_tr[n]["edg"][j] is a tuple (number of the first vertex, number of the second vertex, label of the first vertex, label of the edge, label of the second vertex) of the jth edge of the nth graph.
    """
    
    G_tr = {}
    for i in range(len(RawGraph)):
        if RawGraph[i] == "t # -1":
            break
        if "t #" in RawGraph[i]:
            num_of_graph = RawGraph[i].split(" ")[2]
            G_tr[num_of_graph] = {}
            G_tr[num_of_graph]["vec"] = {}
            G_tr[num_of_graph]["edg"] = {}
            count_of_edge = 0
        if "v" in RawGraph[i]:
            num_of_vertex = RawGraph[i].split(" ")[1]
            lab_of_vertex = RawGraph[i].split(" ")[2]
            G_tr[num_of_graph]["vec"][num_of_vertex] = lab_of_vertex
        if "e" in RawGraph[i]:
            if int(G_tr[num_of_graph]["vec"][RawGraph[i].split(" ")[1]]) < int(G_tr[num_of_graph]["vec"][RawGraph[i].split(" ")[2]]):
                from_ = RawGraph[i].split(" ")[1]
                to_ = RawGraph[i].split(" ")[2]
            else:
                from_ = RawGraph[i].split(" ")[2]
                to_ = RawGraph[i].split(" ")[1]                
            label_of_egde = RawGraph[i].split(" ")[3]            
            G_tr[num_of_graph]["edg"][count_of_edge] = (from_, to_, G_tr[num_of_graph]["vec"][from_], label_of_egde, G_tr[num_of_graph]["vec"][to_])      
            count_of_edge = count_of_edge+1
    
    return G_tr

def TDMFSM(Grpah_tr, min_support):
    """
    Mine maximal frequent subgraphs from all graphs
    
    Inputs:
    Grpah_tr: Data of graphs
    min_support: Threshold of the support
    
    Outputs:
    Maximal_frequent_subgraph: Maximal frequent subgraphs which are as stored as following:
                                {0: {'Maximal frequent subgraph': [(2, 2, 9), (2, 2, 11), ...], #Edges of the 0th maximal frequent subgraph which are expressed by a tuple (label of the first vertex, label of the edge, label of the second vertex)
                                     'Support': 1445}, #Support of the 0th maximal frequent subgraph
                                 1: {'Maximal frequent subgraph': [(2, 2, 9), (2, 2, 11), ...],
                                     'Support': 1445},
                                 ...}

    Computation_time: Computation time
    """
   
    E = [] #A list of labels of edges
    for i in list(Grpah_tr.keys()):
        for j in list(Grpah_tr[i]["edg"].keys()):
            if (Grpah_tr[i]["edg"][j][2], Grpah_tr[i]["edg"][j][3], Grpah_tr[i]["edg"][j][4]) not in E:
                E.append((Grpah_tr[i]["edg"][j][2], Grpah_tr[i]["edg"][j][3], Grpah_tr[i]["edg"][j][4]))  
                
    G_edge = {} #A dict of labels of edges in each graph
    for i in Grpah_tr.keys():
        G_edge[i] = [(Grpah_tr[i]["edg"][x][2], Grpah_tr[i]["edg"][x][3], Grpah_tr[i]["edg"][x][4]) for x in Grpah_tr[i]["edg"].keys()]
    
    Support_of_edg = {} #Support of each edge        
    for i in E:
        Support_of_edg[i] = 0
        for j in G_edge.keys():
            if i in G_edge[j]:
                Support_of_edg[i] = Support_of_edg[i]+1
    
    Infrequent_edge = [] #A list of infrequent edges
    Frequent_edge = [] #A list of frequent edges
    
    for i in Support_of_edg.keys():
        if Support_of_edg[i] < min_support:
            Infrequent_edge.append(i)
        else:
            Frequent_edge.append(i)
    
    Frequent_edge.sort(key=lambda s:(int(s[0]),int(s[2])))
    Edge_code = {}
    n = 0
    for i in Frequent_edge:
        Edge_code[str(i)] = n
        n = n+1
    Edge_recode = {}
    n = 0
    for j in Frequent_edge:
        Edge_recode[n] = j
        n = n+1
        
    #Generate a dict of graphs without infrequent vertexes and edges
    Grpah_tr_without_infr_ver_and_edg = deepcopy(Grpah_tr)
    for i in Grpah_tr_without_infr_ver_and_edg.keys():               
        e_keys = list(Grpah_tr_without_infr_ver_and_edg[i]['edg'].keys())
        for j in e_keys:
            for l in Infrequent_edge:
                if l == (Grpah_tr_without_infr_ver_and_edg[i]['edg'][j][2],Grpah_tr_without_infr_ver_and_edg[i]['edg'][j][3],Grpah_tr_without_infr_ver_and_edg[i]['edg'][j][4]) or l == (Grpah_tr_without_infr_ver_and_edg[i]['edg'][j][4],Grpah_tr_without_infr_ver_and_edg[i]['edg'][j][3],Grpah_tr_without_infr_ver_and_edg[i]['edg'][j][2]):
                    del Grpah_tr_without_infr_ver_and_edg[i]['edg'][j]
                    break
    
    D_final = [] #A dict of merged graphs without infrequent edges
    Count_of_G = {} #A dict of support of merged graphs without infrequent edges
    for i in Grpah_tr_without_infr_ver_and_edg.keys():
        if Grpah_tr_without_infr_ver_and_edg[i]['edg'] == {}:
            continue
        if len(D_final) == 0:
            edge_vector = []
            for j in Grpah_tr_without_infr_ver_and_edg[i]['edg'].keys():
                edge_vector.append((Grpah_tr_without_infr_ver_and_edg[i]['edg'][j][2], Grpah_tr_without_infr_ver_and_edg[i]['edg'][j][3], Grpah_tr_without_infr_ver_and_edg[i]['edg'][j][4]))
            edge_vector.sort(key=lambda s:(int(s[0]),int(s[2])))
            edge_vector_new = []
            for i in edge_vector:
                edge_vector_new.append(Edge_code[str(i)])
            D_final.append(edge_vector_new)
            Count_of_G[str(edge_vector_new)] = 1
        else:
            edge_vector_1 = []
            for j in Grpah_tr_without_infr_ver_and_edg[i]['edg'].keys():
                edge_vector_1.append((Grpah_tr_without_infr_ver_and_edg[i]['edg'][j][2], Grpah_tr_without_infr_ver_and_edg[i]['edg'][j][3], Grpah_tr_without_infr_ver_and_edg[i]['edg'][j][4]))
            edge_vector_1.sort(key=lambda s:(int(s[0]),int(s[2])))
            edge_vector_1_new = []
            for i in edge_vector_1:
                edge_vector_1_new.append(Edge_code[str(i)])            
            flag = 0
            for edge_vector_2 in D_final:
                if str(edge_vector_1_new) == str(edge_vector_2):
                    Count_of_G[str(edge_vector_2)] = Count_of_G[str(edge_vector_2)] +1
                    flag = 1
                    break
            if flag == 0:
                Count_of_G[str(edge_vector_1_new)] = 1
                D_final.append(edge_vector_1_new)
            
    size_of_edges = []
    size_of_edges_sort = []
    for i in D_final:
        size = len(i)
        if size not in size_of_edges_sort:
            size_of_edges_sort.append(size)
        size_of_edges.append([i,size])
    size_of_edges_sort.sort(reverse=True)
    
    Nmuber_of_edge = {}
    for i in size_of_edges_sort:
        Nmuber_of_edge[i] = []
        for j in size_of_edges:
            if j[1] == i:
                Nmuber_of_edge[i].append(j[0])
    
    #Top-down maximal frequent subgraph mining
    G_already_existed = [] #A list to store the graphs which have existed
    Maximal_frequent_subgraph = {} #A dict of maximal frequent subgraphs
    Infrequent_subgraph_in_previous_layer = [] #A dict of infrequent subgraphs in the previous layer
    Support_of_MFS = {} #A dict of support of maximal frequent subgraphs
    start = time.clock()
    for layer in range(size_of_edges_sort[0]):
        if layer == 0:
            for j in range(len(Nmuber_of_edge[size_of_edges_sort[0]])):
                G_already_existed.append(Nmuber_of_edge[size_of_edges_sort[0]][j])
                if Count_of_G[str(Nmuber_of_edge[size_of_edges_sort[0]][j])] >= min_support:
                    Maximal_frequent_subgraph[str(Nmuber_of_edge[size_of_edges_sort[0]][j])] = Nmuber_of_edge[size_of_edges_sort[0]][j]
                    Support_of_MFS[str(Nmuber_of_edge[size_of_edges_sort[0]][j])] = Count_of_G[str(Nmuber_of_edge[size_of_edges_sort[0]][j])]
                else:
                    Infrequent_subgraph_in_previous_layer.append(Nmuber_of_edge[size_of_edges_sort[0]][j])

        else:
            if len(Infrequent_subgraph_in_previous_layer) == 0 and size_of_edges_sort[0]-layer not in size_of_edges_sort:   
                continue

            Tree_original = {}
            
            if len(Infrequent_subgraph_in_previous_layer) != 0:
                for j in Infrequent_subgraph_in_previous_layer:
                    Sub_tree = list(map(list, combinations(j, len(j)-1))) #Generate all subgraphs which have num-1 edges of the remaining graph
                    Sub_tree_ = list(map(lambda x:str(x), Sub_tree))
                    Tree_original.update(dict(zip(Sub_tree_, Sub_tree)))
            if size_of_edges_sort[0]-layer in size_of_edges_sort:
                for G_ in Nmuber_of_edge[size_of_edges_sort[0]-layer]:
                    Tree_original[str(G_)] = G_
                    G_already_existed.append(G_)

            Infrequent_subgraph_in_previous_layer = []
            gc.collect()
            for subgraph_ in Tree_original.keys():
                Sup_count = 0
                for G_al in G_already_existed:
                    if set(Tree_original[subgraph_]).issubset(G_al):
                            Sup_count = Sup_count + Count_of_G[str(G_al)]
                if Sup_count < min_support:
                    Infrequent_subgraph_in_previous_layer.append(Tree_original[subgraph_])
                else:
                    if len(Maximal_frequent_subgraph) != 0:
                        m = 0
                        for max_fre_sub in Maximal_frequent_subgraph.values():
                            if set(Tree_original[subgraph_]).issubset(max_fre_sub):
                                m = 1
                                break
                        if m == 0:
                            Maximal_frequent_subgraph[str(Tree_original[subgraph_])] = Tree_original[subgraph_]
                            Support_of_MFS[str(Tree_original[subgraph_])] = Sup_count
                    else:
                        Maximal_frequent_subgraph[str(Tree_original[subgraph_])] = Tree_original[subgraph_]
                        Support_of_MFS[str(Tree_original[subgraph_])] = Sup_count
        
        if len(Infrequent_subgraph_in_previous_layer) == 0 and len(G_already_existed) == len(D_final):  
            break
        
    end = time.clock()
    Computation_time = end - start
    
    Maximal_frequent_subgraph_output = {}
    m = 0
    for i in Maximal_frequent_subgraph.keys():
        Maximal_frequent_subgraph_output[m] = {}
        Maximal_frequent_subgraph_output[m]["Support"] = Support_of_MFS[i]
        Maximal_frequent_subgraph_output[m]["Maximal frequent subgraph"] = []
        for j in Maximal_frequent_subgraph[i]:
            Maximal_frequent_subgraph_output[m]["Maximal frequent subgraph"].append(Edge_recode[j])
        m = m+1

    return Maximal_frequent_subgraph_output, Computation_time

if __name__ == '__main__':
    ############################################################
    #The data are stored in a txt file as following:
    ########
    #t # 1
    #v 0 2
    #v 1 6
    #v 7 9
    #v 8 10
    #v 9 20
    #e 0 1 2
    #e 0 7 2
    #e 7 8 2
    #e 7 9 2
    #...
    #t # -1
    ########
    #It needs to be noted that the last line should be "t # -1".
    ############################################################

    #Read the data of graphs from a txt file.
    with open("Test.txt", "r") as f:
        data = f.read()
    Graph = data.split("\n")
    
    #Convert raw data of graphs (list) into a dict.
    Grpah_tr = Graph_transform(Graph)
    
    min_support_ = 0.4 #Minimum support (percentage)
    min_support = round(min_support_*len(Grpah_tr)) #Minimum support (number)
    
    #Top-down maximal frequent subgraph mining
    Maximal_frequent_subgraph, Computation_time = TDMFSM(Grpah_tr, min_support)
    print("Computation time: "+str(Computation_time))
    for i in Maximal_frequent_subgraph.keys():
        print(str(i)+"th maximal frequent subgraph")
        print("  Support: "+str(Maximal_frequent_subgraph[i]['Support']))
        print("  Edges:")
        for j in range(len(Maximal_frequent_subgraph[i]['Maximal frequent subgraph'])):
            print("  "+str(Maximal_frequent_subgraph[i]['Maximal frequent subgraph'][j]))