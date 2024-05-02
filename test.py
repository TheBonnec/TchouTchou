import json
from Controller.TransportationProblemViewController import TransportationProblemViewController
from Model.TransportationProblem import TransportationProblem

class MyView:
    def __init__(self):
        self.controller = TransportationProblemViewController()

    def solve_transportation_problem(self, filename):
        print(f"Attempting to solve transportation problem from file: {filename}")
        tp = TransportationProblem(filename)
        solved_tp_bh = self.controller.balasHammerAlgo(tp)
        print("Applied Balas-Hammer Algorithm.")
        self.display_results(solved_tp_bh)

    def display_results(self, solved_tp):
        allocations_exist = False
        for link in solved_tp.links:
            if link.units > 0:
                allocations_exist = True
                print(f"Allocated {link.units} units from {link.supplier.name} to {link.customer.name}")
        if not allocations_exist:
            print("No allocations made using Balas-Hammer Algorithm. Please check the input data and algorithm logic.")





filepath = "TextFiles/TransportationProblem5.json"

view = MyView()
view.solve_transportation_problem(filepath)