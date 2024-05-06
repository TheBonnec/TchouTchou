from Model.TransportationProblem import TransportationProblem
from Model.Supplier import Supplier
from Model.Customer import Customer
from Model.Link import Link
import copy


class TransportationProblemViewController:
    def __init__(self):
        pass


    
    def calculateTotalCost(self, tp: TransportationProblem):
        return sum(link.cost * link.units for link in tp.links)

    
    ''' ----- North West ----- '''

    def northWestAlgorithm(self, transportationProblem: TransportationProblem):
        tpCopy = copy.deepcopy(transportationProblem)
        i, j = 0, 0

        while i < len(tpCopy.suppliers) and j < len(tpCopy.customers):
            # Calculate the minimum amount to allocate
            amount = min(tpCopy.suppliers[i].provision, tpCopy.customers[j].order)
            
            # Find the corresponding Link object and update its quantity
            link = next((l for l in tpCopy.links if l.supplier == tpCopy.suppliers[i] and l.customer == tpCopy.customers[j]), None)
            if link:
                link.units += amount  # Increment the quantity

            # Update the remaining supply and demand
            tpCopy.suppliers[i].provision -= amount
            tpCopy.customers[j].order -= amount

            # Move to the next supplier or customer
            if tpCopy.suppliers[i].provision == 0 and i < len(tpCopy.suppliers) - 1:
                i += 1
            elif tpCopy.customers[j].order == 0 and j < len(tpCopy.customers) - 1:
                j += 1
            elif tpCopy.suppliers[i].provision == 0:
                break
            elif tpCopy.customers[j].order == 0:
                break
        
        self.getOrdersBack(originalTP = transportationProblem, transformedTP = tpCopy)

        return tpCopy
            




    ''' ----- Balas Hammer ----- '''

    def balasHammerAlgo(self, transportationProblem: TransportationProblem):
        tpCopy: TransportationProblem = copy.deepcopy(transportationProblem)

        while any(supplier.provision > 0 for supplier in tpCopy.suppliers) and any(customer.order > 0 for customer in tpCopy.customers):
            self.calculatePenalties(transportationProblem = tpCopy)

            # Get the maximum penalty for each supplier and each customer
            supplierWithMaxPenalty: Supplier = max(tpCopy.suppliers, key = lambda supplier: supplier.penalty, default = None)
            customerWithMaxPenalty: Customer = max(tpCopy.customers, key = lambda customer: customer.penalty , default = None)

            # Determine whether to allocate based on supplier or customer by comparing penalties
            doWeAllocateToSupplier: bool = supplierWithMaxPenalty.penalty >= customerWithMaxPenalty.penalty


            if doWeAllocateToSupplier:
                suppliersLinks: list[Link] = tpCopy.getSupplierLinks(supplier = supplierWithMaxPenalty)
                availableLinks: list[Link] = self.checkLinksAreAvailable(transportationProblem = tpCopy, links = suppliersLinks)
            else:
                customerLinks: list[Link] = tpCopy.getCustomerLinks(customer = customerWithMaxPenalty)
                availableLinks: list[Link] = self.checkLinksAreAvailable(transportationProblem = tpCopy, links = customerLinks)
            
            linkWithMinimumCost: Link = min(availableLinks, key = lambda link: link.cost, default = None)

            if linkWithMinimumCost == None:
                break


            valueToAllocate = min(linkWithMinimumCost.supplier.provision, linkWithMinimumCost.customer.order)
            print(valueToAllocate)
            if valueToAllocate:
                linkWithMinimumCost.units += valueToAllocate
                linkWithMinimumCost.supplier.provision -= valueToAllocate
                linkWithMinimumCost.customer.order -= valueToAllocate
            else:
                break
        
        self.getOrdersBack(originalTP = transportationProblem, transformedTP = tpCopy)
        
        return tpCopy
    




    def calculatePenalties(self, transportationProblem: TransportationProblem):
        # Compute the penalties for each supplier
        for supplier in transportationProblem.suppliers:
            # Check if the supplier still has provisions
            if supplier.provision > 0:
                supplierLinks: list[Link] = transportationProblem.getSupplierLinks(supplier = supplier)
                filteredSupplierLinks: list[Link] = self.checkLinksAreAvailable(transportationProblem = transportationProblem, links = supplierLinks)
                sortedCosts = sorted(link.cost for link in filteredSupplierLinks)
                supplier.penalty = sortedCosts[1] - sortedCosts[0] if len(sortedCosts) > 1 else 0

            else:
                supplier.penalty = -1
        

        # Compute the penalties for each customer
        for customer in transportationProblem.customers:
            # Check if the supplier still has provisions
            if customer.order > 0:
                customerLinks: list[Link] = transportationProblem.getCustomerLinks(customer = customer)
                filteredCustomerLinks: list[Link] = self.checkLinksAreAvailable(transportationProblem = transportationProblem, links = customerLinks)
                sortedCosts = sorted(link.cost for link in filteredCustomerLinks)
                customer.penalty = sortedCosts[1] - sortedCosts[0] if len(sortedCosts) > 1 else 0

            else:
                customer.penalty = -1
        
        # Display Penalties
        print("\nCustomer penalties")
        for customer in transportationProblem.customers:
            print(f"{customer.name} : {customer.penalty}")
        
        print("\nSupplier penalties")
        for supplier in transportationProblem.suppliers:
            print(f"{supplier.name} : {supplier.penalty}")



    # Returns the list of all available links in the input list
    def checkLinksAreAvailable(self, transportationProblem: TransportationProblem, links: list[Link]) -> list[Link]:
        allLinks: list[Link] = transportationProblem.links
        availableLinks: list[Link] = []
        
        for allLink in allLinks:
            if allLink.customer.order > 0 and allLink.supplier.provision > 0:
                for link in links:
                    if link.key == allLink.key:
                        availableLinks.append(link)
        
        return availableLinks
    

    # Returns the list of all non avalaible links in a problem
    def getNonAvailableLinks(self, transportationProblem: TransportationProblem) -> list[Link]:
        allLinks: list[Link] = transportationProblem.links
        nonAvailableLinks: list[Link] = []
        
        for link in allLinks:
            if link.customer.order <= 0 or link.supplier.provision <= 0:
                nonAvailableLinks.append(link)
        
        return nonAvailableLinks
    

    # Puts the orders and provisions back in the transformed TP after execution
    def getOrdersBack(self, originalTP: TransportationProblem, transformedTP: TransportationProblem):
        for originalCustomer in originalTP.customers:
            for transformedCustomer in transformedTP.customers:
                if originalCustomer.name == transformedCustomer.name:
                    transformedCustomer.order = originalCustomer.order
        for originalSupplier in originalTP.suppliers:
            for transformedSupplier in transformedTP.suppliers:
                if originalSupplier.name == transformedSupplier.name:
                    transformedSupplier.provision = originalSupplier.provision

