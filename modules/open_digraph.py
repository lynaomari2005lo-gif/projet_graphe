from random import *
from modules.nodes import node

class open_digraph(): # for open directed graph
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
        for v in self.nodes:
            nodes_s += "id : " + str(self.nodes[v].id) + "\n"
        chaine = "ids of the input nodes : " + "\n" + inputs_s + "ids of the output nodes : " + "\n" + outputs_s + "ids of each node : " + "\n" + nodes_s + "\n"
        return chaine
    def __repr__(self):
        return str(self)
    @classmethod 
    def empty(cls):
        """
        renvoie un graphe vide
        """
        return open_digraph( [], [], [] )
    def get_input_ids(self):
        return self.inputs
    def get_output_ids(self):
        return self.outputs
    def get_id_node_map(self):
        return self.nodes
    def get_nodes(self):
        return [self.nodes[n] for n in self.nodes]
    def get_nodes_dico(self): #renvoie le dictionnaire ayant pour clé l'id de chaque noeud
        return self.nodes
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
        # mixins/compositions_mx.py

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
        return new_id

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
        """
        id1 : int, id du noeud 1 à fusionner
        id2 : int, id du noeud 2 à fusionner
        label : string, nouveau label/ None par défaut prend celui du noeud d'id 1
        Fonction qui fusionne le noeud d'id 1 et celui d'id 2
        """
        node1 = self.get_node_by_id(id1)
        node2 = self.get_node_by_id(id2)
        nv_label = ""
        if label == None:
            nv_label = node1.get_label()
        else:
            nv_label = label
        e = []
        for parent_id, mult in node2.get_parents().items():
            for i in range(mult):
                e.append((parent_id, id1))
        for child_id, mult in node2.get_children().items():
            for i in range(mult):
                e.append((id1, child_id))
        self.add_edges(e)
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
        from modules.open_digraph import open_digraph  # Import local
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
    @classmethod
    def hamming_encoder(cls):
        """
        Encodeur Hamming (7,4) : construit un circuit booléen qui prend 4 bits et en génère 7
        en ajoutant 3 bits de parité.
        """
        return cls.parse_parentheses(
            "((d1^d2)^d4)",  # p1 = d1 ⊕ d2 ⊕ d4
            "((d1^d3)^d4)",  # p2 = d1 ⊕ d3 ⊕ d4
            "((d2^d3)^d4)",  # p3 = d2 ⊕ d3 ⊕ d4
            "d1", "d2", "d3", "d4"  # données inchangées dans la sortie
            )[0]  # [0] pour récupérer le bool_circ (pas la liste des variables)

    @classmethod
    def hamming_decoder(cls):
        """
        Décodeur Hamming (7,4) : construit un circuit booléen qui corrige 1 erreur et retrouve les bits d’origine.
        Cette version suppose qu'on corrige les erreurs avec les XOR des bits de contrôle.
        """
        return cls.parse_parentheses(
            # Syndrome bits (simplifiés à 3 XOR comme dans le graphe)
            "((p1^(d1^d2))^d4)",  # s1
            "((p2^(d1^d3))^d4)",  # s2
            "((p3^(d2^d3))^d4)",  # s3
            # Les bits de données sont transmis tels quels (décodés après correction dans une version complète)
            "d1", "d2", "d3", "d4"
            )[0]


    def is_well_formed(self):
        """
        vérifie si un graphe est toujouts "bien formé" ( vérifie la multiplicité, les inputs et outputs, etc.)
        """
        inp_ids = self.get_input_ids()
        out_ids = self.get_output_ids()
        nodes_ids = self.get_node_ids()
        inps = self.get_nodes_by_ids(inp_ids)
        outs = self.get_nodes_by_ids(out_ids)
        nodes = self.nodes
        inpout_ids = inp_ids + out_ids
        for ids in inpout_ids:
            if ids not in nodes_ids:
                return "tous les noeuds de inputs et outputs ne sont pas dans le graphe"
        for el in inps:
            if len(el.get_children()) != 1 or len(el.get_parents()) != 0:
                return "un noeud input n'a pas un unique enfant ou a un parent"
        for el in outs:
            if len(el.get_children()) != 0 or len(el.get_parents()) != 1:
                return "un noeud output n'a pas d'unique parent ou a un fils"
        for el in nodes:
            # Verification ID
            if el != nodes[el].get_id():
                return "chaque clé de nodes ne pointe pas vers un noeud d'id la clé"
            # Verification Children
            children = nodes[el].get_children()
            for c in children :
                parents = self.get_node_by_id(c).get_parents()
                if el not in parents:
                    return "le parent ne figure pas dans la liste de parents de l'enfant"
                if parents[el] != children[c]:
                    return "pas la bonne multiplicité pour un parent"
            # Verification Parents  
            parents = nodes[el].get_parents()
            for p in parents :
                children = self.get_node_by_id(p).get_children()
                if el not in children:
                    return "l'enfant ne figure pas dans la liste d'enfants du parent"
                if children[el] != parents[p]:
                    return "pas la bonne multiplicité pour un enfant"
        return "bon"
    def assert_is_well_formed(self):
        """
        renvoie une erreur si le graphe n'est pas bien formé
        """
        if self.is_well_formed() != "bon":
            raise Exception(self.is_well_formed())
        else:
            return True
    def add_input_node(self, id):
        """
        id : int; id du noeud vers qui pointe le nouveau input node
        crée un nouveau noeud input
        """
        new_id = self.new_id()
        if id not in self.get_node_ids() :
            raise Exception("l'id donné ne correspond pas à un noeud dans le graphe")
        if id in self.get_input_ids() :
           for i in range (len(self.inputs) -1) :
                if self.inputs[i] == id :
                    self.inputs.pop(i)
        input_node = node(new_id, "", {}, {id : 1})
        nd = self.get_node_by_id(id)
        nd.add_parent_id(new_id)
        self.nodes[new_id] = input_node
        self.add_input_id(new_id)
    def add_output_node(self, id):
        """
        id : int; id du noeud qui pointe vers le nouveau output node
        crée un nouveau noeud output
        """
        new_id = self.new_id()
        if id not in self.get_node_ids() :
            raise Exception("l'id donné ne correspond pas à un noeud dans le graphe")
        if id in self.get_output_ids() :
            for i in range (len(self.outputs) -1) :
                if self.outputs[i] == id :
                    self.outputs.pop(i)
        output_node = node(new_id, "", {id : 1}, {})
        nd = self.get_node_by_id(id)
        nd.add_child_id(new_id)
        self.nodes[new_id] = output_node
        self.add_output_id(new_id)
    @classmethod 
    def random(cls, n, bound, inputs=0, outputs=0, loop_free=False, DAG=False,oriented=False, undirected=False):
        """
        n : int, taille de la matrice carré
        bound : int, chiffre max de la matrice
        inputs : int, nombre d'entrées du graphe (0 par défaut)
        outputs : int, nombre de sorties du graphe (0 par défaut)
        loop_free : bool, on spécifie si on veut un graphe sans boucles
        DAG : bool, on spécifie si on veut un graphe dirigé acyclique
        oriented : bool, on spécifie si on veut un graphe orienté
        undirected : bool, on spécifie si on veut un graphe non orienté
        """
        m = None 
        if DAG:
            if loop_free:
                m = random_triangular_int_matrix(n,bound)
            elif not loop_free:
                m = random_triangular_int_matrix(n,bound,null_diag = False)
        elif oriented:
            if loop_free:
                m = random_oriented_int_matrix(n,bound)
            elif not loop_free:
                m = random_oriented_int_matrix(n,bound,null_diag = False)
        elif undirected:
            if loop_free:
                m = random_sysmetric_int_matrix(n,bound)
            elif not loop_free:
                m = random_sysmetric_int_matrix(n,bound,null_diag = False)
        else:
            if loop_free:
                m = random_int_matrix(n,bound)
            else:
                m = random_int_matrix(n,bound,null_diag = False)
        return graph_from_adjacency_matrix(m)
    def graph_to_dico(self):
        """
        renvoie un dictionnaire associant à chaque id de noeud du graphe un unique entier 0 <= i <= nombre de noeud du graphe
        """
        node_ids = self.get_node_ids()
        return {node_ids[i]: i for i in range(len(node_ids))}
    def adjacency_matrix(self):
        """
        renvoie une matrice 'adjacence du graphe
        """
        id_to_index = self.graph_to_dico()
        n = len(id_to_index)
        matrix = [[0] * n for i in range(n)]
        for node_id, node in self.nodes.items():
            src_index = id_to_index[node_id]
            for child_id, multiplicity in node.get_children().items():
                tgt_index = id_to_index[child_id]
                matrix[src_index][tgt_index] = multiplicity
        return matrix
    def save_as_dot_file(self, path, verbose=False) :
        """
        path : string, chemin où enregistrer le fichier
        verbose : si on spécifie le label d'un noeud celui-ci n'affiche plus son id, lorsque verbose=True on affiche l'id et le label de chaque noeud 

        enregistre le graphe en format.dot à l'endroit spécifier par path
        """
        f = open (path , 'w')
        contenu = "digraph G {\n"
        nodes = self.get_nodes_dico()
        if verbose == False :
            for n in nodes :
                if nodes[n].get_label() != "":
                    contenu = contenu +"    " + str(nodes[n].get_id()) + " [label=\"" + str(nodes[n].get_label()) + "\"]; \n"
            contenu += "\n"
            for n in nodes :
                enfants = nodes[n].get_children()
                for e in enfants :
                    for i in range(enfants[e]) :
                        contenu = contenu +"    " + str(nodes[n].get_id()) + "->" + str(e) + ";\n"
            contenu = contenu + "}"
        else :
            for n in nodes :
                if nodes[n].get_label() != "":
                    contenu = contenu +"    " + str(nodes[n].get_id()) + " [label=\"" + str(nodes[n].get_label()) + "\""  ",id=" + str(nodes[n].get_id()) + "]; \n"
            contenu += "\n"
            for n in nodes :
                enfants = nodes[n].get_children()
                for e in enfants :
                    for i in range(enfants[e]) :
                        contenu = contenu +"    " + str(nodes[n].get_id()) + "->" + str(e) + ";\n"
            contenu = contenu + "}"
        f.write(contenu)
        f.close()
    def from_dot_file(self, path):
        """
        path : string, chemin où est enregistré le fichier
       
        lit un fichier.dot et crée un open_digraph à partir de lui

        """
        f = open (path , 'r')
        texte = f.readlines() 
        f.close()
        nodes = {}
        edges = []
        for ligne in texte:
            ligne = ligne.strip().strip(";")
            if "->" in ligne:  
                liens = ligne.split("->")
                node1 = int(liens[0].strip())
                node2 = int(liens[1].strip())
                edges.append((node1, node2))
            elif "[" in ligne and "]" in ligne: 
                node_part = ligne.split("[")[0].strip()
                label_part = ligne.split("label=")[1].split("]")[0].strip(' "')
                nodes[int(node_part)] = label_part
        nodes_graph = {node_id: node(node_id, label, {}, {}) for node_id, label in nodes.items()}
        for parent, child in edges:
            nodes_graph[parent].add_child_id(child)
            nodes_graph[child].add_parent_id(parent)
        a = list(nodes_graph.values()) 
        return open_digraph([], [], a)

    def display(self, nom, verbose=False) :
        """
        méthode qui affiche directement le graphe
        verbose : si on spécifie le label d'un noeud celui-ci n'affiche plus son id, lorsque verbose=True on affiche l'id et le label de chaque noeud 
        nom : nom du fichier où on crée le graphe

        """
        import os
        import tempfile

        with tempfile.NamedTemporaryFile(delete=True, suffix=".dot", mode='w') as temp_dot_file:
            temp_dot_file_path = temp_dot_file.name 
            self.save_as_dot_file(temp_dot_file_path, verbose) 
            os. system(f"dot -Tpdf {temp_dot_file_path} -o {nom}")
    def is_cyclic(self):
        """
        Vérifie si le graphe est cyclique en supprimant les feuilles (nœuds sans successeurs)
        et en vérifiant si un cycle reste après cette suppression.
        """
        g = self.copy()

        def find_feuilles(graph):
            return [node for node in graph.get_nodes() if node.get_children() == {}]

        while True:
            feuilles = find_feuilles(g)
            
            if feuilles == []:
                return True
            
            for feuille in feuilles:
                g.remove_node_by_id(feuille.get_id())
            
            if len(g.get_nodes()) == 0:
                return False
    def min_id(self):
        """
        renvoie l'indice min des noeuds du graphe
        """
        if not self.nodes:
            return None
        return min(self.nodes.keys())
    
    def max_id(self):
        """
        renvoie l'indice max des noeuds du graphe
        """
        if not self.nodes:
            return None
        return max(self.nodes.keys())
    def connected_components(self):
        """
        Retourne le nombre de composantes connexes du graphe et un dictionnaire associant
        chaque id de noeud à un identifiant de composante connexe
        """
        idn = self. get_node_ids()
        visite = []
        dico = {}
        nbr = 0

        def parcour(n_id):
            visite.append(n_id)
            dico[n_id] = nbr
            voisins = self.nodes[n_id].get_idc() + self.nodes[n_id].get_idp()
            for v in voisins:
                if v not in visite:
                    parcour(v)

        for n in idn:
            if n not in visite:
                parcour(n)
                nbr +=1

        return (nbr, dico)
    def liste_op(self):
        """
        Retourne une liste de sous-graphes correspondant aux composantes connexes du graphe.
        Chaque sous-graphe est construit à partir des nœuds d'une même composante connexe.
        """
        liste = []
        nbr, dico = self.connected_components()
        nodes = self.get_nodes()
        for i in range(nbr):
            liste_n = []
            for j in range(len(nodes)): 
                if dico[nodes[j].get_id()] == i:
                    liste_n.append(nodes[j])
            p,e = inout(liste_n)
            grp = open_digraph(p,e,liste_n)
            liste.append(grp)
        return liste
    def Dijkstra(self, src, direction = None):
        """
        src : int, id du noeud source
        direction : int ou None : 1 ou -1
        tgt : int, id du noeud cible
        Implémente l'algorithme de Dijkstra pour calculer les distances minimales depuis le nœud `src`.
        Peut être orienté suivant la direction : None (tous les voisins), 1 (enfants uniquement), -1 (parents uniquement).
        Renvoie un dictionnaire des distances et un dictionnaire des précédents.
        """
        Q = [src] 
        dist = {src:0}
        prev={}
        while Q != [] :
            u = min(Q, key=lambda node: dist[node])
            Q.remove(u)
            if ( direction == None):
                neighbours = list(self.get_node_by_id(u).get_children().keys()) + list(self.get_node_by_id(u).get_parents().keys())
            elif ( direction == 1):
                neighbours = list(self.get_node_by_id(u).get_children().keys())
            elif ( direction == -1):
                neighbours = list(self.get_node_by_id(u).get_parents().keys())
            for v in neighbours :
                if v not in dist :
                    Q.append(v)
                if v not in dist or dist.get(v) > dist[u] + 1:
                    dist[v] = dist[u] + 1
                    prev[v] = u
        return dist, prev
    def Dijkstra2(self, src, direction=None, tgt=None):
        """
        src : int, id du noeud source
        direction : int ou None : 1 ou -1
        tgt : int, id du noeud cible
        Variante de l'algorithme de Dijkstra avec option d'arrêt anticipé si un nœud cible `tgt` est atteint.
        Utile pour améliorer l'efficacité lorsqu'on cherche un plus court chemin entre deux nœuds spécifiques.
        """
        Q = [src] 
        dist = {src: 0}
        prev = {}
        while Q != []:
            u = min(Q, key=lambda node: dist[node])
            Q.remove(u)

            if tgt is not None and u == tgt:
                break

            if direction is None:
                neighbours = list(self.get_node_by_id(u).get_children().keys()) + list(self.get_node_by_id(u).get_parents().keys())
            elif direction == 1:
                neighbours = list(self.get_node_by_id(u).get_children().keys())
            elif direction == -1:
                neighbours = list(self.get_node_by_id(u).get_parents().keys())

            for v in neighbours:
                if v not in dist:
                    Q.append(v)
                if v not in dist or dist[v] > dist[u] + 1:
                    dist[v] = dist[u] + 1
                    prev[v] = u

        return dist, prev
    def shortest_path(self, u, v):
        """
        u : int, Identifiant du nœud de départ
        v : int, Identifiant du nœud d’arrivée
        Calcule et retourne le plus court chemin entre deux nœuds `u` et `v` sous forme de liste de nœuds.
        Utilise Dijkstra2 avec arrêt à la cible `v`. Retourne une liste vide si aucun chemin n'existe.
        """
        dist, prev = self.Dijkstra2(u, tgt=v)
        if v not in dist:
            return []

        chemin = []
        cn = v
        while cn != u:
            chemin.append(cn)
            cn = prev.get(cn)
            if cn is None:
                return [] 
        chemin.append(u)
        chemin.reverse()
        return chemin
    def ancetres(self, u, v):
        """
        u : int, Identifiant du premier nœud
        v : int, Identifiant du second nœud
        Trouve les ancêtres communs entre deux nœuds `u` et `v` (en remontant dans le graphe).
        Retourne un dictionnaire associant à chaque ancêtre commun la distance depuis `u` et `v`.
        """
        distu , prev1 = self.Dijkstra2(u, direction=-1)
        distv , prev2 = self.Dijkstra2(v, direction=-1)
        ancetre_com = [] 
        for node in distu:
            if node in distv:
                ancetre_com.append(node)
        dico = {}
        for a in ancetre_com:
            dico[a] = (distu[a], distv[a])

        return dico
    def tri_topologique(self):
        res = []
        g = self.copy()
        def find_cofeuilles(self):
            return [node for node in self.get_nodes() if node.get_parents() == {}]
        while len(g.nodes)>0:
            co_feuilles = find_cofeuilles(g)
            l = []
            for feuille in co_feuilles:
                l.append(feuille)
                g.remove_node_by_id(feuille.get_id())
            res.append(l)   


def inout(liste):
    """
    liste : list, liste de noeuds
    Détermine les identifiants des nœuds d'entrée (sans parents) et de sortie (sans enfants) dans une liste de nœuds.
    Hypothèse : chaque entrée a un seul enfant, chaque sortie a un seul parent.
    Retourne un tuple (inputs, outputs) contenant les identifiants.
    """
    inputs = []
    outputs = []
    for i in range(len(liste)):
        if len(liste[i].get_parents()) == 0 and list(liste[i].get_children().values()) == [1]:
            inputs.append(liste[i].get_id())
        if list(liste[i].get_parents().values()) == [1] and len(liste[i].get_children()) == 0:
            outputs.append(liste[i].get_id())
    return (inputs,outputs)

"""

Fonctions Matrices

"""
    
def random_int_list(n,bound):
    """
    n : int, taille de la liste
    bound : int, chiffre max de la liste
    fonction qui génère une liste avec ses éléments des int tirés aléatoirement entre 0 et bound
    """
    liste = []
    for i in range(n):
        liste.append(randint(0,bound))
    return liste

#print(random_int_list(3,6))

def random_int_matrix(n,bound,null_diag=True):
    """
    n : int, taille de la matrice carré
    bound : int, chiffre max de la matrice 
    null_diag : bool, False si on ne veut pas spécialement que la diagonale de la matrice soit nulle
    fonction qui génère une matrice n * n avec ses éléments des int tirés aléatoirement entre 0 et bound avec une diagonale nulle ou non
    """
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
    """
    n : int, taille de la matrice carré
    bound : int, chiffre max de la matrice
    null_diag : bool, False si on ne veut pas spécialement que la diagonale de la matrice soit nulle
    renvoie une matrice symétrique avec une diagonale nulle ou non
    """
    m = random_int_matrix(n,bound,null_diag)
    for i in range(n):
        for j in range(n):
            m[i][j] = m[j][ i]
    return m

#print(random_sysmetric_int_matrix(3,6,null_diag=False))

def random_oriented_int_matrix(n,bound,null_diag=True):
    """
    n : int, taille de la matrice carré
    bound : int, chiffre max de la matrice
    null_diag : bool, False si on ne veut pas spécialement que la diagonale de la matrice soit nulle
    renvoie une matrice orientée avec une diagonale nulle ou non
    """
    m = random_int_matrix(n,bound,null_diag)
    for i in range(n):
        for j in range(n):
            if  m[i][j] != 0:
                m[j][i] = 0
    return m

#print(random_oriented_int_matrix(5,20,null_diag=False))

def random_triangular_int_matrix(n,bound,null_diag=True):
    """
    n : int, taille de la matrice carré
    bound : int, chiffre max de la matrice
    null_diag : bool, False si on ne veut pas spécialement que la diagonale de la matrice soit nulle
    renvoie une matrice trianguaire (supérieur ou non)
    """
    m = random_int_matrix(n,bound,null_diag)
    for i in range(n):
        for j in range(n):
            if i > j :
                m[i][j] = 0
    return m

#print(random_triangular_int_matrix(5,20))

def graph_from_adjacency_matrix(matrix):
    """
    matrix : list * list, matrice d'adjacence
    renvoie un graphe à partir de la matrice d'adjacence donnée en paramètre
    """
    gr = open_digraph([], [], [])
    nodes = {} 
    for i in range(len(matrix)):
        nodes[i] = gr.add_node(label=str(i), parents={}, children={})
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] != 0: 
                for s in range(matrix[i][j]):  
                    gr.get_node_by_id(i).add_child_id(j)
    
    for node_id, node in gr.get_id_node_map().items():
        for child_id, multiplicity in node.get_children().items():
            for k in range(multiplicity):
                gr.get_node_by_id(child_id).add_parent_id(node_id)
    
    return gr


"""

Sous-classe Circuit

"""
class bool_circ(open_digraph):
    def __init__(self, graph):
        if not isinstance(graph, open_digraph):
            raise TypeError("L'argument doit être une instance de open_digraph")
        super().__init__(graph.get_input_ids(), graph.get_output_ids(), graph.get_nodes())
        self.graph = graph
        if not self.is_well_formed_cyclic():
            raise ValueError("Le circuit booléen n'est pas bien formé.")

    def is_well_formed_cyclic(self):
        """
        teste si le circuit booléen est bien un circuit booléen(doit être acyclique et respecter les contraintes de degré)
        """
        if self.is_cyclic():
            return  False
        if not self.graph.assert_is_well_formed():
            return  False
        for node in self.get_nodes():
            label = node.get_label()
            indeg = node.indegree()
            outdeg = node.outdegree()  
            if label == '0' or label == '1':
                if indeg != 0: 
                    return  False
            elif label == '':
                if indeg not in [0,1]:
                    return False
            elif label == ' ':
                if indeg not in [0,1]:
                    return False
            elif label == '&' or label == '|':
                if indeg < 2 or outdeg not in [0,1]:
                    return False
            elif label == '~':
                if indeg != 1 or outdeg not in [0,1] :
                    return False
            elif label == '^':
                if indeg < 2 or outdeg not in [0,1]:
                    return False
            elif label not in [' ','0','1','&','|','^','~','res']:
                return False
        return True

    @classmethod
    def int_bin(cls, n, t):
        """
        n : int, un entier
        t : int, nombre de bits
        Crée un circuit booléen représentant l'entier `n` sur `t` bits.
        """
        nbin = bin(n)[2:].zfill(t)
        nodes = []
        inputs = []
        for i in range(t):
            bit = nbin[i]
            nodes.append(node(i, bit, {}, {}))
            inputs.append(i)
        return cls(open_digraph([], [], nodes))

    @classmethod
    def parse_parentheses(cls, *args):
        """
        Construit un bool_circ à partir d'une ou plusieurs chaîne de caractères bien parenthésée.
        """
        root = node(0, 'res', {}, {})  
        nodes = {0: root}
        current_id = 0
        next_id = 1
        s2 = ''
        s3 = ''
        val = []
        stack = []
        
        for s in args:
            for char in s:
                if char == '(':
                    if s2.strip() and s2 != ' ':
                        nodes[current_id].set_label(s2.strip())
                    if s2 == ' ':
                        nodes[current_id].set_label(s2)
                    parent = node(next_id, '', {}, {current_id: 1})
                    nodes[current_id].add_parent_id(next_id)
                    nodes[next_id] = parent
                    stack.append(current_id)
                    current_id = next_id
                    next_id += 1
                    s2 = ''
                elif char == ')':
                    if s2.strip() and s2 != ' ':
                        nodes[current_id].set_label(s2.strip())
                    if s2 == ' ':
                        nodes[current_id].set_label(s2)
                    if stack:
                        current_id = stack.pop()
                    s2 = ''
                    if s3.strip() not in val and s3.strip() != '':
                        val.append(s3.strip())
                    s3 = ''
                else:
                    s2 += char
                    if (char not in ["|", "^", "~", "&"] )and ( char != ' '):
                        s3 += char
                
        graph = open_digraph([], [], list(nodes.values()))
        
        id_val = {}
        input_ids =  [id1 for id1, nd in graph.nodes.items() if (nd.get_label() == '1' or  nd.get_label() == '0')]
        for x in val:
            if x != '1' and x != '0':
                ids = [id1 for id1, nd in graph.nodes.items() if nd.get_label() == x]
                if ids:
                    main_id = ids[0]
                    for other_id in ids[1:]:
                        graph.fusion_noeuds(main_id, other_id)
                    if graph.nodes[main_id].label not in ['1','0']:
                        graph.nodes[main_id].set_label('')
        #graph.remove_node_by_id(0)
        #graph.inputs = input_ids
        #print(graph.nodes)
        return cls(graph), val
        
    def genere_bool_circ(self, n, inputs=1, outputs=1):
        """
        n: taille du graphe
        inputs : nb de inputs souhaités
        outputs : nb de outputs souhaités
        Retourne un open_digraph représentant un circuit booléen.
        """
        import random as rd
        from random import choice, randint

        g = open_digraph.random(n,1, DAG=True, loop_free=True)

        tab_nodes = g.get_nodes()
        for node in tab_nodes:
            if node.get_parents() == {}:
                g.add_input_node(node.get_id())
            if node.get_children() == {}:
                g.add_output_node(node.get_id())
        
        current_inputs = g.get_input_ids()

        tab_ids_possibles = g.get_node_ids()
        for id in g.get_input_ids():
            tab_ids_possibles.remove(id)
        for id in g.get_output_ids():
            tab_ids_possibles.remove(id)
        
        while len(current_inputs) < inputs:

            id = choice(tab_ids_possibles)
            g.add_input_node(id)

        while len(current_inputs) > inputs:

            a, b = current_inputs.pop(), current_inputs.pop()
            tab_ids_possibles.append(a)
            tab_ids_possibles.append(b)
            op = rd.choice(['&', '|', '^'])
            new_node = g.add_node(op, {} , {a:1, b:1})
            g.add_input_node(new_node)

        current_outputs = g.get_output_ids()
        while len(current_outputs) < outputs:

            id = choice(tab_ids_possibles)
            g.add_output_node(id)

        while len(current_outputs) > outputs:

            a, b = current_outputs.pop(), current_outputs.pop()
            tab_ids_possibles.append(a)
            tab_ids_possibles.append(b)
            op = rd.choice(['&', '|', '^'])
            new_node = g.add_node(op, {a:1, b:1}, {} )
            g.add_output_node(new_node)
        
        for node in g.get_nodes():
            if not node.get_parents():  
                g.add_input_node(node.get_id())
            if not node.get_children():  
                g.add_output_node(node.get_id())
        
        for node in g.get_nodes():
            node_id = node.get_id()
                
            ind = node.indegree()
            oud = node.outdegree()
            
            if ind == 1 and oud == 1:
                node.set_label("~")  
                
            elif ind == 1 and oud > 1:
                node.set_label(' ')

            elif ind > 1 and oud == 1:
                op = rd.choice(['&', '|', '^'])
                node.set_label(op)
                
            elif ind > 1 and oud > 1:
                op = rd.choice(['&', '|', '^'])
                node.set_label(op) 
                
                ucp = g.add_node(' ', {}, {})
                
                children = list(node.get_children().copy().keys())
                for child_idd in children:
                    node_obj = g.get_node_by_id(node_id)    
                    child_obj = g.get_node_by_id(child_idd) 
                    ucp_obj = g.get_node_by_id(ucp)         
                    
                    g.add_edge(ucp_obj, child_obj)          
                    g.remove_edge(node_id, child_idd)       
                g.add_edge(node_obj, ucp_obj)

            elif ind == 0 and oud == 0:
                g.remove_node_by_id(node.get_id())

            for i in g.get_input_ids() :
                inp = g.get_node_by_id(i)
                if inp.outdegree() > 1 :
                        ucp = g.add_node(' ', {}, {})
                    
                        children = list(inp.get_children().copy().keys())
                        for child_idd in children:  
                            child_obj = g.get_node_by_id(child_idd) 
                            ucp_obj = g.get_node_by_id(ucp)         
                            
                            g.add_edge(ucp_obj, child_obj)          
                            g.remove_edge(i, child_idd)       
                        g.add_edge(inp, ucp_obj)
        for node in g.get_nodes():
            to_remove = [child_id for child_id, count in node.get_children().items() if count == 0]
            for child_id in to_remove:
                node.remove_child_id(child_id)
        return bool_circ(g)



    def build_addern(self, n):
        """
        Construit un circuit Addern qui calcule la somme de deux registres de taille 2^n
        avec un bit de retenue en entrée.
        
        Entrées: 2*2^n bits (deux registres) + 1 bit de retenue
        Sorties: 2^n bits (somme) + 1 bit de retenue
        """
        size = 2**n
        g = open_digraph.empty()

        input_a_ids = []
        input_b_ids = []
        sum_ids = []

        # Retenue initiale (bit d'entrée)
        carry_node_id = g.add_node("", {},  {})
        g.add_input_id(carry_node_id)
        prev_carry_id = carry_node_id

        for i in range(size):
            # Entrées a_i et b_i
            a_node_id = g.add_node("",  {},  {})
            b_node_id = g.add_node("",  {},  {})
            g.add_input_id(a_node_id)
            g.add_input_id(b_node_id)
            input_a_ids.append(a_node_id)
            input_b_ids.append(b_node_id)

            # XOR1 : a ^ b
            xor1_id = g.add_node("^", {a_node_id : 1, b_node_id : 1},  {})

            # XOR2 : (a ^ b) ^ c_in
            xor2_id = g.add_node("^", {xor1_id : 1, prev_carry_id : 1},  {})
            g.add_output_node(xor2_id)
            sum_ids.append(xor2_id)

            # Carry : (a & b) | ((a ^ b) & c_in)
            and1_id = g.add_node("&", {a_node_id : 1, b_node_id : 1},  {})
            and2_id = g.add_node("&", {xor1_id : 1, prev_carry_id : 1},  {})
            carry_out_id = g.add_node("|", {and1_id : 1, and2_id : 1},  {})

            prev_carry_id = carry_out_id

        # Dernière retenue
        g.add_output_node(prev_carry_id) 
        for no in g.get_nodes():
            if no.get_label() in ['&', '|', '^'] :
                if no.outdegree() > 1 :
                    ucp = g.add_node(' ', {}, {})
                    node_id = no.get_id()
                
                    children = list(no.get_children().keys())
                    for child_idd in children:
                        node_obj = g.get_node_by_id(node_id)    
                        child_obj = g.get_node_by_id(child_idd) 
                        ucp_obj = g.get_node_by_id(ucp)         
                        
                        g.add_edge(ucp_obj, child_obj)          
                        g.remove_edge(node_id, child_idd)       
                    g.add_edge(node_obj, ucp_obj)
        for i in g.get_input_ids() :
                inp = g.get_node_by_id(i)
                if inp.outdegree() > 1 :
                        ucp = g.add_node(' ', {}, {})
                    
                        children = list(inp.get_children().copy().keys())
                        for child_idd in children:  
                            child_obj = g.get_node_by_id(child_idd) 
                            ucp_obj = g.get_node_by_id(ucp)         
                            
                            g.add_edge(ucp_obj, child_obj)          
                            g.remove_edge(i, child_idd)       
                        g.add_edge(inp, ucp_obj)

        for node in g.get_nodes():
            to_remove = [child_id for child_id, count in node.get_children().items() if count == 0]
            for child_id in to_remove:
                node.remove_child_id(child_id)

        return bool_circ(g)


    def build_half_addern(self, n):
        """
        Construit un circuit Half_Addern qui calcule la somme de deux registres de taille 2^n.
        
        Entrées: 2*2^n bits (deux registres)
        Sorties: 2^n bits (somme) + 1 bit de retenue
        """
        size = 2**n
        g = open_digraph.empty()

        input_a_ids = []
        input_b_ids = []
        sum_ids = []

        prev_carry_id = None

        for i in range(size):
            # 1. Création des nœuds pour a_i et b_i
            a_node_id = g.add_node(" ", {}, {})
            b_node_id = g.add_node(" ", {}, {})
            g.add_input_id(a_node_id)
            g.add_input_id(b_node_id)
            input_a_ids.append(a_node_id)
            input_b_ids.append(b_node_id)

            # 2. XOR intermédiaire : a ^ b
            xor1_id = g.add_node("^", {a_node_id : 1, b_node_id : 1 }, {})

            # 3. AND pour la retenue intermédiaire : a & b
            and1_id = g.add_node("&", {a_node_id : 1, b_node_id: 1}, {})

            if i == 0:
                # Pas de retenue entrante pour le 1er bit
                sum_id = xor1_id
                carry_out_id = and1_id
            else:
                # 4. XOR final : (a ^ b) ^ prev_carry
                xor2_id = g.add_node("^", {xor1_id : 1, prev_carry_id: 1}, {})
                sum_id = xor2_id

                # 5. Nouvelle retenue : (a & b) | ((a ^ b) & prev_carry)
                and2_id = g.add_node("&", {xor1_id : 1, prev_carry_id : 1}, {})
                carry_out_id = g.add_node("|", {and1_id : 1, and2_id : 1}, {})

            g.add_output_node(sum_id)
            sum_ids.append(sum_id)
            prev_carry_id = carry_out_id

        # 6. Sortie finale : bit de retenue final
        g.add_output_node(prev_carry_id)

        for no in g.get_nodes():
            if no.get_label() in ['&', '|', '^'] :
                if no.outdegree() > 1 :
                    ucp = g.add_node(' ', {}, {})
                    node_id = no.get_id()
                
                    children = list(no.get_children().copy().keys())
                    for child_idd in children:
                        node_obj = g.get_node_by_id(node_id)    
                        child_obj = g.get_node_by_id(child_idd) 
                        ucp_obj = g.get_node_by_id(ucp)         
                        
                        g.remove_edge(node_id, child_idd)
                        g.add_edge(ucp_obj, child_obj)                 

                    g.add_edge(node_obj, ucp_obj)

        for i in g.get_input_ids() :
            inp = g.get_node_by_id(i)
            if inp.outdegree() > 1 :
                ucp = g.add_node(' ', {}, {})
            
                children = list(inp.get_children().copy().keys())
                for child_idd in children:  
                    child_obj = g.get_node_by_id(child_idd) 
                    ucp_obj = g.get_node_by_id(ucp)         
                    
                    g.remove_edge(i, child_idd)
                    g.add_edge(ucp_obj, child_obj)    
                g.add_edge(inp, ucp_obj)

        for node in g.get_nodes():
            to_remove = [child_id for child_id, count in node.get_children().items() if count == 0]
            for child_id in to_remove:
                node.remove_child_id(child_id)

        return bool_circ(g)


    def encodeur(self):
        g = open_digraph.empty()

        # Entrées
        b1 = g.add_node(" ", {}, {})
        b2 = g.add_node(" ", {}, {})
        b3 = g.add_node(" ", {}, {})
        b4 = g.add_node(" ", {}, {})

        # Ajouter les entrées
        g.add_input_node(b1)
        g.add_input_node(b2)
        g.add_input_node(b3)
        g.add_input_node(b4)

        # XORs
        xor1 = g.add_node("^", {}, {})
        xor2 = g.add_node("^", {}, {})
        xor3 = g.add_node("^", {}, {})

        # Connexions (parents → enfants)
        g.add_edge(g.get_node_by_id(b1), g.get_node_by_id(xor1))
        g.add_edge(g.get_node_by_id(b2), g.get_node_by_id(xor1))
        g.add_edge(g.get_node_by_id(b4), g.get_node_by_id(xor1))

        g.add_edge(g.get_node_by_id(b1), g.get_node_by_id(xor2))
        g.add_edge(g.get_node_by_id(b3), g.get_node_by_id(xor2))
        g.add_edge(g.get_node_by_id(b4), g.get_node_by_id(xor2))

        g.add_edge(g.get_node_by_id(b2), g.get_node_by_id(xor3))
        g.add_edge(g.get_node_by_id(b3), g.get_node_by_id(xor3))
        g.add_edge(g.get_node_by_id(b4), g.get_node_by_id(xor3))


        # Ajout des sorties : les 4 bits d’entrée + les 3 XOR
        for i in [b1, b2, b3, b4, xor1, xor2, xor3]:
            g.add_output_node(i)

        return bool_circ(g)

    def decodeur(self):
        g = open_digraph.empty()
        b1 = g.add_node(" ", {}, {})
        b2 = g.add_node(" ", {}, {})
        b3 = g.add_node(" ", {}, {})
        b4 = g.add_node(" ", {}, {})
        xor1 = g.add_node("^", {b1:1, b2:1, b4:1}, {})
        xor2 = g.add_node("^", {b1:1, b3:1, b4:1}, {})
        xor3 = g.add_node("^", {b2:1, b3:1, b4:1}, {})
        for id, node in list(g.nodes.items()):
            g.add_input_node(id)
        copie1 = g.add_node(" ", {xor1:1}, {})
        copie2 = g.add_node(" ", {xor2:1}, {})
        copie3 = g.add_node(" ", {xor3:1}, {})
        non1 = g.add_node("~", {copie3:1}, {})
        non2 = g.add_node("~", {copie2:1}, {})
        non3 = g.add_node("~", {copie1:1}, {})
        et1 = g.add_node("&", {copie1:1, copie2:1, non1:1}, {})
        et2 = g.add_node("&", {copie1:1, non2:1, copie3:1}, {})
        et3 = g.add_node("&", {non3:1, copie2:1, copie3:1}, {})
        et4 = g.add_node("&", {copie1:1, copie2:1, copie3:1}, {})
        xor1 = g.add_node("^", {et1:1, b1:1}, {})
        xor2 = g.add_node("^", {et2:1, b2:1}, {})
        xor3 = g.add_node("^", {et3:1, b3:1}, {})
        xor4 = g.add_node("^", {et4:1, b4:1}, {})
        g.add_output_node(xor1)
        g.add_output_node(xor2)
        g.add_output_node(xor3)
        g.add_output_node(xor4)
        return bool_circ(g)


	

    def simplify_once(self):
        """
        Applique les méthodes de simplication à tous les noeuds du graphe.
        Si un noeud ayant un opérateur en label à un seul parent, ils sont fusionnés
        """
        for n in list(self.nodes):  
            if n not in self.graph.nodes:
                continue
            node = self.graph.get_node_by_id(n)
            label = node.get_label()

            parents = [self.graph.get_node_by_id(pid) for pid in node.parents if pid in self.graph.nodes]
            parent_labels = [p.get_label() for p in parents]
            enfants = [self.graph.get_node_by_id(pid) for pid in node.children if pid in self.graph.nodes]
            enfants_labels = [p.get_label() for p in enfants]

            # Porte COPIE

            if label == ' ':
                p = parents[0]
                #if p.get_label() in ['0', '1']:
                self.graph.remove_edge(p.id, node.id)
                node.set_label(p.get_label())
                nig = self.graph.get_node_by_id(p.id)
                for c in enfants:
                    self.graph.add_edge(nig,c)
                return True


            # Porte NON
            elif label == '~' and len(parents) == 1:
                p = parents[0]
                if p.get_label() in ['0', '1']:
                    self.graph.remove_edge(p.id, node.id)
                    self.fusion_noeuds(p.id, node.id, label=str(1 - int(p.get_label())))
                    return True

            # Porte ET
            elif label == '&':
                
                if '0' in parent_labels:
                    for p in parents:
                        self.remove_edge(p.id, node.id)
                    for p in parents:
                        if p.get_label() == '0':
                            self.fusion_noeuds(p.id, node.id, label='0')
                            return True
                elif '1' in parent_labels:
                    for p in parents:
                        if p.get_label() == '1' and len(parents) == 1:
                            self.remove_edge(p.id, node.id)
                            self.fusion_noeuds(p.id, node.id, label='1')
                            return True
                        if p.get_label() == '1' and len(parents) > 1:
                            self.remove_edge(p.id, node.id)
                            return True
                    #return True

            # Porte OU
            elif label == '|':
                if '1' in parent_labels:
                    for p in parents:
                        self.remove_edge(p.id, node.id)
                    for p in parents:
                        if p.get_label() == '1':
                            self.fusion_noeuds(p.id, node.id, label='1')
                            return True
                elif '0' in parent_labels:
                    for p in parents :
                        if p.get_label() == '0' and len(parents) == 1:
                            self.remove_edge(p.id, node.id)
                            self.fusion_noeuds(p.id, node.id, label='0')
                            return True
                        if p.get_label() == '0' and len(parents) > 1:
                            self.remove_edge(p.id, node.id)
                            return True
                    #return True

            # Porte XOR
            elif label == '^':
                if '0' in parent_labels:
                    for p in parents :
                        if p.get_label() == '0' and len(parents) == 1:
                            self.remove_edge(p.id, node.id)
                            self.fusion_noeuds(p.id, node.id, label='0')
                            return True
                        if p.get_label() == '0' and len(parents) > 1:
                            self.remove_edge(p.id, node.id)
                            return True
                elif '1' in parent_labels:
                    # XOR avec 1 revient à une négation
                    ni = self.add_node(label='^')
                    nig = self.get_node_by_id(ni)
                    node.set_label('~')
                    for p in parents:
                        self.graph.remove_edge(p.id, node.id)
                        if p.get_label() != "1":
                            self.graph.add_edge(p, nig)
                    self.graph.add_edge(nig, node)
                    return True

        return False

    def evaluate_parent(self):
        """
        Applique simplify_once tant que nécessaire
        """
        while self.simplify_once():
            pass
    @classmethod
    def encoder(cls):
        return cls.parse_parentheses(
            "((d1^d2)^d4)((d1^d3)^d4)((d2^d3)^d4)d1d2d3d4"
        )[0]

    @classmethod
    def decoder(cls):
        """
        Construit le décodeur du code de Hamming (7,4).
        Cette version reprend les recalculs de parité et tous les bits reçus.
        """
        expr = (
            "(((r1^r3)^r5)^r7)"
            "(((r2^r3)^r6)^r7)"
            "(((r4^r5)^r6)^r7)"
            "r1r2r3r4r5r6r7"
        )
        return cls.parse_parentheses(expr)[0]
    
    def compose_with(self, other):
        """
        Compose ce circuit avec un autre (self ∘ other).
        Relie les sorties de `other` aux entrées de `self`.
        """
        if len(self.get_input_ids()) != len(other.get_output_ids()):
            raise ValueError("Les sorties de 'other' doivent correspondre aux entrées de 'self'.")

        # Fusionner les noeuds des deux circuits
        new_nodes = {**other.get_nodes_dict(), **self.get_nodes_dict()}

        # Création du graphe composé
        composed = open_digraph(
            inputs=other.get_input_ids(),
            outputs=self.get_output_ids(),
            nodes=list(new_nodes.values())
        )

        # Connecter les sorties de other aux entrées de self
        for self_in, other_out in zip(self.get_input_ids(), other.get_output_ids()):
            composed.add_edge(other_out, self_in)

        return bool_circ(composed)

    def rewrite_involution_NOT(self):
        """
        Applique la règle ~~x = x (involution de la porte NON).
        Supprime les doubles NOT consécutifs.
        """
        for node in list(self.get_nodes()):
            if node.get_label() == '~~':
                children = list(node.children)
                if len(children) == 1:
                    child = self.get_node_by_id(children[0])
                    if child.get_label() == '~~' and len(child.children) == 1:
                        grandchild_id = list(child.children)[0]
                        for parent_id in list(node.parents):
                            self.add_edge(parent_id, grandchild_id)
                        self.remove_node_by_id(node.id)
                        self.remove_node_by_id(child.id)
    def rewrite_involution_NOT(self):
        """Applique la règle ~~x = x."""
        for node in list(self.get_nodes()):
            if node.get_label() == '~~':
                children = list(node.children)
                if len(children) == 1:
                    child = self.get_node_by_id(children[0])
                    if child.get_label() == '~~' and len(child.children) == 1:
                        grandchild_id = list(child.children)[0]
                        for parent_id in list(node.parents):
                            self.add_edge(parent_id, grandchild_id)
                        self.remove_node_by_id(node.id)
                        self.remove_node_by_id(child.id)

    def rewrite_effacement(self):
        """Supprime les opérations dont tous les parents ont la même entrée."""
        for node in list(self.get_nodes()):
            if node.indegree() > 1:
                labels = [self.get_node_by_id(p).get_label() for p in node.parents]
                if all(lab == labels[0] for lab in labels):
                    for p in node.parents:
                        for c in node.children:
                            self.add_edge(p, c)
                    self.remove_node_by_id(node.id)

    def rewrite_associativity_XOR(self):
        """Regroupe les XOR en les associant (pas d'effet fonctionnel, utile pour simplification)."""
        for node in self.get_nodes():
            if node.get_label() == '^' and node.indegree() == 2:
                a, b = node.parents
                n1, n2 = self.get_node_by_id(a), self.get_node_by_id(b)
                if n1.get_label() == '^' or n2.get_label() == '^':
                    # Pas une vraie réécriture ici, on pourrait restructurer
                    pass  # Placeholder

    def rewrite_propagate_NOT_through_XOR(self):
        """Applique la règle : ~~(a ^ b) = ~~a ^ b = a ^ ~~b"""
        for node in list(self.get_nodes()):
            if node.get_label() == '~~':
                child_id = list(node.children)[0]
                child = self.get_node_by_id(child_id)
                if child.get_label() == '^':
                    # Duplique le NOT sur les entrées
                    for parent_id in list(child.parents):
                        p = self.get_node_by_id(parent_id)
                        not_node = node(self.new_id(), '~~', {p.id: 1}, {})
                        self.add_node(not_node)
                        child.replace_parent(p.id, not_node.id)

    def rewrite_all(self):
        """Applique toutes les règles jusqu'à stabilisation."""
        prev = None
        while str(prev) != str(self):
            prev = self.copy()
            self.rewrite_involution_NOT()
            self.rewrite_effacement()
            self.rewrite_propagate_NOT_through_XOR()
            # Ajouter d'autres règles si nécessaires

    #############


    # TP12


    ##############

    
    def copies(self, id_log, id_in):
        '''Arguments: id_log (int), id_in (int).
        Returns: None.
        Description: Replaces a logical copy node by a constant (0 or 1) depending on the input node's label.'''
        if self.nodes[id_in].get_label() == "0":
            for child in self.nodes[id_log].get_children():
                self.add_node("0", {}, {child:1})
        elif self.nodes[id_in].get_label() == "1":
            for child in self.nodes[id_log].get_children():
                self.add_node("1", {}, {child:1})
        else:
            raise Exception("label != de 0 ou 1")
        self.remove_node_by_id(id_log)
        self.remove_node_by_id(id_in)

    def non(self, id_log, id_in):
        '''Arguments: id_log (int), id_in (int).
        Returns: None.
        Description: Computes the NOT of the input node and assigns the result to the logical node.'''
        if self.nodes[id_in].get_label() == "0":
            self.nodes[id_log].set_label("1")
        elif self.nodes[id_in].get_label() == "1":
            self.nodes[id_log].set_label("0")
        else:
            raise Exception("label != de 0 ou 1")
        self.remove_node_by_id(id_in)
    
    def et(self, id_log, id_in):
        '''Arguments: id_log (int), id_in (int).
        Returns: None.
        Description: Applies simplification rules for the AND operation based on the input value.'''
        if self.nodes[id_in].get_label() == "0":
            self.nodes[id_log].set_label("0")
            for parent in list(self.nodes[id_log].get_parents()):
                self.nodes[parent].set_label("")
                self.remove_parallel_edges(parent, id_log)
        elif self.nodes[id_in].get_label() == "1":
            self.remove_node_by_id(id_in)
        else:
            raise Exception("label != de 0 ou 1")
    
    def ou(self, id_log, id_in):
        '''Arguments: id_log (int), id_in (int).
        Returns: None.
        Description: Applies simplification rules for the OR operation based on the input value.'''
        if self.nodes[id_in].get_label() == "1":
            self.nodes[id_log].set_label("1")
            for parent in list(self.nodes[id_log].get_parents()):
                self.nodes[parent].set_label("")
                self.remove_parallel_edges(parent, id_log)
        elif self.nodes[id_in].get_label() == "0":
            self.remove_node_by_id(id_in)
        else:
            raise Exception("label != de 0 ou 1")

    def xor(self, id_log, id_in):
        '''Arguments: id_log (int), id_in (int).
        Returns: None.
        Description: Applies simplification rules for the XOR operation based on the input value.'''
        if self.nodes[id_in].get_label() == "1":
            self.remove_node_by_id(id_in)
            new_non = self.add_node("~", {}, self.nodes[id_log].get_children())
            for child in list(self.nodes[id_log].get_children()):
                self.remove_parallel_edges(id_log, child)
            self.add_edge(id_log, new_non)
        elif self.nodes[id_in].get_label() == "0":
            self.remove_node_by_id(id_in)
        else:
            raise Exception("label != de 0 ou 1")

    def neutres(self, id_log):
        '''Arguments: id_log (int).
        Returns: None.
        Description: Replaces a binary logic node (|, ^, &) with its neutral element.'''
        if self.nodes[id_log].get_label() in ["|", "^"]:
            self.nodes[id_log].set_label("0")
        elif self.nodes[id_log].get_label() == "&":
            self.nodes[id_log].set_label("1")
        else:
            raise Exception("label != de & ou | ou ^")

    def logique(self, id_log, id_in):
        '''Arguments: id_log (int), id_in (int).
        Returns: None.
        Description: Applies logic simplification and evaluation depending on the type of logic gate.'''
        if self.nodes[id_in].get_label() in ["|", "^", "&"]:
            self.neutres(id_in)
        elif self.nodes[id_log].get_label() == "":
            self.copies(id_log, id_in)
        elif self.nodes[id_log].get_label() == "~":
            self.non(id_log, id_in)
        elif self.nodes[id_log].get_label() == "&":
            self.et(id_log, id_in)
        elif self.nodes[id_log].get_label() == "|":
            self.ou(id_log, id_in)
        elif self.nodes[id_log].get_label() == "^":
            self.xor(id_log, id_in)
        else:
            raise Exception("label invalide")

    def evaluate(self):
        '''Arguments: None.
        Returns: None.
        Description: Evaluates the circuit by propagating constant values and simplifying logic gates.'''
        fini = False
        while not fini:
            fini = True
            co_leaf = [id for id, node in self.nodes.items() if not node.parents]
            for id in co_leaf:
                for child in list(self.nodes[id].get_children()):
                    if child not in self.outputs:
                        fini = False
                        self.logique(child, id)
        for id, node in list(self.nodes.items()):
            if node.get_label() in ["|", "^", "&"]:
                self.logique(-1, id)
            if node.get_label() == "":
                self.remove_node_by_id(id)

    def asso_xor(self, id1, id2):
        '''Arguments: id1 (int), id2 (int).
        Returns: None.
        Description: Merges two XOR nodes with identical labels and propagates connections.'''
        if self.nodes[id1].get_label() == self.nodes[id2].get_label() and self.nodes[id2].get_label() == "^":
            for parent in list(self.nodes[id1].get_parents()):
                self.add_edge(parent, id2)
            self.remove_node_by_id(id1)
        else:
            raise Exception("erreur label")

    def asso_copie(self, id1, id2):
        '''Arguments: id1 (int), id2 (int).
        Returns: None.
        Description: Merges two copy nodes and forwards connections.'''
        if self.nodes[id1].get_label() == self.nodes[id2].get_label() and self.nodes[id2].get_label() == "":
            for child in list(self.nodes[id2].get_children()):
                self.add_edge(id1, child)
            self.remove_node_by_id(id2)
        else:
            raise Exception("erreur label")

    def invo_xor(self, id_xor, id_copie):
        '''Arguments: id_xor (int), id_copie (int).
        Returns: None.
        Description: Involutes a XOR node with respect to a copy input, handling multiplicity.'''
        if self.nodes[id_xor].get_label() == "^" and self.nodes[id_copie].get_label() == "":
            if self.nodes[id_xor].get_parents()[id_copie] % 2 == 0:
                self.remove_parallel_edges(id_copie, id_xor)
            else:
                self.remove_parallel_edges(id_copie, id_xor)
                self.add_edge(id_copie, id_xor)
        else:
            raise Exception("erreur label")

    def effacement(self, id1, id2):
        '''Arguments: id1 (int), id2 (int).
        Returns: None.
        Description: Deletes a node and a useless copy node that has no children.'''
        if self.nodes[id2].get_label() == "" and not self.nodes[id2].get_children():
            for parent in list(self.nodes[id1].get_parents()):
                self.add_node("", {parent:1}, {})
            self.remove_node_by_id(id1)
            self.remove_node_by_id(id2)
        else:
            raise Exception("erreur label")

    def non_xor(self, id_non, id_xor):
        '''Arguments: id_non (int), id_xor (int).
        Returns: None.
        Description: Merges a NOT gate and a XOR gate by pushing NOT after the XOR.'''
        if self.nodes[id_non].get_label() == "~" and self.nodes[id_xor].get_label() == "^":
            for parent in list(self.nodes[id_non].get_parents()):
                self.add_edge(parent, id_xor)
            self.remove_node_by_id(id_non)
            id_non = self.add_node("~", {}, self.nodes[id_xor].get_children())
            for child in list(self.nodes[id_xor].get_children()):
                self.remove_parallel_edges(id_xor, child)
            self.add_edge(id_xor, id_non)
        else:
            raise Exception("erreur label")

    def non_copie(self, id_non, id_copie):
        '''Arguments: id_non (int), id_copie (int).
        Returns: None.
        Description: Pushes NOT gates after copy nodes by duplicating them on the output branches.'''
        if self.nodes[id_non].get_label() == "~" and self.nodes[id_copie].get_label() == "":
            for parent in list(self.nodes[id_non].get_parents()):
                self.add_edge(parent, id_copie)
            self.remove_node_by_id(id_non)
            for child in list(self.nodes[id_copie].get_children()):
                self.add_node("~", {id_copie:1}, {child:1})
                self.remove_parallel_edges(id_copie, child)
        else:
            raise Exception("erreur label")

    def invo_non(self, id1, id2):
        '''Arguments: id1 (int), id2 (int).
        Returns: None.
        Description: Merges two NOT gates into a direct connection (double negation removal).'''
        if self.nodes[id1].get_label() == self.nodes[id2].get_label() and self.nodes[id2].get_label() == "~":
            for parent in list(self.nodes[id1].get_parents()):
                for child in list(self.nodes[id2].get_children()):
                    self.add_edge(parent, child)
            self.remove_node_by_id(id1)
            self.remove_node_by_id(id2)
        else:
            raise Exception("erreur label")

    def reecrit(self, id1, id2):
        '''Arguments: id1 (int), id2 (int).
        Returns: bool.
        Description: Applies one rewrite rule depending on node labels and structure. Returns True if rewritten.'''
        if self.nodes[id1].get_label() == self.nodes[id2].get_label() and self.nodes[id2].get_label() == "^":
            self.asso_xor(id1, id2)
        elif self.nodes[id1].get_label() == self.nodes[id2].get_label() and self.nodes[id2].get_label() == "":
            self.asso_copie(id1, id2)
        elif self.nodes[id2].get_label() == "^" and self.nodes[id1].get_label() == "":
            if self.nodes[id2].get_parents()[id1] <2:
                return False
            self.invo_xor(id2, id1)
        elif self.nodes[id2].get_label() == "" and not self.nodes[id2].get_children():
            self.effacement(id1, id2)
        elif self.nodes[id1].get_label() == "~" and self.nodes[id2].get_label() == "^":
            self.non_xor(id1, id2)
        elif self.nodes[id1].get_label() == "~" and self.nodes[id2].get_label() == "":
            self.non_copie(id1, id2)
        elif self.nodes[id1].get_label() == self.nodes[id2].get_label() and self.nodes[id2].get_label() == "~":
            self.invo_non(id1, id2)
        else:
            return False
        return True

    def simplifie(self):
        '''Arguments: None.
        Returns: None.
        Description: Repeatedly applies rewrite rules to simplify the boolean circuit.'''
        modifie = False
        for id, node in list(self.nodes.items()):
            if id not in self.nodes:
                continue
            for id2 in list(self.nodes[id].get_children()):
                if id2 not in self.nodes or id == id2 or id not in self.nodes:
                    continue
                if self.reecrit(id, id2):
                    modifie = True
        if modifie:
            self.simplifie()

    def simplifie_evaluate(self):
        '''Arguments: None.
        Returns: None.
        Description: Performs a simplified evaluation by combining logic evaluation and structural simplification.'''
        self.simplifie()
        fini = False
        while not fini:
            fini = True
            co_leaf = [id for id, node in self.nodes.items() if not node.parents]
            for id in co_leaf:
                if id in self.nodes:
                    for child in list(self.nodes[id].get_children()):
                        if child not in self.outputs:
                            fini = False
                            self.logique(child, id)
                            self.simplifie()
        for id, node in list(self.nodes.items()):
            if node.get_label() in ["|", "^", "&"]:
                self.logique(-1, id)
            if id not in self.outputs:
                if not node.get_children():
                    self.remove_node_by_id(id)

