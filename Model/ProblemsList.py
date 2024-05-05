from Model.TransportationProblem import TransportationProblem
from os import listdir


def getAllTransportationProblems():
    files: list[str] = listdir('TextFiles')
    transportationProblems: list[TransportationProblem] = []
    
    # Get all transportation problems
    for index in range(len(files)):
        newTP = TransportationProblem(filename = f"TextFiles/{files[index]}")
        transportationProblems.append(newTP)
    
    sortGraphs(transportationProblems = transportationProblems)
    
    return transportationProblems



def sortGraphs(transportationProblems: list[TransportationProblem]):
    transportationProblems.sort(key = lambda x: x.index, reverse = False)