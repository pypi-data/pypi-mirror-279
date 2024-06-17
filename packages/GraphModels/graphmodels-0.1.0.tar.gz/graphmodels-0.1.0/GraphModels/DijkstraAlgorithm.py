import math
import networkx as nx
import matplotlib.pyplot as plt

class DijkstraAlgorithm :
    def __init__(self, nb_sommets = 6, nb_arcs = 12, sommets = None, arcs = None) :
        self.nb_sommets = nb_sommets
        self.nb_arcs = nb_arcs
        if sommets is None :
            self.sommets = ['s']
            for sommet in range(1, self.nb_sommets + 1) :
                self.sommets.append(sommet)
        else :
            self.sommets = sommets
        if arcs is None :
            self.arcs = self.creation_arcs()
        else :
            self.arcs = arcs
        
    def creation_arcs(self) :
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
                print("The vertices must be integers or 's' . Rèessayer !")
                continue
  
            if sommet_initiale == sommet_terminale : 
                print("The initial and terminal vertices cannot be identical !")
                continue
  
            if sommet_initiale not in self.sommets or sommet_terminale not in self.sommets :
                print("The vertices must belong to the defined list of vertices !")
                continue

            arc = [sommet_initiale, sommet_terminale]
  
            if edge_exist(arc, arcs) :
                print("This arc or its reverse already exists, or the arc enters 's' !")
            else :
                longueur = -1
                while longueur < 0 :
                    longueur = int(input(f"Entrer la longueur de l'arc {len(arcs) +1} : "))
                arc.append(longueur)
                arcs.append(arc)
                print("\n")
        return arcs
    
    def final_solution(self) :
        
        def condition_initiale() :
            S = ['s']
            potentiels = []

            successeur_racine = []
            for arc in self.arcs :
                if arc[0] == 's':
                    successeur_racine.append(arc[1])

            for sommet in range(1, self.nb_sommets + 1):
                if sommet not in successeur_racine:
                    potentiels.append([sommet, math.inf])

            for arc in self.arcs:
                if arc[0] == 's':
                    potentiels.append([arc[1], arc[2]])

            potentiels = sorted(potentiels, key = lambda x: x[0])
            potentiels.insert(0, ['s',0])

            print(f"The vertices marked in S are: {S}")
            print(f"Set of arc potentials: {potentiels}")
            return S, potentiels
        
        def prochain_pivot(S, potentiels):
            pivot = 0
            sommet_condidats = []
            sommet_possibles = []
            arc_plus_court_chemin = 0

            for sommet in self.sommets :
                successeurs_sommet_dans_S = 0
                if sommet in S :
                    continue
                else :
                    for arc in self.arcs :
                        if arc[0] == sommet and arc[1] in S:
                            successeurs_sommet_dans_S += 1
                    if successeurs_sommet_dans_S != 0 :
                        continue
                    else :
                        sommet_condidats.append(sommet)

            for sommet in sommet_condidats :
                if potentiels[self.sommets.index(sommet)][1] not in range(0, 100) :
                    continue
                else :
                    sommet_possibles.append(sommet)

            if len(sommet_possibles) == 0:
                if self.sommets[-1] not in S :
                    pivot = self.sommets[-1]
            else:
                pivot = sommet_possibles[0]
                for sommet in sommet_possibles :
                    if potentiels[self.sommets.index(sommet)][1] < potentiels[self.sommets.index(pivot)][1] :
                        pivot = sommet

            for arc in self.arcs :
                if arc[1] == pivot and potentiels[self.sommets.index(pivot)][1] == potentiels[self.sommets.index(arc[0])][1] + arc[2]:
                    arc_plus_court_chemin = arc
                    break

            return pivot, arc_plus_court_chemin
        
        def mise_a_jour_potentiels(pivot, S, potentiels) :
            successeurs_pivot = []
            for arc in self.arcs :
                if arc[0] == pivot :
                    successeurs_pivot.append(arc)

            for arc in successeurs_pivot :
                if potentiels[self.sommets.index(arc[1])][1] > (potentiels[self.sommets.index(pivot)][1] + arc[2]) :
                    potentiels[self.sommets.index(arc[1])][1] = potentiels[self.sommets.index(pivot)][1] + arc[2]

            S.append(pivot)
            return potentiels, S
        
        S, potentiels = condition_initiale()
        iteration = 0  
        print(f"{iteration} iteration :\nS = {S}\npotentiels = {potentiels}\n")
        pc_chemin = []
        while len(S) < self.nb_sommets + 1:
            iteration += 1 
            pivot, arc = prochain_pivot(S, potentiels)  
            pc_chemin.append(arc)  

            if pivot == 0 :  
                if len(S) == self.nb_sommets + 1 :
                    print("Finished! All vertices are marked: X = S")
                else : 
                    print("Finished! Unable to mark all vertices: vertex 's' is not the root")
                break  
            else :
                potentiels, S = mise_a_jour_potentiels(pivot, S, potentiels)  
                print(f"{iteration} iteration :\nS = {S}\npotentiels = {potentiels}\n")  # Affichage de l'état actuel
        
        print(f"Final potentials : {potentiels}\nShortest path trees : {pc_chemin}")  
        if pc_chemin[-1] == 0 :
            pc_chemin.pop()
        return pc_chemin
    
    def visualization(self) :
        pc_chemin = self.final_solution()
        graphe = nx.DiGraph()
        graphe.add_nodes_from(self.sommets)
        graphe.add_weighted_edges_from(self.arcs)

        pos = nx.shell_layout(graphe)

        nx.draw(graphe, pos, with_labels=True, node_color='SkyBlue', node_size=1000, font_size=15, font_weight='bold')

        edge_labels = nx.get_edge_attributes(graphe, 'weight')
        nx.draw_networkx_edge_labels(graphe, pos, edge_labels=edge_labels, font_size=12, font_color='red')

        edges_to_highlight = [(arc[0], arc[1]) for arc in pc_chemin]
        nx.draw_networkx_edges(graphe, pos, edgelist=edges_to_highlight, edge_color='tab:green', width=8, alpha= 0.5)

        plt.show()

        for sommet in graphe.nodes :
            print(f"degrè de {sommet} = {graphe.degree(sommet)}")
            graphe.nodes[sommet]['label'] = sommet

        print(f"Number of vertices : {graphe.number_of_nodes()}")
        print(f"Number of edges : {graphe.number_of_edges()}")

