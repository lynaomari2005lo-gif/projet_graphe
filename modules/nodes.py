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
    def get_idc(self):
        return [n for n in self.children]
    def get_idp(self):
        return [n for n in self.parents]
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
