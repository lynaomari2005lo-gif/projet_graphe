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
    def copy(self):
        """
        renvoie une copie du node 
        """
        return node(self.id,self.label,self.parents,self.children)
    def get_id(self):
        return self.id
    def get_label(self):
        return self.label
    def get_parents(self):
        return self.parents
    def get_children(self):
        return self.children
    def set_id(self,id1):
        self.id = id1
    def set_label(self,lab):
        self.label = lab
    def set_parents(self,p):
        self.parents = p 
    def set_children(self,c):
        self.children = c 
    def add_child_id(self,n):
        if(n in self.children):
            self.children[n] += 1
        else:
            self.children[n] = 1
    def add_parent_id(self,n):
        if(n in self.parents):
            self.parents[n] += 1
        else:
            self.parents[n] = 1

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
        """
        renvoie un graphe vide
        """
        return open_digraph( [], [], [] )
    def copy(self): #Poser la question si on doit copier les noeuds aussi car si on modifie les edges ça modifie aussi
        """
        renvoie une copie du open_digraph 
        """
        d = open_digraph( [], [], [] )
        d.inputs = self.inputs
        d.outputs = self.outputs
        d.nodes = self.nodes
        return d
    def get_input_ids(self):
        return self.inputs
    def get_output_ids(self):
        return self.outputs
    def get_id_node_map(self):
        return self.nodes
    def get_nodes(self):
        return [self.nodes[n] for n in self.nodes]
    def get_node_ids(self):
        return [n for n in self.nodes]
    def get_node_by_id(self, i):
        return self.nodes[i]
    def get_nodes_by_ids(self,liste_id): #renvoie une liste de noeuds à partir d'une liste d'ids
        return [self.nodes[i] for i in liste_id]
    def set_inputs(self,l):
        self.inputs = l
    def set_outputs(self,l):
        self.outputs = l
    def add_input_id(self,idi):
        self.inputs.append(ido)
    def add_output_id(self,idi):
        self.outputs.append(ido)
    def new_id(self):
        """
        renvoie un id non utilisé dans le graphe
        """
        id_n = self.get_node_ids()
        next_id = 0
        while next_id in id_n:
            next_id += 1
        return next_id
    def add_edge(self,src,tgt):
        """
        src : node ; noeud source
        tgt : node ; noeud target
        rajoute une arrête du noeud d'id src au noeud d'id tgt
        """
        src.add_child_id(tgt.get_id())
        tgt.add_parent_id(src.get_id())
    def add_edges(self,edges):
        """
        edges : int tuple list; liste de paires d'id
        rajoute une arrête entre chacune des paires
        """
        for src_id,tgt_id in edges:
            src_node = self.nodes.get(src_id)
            tgt_node = self.nodes.get(tgt_id)
            self.add_edge(src_node, tgt_node)
    def add_node(self, label = "", parents = None, children = None):
        if parents is None:
            parents = {}
        if children is None:
            children = {}
        new_id = self.new_id()
        new_node = node(new_id, label, parents, children)
        self.nodes[new_id] = new_node

        for parent_id, mul in parents.items():
            if parent_id in self.nodes:
                parent_node = self.nodes[parent_id]
                for i in range(mul):
                    parent_node.add_child_id(new_id)

        for child_id, mul in children.items():
            if child_id in self.nodes:
                child_node = self.nodes[child_id]
                for j in range(mul):
                    child_node.add_parent_id(new_id)

