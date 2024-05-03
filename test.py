from Controller.SteppingStoneViewController import SteppingStoneViewController
from Model.TransportationProblem import TransportationProblem

tp = TransportationProblem("TextFiles/TransportationProblem6.json")

controller = SteppingStoneViewController()

potentialCost = controller.calculatePotentials(tp)

for costLink in potentialCost:
    print(f"Potential cost from {costLink.supplier.name} to {costLink.customer.name}: {costLink.cost}")
