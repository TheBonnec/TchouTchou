import json

def readFile(filename : str):
    file = open(filename)
    dictOfValues = json.load(file)
    file.close()
    return dictOfValues