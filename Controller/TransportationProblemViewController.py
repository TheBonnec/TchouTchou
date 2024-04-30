from Model.TransportationProblem import TransportationProblem
from Model.Supplier import Supplier
from Model.Customer import Customer
from Model.Link import Link
import copy


class TransportationProblemViewController:
    def __init__(self):
        pass




    def NordWestAlgorithm(transportationProblem: TransportationProblem):
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

        return tpCopy
            



    def calculatePenalties(self, transportationProblem: TransportationProblem):
        nonAvailableLinks: list[Link] = self.getNonAvailableLinks(transportationProblem = transportationProblem)

        # Compute the penalties for each supplier
        for supplier in transportationProblem.suppliers:
            # Check if the supplier still has provisions
            if supplier.provision > 0:
                supplierLinks: list[Link] = transportationProblem.getSupplierLinks(supplier = supplier)
                filteredSupplierLinks: list[Link] = self.mutuallyExcludeLinksSets(linkSet1 = supplierLinks, linkSet2 = nonAvailableLinks)
                sortedCosts = sorted(link.cost for link in filteredSupplierLinks)
                supplier.penalty = sortedCosts[1] - sortedCosts[0] if len(sortedCosts) > 1 else 0

            else:
                supplier.penalty = -1
        

        # Compute the penalties for each customer
        for customer in transportationProblem.customers:
            # Check if the supplier still has provisions
            if customer.order > 0:
                customerLinks: list[Link] = transportationProblem.getCustomerLinks(customer = customer)
                filteredCustomerLinks: list[Link] = self.mutuallyExcludeLinksSets(linkSet1 = customerLinks, linkSet2 = nonAvailableLinks)
                sortedCosts = sorted(link.cost for link in filteredCustomerLinks)
                customer.penalty = sortedCosts[1] - sortedCosts[0] if len(sortedCosts) > 1 else 0

            else:
                customer.penalty = -1


    

    def balasHammerAlgo(self, transportationProblem: TransportationProblem):
        tpCopy: TransportationProblem = copy.deepcopy(transportationProblem)
        count = 0

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
                self.printAvailableLinks(availableLinks)
            else:
                customerLinks: list[Link] = tpCopy.getCustomerLinks(customer = customerWithMaxPenalty)
                availableLinks: list[Link] = self.checkLinksAreAvailable(transportationProblem = tpCopy, links = customerLinks)
                self.printAvailableLinks(availableLinks)
            
            linkWithMinimumCost: Link = min(availableLinks, key = lambda link: link.cost, default = None)

            if linkWithMinimumCost == None:
                print("None")
                break


            print(f"\nLien choisit : {linkWithMinimumCost.supplier.name} : {linkWithMinimumCost.supplier.provision} - {linkWithMinimumCost.customer.name} {linkWithMinimumCost.customer.order}")
            valueToAllocate = min(linkWithMinimumCost.supplier.provision, linkWithMinimumCost.customer.order)
            if valueToAllocate:
                linkWithMinimumCost.units += valueToAllocate
                linkWithMinimumCost.supplier.provision -= valueToAllocate
                linkWithMinimumCost.customer.order -= valueToAllocate
            else:
                print("Pas de valeur à alouer")
                break

            count += 1
            if count > 10:
                print("> 10")
                break

            print("\n\n")
        
        return tpCopy
    


    def checkLinksAreAvailable(self, transportationProblem: TransportationProblem, links: list[Link]) -> list[Link]:
        allLinks: list[Link] = transportationProblem.links
        availableLinks: list[Link] = []
        
        for allLink in allLinks:
            if allLink.customer.order > 0 and allLink.supplier.provision > 0:
                for link in links:
                    if link.key == allLink.key:
                        availableLinks.append(link)
        
        return availableLinks
    

    def getNonAvailableLinks(self, transportationProblem: TransportationProblem) -> list[Link]:
        allLinks: list[Link] = transportationProblem.links
        nonAvailableLinks: list[Link] = []
        print("\nNon Available Links")
        
        for link in allLinks:
            if link.customer.order <= 0 or link.supplier.provision <= 0:
                print(f"{link.customer.name} : {link.customer.order}     {link.supplier.name} : {link.supplier.provision}")
                nonAvailableLinks.append(link)
        
        print("FIn")
        return nonAvailableLinks

    



    def printPenalties(self, tp: TransportationProblem):
        for supplier in tp.suppliers:
            print(f"{supplier.name} : {supplier.penalty}")
        for customer in tp.customers:
            print(f"{customer.name} : {customer.penalty}")

    def printAvailableLinks(self, links: list[Link]):
        print("\nAvailable Links (for a given supplier or customer)")
        for link in links:
            print(f"{link.supplier.name} : {link.supplier.provision}     {link.customer.name} : {link.customer.order}")

    def printUsedLinks(self, links: list[Link]):
        print("Used Links")
        for link in links:
            print(f"{link.supplier.name} : {link.supplier.provision}     {link.customer.name} : {link.customer.order}")


























    '''
    def calculatePenalties(self, transportationProblem: TransportationProblem, usedLinks: list[Link]):
        # Calculate row penalties
        for supplier in transportationProblem.suppliers:
            suppliersLinks: list[Link] = transportationProblem.getSupplierLinks(supplier = supplier)

            if suppliersLinks:
                filteredSuppliersLinks: list[Link] = self.mutuallyExcludeLinksSets(linkSet1 = suppliersLinks, linkSet2 = usedLinks)
                sortedCosts = sorted(link.cost for link in filteredSuppliersLinks)
                supplier.penalty = sortedCosts[1] - sortedCosts[0] if len(sortedCosts) > 1 else 0


        # Calculate column penalties
        for customer in transportationProblem.customers:
            customersLink = transportationProblem.getCustomerLinks(customer = customer)
            
            if customersLink:
                filteredCustomersLinks: list[Link] = self.mutuallyExcludeLinksSets(linkSet1 = customersLink, linkSet2 = usedLinks)
                sortedCosts = sorted(link.cost for link in filteredCustomersLinks)
                customer.penalty = sortedCosts[1] - sortedCosts[0] if len(sortedCosts) > 1 else 0
    '''



        
    def BalasHammerAlgo(self, transportationProblem: TransportationProblem):
        tpCopy: TransportationProblem = copy.deepcopy(transportationProblem)
        usedLinks: list[Link] = []      # Keeps track of links that we already used


        while any(supplier.provision > 0 for supplier in tpCopy.suppliers) and any(customer.order > 0 for customer in tpCopy.customers):
            # Calculate the penalties
            self.calculatePenalties(transportationProblem = tpCopy, usedLinks = usedLinks)

            for supplier in tpCopy.suppliers:
                print(supplier.penalty) 
            for supplier in tpCopy.customers:
                print(supplier.penalty)
            
            # Get the maximum penalty for each supplier and each customer
            supplierWithMaxPenalty: Supplier = max(tpCopy.suppliers, key = lambda supplier: supplier.penalty, default = None)
            customerWithMaxPenalty: Customer = max(tpCopy.customers, key = lambda customer: customer.penalty, default = None)

            # Determine whether to allocate based on supplier or customer by comparing penalties
            doWeAllocateToSupplier: bool = supplierWithMaxPenalty.penalty >= customerWithMaxPenalty.penalty



            # Get the cell with minimum transportation cost
            if doWeAllocateToSupplier:
                supplierLinks: list[Link] = tpCopy.getSupplierLinks(supplier = supplierWithMaxPenalty)
                filteredSupplierLinks: list[Link] = self.mutuallyExcludeLinksSets(linkSet1 = supplierLinks, linkSet2 = usedLinks)
                linksWithPositiveOrdersAndProvisions: list[Link] = (link for link in filteredSupplierLinks if link.supplier.provision > 0 and link.customer.order > 0)
            else:
                customerLinks = tpCopy.getCustomerLinks(customer = customerWithMaxPenalty)
                filteredCustomerLinks: list[Link] = self.mutuallyExcludeLinksSets(linkSet1 = customerLinks, linkSet2 = usedLinks)
                linksWithPositiveOrdersAndProvisions: list[Link] = (link for link in filteredCustomerLinks if link.supplier.provision > 0 and link.customer.order > 0)

            linkWithMinimumCost: Link = min(linksWithPositiveOrdersAndProvisions, key = lambda link: link.cost, default = None)
            


            # Check if minimumCostLink is not None
            if linkWithMinimumCost == None:
                break

            # Perform the allocation
            valueToAllocate = min(linkWithMinimumCost.supplier.provision, linkWithMinimumCost.customer.order)
            if valueToAllocate > 0:
                #usedLinks.append(linkWithMinimumCost)
                if valueToAllocate == linkWithMinimumCost.supplier.provision:
                    print(tpCopy.suppliers)
                    for link in tpCopy.getSupplierLinks(supplier = linkWithMinimumCost.supplier):
                        if link not in usedLinks:
                            usedLinks.append(link)
                elif valueToAllocate == linkWithMinimumCost.customer.order:
                    for link in tpCopy.getCustomerLinks(customer = linkWithMinimumCost.customer):
                        if link not in usedLinks:
                            usedLinks.append(link)
                print(usedLinks)


                linkWithMinimumCost.units += valueToAllocate
                linkWithMinimumCost.supplier.provision -= valueToAllocate
                linkWithMinimumCost.customer.order -= valueToAllocate
            else:
                # If no allocation can be made, break the loop to prevent infinite loop
                break
            print("")

        return tpCopy
    



    def mutuallyExcludeLinksSets(self, linkSet1: list[Link], linkSet2: list[Link]) -> list[Link]:
        finalList: list[Link] = []

        print("\nMutally Exclude sets")

        for link in linkSet1:
            finalList.append(link)

        for link1 in linkSet1:
            for link2 in linkSet2:
                if link1.key == link2.key:
                    for j in range(len(finalList) - 1):
                        if finalList[j].key == link1.key:
                            print(f"{link1.supplier.name} : {link1.supplier.provision}     {link1.customer.name} : {link1.customer.order}")
                            finalList.pop(j)
        return finalList
