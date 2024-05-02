from Controller.SteppingStoneViewController import SteppingStoneViewController
from Model.TransportationProblem import TransportationProblem
from Model.IsConnected import isConnected
<<<<<<< HEAD
from Controller.TransportationProblemViewController import TransportationProblemViewController
=======
>>>>>>> e4e8561 (test isConnected et debut ToNonDegenerate)

<<<<<<< HEAD
# Create the problem instance from a JSON file
<<<<<<< HEAD
tp = TransportationProblem("TextFiles/TransportationProblem8.json")
tp = TransportationProblemViewController.NordWestAlgorithm(tp)
for i in tp.links:
    i.print()
print(isConnected(tp))
=======
tp = TransportationProblem("TextFiles/TransportationProblem5.json")
controller = SteppingStoneViewController(tp)
constraintValue = controller.calculateConstraint()
print("Transportation Constraint:", constraintValue)
=======
class MyView():
    TP = TransportationProblem("TextFiles/TransportationProblem3.json")

    #def __init__(self):
     #super().__init__()


MyView()
>>>>>>> 2470b88 (test isConnected et debut ToNonDegenerate)
>>>>>>> e4e8561 (test isConnected et debut ToNonDegenerate)
