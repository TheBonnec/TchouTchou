from Controller.SteppingStoneViewController import SteppingStoneViewController
from Model.TransportationProblem import TransportationProblem
from Controller.TransportationProblemViewController import TransportationProblemViewController
from View.View import View

View().afficher_proposition_transport(tp, solution)

from Controller.verifyCycle import isAcylique
print(isAcylique(solution))

from Model.IsConnected import isConnected
from Controller.TransportationProblemViewController import TransportationProblemViewController


class MyView():
    TP = TransportationProblem("TextFiles/TransportationProblem3.json")

    #def __init__(self):
     #super().__init__()


MyView()
