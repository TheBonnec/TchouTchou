from Model.TransportationProblem import TransportationProblem
from Model.Supplier import Supplier
from Model.Customer import Customer
from Controller.verifyCycle import detectCycle

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
