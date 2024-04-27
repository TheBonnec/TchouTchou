from Model.Supplier import Supplier
from Model.Customer import Customer


class Link:
    def __init__(self, supplier: Supplier, customer: Customer, cost: int, units: int = 0):
        self.supplier = supplier
        self.customer = customer
        self.cost = cost
        self.units = units

    def print(self):
        print("Delivery of "+str(self.units)+" units from "+self.supplier.name+" to customer "+self.customer.name+" with cost per units "+str(self.cost))