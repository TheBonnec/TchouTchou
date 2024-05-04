from Model.TransportationProblem import TransportationProblem
from Controller.IsConnected import isConnected
from Controller.verifyCycle import isGraphAcylic
import copy


def toNonDegenerate(TP : TransportationProblem):
    tempTP = copy.deepcopy(TP)
    listLink = TP.links
    listLinkExisting = []
    listLinkat0 = []
    for link in listLink:
        if (link.units != 0):
            listLinkExisting.append(link)
        else:
            listLinkat0.append(link)
    listVertices = TP.customers + TP.suppliers
    while (len(listLinkExisting) != len(listVertices)-1):
        minCost = listLinkat0[0].cost
        for link in listLinkat0:
            minCost = min(minCost, link.cost)
        for i in range(len(listLinkat0)):
            if (listLinkat0[i].cost == minCost):
                for link in tempTP.links:
                    if (link.supplier.name == listLinkat0[i].supplier.name and link.customer.name == listLinkat0[i].customer.name):
                        link.units = 1
                        print("Trying to add edge :",link.supplier.name, "to ",link.customer.name)
                        if (isGraphAcylic(tempTP) == False):
                            print("Creating a cycle so we remove edge :",link.supplier.name, "to ",link.customer.name)
                            link.units = 0
                            listLinkat0[i].remove()
                        else:
                            print("No cycle created")
                            print("Edge",link.supplier.name, "to",link.customer.name, "added")
                            listLinkExisting.append(link)
                            break
                else:
                    continue
                break
    return tempTP
        
