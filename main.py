from Controller.SteppingStoneViewController import SteppingStoneViewController
from Model.TransportationProblem import TransportationProblem
from Controller.TransportationProblemViewController import TransportationProblemViewController
# Create the problem instance from a JSON file
tp = TransportationProblem("TextFiles/TransportationProblem5.json")

"""
controller = SteppingStoneViewController(tp)
constraintValue = controller.calculateConstraint()
print("Transportation Constraint:", constraintValue)
"""

tpcontroler = TransportationProblemViewController()

solution = tpcontroler.NordWestAlgorithm(tp)


from View.View import View
View().afficher_proposition_transport(tp, solution)

from Controller.verifyCycle import isAcylique
print(isAcylique(solution))


