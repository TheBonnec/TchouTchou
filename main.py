from Controller.SteppingStoneViewController import SteppingStoneViewController
from Model.TransportationProblem import TransportationProblem
from Model.IsConnected import isConnected
from Controller.TransportationProblemViewController import TransportationProblemViewController

# Create the problem instance from a JSON file
tp = TransportationProblem("TextFiles/TransportationProblem8.json")
tp = TransportationProblemViewController.NordWestAlgorithm(tp)
for i in tp.links:
    i.print()
print(isConnected(tp))
