import sys
import os
root = os.path.normpath(os.path.join(__file__, "./../.."))
sys.path.append(root) # allows us to fetch files from the project root
import unittest
from modules.open_digraph import *
from modules.nodes import node

class InitTest(unittest.TestCase):
    def test_init_node(self):
        n0 = node(0, 'i', {}, {1:1})
        self.assertEqual(n0.id, 0)
        self.assertEqual(n0.label, 'i')
        self.assertEqual(n0.parents, {})
        self.assertEqual(n0.children, {1:1})
        self.assertIsInstance(n0, node)
        # Test copy()
        n00 = n0.copy()
        n0.set_label("ii")
        n0.parents = {1:1}
        self.assertIsNot(n00.label,n0.label)
        self.assertIsNot(n00.parents,n0.parents)
        n0.set_label("i")
        n0.parents = {}
        # Test getteurs
        self.assertEqual(n0.get_id(), 0)
        self.assertEqual(n0.get_label(), 'i')
        self.assertEqual(n0.get_parents(), {})
        self.assertEqual(n0.get_children(), {1:1})
        # Test setteurs
        n2 = node(2, 'n2', {}, {})
        n0.add_parent_id(2)
        n3 = node(3, 'n3', {}, {})
        n0.add_parent_id(3)
        n4 = node(4, 'n4', {}, {})
        n0.add_child_id(4)
        n0.set_label("n0")
        self.assertEqual(n0.get_parents(), {2:1, 3:1})
        self.assertEqual(n0.get_children(), {1:1, 4:1})
        self.assertEqual(n0.label, 'n0')
        n0.set_children({1:1})
        self.assertEqual(n0.children, {1:1})
        # Test remove_parent_once et remove_child_once 
        ns = node(10, 's', {3:5 , 2:1}, {1:2, 2:3})
        ns.remove_parent_once(3)
        self.assertEqual(ns.get_parents(), {3:4 , 2:1})
        ns.remove_parent_once(2)
        self.assertEqual(ns.get_parents(), {3:4})
        ns.remove_child_once(1)
        self.assertEqual(ns.get_children(), {1:1, 2:3})
        ns.remove_child_once(2)
        self.assertEqual(ns.get_children(), {1:1, 2:2})
        # Test remove_parent_id et remove_child_id 
        nt = node(10, 's', {3:5 , 2:1}, {1:2, 2:3})
        nt.remove_parent_id(3)
        self.assertEqual(nt.get_parents(), {2:1})
        nt.remove_child_id(2)
        self.assertEqual(nt.get_children(), {1:2})
        # Test indegree, outdegree, degree
        ns = node(10, 's', {3:5 , 2:1}, {1:2, 2:3,})
        self.assertEqual(ns.indegree(), 6)
        self.assertEqual(ns.outdegree(), 5)
        self.assertEqual(ns.degree(), 11)



    def test_init_open_digraph(self):
        n0 = node(0, 'a', {3:1 , 4:1}, {1:1, 2:1})
        n1 = node(1, 'b', {0:1}, {2:2 , 5:1})
        n2 = node(2, 'c', {0:1 , 1:2}, {6:1})
        i0 = node(3, "i0",{},{0:1})
        i1 = node(4, "i1",{},{0:1})
        o0 = node(5,"o0",{1:1},{})
        o1 = node(6,"o1",{2:1},{})
        t = node(7,"t",{},{})
        nodes = [n0,n1,n2,i0,i1,o0,o1]
        d0 = open_digraph([3,4], [5,6], [n0,n1,n2,i0,i1,o0,o1])
        self.assertEqual(d0.inputs, [3,4])
        self.assertEqual(d0.outputs, [5,6])
        self.assertEqual(d0.nodes, {node.id:node for node in nodes})
        self.assertIsInstance(d0, open_digraph)
        self.assertEqual(d0.assert_is_well_formed(), True )

        # Test empty()
        d_vide = open_digraph.empty()
        self.assertIsInstance(d_vide, open_digraph)
        self.assertEqual(d_vide.inputs, [])
        self.assertEqual(d_vide.outputs, [])
        self.assertEqual(d_vide.nodes, {})

        # Test copy()
        d00 = d0.copy()
        d0.inputs = [3,1]
        d00.nodes[7] = t
        d0.nodes[0].set_label("test")
        self.assertIsNot(d00.inputs,d0.inputs)
        self.assertEqual(d00.nodes[7].get_id(), 7)
        self.assertEqual(len(d00.nodes), 8)
        self.assertEqual(len(d0.nodes), 7)
        self.assertEqual(d0.nodes[0].get_label(), "test")
        self.assertEqual(d00.nodes[0].get_label(), "a")
        d0.inputs = [3,4]
        d0.nodes[0].set_label("a")

        # Test getteurs
        self.assertEqual(d0.get_input_ids(), [3,4])
        self.assertEqual(d0.get_output_ids(), [5,6])
        self.assertEqual(d0.get_id_node_map(), {node.id:node for node in nodes})
        self.assertEqual(d0.get_nodes(), [n0,n1,n2,i0,i1,o0,o1])
        self.assertEqual(d0.get_node_ids(), [0,1,2,3,4,5,6])
        self.assertEqual(d0.get_node_by_id(0), n0)
        self.assertEqual(d0.get_nodes_by_ids([0,2,4]), [n0,n2,i1])

        # Test new_id
        self.assertEqual(d0.new_id(),7 )

        # Test add_edge
        d0.add_edge(n0,n2)
        l = d0.get_nodes()
        self.assertEqual(l[0].get_children(),   {1:1, 2:2}) 
        self.assertEqual(l[2].get_parents(), {0:2 , 1:2} )

        # Test add_edges
        d0.add_edges([(0,2),(0,1)])
        l2 = d0.get_nodes()
        self.assertEqual(l2[0].get_children(), {1:2, 2:3}) 
        self.assertEqual(l2[2].get_parents(), {0:3 , 1:2} )
        self.assertEqual(l2[1].get_parents(), {0:2})

        # Test add_node
        g = open_digraph([], [], []) 
        g.add_node(label='A')
        g.add_node(label='B')
        g.add_node(label='C', parents={0: 2}, children={1: 3})
        self.assertEqual(g.inputs, [])
        self.assertEqual(g.outputs, [])
        l3 = g.get_nodes()
        self.assertEqual(l3[2].get_children(), {1:3})
        self.assertEqual(l3[2].get_parents(), {0:2})
        self.assertEqual(l3[0].get_children(), {2:2})
        self.assertEqual(l3[1].get_parents(), {2:3})
        self.assertEqual(l3[2].get_id(), 2)
        self.assertEqual(l3[2].get_label(), "C")

        # Test remove_edge
        g.remove_edge(0,2)
        self.assertEqual(l3[2].get_parents(), {0:1})
        self.assertEqual(l3[0].get_children(), {2:1})
        self.assertEqual(g.assert_is_well_formed(), True )

        # Test remove_edges
        g.remove_parallel_edges(2,1)
        self.assertEqual(l3[2].get_children(), {})
        self.assertEqual(l3[1].get_parents(), {})
        self.assertEqual(g.assert_is_well_formed(), True )

        # Test remove_node_by_id
        self.assertEqual(len(l3), 3)
        g.remove_node_by_id(2)
        l33 = g.get_nodes()
        self.assertEqual(len(l33), 2)
        self.assertEqual(l33[0].get_id(), 0)
        self.assertEqual(l33[1].get_id(), 1)
        self.assertEqual(l33[0].get_children(), {})
        self.assertEqual(g.assert_is_well_formed(), True )

        # Test remove_edges
        gr = open_digraph([], [], [])
        gr.add_node(label='A') 
        gr.add_node(label='B') 
        gr.add_node(label='C', parents={0: 2}, children={1: 3}) 
        gr.add_node(label='D', parents={0: 1, 2: 2}, children={}) 
        gr.add_node(label='E', parents={3: 3, 0: 4}, children={1: 2}) 
        gr.remove_edges([(0,4),(2,3)])
        lgr = gr.get_nodes()
        self.assertEqual(lgr[0].get_children(),{2: 2, 3: 1, 4: 3})
        self.assertEqual(lgr[4].get_parents(),{3: 3, 0: 3})
        self.assertEqual(lgr[2].get_children(),{1:3, 3:1})
        self.assertEqual(lgr[3].get_parents(),{0: 1, 2: 1})
        self.assertEqual(gr.assert_is_well_formed(), True )

        # Test remove_several_parallel_edges
        gr.remove_several_parallel_edges([(0,4),(2,3),(0,2)])
        self.assertEqual(lgr[0].get_children(),{ 3: 1})
        self.assertEqual(lgr[3].get_parents(),{0: 1})
        self.assertEqual(lgr[4].get_parents(),{3: 3})
        self.assertEqual(gr.assert_is_well_formed(), True )

        # Test removes_nodes_by_id
        gr.remove_nodes_by_id([0, 3])
        lgr2 = gr.get_nodes()
        self.assertEqual(len(lgr2), 3)
        self.assertEqual(lgr[0].get_children(),{})
        self.assertEqual(lgr[4].get_parents(),{})
        self.assertEqual(gr.assert_is_well_formed(), True )

        # Test is_well_formed
        a = node(0, 'a', {3:1 , 2:1, 4:1}, {1:1, 2:1})
        b = node(1, 'b', {0:1}, { 5:1, 2:2})
        c = node(2, 'c', {0:1 , 1:2}, {0:1, 6:1})
        d = node(3, 'd',{},{0:1})
        e = node(4, 'e',{},{0:1})
        f = node(5, 'f',{1:1},{})
        g = node(6, 'g',{2:1},{})
        gra_well = open_digraph([3,4], [5,6],[a,b,c,d,e,f,g])
        self.assertEqual(d0.assert_is_well_formed(), True )
        self.assertEqual(gra_well.assert_is_well_formed(), True )

        #Test save_as_dot_file et from_dot_file
        gra_well.save_as_dot_file("doc_test")
        graFromDot = gra_well.from_dot_file("doc_test")
        self.assertEqual(graFromDot.assert_is_well_formed(), True )
        graFromDot.save_as_dot_file("doc_test2")
        gra_well.display("gra_well.pdf")

        # Test add_input_node et add_output_node
        gra_well.add_input_node(3)
        self.assertEqual(gra_well.get_input_ids(),[4,7])
        self.assertEqual(gra_well.assert_is_well_formed(), True )
        gra_well.add_input_node(5)
        self.assertEqual(gra_well.get_input_ids(),[4,7,8])
        gra_well.add_output_node(5)
        self.assertEqual(gra_well.get_output_ids(),[6,9])
        self.assertEqual(gra_well.assert_is_well_formed(), True )

        # Test copy 2
        n0 = node(0, 'a', {3:1 , 2:1}, {1:1, 2:1})
        n1 = node(1, 'b', {0:1}, {2:1 , 5:1})
        n2 = node(2, 'c', {0:1 , 1:2}, {0:1})
        d0 = open_digraph([3,4], [5,6], [n0,n1,n2])
        d02 = d0.copy()
        d0.add_edges([(0,2),(0,1)])
        d0.inputs.append(5)
        l1 = d02.get_nodes()
        l2 = d0.get_nodes()
        self.assertEqual(l2[0].get_children(), {1:2, 2:2}) 
        self.assertEqual(l2[2].get_parents(), {0:2 , 1:2} )
        self.assertEqual(l2[1].get_parents(), {0:2})
        self.assertEqual(l1[0].get_children(), {1:1, 2:1}) 
        self.assertEqual(l1[2].get_parents(), {0:1 , 1:2} )
        self.assertEqual(l1[1].get_parents(), {0:1})
        self.assertIsNot(d0.get_input_ids(), d02.get_input_ids())

        # test random
        d0i = open_digraph.random(5 , 10, inputs=0, outputs=0, loop_free=False, DAG=False,oriented=False, undirected=True)
        d2i = open_digraph.random(5 , 10, inputs=0, outputs=0, loop_free=False, DAG=False,oriented=True, undirected=False)
        d3i = open_digraph.random(5 , 10, inputs=0, outputs=0, loop_free=False, DAG=True,oriented=False, undirected=False)
        d0i2 = open_digraph.random(5 , 10, inputs=0, outputs=0, loop_free=True, DAG=False,oriented=False, undirected=True)
        d2i2 = open_digraph.random(5 , 10, inputs=0, outputs=0, loop_free=True, DAG=False,oriented=True, undirected=False)
        d3i2 = open_digraph.random(5 , 10, inputs=0, outputs=0, loop_free=True, DAG=True,oriented=False, undirected=False)
        gr = graph_from_adjacency_matrix([
        [0, 1, 1, 0, 0],
        [0, 0, 0, 1, 2],
        [0, 0, 0, 2, 0],
        [1, 0, 0, 0, 1],
        [0, 0, 0, 0, 0]
         ])
        self.assertEqual(gr.assert_is_well_formed(), True )
        self.assertEqual(d0i.assert_is_well_formed(), True )
        self.assertEqual(d2i.assert_is_well_formed(), True )
        self.assertEqual(d3i.assert_is_well_formed(), True )
        self.assertEqual(d0i2.assert_is_well_formed(), True )
        self.assertEqual(d2i2.assert_is_well_formed(), True )
        self.assertEqual(d3i2.assert_is_well_formed(), True )

        # test graph_to_dico()
        dico_test = d0.graph_to_dico()
        self.assertEqual(dico_test,{0:0,1:1,2:2})

        # test adjacency_matrix()
        n0 = node(0, 'a', {3:1 , 4:1}, {1:1, 2:1})
        n1 = node(1, 'b', {0:1}, {2:2 , 5:1})
        n2 = node(2, 'c', {0:1 , 1:2}, {6:1})
        i0 = node(3, "i0",{},{0:1})
        i1 = node(4, "i1",{},{0:1})
        o0 = node(5,"o0",{1:1},{})
        o1 = node(6,"o1",{2:1},{})
        d0 = open_digraph([3,4], [5,6], [n0,n1,n2,i0,i1,o0,o1])
        self.assertEqual(d0.assert_is_well_formed(), True )
        self.assertEqual(d0.adjacency_matrix(),[[0, 1, 1, 0, 0, 0, 0], [0, 0, 2, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]])
        
        # Test bool_circ
        #bb = bool_circ(d0)
        # bb = bool_circ(n0) renvoie une erreur car pas un graph
        # Test is_cyclic()
        n0 = node(0, 'a', {3: 1, 4: 1}, {1: 1, 2: 1})
        n1 = node(1, 'b', {0: 1}, {2: 2, 5: 1})
        n2 = node(2, 'c', {0: 1, 1: 2}, {6: 1})
        i0 = node(3, "i0", {}, {0: 1})
        i1 = node(4, "i1", {}, {0: 1})
        o0 = node(5, "o0", {1: 1}, {})
        o1 = node(6, "o1", {2: 1}, {})
        g1 = open_digraph([3,4],[5,6],[n0, n1, n2, i0, i1, o0, o1] )
        self.assertEqual(g1.is_cyclic(), False)
        n0 = node(0, 'a', {3: 1, 4: 1, 6:1}, {1: 1, 2: 1})
        n1 = node(1, 'b', {0: 1}, {2: 2, 5: 1})
        n2 = node(2, 'c', {0: 1, 1: 2}, {6: 1})
        i0 = node(3, "i0", {}, {0: 1})
        i1 = node(4, "i1", {}, {0: 1})
        o0 = node(5, "o0", {1: 1}, {})
        o1 = node(6, "o1", {2: 1}, {0:1})
        g2 = open_digraph([3,4],[5,6],[n0, n1, n2, i0, i1, o0, o1] )
        self.assertEqual(g2.is_cyclic(), True)
        # Test is_well_formed pour circuit boléen
        #b2 = bool_circ(g2)
        #self.assertEqual(b2.is_well_formed_cyclic(), False)
        # Graphe où une porte "copie" (nœud avec label '') a un degré entrant != 1
        n0 = node(0, '', {3: 1, 4: 1, 6: 1}, {1: 1, 2: 1})  # Nœud de type "copie"
        n1 = node(1, '&', {0: 1}, {2: 2, 5: 1})  # Porte ET
        n2 = node(2, '|', {0: 1, 1: 2}, {6: 1})  # Porte OU
        i0 = node(3, "i0", {}, {0: 1})  # Entrée
        i1 = node(4, "i1", {}, {0: 1})  # Entrée
        o0 = node(5, "o0", {1: 1}, {})  # Sortie
        o1 = node(6, "o1", {2: 1}, {0: 1})  # Sortie
        gtest1 = open_digraph([3, 4], [5, 6], [n0, n1, n2, i0, i1, o0, o1])
        #b1 = bool_circ(gtest1)
        #self.assertEqual(b1.is_well_formed_cyclic(), False)
        # Graphe où une porte ET/OU a un degré sortant != 1
        n0 = node(0, '', {4: 1}, {1: 1, 2: 1}) 
        n1 = node(1, '&', {0: 1}, {2: 2, 5: 2})
        n2 = node(2, '|', {0: 1, 1: 2}, {6: 1}) 
        i1 = node(4, "i1", {}, {0: 1})  
        o0 = node(5, "o0", {1: 2}, {})  
        o1 = node(6, "o1", {2: 1}, {}) 
        gtest2 = open_digraph([4], [5, 6], [n0, n1, n2, i1, o0, o1])
        #bt2 = bool_circ(gtest2)
        #self.assertEqual(bt2.is_well_formed_cyclic(), False)
        # Graphe respectant toutes les conditions
        n0 = node(0, '', {4: 1}, {1: 1, 2: 1}) 
        n1 = node(1, '&', {0: 1}, { 5: 1})
        n2 = node(2, '|', {0: 1}, {6: 1})  
        i1 = node(4, "i1", {}, {0: 1})  
        o0 = node(5, "o0", {1: 1}, {})  
        o1 = node(6, "o1", {2: 1}, {})  
        gtest3 = open_digraph([4], [5, 6], [n0, n1, n2, i1, o0, o1])
        #b3 = bool_circ(gtest3)
        #self.assertEqual(b3.is_well_formed_cyclic(), True)

        # Test min_id() et max_id()
        n0 = node(0, 'a', {3:1 , 4:1}, {1:1, 2:1})
        n1 = node(1, 'b', {0:1}, {2:2 , 5:1})
        n2 = node(2, 'c', {0:1 , 1:2}, {6:1})
        i0 = node(3, "i0",{},{0:1})
        i1 = node(4, "i1",{},{0:1})
        o0 = node(5,"o0",{1:1},{})
        o1 = node(6,"o1",{2:1},{})
        exo67 = open_digraph([3,4], [5,6], [n0,n1,n2,i0,i1,o0,o1])
        maxi = exo67.max_id()
        self.assertEqual(maxi,6)
        mini = exo67.min_id()
        self.assertEqual(mini,0)

        # Test shift_indices()
        exo67.shift_indices(2)
        liste_n = exo67.get_nodes()
        for i in range(len(liste_n)):
            self.assertEqual(liste_n[i].get_id(), i + 2)
        self.assertEqual(exo67.assert_is_well_formed(), True )
        
        #Test iparallel et parallel 
        n0 = node(0, 'a', {3: 1}, {1: 1, 2: 1})
        n1 = node(1, 'b', {0: 1}, {2: 2})
        n2 = node(2, 'c', {0: 1, 1: 2}, {4: 1})
        n3 = node(3, 'd', {}, {0: 1})
        n4 = node(4, 'e', {2:1}, {})
        g = open_digraph([3],[4],[n0, n1, n2, n3, n4] )
        self.assertEqual(g.assert_is_well_formed(), True)
        i0 = node(0, "i0", {3: 1}, {1: 1, 2: 1})
        i1 = node(1, "i1", {0: 1}, {2: 2})
        i2 = node(2, "i2", {0: 1, 1: 2}, {4: 1})
        i3 = node(3, "i3", {}, {0: 1})
        i4 = node(4, "i4", {2:1}, {})
        g1 = open_digraph([3],[4],[i0, i1, i2, i3, i4] )
        self.assertEqual(g1.assert_is_well_formed(), True)
        g_vide = open_digraph([],[],[] )
        self.assertEqual(g_vide.assert_is_well_formed(), True)
        g.iparallel(g_vide)
        #g.display("test_iparallel_elmntneutregrphvide.pdf")
        g.iparallel(g1)
        self.assertEqual(g.assert_is_well_formed(), True)
        #g.display("test_iparallel.pdf")
        #g1.display("test_iparallel_pasdemodif.pdf")
        t0 = node(0, "t0", {}, {1: 1})
        t1 = node(1, "t1", {0: 1}, {})
        gtest = open_digraph([0],[1],[t0, t1] )
        gpar = gtest.parallel(g, g1)
        self.assertEqual(gpar.assert_is_well_formed(), True)
        #gpar.display("test_parallel.pdf")
        #g.display("test_iparallel2.pdf")
        #g1.display("test_iparallel_pasdemodif2.pdf")

        #Test icompose et compose 
        n0 = node(0, 'a', {3: 1}, {1: 1, 2: 1})
        n1 = node(1, 'b', {0: 1}, {2: 2})
        n2 = node(2, 'c', {0: 1, 1: 2}, {4: 1})
        n3 = node(3, 'd', {}, {0: 1})
        n4 = node(4, 'e', {2:1}, {})
        g = open_digraph([3],[4],[n0, n1, n2, n3, n4] )
        self.assertEqual(g.assert_is_well_formed(), True)
        g_neutre = g.identity(1)
        #g_neutre.display("grphidentity.pdf")
        self.assertEqual(g_neutre.assert_is_well_formed(), True)
        g.icompose(g_neutre)
        #g.display("test_icompose_elmntneutregrphidentity.pdf")
        i0 = node(0, "i0", {3: 1}, {1: 1, 2: 1})
        i1 = node(1, "i1", {0: 1}, {2: 2})
        i2 = node(2, "i2", {0: 1, 1: 2}, {4: 1})
        i3 = node(3, "i3", {}, {0: 1})
        i4 = node(4, "i4", {2:1}, {})
        g1 = open_digraph([3],[4],[i0, i1, i2, i3, i4] )
        self.assertEqual(g1.assert_is_well_formed(), True)
        #g.display("g.pdf")
        #g1.display("g1.pdf")
        g.icompose(g1)
        self.assertEqual(g.assert_is_well_formed(), True)
        #g.display("test_icompose.pdf")
        #g1.display("test_icompose_pasdemodifdansgraphe2.pdf")
        n0 = node(0, 'a', {3: 1}, {1: 1, 2: 1})
        n1 = node(1, 'b', {0: 1}, {2: 2})
        n2 = node(2, 'c', {0: 1, 1: 2}, {4: 1})
        n3 = node(3, 'd', {}, {0: 1})
        n4 = node(4, 'e', {2:1}, {})
        g = open_digraph([3],[4],[n0, n1, n2, n3, n4] )
        self.assertEqual(g.assert_is_well_formed(), True)
        i0 = node(0, "i0", {3: 1}, {1: 1, 2: 1})
        i1 = node(1, "i1", {0: 1}, {2: 2})
        i2 = node(2, "i2", {0: 1, 1: 2}, {4: 1})
        i3 = node(3, "i3", {}, {0: 1})
        i4 = node(4, "i4", {2:1}, {})
        g1 = open_digraph([3],[4],[i0, i1, i2, i3, i4] )
        self.assertEqual(g1.assert_is_well_formed(), True)
        t0 = node(0, "t0", {}, {1: 1})
        t1 = node(1, "t1", {0: 1}, {})
        gtest = open_digraph([0],[1],[t0, t1] )
        #gtest.display("gtest.pdf")
        #g.display("g.pdf")
        #g1.display("g1.pdf")
        self.assertEqual(gtest.assert_is_well_formed(), True)
        gcomp = gtest.compose(g, g1)
        self.assertEqual(gcomp.assert_is_well_formed(), True)
        self.assertEqual(gtest.assert_is_well_formed(), True)
        #gcomp.display("gcomp.pdf")
        #gtest.display("gtestsansmodif.pdf")
        #g.display("gsansmodif.pdf")
        #g1.display("g1sansmodif.pdf")

        # Test identity(n)

        g = open_digraph.identity(3)
        self.assertEqual(g.assert_is_well_formed(), True)

        # Test connected_components()

        n1 = node(1, "N1", {}, {2: 1})
        n2 = node(2, "N2", {1: 1}, {3: 1})
        n3 = node(3, "N3", {2: 1}, {})
        n4 = node(4, "N4", {}, {})
        n5 = node(5, "N5", {}, {6: 1})
        n6 = node(6, "N6", {5: 1}, {})
        g = open_digraph([5], [6], [n1,n2,n3,n4,n5,n6])
        nbr, dico = g.connected_components()
        self.assertEqual(nbr,3)
        self.assertEqual(dico[1],0)
        self.assertEqual(dico[2],0)
        self.assertEqual(dico[3],0)
        self.assertEqual(dico[4],1)
        self.assertEqual(dico[5],2)
        self.assertEqual(dico[6],2)

        # Test list_op
    
        n1 = node(1, "N1", {}, {2: 1})
        n2 = node(2, "N2", {1: 1}, {3: 1})
        n3 = node(3, "N3", {2: 1}, {})
        n4 = node(4, "N4", {}, {})
        n5 = node(5, "N5", {}, {6: 1})
        n6 = node(6, "N6", {5: 1}, {})
        g = open_digraph([5], [6], [n1,n2,n3,n4,n5,n6])
        self.assertEqual(g.assert_is_well_formed(), True)
        l = g.liste_op()
        c1 = open_digraph([1], [3], [n1, n2, n3])
        c2 = open_digraph([], [], [n4])
        c3 = open_digraph([5], [6], [n5, n6])
        self.assertEqual(l[0].get_input_ids(), c1.get_input_ids())
        self.assertEqual(l[1].get_input_ids(), c2.get_input_ids())
        self.assertEqual(l[2].get_input_ids(), c3.get_input_ids())
        self.assertEqual(l[0].assert_is_well_formed(), True)
        self.assertEqual(l[1].assert_is_well_formed(), True)
        self.assertEqual(l[2].assert_is_well_formed(), True)


        #Test Dijkstra Djikstra 2 et shortest_path
        n0 = node(0, 'a', {3: 1}, {1: 1, 2: 1})
        n1 = node(1, 'b', {0: 1}, {2: 2})
        n2 = node(2, 'c', {0: 1, 1: 2}, {4: 1})
        n3 = node(3, 'd', {}, {0: 1})
        n4 = node(4, 'e', {2:1}, {})
        n5 = node(5, 'f', {}, {})
        g = open_digraph([3],[4],[n0, n1, n2, n3, n4, n5] )
        self.assertEqual(g.assert_is_well_formed(), True)
        print("test Dijkstra")
        print(g.Dijkstra(n0.get_id()))
        print(g.Dijkstra2(n0.get_id(), tgt = n1.get_id()))
        print(g.shortest_path(n0.get_id(),n5.get_id()))

        # Test ancetres
        n0 = node(0, 'a', {}, {3: 1})
        n1 = node(1, 'b', {}, {5:1, 8:1, 4:1})
        n2 = node(2, 'c', {}, {4: 1})
        n3 = node(3, 'd', {0:1}, {7:1,5:1,6:1})
        n4 = node(4, 'e', {2:1,1:1}, {6:1})
        n5 = node(5, 'f', {3:1,1:1}, {7:1})
        n6 = node(6, 'g', {4:1,3:1}, {8:1,9:1})
        n7 = node(7, 'h', {3:1,5:1}, {})
        n8 = node(8, 'ei', {6:1,1:1}, {})
        n9 = node(9, 'j', {6:1}, {})
        g = open_digraph([],[],[n0, n1, n2, n3, n4, n5,n6,n7,n8,n9] )
        self.assertEqual(g.assert_is_well_formed(), True)
        print("test Ancetres\n")
        print(g.ancetres(5,8))

        #Test tri_topologique
        n0 = node(1, "N0", {}, {3: 1})
        n1 = node(1, "N1", {}, {5: 1, 4:1, 8:1})
        n2 = node(2, "N2", {}, {4: 1})
        n3 = node(3, "N3", {0: 1}, {7:1, 5:1, 6:1})
        n4 = node(4, "N4", {1:1, 2:1}, {6:1})
        n5 = node(5, "N5", {3:1, 1:1}, {7: 1})
        n6 = node(6, "N6", {3: 1, 4:1}, {8:1, 9:1})
        n7 = node(7, "N7", {3:1, 5:1}, {})
        n8 = node(8, "N8", {1: 1, 6:1}, {})
        n9 = node(9, "N9", {6: 1}, {})
        g = open_digraph([0, 2], [7], [n1,n2,n3,n4,n5,n6,n7,n8,n9])
        #self.assertEqual(g.assert_is_well_formed(), True)
        #self.assertEqual(g.tri_topologique(), [[n0,n1,n2], [n3,n4], [n5,n6], [n7,n8,n9]])
        
        # Test bool
        #h = bool_circ.parse_parentheses("((x0)&((x1)&(x2)))|((x1)&(~(x2)))")
        #print(h)

        # Test fusion noeud
        n0 = node(0, 'a', {}, {3: 1})
        n1 = node(1, 'b', {}, {5:1, 8:1, 4:1})
        n2 = node(2, 'c', {}, {4: 1})
        n3 = node(3, 'd', {0:1}, {7:1,5:1,6:1})
        n4 = node(4, 'e', {2:1,1:1}, {6:1})
        n5 = node(5, 'f', {3:1,1:1}, {7:1})
        n6 = node(6, 'g', {4:1,3:1}, {8:1,9:1})
        n7 = node(7, 'h', {3:1,5:1}, {})
        n8 = node(8, 'ei', {6:1,1:1}, {})
        n9 = node(9, 'j', {6:1}, {})
        g = open_digraph([],[],[n0, n1, n2, n3, n4, n5,n6,n7,n8,n9] )
        self.assertEqual(g.assert_is_well_formed(), True)
        g.fusion_noeuds(8,9,"nv")
        self.assertEqual(g.assert_is_well_formed(), True)

        """
        Tests bool_circ 

        """

        # Test parenthèses
        expr = "((~(( (x1))&(x2)))|(x2))"
        circuit = bool_circ.parse_parentheses(expr)
        circuit[0].display("pp")
        expr1 = "(((x0)&((x1)&(x2)))|((x1)&(~(x2))))"
        expr2 = "(((x0)&(~(x1)))|(x2))"
        g = bool_circ.parse_parentheses(expr1,expr2)
        g[0].display("pp2")
        print(g[1])

        # Test int_bin
        g = bool_circ.int_bin(11,8)
        g.display('bin')

        # Test evaluate

        # On test toutes les méthodes de simplification
        cop1 = "( (1))" #ok
        cop0 = "( (0))" #ok
        non1 = "(~(1))" #ok
        non0 = "(~(0))" #ok
        et1 = "((x1)&(x2)&(1))" #ok
        et0 = "((x1)&(x2)&(0))" #ok
        ou1 = "((x1)|(x2)|(1))" #ok 
        ou0 = "((x1)|(x2)|(0))"  #ok 
        xor1 = "((x1)^(x2)^(1))" #ok 
        xor0 = "((x1)^(x2)^(0))" #ok
        
        g = bool_circ.parse_parentheses(cop1,cop0,non1,non0,et1,et0,ou1,ou0,xor1,xor0)
        g[0].display("avant_simply")
        g[0].evaluate()
        g[0].display("apres_simply")
        
        # Test additionneur : On fait les calculs pour avoir le résultat final dans le noeud parent du noeud res
        e = '(((1)&(0))&(0))','(((1)&(1))&(0))','(((1)&(1))&(1))'
        # Test sur les entiers 11 et 01 , res = 01
        # Test sur les entiers 111 et 011 et 001 , res = 001
        g = bool_circ.parse_parentheses(e[0],e[1], e[2])
        g[0].display("add")
        g[0].evaluate()
        g[0].display("add_apres")




if __name__ == '__main__' : # the following code is called only when
    unittest.main()         # precisely this file is run


class NodeTest(unittest.testcase):
    def setUp(self):
        self.n0 = node(0, 'a', [], [1])
    def test_get_id(self):
        self.assertEqual(self.n0.get_id(), 0)
    def test_get_label(self):
        self.assertEqual(self.n0.get_label(), 'a')


class BoolCircTest(unittest.testcase):
    def test_hamming_identity(self):
        print("TEST CODE DE HAMMING")

        # Étape 1 : Créer le message à encoder
        original = bool_circ.int_bin(6, 4)  # 0110

        # Étape 2 : Encoder
        enc = bool_circ.encoder()
        encoded = enc.compose_with(original)

        # Étape 3 : Simuler une erreur (inversion d’un bit)
        nodes = encoded.get_nodes()
        for node in nodes:
            if node.get_label() in ['0', '1']:
                id_ = node.id
                # Ajouter une porte NON (~~) au-dessus
                not_node = node.__class__(9999, '~~', {id_: 1}, {})
                encoded.add_node(not_node)
                encoded.add_edge(not_node.id, id_)
                break

        # Étape 4 : Décoder
        dec = bool_circ.decoder()
        result = dec.compose_with(encoded)

        # Étape 5 : Appliquer les réécritures
        result.rewrite_all()
        result.display("Final")

        # Pas d’assertion automatique ici, mais affichage du graphe corrigé

            