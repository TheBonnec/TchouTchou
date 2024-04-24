from Supplier import Supplier
from Customer import Customer


class Link:
    def __init__(self, supplier: Supplier, customer: Customer, cost: int, units: int = 0):
        self.supplier = supplier
        self.customer = customer
        self.cost = cost
        self.units = units