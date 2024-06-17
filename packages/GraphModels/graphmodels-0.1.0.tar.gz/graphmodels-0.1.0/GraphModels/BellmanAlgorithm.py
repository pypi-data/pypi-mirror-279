import random
import matplotlib.pyplot as plt
import networkx as nx

class BellmanAlgorithm :
    def __init__(self, nb_sommets = 6, nb_arcs = 12,  sommets = None, edges = None) :
        self.nb_sommets = nb_sommets
        self.nb_arcs = nb_arcs
        if sommets is None :
            self.sommets = ['s']
            for sommet in range(1, self.nb_sommets+1) :
                self.sommets.append(sommet)
        else :
            self.sommets = sommets
        
        if edges is None :
            self.edges = self.creation_edges()
        else :
            self.edges = edges
    
    def creation_edges(self) :
        
        def edge_exist(arc, arcs) :
            arc_inverse = [arc[1], arc[0]]
            return (arc_inverse in arcs) or (arc[1] == 's') or  (arc in arcs)
        
        arcs = []
        while len(arcs) < self.nb_arcs :
            sommet_initiale = input(f"Provide the initial vertex of the arc {len(arcs) + 1} : ")
            sommet_terminale = input(f"Provide the terminal vertex of the arc {len(arcs) + 1} : ")

            try :
                if sommet_initiale != 's' :
                    sommet_initiale = int(sommet_initiale)
                sommet_terminale = int(sommet_terminale)
            except ValueError :
                print("The vertices must be integers or 's' !")
                continue
  
            if sommet_initiale == sommet_terminale : 
                print("The initial and terminal vertices cannot be identical!")
                continue
  
            if sommet_initiale not in self.sommets or sommet_terminale not in self.sommets :
                print("The vertices must belong to the defined list of vertices !")
                continue

            arc = [sommet_initiale, sommet_terminale]
  
            if edge_exist(arc, arcs) :
                print("This arc or its reverse already exists, or the arc enters 's' !")
            else :
                longueur = int(input(f"Enter the length of the arc {len(arcs) +1} : "))
                arc.append(longueur)
                arcs.append(arc)
                print("\n")
        return arcs    
    
    
    def final_solution(self) :
        
        def condition_initiale() :
            S = ['s']
            potentiels = []
            pc_chemins = []

            for sommet in self.sommets :
                potentiels.append([sommet, 0])
            return S, potentiels, pc_chemins
    
        def prochain_voisin(S) :
            nouveau_pivot = 0
            arcs_predecesseurs = []
            sommets_condidats = []

            for sommet in self.sommets :
                predecesseurs_sommets_pas_dans_S = 0
                if sommet in S :
                    continue
                else :
                    for arc in self.edges :
                        if arc[1] == sommet :
                            arcs_predecesseurs.append(arc)
                    if arcs_predecesseurs == [] :
                        continue
                    else :
                        for arc in arcs_predecesseurs :
                            if arc[0] not in S :
                                predecesseurs_sommets_pas_dans_S += 1
                        if predecesseurs_sommets_pas_dans_S != 0 :
                            continue
                        else :
                            sommets_condidats.append(sommet)

            if len(sommets_condidats) == 0 :
                if len(S) == self.nb_sommets + 1 :
                    return None
                elif len(S) < self.nb_sommets + 1 :
                    return nouveau_pivot
            else :
                nouveau_pivot = random.choice(sommets_condidats)
                return nouveau_pivot
    
        def mise_a_jour_reseaux(S, potentiels, pivot, pc_chemins) :
            predecesseurs_pivot = []
            plus_court_chemin = 0
            for arc in self.edges :
                if arc[1] == pivot :
                    predecesseurs_pivot.append(arc)

            plus_court_chemin = predecesseurs_pivot[0]
            minimum = potentiels[self.sommets.index(plus_court_chemin[0])][1] + plus_court_chemin[2]
            for arc in predecesseurs_pivot :
                if potentiels[self.sommets.index(arc[0])][1] + arc[2] < minimum :
                    minimum = potentiels[self.sommets.index(arc[0])][1] + arc[2]
                    plus_court_chemin = arc

            potentiels[self.sommets.index(pivot)][1] = minimum

            S.append(pivot)
            pc_chemins.append(plus_court_chemin)
            return S, potentiels, pc_chemins
    
    
        iteration = 0
        S, potentiels, pc_chemins = condition_initiale()
        print(f"{iteration} iteration : \nS = {S}\nPotentiels : {potentiels}\nShortest path trees : {pc_chemins}\n")

        while len(S) < len(self.sommets) + 1 :
            iteration += 1
            pivot = prochain_voisin(S)
            if pivot is None :
                print("We have been able to mark all vertices of S !")
                break
            elif pivot == 0 :
                print("We have not been able to mark all vertices of S, s is not the root!")
                break
            else :
                S, potentiels, pc_chemins = mise_a_jour_reseaux(S, potentiels, pivot, pc_chemins)
                print(f"{iteration} iteration : \nS = {S}\npotentiels = {potentiels}\ntree : {pc_chemins}")
                
        if len(S) == self.nb_sommets + 1 :
            return pc_chemins
        else :
            return None
    
    def visualization(self) :
        pc_chemins = self.final_solution()
        if pc_chemins is None :
            print("Can't visualze the graph !")
        else :
            arcs_sans_longueur = []
            for arc in self.edges :
                arcs_sans_longueur.append([arc[0], arc[1]])

            graphe = nx.DiGraph()

            graphe.add_nodes_from(self.sommets)
            graphe.add_edges_from(arcs_sans_longueur)

            pos = nx.shell_layout(graphe)

            nx.draw(graphe,pos, with_labels= True, node_color= 'Skyblue', node_size= 1000, font_size= 15)

            edge_labels= nx.get_edge_attributes(graphe,'weight')
            nx.draw_networkx_edge_labels(graphe,pos,edge_labels= edge_labels, font_size= 12, font_color= 'black')

            edges_to_highlight = [(arc[0], arc[1]) for arc in pc_chemins]
            nx.draw_networkx_edges(graphe, pos, edgelist= edges_to_highlight, edge_color= 'tab:green', width= 8, alpha= 0.5)

            plt.show()
