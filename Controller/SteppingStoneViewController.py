from Model.TransportationProblem import TransportationProblem
from Model.Supplier import Supplier
from Model.Customer import Customer
from Controller.verifyCycle import detectCycle
from Model.TransportationProblem import Link

import numpy as np

class CostLink:
    def __init__(self, supplier: Supplier, customer: Customer, cost: int):
        self.supplier = supplier
        self.customer = customer
        self.cost = cost

class SteppingStoneViewController:
    def __init__(self):
        self.currentTotalCost = None
        self.initTotalCost = None

    def calculatePotentials(self, tp: TransportationProblem):
        costLinks = []
        for supplier in tp.suppliers:
            for customer in tp.customers:
                cost = supplier.provision - customer.order
                costLinks.append(CostLink(supplier, customer, cost))
        return costLinks

        
    def calculateConstraint(self, tp: TransportationProblem):
        totalProvisions = sum(supplier.provision for supplier in self.tp.suppliers)
        totalOrders = sum(customer.order for customer in self.tp.customers)
        totalShipped = sum(link.units for link in self.tp.links) 
        
        print(f"Total provisions: {totalProvisions}, Total orders: {totalOrders}, Total shipped: {totalShipped}")
        return min(totalProvisions, totalOrders, totalShipped)
    
    

    
    def calculateTotalCost(self, tp):
        return sum(link.cost * link.units for link in tp.links)
        
    def removeCycle(self, tp: TransportationProblem, cycle_nodes):
        """Remove cycles from the transportation problem to optimize costs and ensure acyclicity."""
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
    

    def calculateMarginalCosts(self, costLinks, potentialsLinks): # costLinks liste de CostLink,potentials: liste de CostLink
        marginalCosts = []
        for costLink in costLinks:
            supplier = costLink.supplier
            customer = costLink.customer
            cost = costLink.cost - next(pot for pot in potentialsLinks if pot.supplier == supplier and pot.customer == customer).cost
            marginalCosts.append(CostLink(supplier, customer, cost))
        return marginalCosts
        
    
    # Dans le dossier Controller, dans le ficher SteppingStoneViewController, écrire une fonction qui prend en entrée un objet TransportationProblem et une matrice de coûts marginaux, et vérifie qu'aucun des coûts marginaux n'est négatif. Si tel est le cas, la fonction doit ajouter un lien entre le supplier et le customer pour lesquels le coût marginal est négatif, et lui donner le maximum de nombre de trucs à transporter, en modifiant les autres liens si besoin.
    # La fonction ne s'intéresse pas au fait que cette modification entraine un cycle. On vérifiera ça plus tard dans le programme.
    # La fonction doit retourner un TransportationProblem modifié si l'un des coûts est négatifs, sinon None
    def checkMarginalCosts(self, tp: TransportationProblem, marginalCosts):
        # trouver le cout le plus négatif
        minCost = min(marginalCosts, key=lambda x: x.cost)
        if minCost.cost >= 0:
            return None
        
        # trouver le maximum que l'on peut lui assigner
        supplier = minCost.supplier
        customer = minCost.customer
        maxUnits = min(supplier.provision, customer.order)
        # trouver le lien correspondant
        for link in tp.links:
            if link.supplier == supplier and link.customer == customer:
                break
            else:
                link = Link(supplier, customer, 0)
                tp.links.append(link)

        # modifier le lien
        link.units = maxUnits
        tp.links[tp.links.index(link)] = link

        # modifier les autres liens si besoin pour respecter les contraintes
        # TODO : modifier les autres liens si besoin

                
        return tp


    def calculatePotentialCosts(self, tp: TransportationProblem, ts: TransportationProblem):
        # parcourir les units de ts et si elle est différente de 0, on ajoute le coût de la liaison dans un systeme comme ceci : E(Si) - E(Cj) = Cij. Cela donne dans un systeme une ligne [1, -1, 0, 2] ([i, j, k, Cij])
        
        system = []
        for i in range(len(tp.suppliers)):
            for j in range(len(tp.customers)):
                if ts.links[i * (len(tp.customers)) + j].units != 0:
                    # ajouter le coût de la liaison dans un systeme (si on est à un lien entre i et j, alors on met 1 à la position i et -1 à la position j)
                    row = [0] * (len(tp.customers) + len(tp.suppliers))
                    row[i] = 1
                    row[len(tp.suppliers) + j] = -1
                    row.append(ts.links[i * len(tp.customers) + j].cost)
                    system.append(row)

        # ajouter au systeme la premiere variable qui est égale à 0
        row = [1] + [0] * (len(tp.customers) + len(tp.suppliers))
        system.append(row)

        for line in system:
            print(line)

        # on solve le systeme
        A = np.array([row[:-1] for row in system])
        B = np.array([row[-1] for row in system])
        variables =  np.linalg.solve(A, B)

        # on doit recréer un tableau de coûts potentiels avec comme valeurs E(Si) - E(Cj) = Cij
        costLinks = []
        for supplier in tp.suppliers:
            for customer in tp.customers:
                costLinks.append(CostLink(supplier, customer, variables[tp.suppliers.index(supplier)] - variables[len(tp.suppliers) + tp.customers.index(customer)]))

        return costLinks
    