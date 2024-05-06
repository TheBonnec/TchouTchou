import json
from Model.Customer import Customer
from Model.Link import Link
from Model.Supplier import Supplier
from Model.ReadFile import readFile
from Model.CostLink import CostLink
import copy



class TransportationProblem:
    def __init__(self, filename:str):
        dict_of_values = readFile(filename)

        self.name: str = dict_of_values["name"]
        self.index: int = dict_of_values["index"]
        self.customers: list[Customer] = []
        self.suppliers: list[Supplier] = []
        self.links: list[Link] = []
        

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
        




    def calculateConstraint(self):
        totalProvisions = sum(supplier.provision for supplier in self.suppliers)
        totalOrders = sum(customer.order for customer in self.customers)
        totalShipped = sum(link.units for link in self.links)

        print(f"Total provisions: {totalProvisions}, Total orders: {totalOrders}, Total shipped: {totalShipped}")
        return min(totalProvisions, totalOrders, totalShipped)
    


    def getSupplierLinks(self, supplier: Supplier) -> list[Link]:
        linksList: list[Link] = []
        for link in self.links:
            if link.supplier.name == supplier.name:
                linksList.append(link)
        return linksList
    

    def getCustomerLinks(self, customer: Customer) -> list[Link]:
        linksList: list[Link] = []
        for link in self.links:
            if link.customer.name == customer.name:
                linksList.append(link)
        return linksList


    def getCostsLinks(self) -> list[CostLink]:
        costsLink: list[CostLink] = []
        for link in self.links:
            newCostLink = CostLink(link.supplier, link.customer, link.cost)
            costsLink.append(newCostLink)
        return costsLink