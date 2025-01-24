class node:
    def __init__(self, identity, label, parents, children):
        """
        identity : int; its unique id in the graph
        label : string;
        parents : int->int dict; maps a parent node's id to its multiplicity
        children : int->int dict; maps a child node's id to its multiplicity
        """
        self.id = identity
        self.label = label
        self.parents = parents
        self.children = children
    def __str__(self):
        parents_s = ""
        children_s = ""
        for p in self.parents:
             parents_s += "id du parent :" + str(p) +" ,nombre de liens : " + str(self.parents[p]) + "\n"
        for c in self.children:
             children_s += "id de l'enfant :" + str(c) +" ,nombre de liens : " + str(self.children[c]) + "\n"
        chaine = "id : " + str(self.id) + "\n" + "label : " + self.label + "\n" + "parents : \n" + parents_s + "enfants : \n" + children_s + "\n"
        return chaine
    def __repr__(self):
        return str(self)

class open_digraph : # for open directed graph
    def __init__(self, inputs, outputs, nodes):
        """
        inputs : int list ; the ids of the input nodes
        outputs: int list; the ids of the output nodes
        nodes: node iter;
        """
        self.inputs = inputs
        self.outputs = outputs
        self.nodes = {node.id:node for node in nodes} # self.nodes: <int,node> dict
    def __str__(self):
        inputs_s = ""
        outputs_s = ""
        nodes_s = ""
        for i in range(len(self.inputs)):
            inputs_s += "id : " + str(self.inputs[i]) + "\n"
        for i in range(len(self.outputs)):
            outputs_s += "id : " + str(self.outputs[i]) + "\n"
        for i in range(len(self.nodes)):
            nodes_s += "id : " + str(self.nodes[i].id) + "\n"
        chaine = "ids of the input nodes : " + "\n" + inputs_s + "ids of the output nodes : " + "\n" + outputs_s + "ids of each node : " + nodes_s + "\n"
        return chaine
    def __repr__(self):
        return str(self)
    @classmethod 
    def empty(cls):
        return ( [], [], [] )


