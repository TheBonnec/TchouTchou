from Controller.SteppingStoneViewController import SteppingStoneViewController
from Model.TransportationProblem import TransportationProblem
from Model.IsConnected import isConnected

<<<<<<< HEAD
# Create the problem instance from a JSON file
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
