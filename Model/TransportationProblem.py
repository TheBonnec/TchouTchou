from Model.Customer import Customer
from Model.Link import Link
from Model.Supplier import Supplier
from Model.ReadFile import readFile
import copy

class TransportationProblem:
    def __init__(self, filename:str):
        dict_of_values = readFile(filename)
        
        self.name = dict_of_values["name"]
        self.index = dict_of_values["index"]
        self.customers = []
        self.suppliers = []
        self.links = []

        for i in dict_of_values["customers"]:
            customer = Customer(i["name"],i["orders"])
            self.customers.append(customer)
        for i in dict_of_values["suppliers"]:
            supplier = Supplier(i["name"], i["provisions"])
            self.suppliers.append(supplier)
        for i in range(len(dict_of_values["links"])):
            for k in range(len(dict_of_values["links"][i])):
                link = Link(self.suppliers[i], self.customers[k], dict_of_values["links"][i][k])
                self.links.append(link)
                
                
    def NordWestAlgorithm(self):
        tp_copy = copy.deepcopy(self)
        i, j = 0, 0

        while i < len(tp_copy.suppliers) and j < len(tp_copy.customers):
            # Calculate the minimum amount to allocate
            amount = min(tp_copy.suppliers[i].provision, tp_copy.customers[j].order)
            
            # Find the corresponding Link object and update its quantity
            link = next((l for l in tp_copy.links if l.supplier == tp_copy.suppliers[i] and l.customer == tp_copy.customers[j]), None)
            if link:
                link.units += amount  # Increment the quantity

            # Update the remaining supply and demand
            tp_copy.suppliers[i].provision -= amount
            tp_copy.customers[j].order -= amount

            # Move to the next supplier or customer
            if tp_copy.suppliers[i].provision == 0 and i < len(tp_copy.suppliers) - 1:
                i += 1
            elif tp_copy.customers[j].order == 0 and j < len(tp_copy.customers) - 1:
                j += 1
            elif tp_copy.suppliers[i].provision == 0:
                break
            elif tp_copy.customers[j].order == 0:
                break

        return tp_copy
