import json

from Model.Customer import Customer
from Model.Link import Link
from Model.Supplier import Supplier

class TransportationProblem:
    def __init__(self, filepath):
        with open(filepath, 'r') as file:
            data = json.load(file)
        
        self.name = data["name"]
        self.index = data["index"]
        self.customers = [Customer(c['name'], c['orders']) for c in data['customers']]
        self.suppliers = [Supplier(s['name'], s['provisions']) for s in data['suppliers']]
        self.links = []
        
        for i, row in enumerate(data['links']):
            for j, units in enumerate(row):
                link = Link(self.suppliers[i], self.customers[j], units)
                self.links.append(link)

    def calculateConstraint(self):
        totalProvisions = sum(supplier.provision for supplier in self.suppliers)
        totalOrders = sum(customer.order for customer in self.customers)
        totalShipped = sum(link.units for link in self.links)

        print(f"Total provisions: {totalProvisions}, Total orders: {totalOrders}, Total shipped: {totalShipped}")
        return min(totalProvisions, totalOrders, totalShipped)