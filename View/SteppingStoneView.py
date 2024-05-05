from Controller.SteppingStoneViewController import SteppingStoneViewController
from Model.TransportationProblem import TransportationProblem
from View.View import View


class SteppingStoneView(View):
    
    ''' ----- Attributes ----- '''

    def __init__(self, transportationProblem: TransportationProblem, method: str):
        self.transportationProblem: TransportationProblem = transportationProblem
        self.viewController: SteppingStoneViewController = SteppingStoneViewController(transportationProblem = transportationProblem)
        self.method = method

        super().__init__()




    ''' ----- View ----- '''

    def body(self):
        print(f"\n{self.transportationProblem.name} - {self.method}\n")
        self.displayTransportationProblemMatrix(transportationProblem = self.transportationProblem)

        input("\nContinuer ")
        self.isViewRunning = False