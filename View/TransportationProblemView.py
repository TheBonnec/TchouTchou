from Controller.TransportationProblemViewController import TransportationProblemViewController
from Model.TransportationProblem import TransportationProblem
from View.SteppingStoneView import SteppingStoneView
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from colorama import Fore, Style
from InquirerPy import inquirer
from tabulate import tabulate
from Model.Link import Link
from View.View import View


class TransportationProblemView(View):

    ''' ----- Attributes ----- '''

    def __init__(self, transportationProblem: TransportationProblem):
        self.transportationProblem: TransportationProblem = transportationProblem
        self.viewController: TransportationProblemViewController = TransportationProblemViewController()

        self.optionExit = Choice("Exit")
        self.optionNorthWest = Choice("North-West")
        self.optionBalasHammer = Choice("Balas-Hammer (Vogel's approximation)")

        self.options = [self.optionNorthWest, self.optionBalasHammer]
        self.options.append(Separator())
        self.options.append(self.optionExit)

        super().__init__()



    

    ''' ----- View ----- '''

    def body(self):
        print(f"{self.transportationProblem.name}\n")
        self.displayTransportationProblemMatrix(transportationProblem = self.transportationProblem)

        print("\n\n")

        menu = inquirer.select(
            message = "Select an algorithm to improve this problem : ",
            choices = self.options,
            default = None
        ).execute()


        if menu == self.optionExit.value:
            self.isViewRunning = False
        elif menu == self.optionNorthWest.value:
            NorthWestView(transportationProblem = self.transportationProblem, viewController = self.viewController)
        elif menu == self.optionBalasHammer.value:
            BalasHammerView(transportationProblem = self.transportationProblem, viewController = self.viewController)

    




class NorthWestView(View):
    def __init__(self, transportationProblem: TransportationProblem, viewController: TransportationProblemViewController):
        self.viewController = viewController
        self.transportationProblem = self.viewController.northWestAlgorithm(transportationProblem = transportationProblem)

        self.optionExit = Choice("Exit")
        self.optionSteppingStone = Choice("Continue with Stepping Stone Algorithm")

        self.options = [self.optionSteppingStone]
        self.options.append(Separator())
        self.options.append(self.optionExit)

        super().__init__()



    def body(self):
        print(f"\n{self.transportationProblem.name} - North West\n")
        self.displayTransportationProblemMatrix(transportationProblem = self.transportationProblem)

        print(f"\nTotal Cost of the proposition : {self.viewController.calculateTotalCost(tp = self.transportationProblem)}\n\n")


        menu = inquirer.select(
            message = "Select an option to continue : ",
            choices = self.options,
            default = None
        ).execute()

        
        if menu == self.optionExit.value:
            self.isViewRunning = False
        elif menu == self.optionSteppingStone.value:
            SteppingStoneView(transportationProblem = self.transportationProblem)

        self.isViewRunning = False





class BalasHammerView(View):
    def __init__(self, transportationProblem: TransportationProblem, viewController: TransportationProblemViewController):
        self.viewController = viewController
        self.transportationProblem = self.viewController.balasHammerAlgo(transportationProblem = transportationProblem)

        self.viewController.calculatePenalties(transportationProblem = self.transportationProblem)

        self.optionExit = Choice("Exit")
        self.optionSteppingStone = Choice("Continue with Stepping Stone Algorithm")

        self.options = [self.optionSteppingStone]
        self.options.append(Separator())
        self.options.append(self.optionExit)

        super().__init__()



    def body(self):
        print(f"\n{self.transportationProblem.name} - Balas Hammer\n")
        self.displayTransportationProblemMatrixWithPenalties(transportationProblem = self.transportationProblem)

        print(f"\nTotal Cost of the proposition : {self.viewController.calculateTotalCost(tp = self.transportationProblem)}\n\n")


        menu = inquirer.select(
            message = "Select an option to continue : ",
            choices = self.options,
            default = None
        ).execute()

        
        if menu == self.optionExit.value:
            self.isViewRunning = False
        elif menu == self.optionSteppingStone.value:
            SteppingStoneView(transportationProblem = self.transportationProblem)

        self.isViewRunning = False