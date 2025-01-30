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
        n0.label = "ii"
        self.assertIsNot(n00,n0)
        n0.label = "i"
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



    def test_init_open_digraph(self):
        n0 = node(0, 'a', {3:1 , 2:1}, {1:1, 2:1})
        n1 = node(1, 'b', {0:1}, {1:1 , 5:1})
        n2 = node(2, 'c', {0:1 , 1:2}, {0:1})
        i0 = node(3, "i0",{},{0:1})
        i1 = node(4, "i1",{},{0:1})
        o0 = node(5,"o0",{1:1},{})
        o1 = node(6,"o1",{2:1},{})
        nodes = [n0,n1,n2,i0,i1,o0,o1]
        d0 = open_digraph([3,4], [5,6], [n0,n1,n2,i0,i1,o0,o1])
        self.assertEqual(d0.inputs, [3,4])
        self.assertEqual(d0.outputs, [5,6])
        self.assertEqual(d0.nodes, {node.id:node for node in nodes})
        self.assertIsInstance(d0, open_digraph)
        # Test empty()
        d_vide = open_digraph.empty()
        self.assertIsInstance(d_vide, open_digraph)
        self.assertEqual(d_vide.inputs, [])
        self.assertEqual(d_vide.outputs, [])
        self.assertEqual(d_vide.nodes, {})
        # Test copy()
        d00 = d0.copy()
        d0.inputs = [3,1]
        self.assertIsNot(d00.inputs,d0.inputs)
        d0.inputs = [3,4]
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
        """
        d0.add_edge(n0,n2)
        l = d0.get_nodes()
        self.assertEqual(l[0].get_children(),   {1:1, 2:2}) 
        self.assertEqual(l[2].get_parents(), {0:2 , 1:2} )
        """
        # Test add_edges
        d00.add_edges([(0,2),(0,1)])
        l2 = d00.get_nodes()
        self.assertEqual(l2[0].get_children(), {1:2, 2:2}) 
        self.assertEqual(l2[2].get_parents(), {0:2 , 1:2} )
        self.assertEqual(l2[1].get_parents(), {0:2})
        # Test add_node
        g = open_digraph([], [], [])
        g.add_node(label='A')
        g.add_node(label='B')
        g.add_node(label='C', parents={0: 2}, children={1: 1})
        self.assertEqual(g.inputs, [])
        self.assertEqual(g.outputs, [])
        l3 = g.get_nodes()
        self.assertEqual(l3[2].get_children(), {1:1})
        self.assertEqual(l3[2].get_parents(), {0:2})
        self.assertEqual(l3[2].get_id(), 2)
        self.assertEqual(l3[2].get_label(), "C")




if __name__ == '__main__' : # the following code is called only when
    unittest.main()         # precisely this file is run


class NodeTest(unittest.testcase):
    def setUp(self):
        self.n0 = node(0, 'a', [], [1])
    def test_get_id(self):
        self.assertEqual(self.n0.get_id(), 0)
    def test_get_label(self):
        self.assertEqual(self.n0.get_label(), 'a')

