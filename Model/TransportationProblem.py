from Model.Customer import Customer
from Model.Link import Link
from Model.Supplier import Supplier
from Model.ReadFile import readFile


class TransportationProblem:
    def __init__(self, filename:str):
        dictOfValues = readFile(filename)
        
        self.name = dictOfValues["name"]
        self.index = dictOfValues["index"]
        self.customers = []
        self.suppliers = []
        self.links = []

        for i in dictOfValues["customers"]:
            customer = Customer(i["name"],i["orders"])
            self.customers.append(customer)
        for i in dictOfValues["suppliers"]:
            supplier = Supplier(i["name"], i["provisions"])
            self.suppliers.append(supplier)
        for i in range(len(dictOfValues["links"])):
            for k in range(len(dictOfValues["links"][i])):
                link = Link(self.suppliers[i], self.customers[k], dictOfValues["links"][i][k])
                self.links.append(link)