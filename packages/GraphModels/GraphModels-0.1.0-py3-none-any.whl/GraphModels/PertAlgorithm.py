import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random

class PertAlgorithm :
    def __init__(self, nb_tache = 7, taches = None, durees = None, contraintes_anteriorites = None) :
        self.nb_tache = nb_tache
        
        if taches is None :
            self.taches = []
            while len(self.taches) < self.nb_tache :
                tache = input(f"La tache {len(self.taches) + 1} : ")
                if tache in self.taches :
                    print("Tache dèja existe !")
                else :
                    self.taches.append(tache)
        else :
            self.taches = taches
        
        if durees is None :
            self.durees = []
            for tache in self.taches :
                duree = int(input(f"La durèes de la tache {tache} : "))
                if duree < 0 :
                    duree = duree * (-1)
                    self.durees.append([tache, duree])
                else :
                    self.durees.append([tache, duree])
        else :
            self.durees = durees
        
        if contraintes_anteriorites is None :
            self.contraintes_anteriorites = self.creation_contraintes()
        else :
            self.contraintes_anteriorites = contraintes_anteriorites
    
    def creation_contraintes(self):
        print(f"Donner l'ensemble des taches prècèdentes :")
        taches_precedentes = []
        taches_sans_contraintes_debut = []
        taches_sans_contraintes_fin = []
        contraintes_anteriorites = []

        for tache in self.taches :
            nb_predecesseurs = int(input(f"Nombre de taches qui prècèdes la tache {tache} : "))
            if nb_predecesseurs == 0 :
                print(f"la tache {tache} sans predecesseur !")
                taches_sans_contraintes_debut.append(tache)
            else :
                arc = []
                arc_inverse = []
                i = 0
                while i < nb_predecesseurs :
                    predecesseur = input(f"predecesseur {i + 1} : ")
                    arc = [predecesseur, tache]
                    arc_inverse == [arc[1], arc[0]]
                    if (arc in contraintes_anteriorites) or (arc_inverse in contraintes_anteriorites) :
                        print(f"cette contrainte existe dèja !Ressayer\n")
                    else :
                        contraintes_anteriorites.append(arc)
                        taches_precedentes.append(predecesseur)
                        i += 1

        for tache in self.taches :
            if tache not in taches_precedentes :
                taches_sans_contraintes_fin.append(tache)
        
        for contrainte in contraintes_anteriorites :
            contrainte.append(self.durees[self.taches.index(contrainte[0])][1])
        
        for tache in taches_sans_contraintes_debut :
            arc = ["α", tache, 0]
            contraintes_anteriorites.insert(0, arc)
        
        for tache in taches_sans_contraintes_fin :
            arc = [tache, "β", self.durees[self.taches.index(tache)][1]]
            contraintes_anteriorites.append(arc)
        
        self.taches.insert(0, "α")
        self.taches.append("β")
        self.durees.insert(0, ["α", 0])
        self.durees.append(["β", 0])
            
        return contraintes_anteriorites
    
    def dates_au_plutot(self) :
        def initiale_step_dates_au_plutot() :
            S = ['α']
            date_au_plutot = []
            for tache in self.taches :
                date_au_plutot.append([tache, 0])
            return S, date_au_plutot
        
        def choisi_tache_dates_au_plutot(S) :
            next_tache = None
            taches_condidats = []
            for tache in self.taches :
                predecesseurs_contraintes = []
                if tache in S :
                    continue
                else :
                    for contrainte in self.contraintes_anteriorites :
                        if contrainte[1] == tache :
                            predecesseurs_contraintes.append(contrainte)
                    predecesseurs_not_in_S = 0
                    for contrainte in predecesseurs_contraintes :
                        if contrainte[0] not in S :
                            predecesseurs_not_in_S += 1
                    if predecesseurs_not_in_S != 0 :
                        continue
                    else :
                        taches_condidats.append(tache)
  
            if len(taches_condidats) == 0 :
                if len(S) == len(self.taches) :
                    next_tache = 0
                    return next_tache
                elif len(S) < len(self.taches) :
                    return next_tache
            else :
                next_tache = random.choice(taches_condidats)
                return next_tache
        
        def mise_a_jour_date_au_plutot(S, date_au_plutot, next_tache) :
            predecesseurs_next_tache = []
            for contrainte in self.contraintes_anteriorites :
                if contrainte[1] == next_tache :
                    predecesseurs_next_tache.append(contrainte)
  
            maximum = predecesseurs_next_tache[0]
            date_au_plutot_max = date_au_plutot[self.taches.index(maximum[0])][1] + maximum[2]

            for contrainte in predecesseurs_next_tache : 
                if date_au_plutot[self.taches.index(contrainte[0])][1] + contrainte[2] > date_au_plutot_max :
                    maximum = contrainte
                    date_au_plutot_max = date_au_plutot[self.taches.index(maximum[0])][1] + maximum[2]
  
            S.append(next_tache)
            date_au_plutot[self.taches.index(next_tache)][1] = date_au_plutot_max
            return S, date_au_plutot
        
        def generate_dates_au_plutot() :
            S, date_au_plutot = initiale_step_dates_au_plutot()
            while len(S) < len(self.taches) :
                next_tache = choisi_tache_dates_au_plutot(S)
                if next_tache == 0 :
                    print("we have reashed all the taches ! ")
                    break
                elif next_tache is None :
                    print("this project is not possible ! ")
                    break
                else :
                    S, date_au_plutot = mise_a_jour_date_au_plutot(S, date_au_plutot, next_tache)
            return date_au_plutot
        
        return generate_dates_au_plutot()
    
    def duree_maximal(self) :
        date_au_plutot = self.dates_au_plutot()
        duree_minimal = date_au_plutot[-1][1]
        print(f"la duree minimal pour la realisation de projet est {duree_minimal}")
        
    def dates_au_plus_tard(self) :
        def initiale_step_dates_au_plus_tard(date_au_plutot) :
            G = ['β']
            date_au_plus_tard = date_au_plutot
            return G, date_au_plus_tard
        
        def choisi_tache_dates_au_plus_tard(G) :
            next_tache = None
            taches_condidats = []
            taches = self.taches[::-1]
            for tache in taches :
                sucesseurs_contraintes = []
                if tache in G :
                    continue
                else :
                    for contrainte in self.contraintes_anteriorites :
                        if contrainte[0] == tache :
                            sucesseurs_contraintes.append(contrainte)

                nb_sucesseurs_not_in_G = 0
                for contrainte in sucesseurs_contraintes :
                    if contrainte[1] not in G :
                        nb_sucesseurs_not_in_G += 1
      
                if nb_sucesseurs_not_in_G != 0 :
                    continue
                else :
                    taches_condidats.append(tache)
   
            if len(taches_condidats) == 0 :
                if len(G) == len(self.taches) :
                    next_tache = 0
                    return next_tache
                elif len(G) < len(self.taches) :
                    return next_tache
            else :
                next_tache = random.choice(taches_condidats)
                return next_tache
        
        def mise_a_jour_date_au_plus_tard(G, date_au_plus_tard, next_tache) :
            sucesseurs_next_tache = []
            for contrainte in self.contraintes_anteriorites :
                if contrainte[0] == next_tache :
                    sucesseurs_next_tache.append(contrainte)
  
            minimum = sucesseurs_next_tache[0]
            date_au_plus_tard_min = date_au_plus_tard[self.taches.index(minimum[1])][1] - minimum[2]
            for contrainte in sucesseurs_next_tache : 
                if date_au_plus_tard[self.taches.index(contrainte[1])][1] - contrainte[2] < date_au_plus_tard_min :
                    minimum = contrainte
                    date_au_plus_tard_min = date_au_plus_tard[self.taches.index(minimum[1])][1] - minimum[2]
  
            G.append(next_tache)
            date_au_plus_tard[self.taches.index(next_tache)][1] = date_au_plus_tard_min
            return G, date_au_plus_tard
        
        def generate_dates_au_plus_tard(date_au_plutot) :
            G, date_au_plus_tard = initiale_step_dates_au_plus_tard(date_au_plutot)
            while len(G) < len(self.taches) :
                next_tache = choisi_tache_dates_au_plus_tard(G)
                if next_tache == 0 :
                    print("we have reashed all the taches ! ")
                    break
                elif next_tache is None :
                    print("this project is not possible ! ")
                    break
                else :
                    G, date_au_plus_tard = mise_a_jour_date_au_plus_tard(G, date_au_plus_tard, next_tache)
            return date_au_plus_tard
        
        return generate_dates_au_plus_tard(self.dates_au_plutot())
    
    def chemin_critique(self) :
        date_au_plutot = self.dates_au_plutot()
        date_au_plus_tard = self.dates_au_plus_tard()
        marge_taches = []
        for tache in self.taches :
            marge_taches.append([tache, 0])

        for t , T, m in zip(date_au_plutot, date_au_plus_tard, marge_taches) :
            if T[1] == t[1]  :
                m[1] = 0
            else :
                m[1] = T[1] - t[1]
        print(f"la marge : {marge_taches}")
        
        chemin_critique = []
        for tache in self.taches :
            for contrainte in self.contraintes_anteriorites :
                if contrainte[0] == tache and marge_taches[self.taches.index(tache)][1] == 0 and marge_taches[self.taches.index(contrainte[0])][1] == 0:
                    chemin_critique.append(contrainte)
                    break
        return chemin_critique
    
    def visualization(self) :
        chemin_critique = self.chemin_critique()
        if chemin_critique is None :
            print("Can't visualze the graph !")
        else :
            contrainte_sans_longueur = []
            for arc in self.contraintes_anteriorites:
                contrainte_sans_longueur.append([arc[0], arc[1]])

            graphe = nx.DiGraph()

            graphe.add_nodes_from(self.taches)
            graphe.add_edges_from(contrainte_sans_longueur)

            pos = nx.shell_layout(graphe)

            nx.draw(graphe,pos, with_labels= True, node_color= 'Skyblue', node_size= 1000, font_size= 15)

            edge_labels= nx.get_edge_attributes(graphe,'weight')
            nx.draw_networkx_edge_labels(graphe,pos,edge_labels= edge_labels, font_size= 12, font_color= 'black')

            edges_to_highlight = [(arc[0], arc[1]) for arc in chemin_critique]
            nx.draw_networkx_edges(graphe, pos, edgelist= edges_to_highlight, edge_color= 'tab:green', width= 8, alpha= 0.5)

            plt.show()

