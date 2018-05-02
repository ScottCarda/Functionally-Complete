from itertools import product
import copy

def intersect_graph( sets ):
    graph = {}
    for name1, S1 in sets.items():
        edges = { name2 for name2, S2 in sets.items() if S1 & S2 }
        graph[name1] = edges
    return graph

def remove_self_ref( graph ):
    rtrn = copy.deepcopy(graph)
    for vert in rtrn:
        rtrn[vert].discard(vert)
    return rtrn
    
def sort_graph( graph ):
    return [ e[0] for e in sorted( graph.items(), key=( lambda x : len(x[1]) ) ) ]
    
def find_max_degree( graph, keys=None ):
    val = -1
    key = ''
    
    pool = graph.keys()
    if keys is not None:
        pool &= set(keys)
        
    for vert in pool:
        if len(graph[vert]) > val:
            val = len(graph[vert])
            key = vert
    return key, val
        
def find_min_degree( graph, keys=None ):
    first = True
    val = -1
    key = ''
    
    pool = graph.keys()
    if keys is not None:
        pool &= set(keys)
        
    for vert in pool:
        if first:
            first = False
            val = len(graph[vert])
            key = vert
        elif len(graph[vert]) < val:
            val = len(graph[vert])
            key = vert
    return key, val
        
def make_sets():
    a = {1,2}
    b = {2,3,4,5,6}
    c = {4,5,7,8,10,11}
    d = {5,6,8,9,11,12}
    e = {10,11,12,13}
    f = {20,21,22}
    return { 'A':a, 'B':b, 'C':c, 'D':d, 'E':e, 'F':f }

def max_clique_req( A, B, C ):
    if max_clique_req.graph is None:
        return -1
    graph = max_clique_req.graph

    if len(B|C) == 0:
        return [A]
        
    piv = find_max_degree( graph, B|C )[0]
    pool = B - ( graph[piv] - {piv} )
    
    size = 0
    large = [set()]
    for vert in pool:
        cliques = max_clique_req( A | {vert}, B & graph[vert] , C & graph[vert] )
        B -= {vert}
        C |= {vert}
        if len(cliques[0]) == size:
            large.extend( cliques )
        if len(cliques[0]) > size:
            large = list(cliques)
            size = len(cliques[0])
    return large
max_clique_req.graph = None

'''def max_clique_req( A, B, C ):
    if max_clique_req.graph is None:
        return -1
    graph = max_clique_req.graph

    if len(B|C) == 0:
        return A
        
    piv = find_max_degree( graph, B|C )[0]
    pool = B - ( graph[piv] - {piv} )
    
    large = set()
    for vert in pool:
        clique = max_clique_req( A | {vert}, B & graph[vert] , C & graph[vert] )
        B -= {vert}
        C |= {vert}
        if len(clique) > len(large):
            large = clique
    return large
max_clique_req.graph = None'''

def max_clique( graph ):
    max_clique_req.graph = graph
    rtn = max_clique_req( set(), set(graph.keys()), set() )
    max_clique_req.graph = None
    return rtn
    
def max_clique_node( graph, node ):
    temp_g = copy.deepcopy( graph )
    
    #node = find_min_degree( temp_g )[0]
    neigh = temp_g[node]
    
    #remove = set(temp_g.keys()) - neigh
    subgraph = remove_nodes( temp_g, set(temp_g.keys()) - neigh )
    #for key in remove:
    #    temp_g.pop(key)
    #for key, val in temp_g.items():
    #    temp_g[key] = val - remove
    
    return max_clique( subgraph )[0] | {node}
    
def remove_nodes( graph, nodes ):
    temp_g = copy.deepcopy( graph )

    for key in nodes:
        temp_g.pop(key, None)
    for key, val in temp_g.items():
        temp_g[key] = val - nodes
        
    return temp_g
    
def min_sample_set_names( graph ):
    max_cliques = []
    remaining_nodes = set(graph.keys())

    while len(remaining_nodes) > 0:
        node = find_min_degree( graph, remaining_nodes )[0]
        clique = max_clique_node( graph, node )
        max_cliques.append( clique )
        remaining_nodes -= clique
        
    return max_cliques

def min_sample_sets( sets ):

    graph = intersect_graph( sets )
    graph = remove_self_ref( graph )

    intersects = min_sample_set_names( graph )
    return [intersection( sets, i ) for i in intersects]
    
def intersection( sets, names ):
    temp = set(names)
    inter = sets[temp.pop()]
    for s in temp:
        inter &= sets[s]
    return inter
     
def min_spanning_sets( sets ):
    return [ set(i) for i in product(*min_sample_sets( sets )) ]
    
    
    


















