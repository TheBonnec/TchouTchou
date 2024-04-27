from View.View import View
from Model.TransportationProblem import TransportationProblem

class MyView():
    TP = TransportationProblem("TextFiles/TransportationProblem3.json")
    TP.suppliers[1].print()

    #def __init__(self):
     #super().__init__()


MyView()