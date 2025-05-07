# mixins/compositions_mx.py

class OpenDigraphCompositionsMixin:
    def copy(self):
        """
        renvoie une copie du open_digraph 
        """
        d = self.__class__([], [], [])
        d.inputs = list(self.inputs)
        d.outputs = list(self.outputs)
        dico = self.nodes
        new_dico = {}
        for n in dico:
            new_dico[n] = dico[n].copy()
        d.nodes = new_dico
        return d

    def new_id(self):
        """
        renvoie un id non utilisé dans le graphe
        """
        id_n = self.get_node_ids()
        next_id = 0
        while next_id in id_n:
            next_id += 1
        return next_id

    def add_edge(self, src, tgt):
        """
        src : node ; noeud source
        tgt : node ; noeud target
        rajoute une arrête du noeud d'id src au noeud d'id tgt
        """
        src.add_child_id(tgt.get_id())
        tgt.add_parent_id(src.get_id())

    def add_edges(self, edges):
        """
        edges : int tuple list; liste de paires d'id
        rajoute une arrête entre chacune des paires
        """
        for (src, tgt) in edges:
            self.nodes[src].add_child_id(tgt)
            self.nodes[tgt].add_parent_id(src)

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

    def remove_nodes_by_id(self,liste):
        """
        liste : (int) list; liste de id des noeuds à supprimer
        supprime les noeuds du graphe dont l'id est dans la liste
        """
        for id in liste:
             self.remove_node_by_id(id)
    
    def fusion_noeuds(self, id1, id2, label=None):
        node1 = self.get_node_by_id(id1)
        node2 = self.get_node_by_id(id2)
        nv_label = ""
        if label == None:
            nv_label = node1.get_label()
        else:
            nv_label = label
        for parent_id, mult in node2.get_parents().items():
            self.add_edges(parent_id, id1, mult)
        for child_id, mult in node2.get_children().items():
            self.add_edges(id1, child_id, mult)
        self.remove_node_by_id(id2)
        self.get_node_by_id(id1).set_label(nv_label)
    def compose(self, f, g):
        """
        f : open_digraph
        g : open_digraph
        méthode qui renvoie un nouveau graphe qui est la composition en séquence de f et g (sans modifier ces derniers)
        """
        ff = f.copy()
        ff.icompose(g)
        return ff
    def icompose(self, f):
        """
        g : open_digraph 
        méthode qui ajoute g à self avec un composition en séquence ( g n'est pas modifié) 
        """
        ff = f.copy()
        out_ff = ff.get_output_ids()
        inp_self = self.get_input_ids()
        if len(out_ff) != len(inp_self) :
            raise Exception("le nombre d'entrées du graphe ne coïncident pas avec le nombre de sorties du graphe donné en paramètre")
        else :
            nodes_self = self.get_nodes()
            n = len(nodes_self)
            ff.shift_indices(n)
            nodes_gg = ff.get_nodes()
            self.nodes.update(ff.get_nodes_dico())
            out_ff = ff.get_output_ids()
            for i in range(len(out_ff)) :
                self.add_edge(self.nodes[out_ff[i]],self.nodes[inp_self[i]])
            self.inputs = ff.get_input_ids()
    def shift_indices(self, n):
        """
        n : int, valeur à ajouter aux indices
        ajoute n à tous les indices du graphe, n peut être négatif
        """
        new_nodes = {}
        for node_id, node in self.nodes.items():
            new_id = node_id + n
            new_node = node.copy()
            new_node.set_id(new_id)
            new_node.set_parents({k + n: v for k, v in node.parents.items()})
            new_node.set_children({k + n: v for k, v in node.children.items()})
            new_nodes[new_id] = new_node
        self.nodes = new_nodes
        self.inputs = [i + n for i in self.inputs]
        self.outputs = [o + n for o in self.outputs]   
    def iparallel(self, g):
        """
        g : open_digraph 
        méthode qui ajoute g à self avec un composition en parallèle ( g n'est pas modifié) 
        """
        gg = g.copy()
        nodes_self = self.get_nodes()
        n = len(nodes_self)
        gg.shift_indices(n)
        nodes_gg = gg.get_nodes()
        if nodes_self == []:
            self.nodes = gg.get_nodes_dico()
        elif nodes_gg == [] :
            nodes_self = nodes_self
        else :
            self.nodes.update(gg.get_nodes_dico())
            self.add_edge(nodes_self[0], nodes_gg [0])

    def parallel(self,f, g):
        """
        f : open_digraph
        g : open_digraph
        méthode qui renvoie un nouveau graphe qui est la composition en parallèle de f et g (sans modifier ces derniers)
        """
        ff = f.copy()
        ff.iparallel(g)
        return ff
    @classmethod
    def identity(cls, n):
        """
        n : int ; nombre de fils
        Crée un open_digraph représentant l'identité sur n fils.
        """
        inputs = []
        outputs = []
        for i in range(n):
            inputs.append(i)
            outputs.append(n + i)
        nodes = []
        for i in range(n):
            nodes.append(node(i, str(i), {}, {n+i : 1}))
        for i in range(n):
            nodes.append(node(n+i, str(n+i), {i : 1}, {}))
        return open_digraph(inputs, outputs, nodes)
	
