from Model.Supplier import Supplier
from Model.Customer import Customer


class CostLink:
    def __init__(self, supplier: Supplier, customer: Customer, cost: int):
        self.supplier = supplier
        self.customer = customer
        self.cost = cost