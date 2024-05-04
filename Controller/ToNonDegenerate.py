from Model.TransportationProblem import TransportationProblem
from Controller.IsConnected import isConnected
from Model.VerifyCycle import VerifyCycle
from copy import *

def toNonDegenerate(TP : TransportationProblem):
    tempTP = copy.deepcopy(TP)
    listLink = TP.links
    listLinkExisting = []
    listLinkat0 = []
    for i in listLink:
        if (i.units != 0):
            listLinkExisting.append(i)
        else:
            listLinkat0.append(i)
    #or VerifyCycle == []
    listVertices = TP.customers + TP.suppliers
    if ((isConnected(TP)==TP) and len(listLinkExisting) == len(listVertices)-1):
        return TP
    else:
        minCost = listLinkat0[0].cost
        for link in listLinkat0:
            minCost = min(minCost, link.cost)
        
