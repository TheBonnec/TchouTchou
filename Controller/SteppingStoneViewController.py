class SteppingStoneViewController:
    def __init__(self, transportationProblem):
        self.tp = transportationProblem

    def calculateConstraint(self):
        totalProvisions = sum(supplier.provision for supplier in self.tp.suppliers)
        totalOrders = sum(customer.order for customer in self.tp.customers)
        totalShipped = sum(link.units for link in self.tp.links)  # Make sure 'units' is the name of the attribute in Link class

        print(f"Total provisions: {totalProvisions}, Total orders: {totalOrders}, Total shipped: {totalShipped}")
        return min(totalProvisions, totalOrders, totalShipped)
