from Model.TransportationProblem import TransportationProblem


class MyView:
    def __init__(self):
        self.transportation_problem = None

    def solve_transportation_problem(self, filename):
        print(f"Loading Transportation Problem from {filename}")
        self.transportation_problem = TransportationProblem(filename)

        solved_tp = self.transportation_problem.NordWestAlgorithm()

        for link in solved_tp.links:
            if link.units > 0:
                print(f"Allocated {link.units} units from {link.supplier.name} to {link.customer.name}")

        if not any(link.units > 0 for link in solved_tp.links):
            print("No allocations made. Please check the input data and algorithm logic.")

if __name__ == "__main__":
    filename = "TextFiles/TransportationProblem5.json"
    view = MyView()
    view.solve_transportation_problem(filename)

