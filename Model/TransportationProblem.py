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
    


    def getSupplierLinks(self, supplier: Supplier) -> list[Link]:
        linksList: list[Link] = []
        for link in self.links:
            if link.supplier == supplier:
                linksList.append(link)
        return linksList
    

    def getCustomerLinks(self, customer: Customer) -> list[Link]:
        linksList: list[Link] = []
        for link in self.links:
            if link.customer == customer:
                linksList.append(link)
        return linksList
                
   
