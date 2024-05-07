from Model.TransportationProblem import TransportationProblem

def createGraph(proposition_transport):
        nbRows = len(proposition_transport)
        nbColumns = len(proposition_transport[0])
        graph = {}
        # On crée un graphe orienté à partir de la proposition de transport
        for i in range(nbRows): # On parcourt les rows
            graph[i] = []
            for j in range(nbColumns): # On parcourt les columns
                if proposition_transport[i][j] > 0:  # Si la case est non nulle
                    graph[i].append(j + nbRows)  # On ajoute un arc de i à j
        for j in range(nbColumns):
            graph[j + nbRows] = []
            for i in range(nbRows):
                if proposition_transport[i][j] > 0:
                    graph[j + nbRows].append(i)
        return graph



def isGraphAcylic(transportProposition):
        nbRows = len(transportProposition.suppliers)
        nbColumns = len(transportProposition.customers)
        
        proposition_transport = [[0 for _ in range(nbColumns)] for _ in range(nbRows)]
        for i in range(nbRows):
            for j in range(nbColumns):
                proposition_transport[i][j] = transportProposition.links[i * nbColumns + j].units

        # On crée un graphe orienté à partir de la proposition de transport
        graph = createGraph(proposition_transport)
        
        # on construit la matrice d'adjacence (ici symétrique car le graphe est non orienté)
        adjMatrix = computeAdjacencyMatrix(transportProposition, graph)

        
        # On prends tous les sommets. Pour chaque sommet, on fait un parcours en largeur pour tenter de retomber sur le sommet de départ
        for s in graph:
            result = detectCycle(adjMatrix, s)
            if result:
                print("Cycle detected :", end=" ")
                for i in range(len(result)):
                    # le resultat est affiché sous cette forme : [0, 1, 9, 5]
                    # or on veut afficher les sommets correspondants dans la proposition de transport
                    if result[i] < nbRows:
                        print(f"P{result[i] + 1} -> ", end="")
                    else:
                        print(f"C{result[i] - nbRows + 1} -> ", end="")
                print("etc...")
                return False
        return True
    

def detectCycle(adjMatrix, u):
    n = len(adjMatrix)
    file = []
    visitedVertices = [False] * n
    visitedVertices[u] = True
 
    # Pour mémoriser à partir de quel sommet nous avons découvert chaque sommet du graphe
    parent = [-1] * n
 
    # Au départ le parent de u est u lui même
    parent[u] = u
 
    file.append(u)
    while file:
        current = file.pop(0)
        visitedVertices[current] = True
        for i in range(n):
            if adjMatrix[current][i] > 0 and visitedVertices[i] == False:
                file.append(i)
                visitedVertices[i] = True
 
                # Parent de i et le noeud current
                parent[i] = current
 
            # Si "i" est un noeud adjacent, déjà visité et "i" n'est pas le parent de current
            # Donc il y a un cycle, retourner le cycle
            elif adjMatrix[current][i] > 0 and visitedVertices[i] == True and parent[current] != i:

                cycle = []
                cycle.append(current)
                cycle.append(i)
                while parent[i] != i:
                    i = parent[i]
                    cycle.append(i)
                return cycle
    return False



def computeAdjacencyMatrix(self, transportationProblem: TransportationProblem, graph) -> list[list[int]]:
    nbRows = len(transportationProblem.suppliers)
    nbColumns = len(transportationProblem.customers)

    adjMatrix = [[0 for _ in range(nbRows + nbColumns)] for _ in range(nbRows + nbColumns)]
    for i in range(nbRows):
        for j in graph[i]:
            adjMatrix[i][j] = 1
            adjMatrix[j][i] = 1
    
    return adjMatrix