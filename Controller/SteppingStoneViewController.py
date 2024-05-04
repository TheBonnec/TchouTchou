from Model.TransportationProblem import TransportationProblem
from Model.Supplier import Supplier
from Model.Customer import Customer

class CostLink:
    def __init__(self, supplier: Supplier, customer: Customer, cost: int):
        self.supplier = supplier
        self.customer = customer
        self.cost = cost

class SteppingStoneViewController:
    def __init__(self):
        pass  
    
    def calculatePotentials(self, tp: TransportationProblem):
        costLinks = []
        for supplier in tp.suppliers:
            for customer in tp.customers:
                cost = supplier.provision - customer.order
                costLinks.append(CostLink(supplier, customer, cost))
        return costLinks

        
    def calculateConstraint(self):
        totalProvisions = sum(supplier.provision for supplier in self.tp.suppliers)
        totalOrders = sum(customer.order for customer in self.tp.customers)
        totalShipped = sum(link.units for link in self.tp.links) 
        
        print(f"Total provisions: {totalProvisions}, Total orders: {totalOrders}, Total shipped: {totalShipped}")
        return min(totalProvisions, totalOrders, totalShipped)
    
        
    def removeCycle(self, tp, cycleNodes):
        removedLinks = []
        # Collect all links that match the cycle nodes for removal
        for link in tp.links[:]:  # creates a shallow copy of the list
            if (link.supplier.name, link.customer.name) in cycleNodes:
                removedLinks.append(link)
                tp.links.remove(link)
        return tp, removedLinks