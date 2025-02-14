import sys
import os
root = os.path.normpath(os.path.join(__file__, "./../.."))
sys.path.append(root) # allows us to fetch files from the project root
import unittest
from modules.open_digraph import *


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
        gr.add_node(label='A') # p = {}  c = {2:2, 3:1, 4:4}
        gr.add_node(label='B') # p = {2:3, 4:2}  c = {}
        gr.add_node(label='C', parents={0: 2}, children={1: 3}) # p = {0:2}  c = {1:3, 3:2}
        gr.add_node(label='D', parents={0: 1, 2: 2}, children={}) # p = {0:1, 2:2}  c = {4:3}
        gr.add_node(label='E', parents={3: 3, 0: 4}, children={1: 2}) # p = {3: 3, 0: 4}  c = {1:2}
        gr.remove_edges([(0,4),(2,3)])
        # 0 : p = {}  c = {2:2, 3:1, 4:3}
        # 4 : p = {3: 3, 0: 3}  c = {1:2}
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
        self.assertEqual(d0.adjacency_matrix(),[[0, 1, 1, 0, 0, 0, 0], [0, 0, 2, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]])
        
        
        
       
        



if __name__ == '__main__' : # the following code is called only when
    unittest.main()         # precisely this file is run


class NodeTest(unittest.testcase):
    def setUp(self):
        self.n0 = node(0, 'a', [], [1])
    def test_get_id(self):
        self.assertEqual(self.n0.get_id(), 0)
    def test_get_label(self):
        self.assertEqual(self.n0.get_label(), 'a')

