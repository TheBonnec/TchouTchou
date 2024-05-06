from Model.TransportationProblem import TransportationProblem
from Model.CostLink import CostLink
from Model.TransportationProblem import Link
from collections import defaultdict, deque
import numpy as np
import copy



class SteppingStoneViewController:
    def __init__(self):
        self.currentTotalCost = None
        self.initTotalCost = None

        
    def calculateConstraint(self, tp: TransportationProblem):
        totalProvisions = sum(supplier.provision for supplier in tp.suppliers)
        totalOrders = sum(customer.order for customer in tp.customers)
        totalShipped = sum(link.units for link in tp.links) 
        
        print(f"Total provisions: {totalProvisions}, Total orders: {totalOrders}, Total shipped: {totalShipped}")
        return min(totalProvisions, totalOrders, totalShipped)
    

        
    def removeCycle(self, tp: TransportationProblem, cycle_nodes):
        # Remove cycles from the transportation problem to optimize costs and ensure acyclicity
        # Set initial cost at the start of cycle removal if not already set
        if self.initTotalCost is None:
            self.initTotalCost = self.calculateTotalCost(tp)

        # Step 1 : Process each cycle only once per method call
        minFlow = float('inf')
        relovedLinks = []
        # Identify the bottleneck in the cycle
        for (supplierName, customerName) in cycle_nodes:
            for link in tp.links:
                if link.supplier.name == supplierName and link.customer.name == customerName and link.units < minFlow:
                    minFlow = link.units

        # Step 2 : Modify edges to break cycles and collect removed links
        for (supplierName, customerName) in cycle_nodes:
            for link in tp.links:
                if link.supplier.name == supplierName and link.customer.name == customerName:
                    link.units -= minFlow
                    if link.units == 0:
                        relovedLinks.append(link)

        # Step 3 : Remove the links with zero flow from the transportation problem
        tp.links = [link for link in tp.links if link.units > 0]

        # Step 4 : Recalculate current total cost after modification
        self.currentTotalCost = self.calculateTotalCost(tp)

        # Step 5 : Check if the new total cost is higher than the initial total cost
        if self.currentTotalCost > self.initTotalCost:
            raise ValueError("New total cost is higher than the initial cost, which is not allowed")

        return tp, relovedLinks
    


    def calculateMarginalCosts(self, costLinks, potentialsLinks): 
        marginalCosts = []
        for costLink in costLinks:
            supplier = costLink.supplier
            customer = costLink.customer
            cost = costLink.cost - next(pot for pot in potentialsLinks if pot.supplier == supplier and pot.customer == customer).cost
            marginalCosts.append(CostLink(supplier, customer, cost))
        return marginalCosts
        
    

    def checkMarginalCosts(self, tp: TransportationProblem, marginalCosts):
        # find the most negative marginal cost
        minCost = min(marginalCosts, key=lambda x: x.cost)
        if minCost.cost >= 0:
            return None
        
        # find the maximum capacity we can assign
        supplier = minCost.supplier
        customer = minCost.customer
        maxUnits = min(supplier.provision, customer.order)
        # find the asssociated link
        for link in tp.links:
            if link.supplier == supplier and link.customer == customer:
                break

        # modify this link
        link.units = maxUnits
        tp.links[tp.links.index(link)] = link

        # find the created cycle
        graph = self.createGraph(tp)
        adjMatrix = self.computeAdjacencyMatrix(transportationProblem = tp, graph = graph)
        cycle = False

        for vertex in graph:
            cycle = self.detectCycle(adjMatrix = adjMatrix, u = vertex)
            if cycle != False:
                break
        
        '''
        deltaCost = []
        for i in range(len(cycle)):
        '''
                
        return tp
    



    def calculatePotentialCosts(self, tp: TransportationProblem):
        # we create a system of equations to solve the potentials
        system = []
        for i in range(len(tp.suppliers)):
            for j in range(len(tp.customers)):
                print(tp.links[i * (len(tp.customers)) + j].units)
                if tp.links[i * (len(tp.customers)) + j].units != 0:
                    # add costs to the system : we put 1 to i and -1 to j if there is a link
                    row = [0] * (len(tp.customers) + len(tp.suppliers))
                    row[i] = 1
                    row[len(tp.suppliers) + j] = -1
                    row.append(tp.links[i * len(tp.customers) + j].cost)
                    system.append(row)

        # we add to the system the first variable
        row = [1] + [0] * (len(tp.customers) + len(tp.suppliers))
        system.append(row)

        print(system)

        # we solve the system with numpy
        A = np.array([row[:-1] for row in system])
        B = np.array([row[-1] for row in system])
        print(A, B)
        variables = np.linalg.solve(A, B)

        # we recreate a potential costs table with values such as E(Si) - E(Cj) = Cij
        costLinks = []
        for supplier in tp.suppliers:
            for customer in tp.customers:
                costLinks.append(CostLink(supplier, customer, variables[tp.suppliers.index(supplier)] - variables[len(tp.suppliers) + tp.customers.index(customer)]))

        return costLinks

    

    def isConnected(self, TP : TransportationProblem):
        listLink = TP.links
        listLinkExisting = []
        for i in listLink:
            if (i.units != 0):
                listLinkExisting.append(i)
        listVertices = TP.customers + TP.suppliers
        if (len(listLinkExisting) >= (len(listVertices) -1)):
            return TP
        
        visitedVertices = []
        listNextVertices =[]
        currentVertex = TP.suppliers[0]
        queue = []
        queue.append(currentVertex)
        for i in listLinkExisting:
            if (i.supplier == currentVertex):
                listNextVertices.append(i.customer)
            elif(i.customer == currentVertex):
                listNextVertices.append(i.supplier)

        while listNextVertices != []:
            listNextVertices = []
            for i in listLinkExisting:
                if (i.supplier == currentVertex and i.customer not in visitedVertices):
                    listNextVertices.append(i.customer)
                elif(i.customer == currentVertex and i.supplier not in visitedVertices):
                    listNextVertices.append(i.supplier)
            visitedVertices.append(queue[-1])
            queue.pop()
            for i in listNextVertices:
                if i not in visitedVertices:
                    queue.append(i)
            if queue != []:
                currentVertex = queue[-1]
        if (len(visitedVertices) == (len(listVertices))):
            return True
        else:
            return False
        

    
    def toNonDegenerate(self, TP : TransportationProblem):
        tempTP = copy.deepcopy(TP)
        listLink = TP.links
        listLinkExisting = []
        listLinkat0 = []
        for link in listLink:
            if (link.units != 0):
                listLinkExisting.append(link)
            else:
                listLinkat0.append(link)
        listVertices = TP.customers + TP.suppliers
        while (len(listLinkExisting) != len(listVertices)-1):
            minCost = listLinkat0[0].cost
            for link in listLinkat0:
                minCost = min(minCost, link.cost)
            for i in range(len(listLinkat0)):
                if (listLinkat0[i].cost == minCost):
                    for link in tempTP.links:
                        if (link.supplier.name == listLinkat0[i].supplier.name and link.customer.name == listLinkat0[i].customer.name):
                            link.units = 1
                            print("Trying to add edge :",link.supplier.name, "to ",link.customer.name)
                            if (self.isGraphAcylic(tempTP) == False):
                                print("Creating a cycle so we remove edge :",link.supplier.name, "to ",link.customer.name)
                                link.units = 0
                                listLinkat0[i].remove()
                            else:
                                print("No cycle created")
                                print("Edge",link.supplier.name, "to",link.customer.name, "added")
                                listLinkExisting.append(link)
                                break
                    else:
                        continue
                    break
        return tempTP
    


    def createGraph(self, transportationProblem: TransportationProblem):
        nbRows = len(transportationProblem.suppliers)
        nbColumns = len(transportationProblem.customers)

        transportProposition = [[0 for _ in range(nbColumns)] for _ in range(nbRows)]
        for i in range(nbRows):
            for j in range(nbColumns):
                transportProposition[i][j] = transportationProblem.links[i * nbColumns + j].units

        graph = {}
        # we create an oriented graph
        for i in range(nbRows):
            graph[i] = []
            for j in range(nbColumns):
                if transportProposition[i][j] > 0: 
                    graph[i].append(j + nbRows)
        for j in range(nbColumns):
            graph[j + nbRows] = []
            for i in range(nbRows):
                if transportProposition[i][j] > 0:
                    graph[j + nbRows].append(i)
        return graph
    


    def computeAdjacencyMatrix(self, transportationProblem: TransportationProblem, graph) -> list[list[int]]:
        nbRows = len(transportationProblem.suppliers)
        nbColumns = len(transportationProblem.customers)

        adjMatrix = [[0 for _ in range(nbRows + nbColumns)] for _ in range(nbRows + nbColumns)]
        for i in range(nbRows):
            for j in graph[i]:
                adjMatrix[i][j] = 1
                adjMatrix[j][i] = 1
        
        return adjMatrix



    def isGraphAcylic(self, transportationProblem: TransportationProblem):
        nbRows = len(transportationProblem.suppliers)

        # we create the oriented graph from the transport proposition
        graph = self.createGraph(transportationProblem = transportationProblem)
        
        # we build an adjency matrix, which is symmetrical
        adjMatrix = self.computeAdjacencyMatrix(transportationProblem = transportationProblem, graph = graph)
        
        # we iterate with each vertex to check if there is a cycle
        for s in graph:
            result = self.detectCycle(adjMatrix, s)
            if result:
                print("Cycle detected :", end=" ")
                for i in range(len(result)):
                    if result[i] < nbRows:
                        print(f"P{result[i] + 1} -> ", end="")
                    else:
                        print(f"C{result[i] - nbRows + 1} -> ", end="")
                print("etc...")
                return False
        return True
        


    def detectCycle(self, adjMatrix, u):
        n = len(adjMatrix)
        file = []
        visitedVertices = [False] * n
        visitedVertices[u] = True
    
        parent = [-1] * n
        parent[u] = u
    
        file.append(u)
        while file:
            current = file.pop(0)
            visitedVertices[current] = True
            for i in range(n):
                if adjMatrix[current][i] > 0 and visitedVertices[i] == False:
                    file.append(i)
                    visitedVertices[i] = True
                    parent[i] = current
    
                elif adjMatrix[current][i] > 0 and visitedVertices[i] == True and parent[current] != i:
                    cycle = []
                    cycle.append(current)
                    cycle.append(i)
                    while parent[i] != i:
                        i = parent[i]
                        cycle.append(i)
                    return cycle
        return False

