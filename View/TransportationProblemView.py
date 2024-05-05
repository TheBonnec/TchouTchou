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
            newTP: TransportationProblem = self.viewController.northWestAlgorithm(transportationProblem = self.transportationProblem)
            SteppingStoneView(transportationProblem = newTP, method = "North West")
        elif menu == self.optionBalasHammer.value:
            newTP: TransportationProblem = self.viewController.balasHammerAlgo(transportationProblem = self.transportationProblem)
            SteppingStoneView(transportationProblem = newTP, method = "Balas - Hammer")