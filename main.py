from Controller.SteppingStoneViewController import SteppingStoneViewController
from Model.TransportationProblem import TransportationProblem

# Create the problem instance from a JSON file
tp = TransportationProblem("TextFiles/TransportationProblem5.json")
controller = SteppingStoneViewController(tp)
constraintValue = controller.calculateConstraint()
print("Transportation Constraint:", constraintValue)
