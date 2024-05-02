def createGraph(proposition_transport):
        nb_lignes = len(proposition_transport)
        nb_colonnes = len(proposition_transport[0])
        graph = {}
        # On crée un graphe orienté à partir de la proposition de transport
        for i in range(nb_lignes): # On parcourt les lignes
            graph[i] = []
            for j in range(nb_colonnes): # On parcourt les colonnes
                if proposition_transport[i][j] > 0:  # Si la case est non nulle
                    graph[i].append(j + nb_lignes)  # On ajoute un arc de i à j ( on ajoute)
        for j in range(nb_colonnes):
            graph[j + nb_lignes] = []
            for i in range(nb_lignes):
                if proposition_transport[i][j] > 0:
                    graph[j + nb_lignes].append(i)
        return graph



def isAcylique(transportProposition):
        nb_lignes = len(transportProposition.suppliers)
        nb_colonnes = len(transportProposition.customers)
        
        proposition_transport = [[0 for _ in range(nb_colonnes)] for _ in range(nb_lignes)]
        for i in range(nb_lignes):
            for j in range(nb_colonnes):
                proposition_transport[i][j] = transportProposition.links[i * nb_colonnes + j].units

        # On crée un graphe orienté à partir de la proposition de transport
        graph = createGraph(proposition_transport)
        
        # on construit la matrice d'adjacence (ici symétrique car le graphe est non orienté)
        matriceAdj = [[0 for _ in range(nb_lignes + nb_colonnes)] for _ in range(nb_lignes + nb_colonnes)]
        for i in range(nb_lignes):
            for j in graph[i]:
                matriceAdj[i][j] = 1
                matriceAdj[j][i] = 1
        # On prends tous les sommets. Pour chaque sommet, on fait un parcours en largeur pour tenter de retomber sur le sommet de départ
        for s in graph:
            result = estCycle(matriceAdj, s)
            if result:
                print("Cycle trouvé:", end=" ")
                for i in range(len(result)):
                    # le resultat est affiché sous cette forme : [0, 1, 9, 5]
                    # or on veut afficher les sommets correspondants dans la proposition de transport
                    if result[i] < nb_lignes:
                        print(f"P{result[i] + 1} -> ", end="")
                    else:
                        print(f"C{result[i] - nb_lignes + 1} -> ", end="")
                print("etc...")
                return False
        return True
    

def estCycle(matriceAdj, u):
    n = len(matriceAdj)
    file = []
    visites = [False] * n
    visites[u] = True
 
    # Pour mémoriser à partir de quel sommet nous avons découvert chaque sommet du graphe
    parent = [-1] * n
 
    # Au départ le parent de u est u lui même
    parent[u] = u
 
    file.append(u)
    while file:
        courant = file.pop(0)
        visites[courant] = True
        for i in range(n):
            if matriceAdj[courant][i] > 0 and visites[i] == False:
                file.append(i)
                visites[i] = True
 
                # Parent de i et le noeud courant
                parent[i] = courant
 
            # Si "i" est un noeud adjacent, déjà visité et "i" n'est pas le parent de courant
            # Donc il y a un cycle, retourner le cycle
            elif matriceAdj[courant][i] > 0 and visites[i] == True and parent[courant] != i:

                cycle = []
                cycle.append(courant)
                cycle.append(i)
                while parent[i] != i:
                    i = parent[i]
                    cycle.append(i)
                return cycle
    return False
