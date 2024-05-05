from Controller.SteppingStoneViewController import SteppingStoneViewController
from Model.TransportationProblem import TransportationProblem
from Controller.IsConnected import isConnected
from Controller.ToNonDegenerate import toNonDegenerate
from Controller.TransportationProblemViewController import TransportationProblemViewController
from View.View import View


if __name__ == "__main__":
    # Load transportation problem from JSON (mocked for the example)
    tp = TransportationProblem("TextFiles/caca.json")
    #solve tp with BH
    TransportationProblemViewController = TransportationProblemViewController()

    SteppingStoneViewController = SteppingStoneViewController()
    solved_tp_bh = TransportationProblemViewController.balasHammerAlgo(tp)

    # Modifications parce que votre balas hammer est cassé
    solved_tp_bh.links[6].units = 30
    solved_tp_bh.links[5].units = 0
    solved_tp_bh.links[2].units = 1 # on fait ca pour que le tp soit non dégénéré
    solved_tp_bh.links[9].units = 75
    solved_tp_bh.links[10].units = 0

    View = View()
    View.displayTransportProposition(tp, solved_tp_bh)
    



    # Calculate and print potential costs
    potentialCosts = SteppingStoneViewController.calculatePotentialCosts(tp, solved_tp_bh)
    print("\nPotential costs:")
    for link in potentialCosts:
        print(f"Potential cost from {link.supplier.name} to {link.customer.name}: {link.cost}")

    # Calculate and print marginal costs
    marginalCost = SteppingStoneViewController.calculateMarginalCosts(tp.links, potentialCosts)
    print("\nMarginal costs:")
    for costLink in marginalCost:
        print(f"Marginal cost from {costLink.supplier.name} to {costLink.customer.name}: {costLink.cost}")

    
    solved_tp_bh.links[2].units = 0 # on remet la modif qu'on avait faite comme avant
    new = SteppingStoneViewController.checkMarginalCosts(solved_tp_bh, marginalCost)
    print("\nNew solution:")
    View.displayTransportProposition(tp, new)

    
    """
    # Calculate and print marginal costs
    marginalCost = SteppingStoneViewController.calculateMarginalCosts(tp)
    for costLink in marginalCost:
        print(f"Marginal cost from {costLink.supplier.name} to {costLink.customer.name}: {costLink.cost}")

    # Define cycle nodes and remove the cycle
    cycleNodes = [("P1", "C1"), ("P2", "C2"), ("P3", "C1")]
    updatedTp, removedLinks = SteppingStoneViewController.removeCycle(tp, cycleNodes)

    # Print removed links with their costs
    print("\nRemoved Links:")
    for link in removedLinks:
        print(f"Removed link from {link.supplier.name} to {link.customer.name} with cost {link.cost}")
    """
'''
class MyView:
    def __init__(self):
        self.controller = TransportationProblemViewController()


    def solve_transportation_problem(self, filename):
        print(f"Attempting to solve transportation problem from file: {filename}")
        tp = TransportationProblem(filename)
        solved_tp_bh = self.controller.NordWestAlgorithm(tp)
        print("Applied NorthWest Algorithm.")

        tpNonDegenerate = self.isConnectedAndToNonDegenerate(solved_tp_bh)
        self.display_results(tpNonDegenerate)

    def display_results(self, solved_tp):
        allocations_exist = False
        for link in solved_tp.links:
            allocations_exist = True
            print(f"Allocated {link.units} units from {link.supplier.name} to {link.customer.name}")
        if not allocations_exist:
            print("No allocations made using Balas-Hammer Algorithm. Please check the input data and algorithm logic.")
    
    def isConnectedAndToNonDegenerate(self, initialProposal):
        if (type(isConnected(initialProposal))!=type(initialProposal)):
            nonDegenerateTP = toNonDegenerate(initialProposal)
            return nonDegenerateTP
        return initialProposal




filepath = "TextFiles/TransportationProblem1.json"

view = MyView()
view.solve_transportation_problem(filepath)
'''
