from random import *
from modules.mixins.compositions_mx import OpenDigraphCompositionsMixin
from modules.nodes import node

class open_digraph(OpenDigraphCompositionsMixin): # for open directed graph
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
        if not isinstance(graph, open_digraph):
            raise TypeError("L'argument doit être une instance de open_digraph")
        super().__init__(graph.get_input_ids(), graph.get_output_ids(), graph.get_nodes())
        self.graph = graph
        if not self.is_well_formed_cyclic():
            raise ValueError("Le circuit booléen n'est pas bien formé.")

    def is_well_formed_cyclic(self):
        """
        Vérifie si le circuit est acyclique et respecte les contraintes de degré pour chaque type de nœud.
        """
        if self.is_cyclic():
            return False
        if not self.graph.assert_is_well_formed():
            return False
        for node in self.get_nodes():
            label = node.get_label()
            indeg = node.indegree()
            outdeg = node.outdegree()
            if label in {'0', '1'}:
                if indeg != 0:
                    return False
            elif label == '':
                if indeg not in [0, 1]:
                    return False
            elif label in {'&', '|'}:
                if indeg < 2 or outdeg != 1:
                    return False
            elif label == '~~':
                if indeg != 1 or outdeg != 1:
                    return False
            elif label == '^':
                if indeg < 2 or outdeg != 1:
                    return False
            elif label not in {'', '0', '1', '&', '|', '^', '~~'}:
                return False
        return True

    @classmethod
    def int_bin(cls, n, t):
        """
        Crée un circuit booléen représentant l'entier `n` sur `t` bits.
        """
        nbin = bin(n)[2:].zfill(t)
        nodes = []
        for i in range(t):
            bit = nbin[i]
            nodes.append(node(i, bit, {}, {}))
        return cls(open_digraph([], [], nodes))

    @classmethod
    def parse_parentheses(cls, *args):
        """
        Construit un bool_circ à partir de chaînes bien parenthésées.
        """
        root = node(0, '', {}, {})
        nodes = {0: root}
        current_id = 0
        next_id = 1
        s2, s3 = '', ''
        val = []
        stack = []

        for s in args:
            for char in s:
                if char == '(':
                    if s2.strip():
                        nodes[current_id].set_label(s2.strip())
                    parent = node(next_id, '', {}, {current_id: 1})
                    nodes[current_id].add_parent_id(next_id)
                    nodes[next_id] = parent
                    stack.append(current_id)
                    current_id = next_id
                    next_id += 1
                    s2 = ''
                elif char == ')':
                    if s2.strip():
                        nodes[current_id].set_label(s2.strip())
                    if stack:
                        current_id = stack.pop()
                    if s3.strip() and s3.strip() not in val:
                        val.append(s3.strip())
                    s2 = ''
                    s3 = ''
                else:
                    s2 += char
                    if char not in {'|', '^', '~', '&'}:
                        s3 += char

        graph = open_digraph([], [], list(nodes.values()))

        id_val = {}
        input_ids = []
        for x in val:
            ids = [i for i, n in graph.nodes.items() if n.get_label() == x]
            if ids:
                main_id = ids[0]
                for other_id in ids[1:]:
                    graph.fusion_noeuds(main_id, other_id)
                graph.nodes[main_id].set_label('')
                input_ids.append(main_id)

        graph.remove_node_by_id(0)
        return cls(graph), val
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
