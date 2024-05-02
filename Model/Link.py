from Model.Supplier import Supplier
from Model.Customer import Customer


class Link:
    def __init__(self, supplier: Supplier, customer: Customer, cost: int, units: int = 0):
        self.supplier = supplier
        self.customer = customer
        self.cost = cost
        self.units = units
        self.key = f"{supplier.name}{customer.name}"

    def print(self):
        print("Delivery of "+str(self.units)+" units from "+self.supplier.name+" to customer "+self.customer.name+" with cost per units "+str(self.cost))

    def __eq__(self, other):
        if type(other) == Link:
            return self.key == other.key
        return False
<<<<<<< HEAD
<<<<<<< HEAD
=======
=======
>>>>>>> 546dbeb (fin fonction isConnected, J'attends le verifyCycle)

"""
class Link:
    def __init__(self, supplier, customer, units):
        self.supplier = supplier
        self.customer = customer
        self.units = units  # Ensure this attribute is correctly named and used
"""      

<<<<<<< HEAD
=======
>>>>>>> efdfb5b (ça marche)
=======
>>>>>>> 8554dc0 (fin fonction isConnected, J'attends le verifyCycle)
>>>>>>> 546dbeb (fin fonction isConnected, J'attends le verifyCycle)

    