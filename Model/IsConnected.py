from Model.TransportationProblem import TransportationProblem

def isConnected(TP : TransportationProblem):
    listLink = TP.links
    listLinkExisting = []
    for i in listLink:
        if (i.units != 0):
            listLinkExisting.append(i)
    listVertices = TP.customers + TP.suppliers
    if (len(listLinkExisting) >= (len(listVertices) -1)):
        return TP
    
    visitedVertices = []
    listNextVertices =[]
    currentVertex = TP.suppliers[0]
    queue = []
    queue.append(currentVertex)
    while listNextVertices != []:
        visitedVertices.append(queue[-1])
        queue.pop()
        for i in listLinkExisting:
            if (i.supplier == currentVertex):
                listNextVertices.append(i.customer)
            elif(i.customer == currentVertex):
                listNextVertices.append(i.supplier)
        queue.append(p for p in listNextVertices if p not in visitedVertices)
        currentVertex = queue[-1]
    if (len(visitedVertices) == (len(listVertices))):
        return TP
    else:
        return (visitedVertices, [p for p in listVertices if p not in visitedVertices])


