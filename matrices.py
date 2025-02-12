from modules.open_digraph import *
from random import *

def random_int_list(n,bound):
    liste = []
    for i in range(n):
        liste.append(randint(0,bound))
    return liste

#print(random_int_list(3,6))

def random_int_matrix(n,bound,null_diag=True):
    liste = []
    for i in range(n):
        if null_diag:
            l = random_int_list(n,bound)
            l[i] = 0
            liste.append(l)
        else:
            liste.append(random_int_list(n,bound))

    return liste

#print(random_int_matrix(5,100))

def random_sysmetric_int_matrix(n,bound,null_diag=True):
    m = random_int_matrix(n,bound,null_diag)
    for i in range(n):
        for j in range(n):
            m[i][j] = m[j][ i]
    return m

#print(random_sysmetric_int_matrix(3,6,null_diag=False))

def random_oriented_int_matrix(n,bound,null_diag=True):
    m = random_int_matrix(n,bound,null_diag)
    for i in range(n):
        for j in range(n):
            if  m[i][j] != 0:
                m[j][i] = 0
    return m

#print(random_oriented_int_matrix(5,20,null_diag=False))

def random_triangular_int_matrix(n,bound,null_diag=True):
    m = random_int_matrix(n,bound,null_diag)
    for i in range(n):
        for j in range(n):
            if i > j :
                m[i][j] = 0
    return m

#print(random_triangular_int_matrix(5,20,null_diag=False))


def graph_from_adjacency_matrix(matrix):
    gr = open_digraph([], [], [])
    for i in range(len(matrix[0]) ):
        for j in range(len(matrix[0]) ):
            enfants = {}
            if matrix[i][j] != 0:
                enfants[j] = matrix[i][j]
        gr.add_node(label=chr(i), parents={}, children=enfants)
    return gr

def test() :
    gr = graph_from_adjacency_matrix([[0, 1, 1, 0, 0],
    [0, 0, 0, 1, 2],
    [0, 0, 0, 2, 0],
    [1, 0, 0, 0, 1],
    [0, 0, 0, 0, 0]])
    nodes = gr.get_nodes_dico()
    for node in nodes:
        print(nodes[node].__str__())

test()
