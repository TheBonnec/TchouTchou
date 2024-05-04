import json
from Controller.TransportationProblemViewController import TransportationProblemViewController
from Model.TransportationProblem import TransportationProblem
from Controller.IsConnected import isConnected
from Controller.ToNonDegenerate import toNonDegenerate

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