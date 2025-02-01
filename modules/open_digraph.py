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
        return node(int(self.id),str(self.label),dict(self.parents), dict(self.children))
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
    def remove_parent_once(self, id):
        """
        id : int; id du noeud
        retire une occurence de l'id donné en paramètre
        """ 
        if id in self.parents :
            self.parents[id]-= 1
        if self.parents[id] == 0 :
            self.parents.pop(id)
     
    def remove_child_once(self, id):
        """
        id : int; id du noeud
        retire une occurence de l'id donné en paramètre
        """ 
        if id in self.children :
            self.children[id]-= 1
        if self.children[id] == 0 :
            self.children.pop(id)
    def remove_parent_id(self, id):
        """
        id : int; id du noeud
        retire toutes les occurences de l'id donné en paramètre

        """ 
        if id in self.parents :
            self.parents.pop(id)
     
    def remove_child_id(self, id):
        """
        id : int; id du noeud
        retire toutes les occurences de l'id donné en paramètre

        """ 
        if id in self.children :
            self.children.pop(id)


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
    def copy(self):
        """
        renvoie une copie du open_digraph 
        """
        d = open_digraph( [], [], [] )
        d.inputs = list(self.inputs)
        d.outputs = list(self.outputs)
        dico = self.nodes
        new_dico = {}
        for n in dico:
            new_dico[n] = dico[n].copy()
        d.nodes = new_dico
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
        self.inputs.append(idi)
    def add_output_id(self,ido):
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
            src_node = self.get_node_by_id(src_id)
            tgt_node = self.get_node_by_id(tgt_id)
            self.add_edge(src_node, tgt_node)
    def add_node(self, label = "", parents = None, children = None):
        """
        label : string ; label du noeud, rien par défaut
        parents : int dict; noeuds du parent
        children : int dict; noeud de l'enfant
        rajoute un noeud au graphe et le lie avec les noeuds d'ids parents et children.
        Si None : attribue un dictionnaire vide.
        renvoie l'id du nouveau noeud
        """
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
    def remove_edge(self,src,tgt):
        """
        src : int ; id du noeud source
        tgt : int ; id du noeud target
        retire une arrête entre le noeud source et le noeud target
        """
        s = self.get_node_by_id(src)
        t = self.get_node_by_id(tgt)
        s.remove_child_once(tgt)
        t.remove_parent_once(src)
    def remove_parallel_edges(self,src,tgt):
        """
        src : int ; id du noeud source
        tgt : int ; id du noeud target
        retire toutes les arrêtes entre le noeud source et le noeud target
        """
        s = self.get_node_by_id(src)
        t = self.get_node_by_id(tgt)
        s.remove_child_id(tgt)
        t.remove_parent_id(src)
    def remove_node_by_id(self,n):
        """
        n : int ; id du noeud à supprimer
        supprime le noeud d'id n dans le graphe
        """
        for nd in self.nodes :
            snd = self.get_node_by_id(nd)
            if n in snd.get_children():
                self.remove_parallel_edges(nd,n)
            if n in snd.get_parents():
                self.remove_parallel_edges(n,nd)
        self.nodes.pop(n)
    def remove_edges(self,liste):
        """
        liste : (int*int) list; liste de paires (src,tgt)
        retire une arrête entre toutes les paires (src,tgt)
        """
        for src_id,tgt_id in liste:
            self.remove_edge(src_id,tgt_id)
    def remove_several_parallel_edges(self,liste):
        """
        liste : (int*int) list; liste de paires (src,tgt)
        retire toutes les arrêtes entre toutes les paires (src,tgt)
        """
        for src_id,tgt_id in liste:
            self.remove_parallel_edges(src_id,tgt_id)
    def is_well_formed(self):
        inps = self.get_input_ids()
        outs = self.get_output_ids()
        for el in inps:
            if len(el.get_children()) != 1 or len(el.get_parents()) != 0:
                raise Exception("un noeud input n'a pas un unique enfant ou a un parent")
        for el in outs:
            if len(el.get_children()) != 0 or len(el.get_parents()) != 1:
                raise Exception("un nselfoeud output n'a pas d'unique parent ou a un fils au moins")
        nodes = self.get_nodes()
        inpout = inps + outs
        for ids in inpout:
            if ids not in nodes:
                raise Exception("tous les noeuds de inputs et outputs ne sont pas dans le graphe")
        for el in nodes:
            if el != nodes[el].get_id():
                raise Exception("chaque clé de nodes ne pointe pas vers un noeud d'id la clé")
        for el in nodes :
            children = nodes[el].get_children()
            for c in children :
                parents = children[c].get_parents()
                if el not in parents:
                    raise Exception("le parent ne figure pas dans la liste de parents de l'enfant")
                if parents[el] != children[c]:
                    raise Exception("pas la bonne multiplicité")
        for el in nodes :
            parents = nodes[el].get_parents()
            for p in parents :
                children = parents[p].get_children()
                if el not in children:
                    raise Exception("l'enfant ne figure pas dans la liste d'enfants du parent")
                if children[el] != parents[p]:
                    raise Exception("pas la bonne multiplicité")
        

