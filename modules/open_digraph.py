from random import *

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
        if self.children[id] == 0 :
            self.children.pop(id)
        if id in self.children :
            self.children[id]-= 1
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
    def indegree(self):
        """
        renvoie le degré entrant (nombre d'arêtes qui arrivent vers ce noeud)
        """
        s = 0
        for p in self.parents:
            s += self.parents[p]
        return s

    def outdegree(self):
        """
        renvoie le degré sortant (nombre d'arêtes qui partent de ce noeud)
        """
        s = 0
        for c in self.children:
            s += self.children[c]
        return s

    def degree(self):
        """
        renvoie le degré total (somme du degré entrant et du degré sortant)
        """
        return self.indegree() + self.outdegree()


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
    def get_nodes_dico(self): #renvoie le dictionnaire ayyant pour clé l'id de chaque noeud
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

    def remove_nodes_by_id(self,liste):
        """
        liste : (int) list; liste de id des noeuds à supprimer
        supprime les noeuds du graphe dont l'id est dans la liste
        """
        for id in liste:
             self.remove_node_by_id(id)

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
                return "un noeud output n'a pas d'unique parent ou a un fils au moins"
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
def test():
    gr = graph_from_adjacency_matrix([
        [0, 1, 1, 0, 0],
        [0, 0, 0, 1, 2],
        [0, 0, 0, 2, 0],
        [1, 0, 0, 0, 1],
        [0, 0, 0, 0, 0]
    ])
    nodes = gr.get_nodes_dico()
    for node in nodes:
        print(nodes[node])  
test()
"""


"""

Sous-classe Circuit

"""

class bool_circ(open_digraph):
    def __init__(self, graph): 
        super().__init__(graph.get_input_ids(), graph.get_output_ids(), graph.get_nodes())
        if not isinstance(graph, open_digraph):  
            raise TypeError("L'argument doit être une instance de open_digraph") 
        else:
            self.graph = graph
        if not self.is_well_formed_cyclic():
            raise ValueError("Le circuit booléen n'est pas bien formé.")
    def is_well_formed_cyclic(self):
        """
        teste si le circuit booléen est bien un circuit booléen(doit être acyclique et respecter les contraintes de degré)
        """
        if self.is_cyclic():
            return False
        if not self.graph.assert_is_well_formed():
            return False
        for node in self.get_nodes():
            label = node.get_label()
            indeg = node.indegree()
            outdeg = node.outdegree()
            if label == '':
                if indeg != 1:
                    return False  
            elif label == '&' or label == '|': 
                if outdeg != 1:
                    return False  
            elif label == '~': 
                if indeg != 1 or outdeg != 1:
                    return False 
            elif label == '^': 
                if indeg < 2 or outdeg != 1:
                    return False 
        return True
 

