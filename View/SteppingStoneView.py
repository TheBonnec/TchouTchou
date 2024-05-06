from Controller.SteppingStoneViewController import SteppingStoneViewController
from Model.TransportationProblem import TransportationProblem
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from colorama import Fore, Style
from InquirerPy import inquirer
from View.View import View


class SteppingStoneView(View):
    
    ''' ----- Attributes ----- '''

    def __init__(self, transportationProblem: TransportationProblem):
        self.transportationProblem: TransportationProblem = transportationProblem
        self.viewController: SteppingStoneViewController = SteppingStoneViewController()

        self.optionExit = Choice("Exit")
        self.optionSteppingStone = Choice("Continue with Stepping Stone Algorithm")

        self.options = [self.optionSteppingStone]
        self.options.append(Separator())
        self.options.append(self.optionExit)

        super().__init__()




    ''' ----- View ----- '''

    def body(self):
        RED = Fore.RED
        GREEN = Fore.GREEN
        BLUE = Fore.BLUE
        RESET = Style.RESET_ALL

        self.displayTransportationProblemMatrix(transportationProblem = self.transportationProblem)

        usedTP = self.transportationProblem

        isGraphConnected = self.viewController.isConnected(usedTP)
        isGraphAcyclic = self.viewController.isGraphAcylic(transportationProblem = usedTP)


        if not isGraphConnected or not isGraphAcyclic:
            print(f"\n\n{RED}The proposition is degenerated. We will create a non degenerate one.{RESET}")
            input("\n\n")

            usedTP = self.viewController.toNonDegenerate(TP = self.transportationProblem)

            print("\nNew Non Degenerated Proposition :\n")
            self.displayTransportationProblemMatrix(transportationProblem = usedTP)
        else:
            print(f"\n\n{GREEN}The proposition is not degenerated.{RESET}")
            input("\n\n")


        potentialCosts = self.viewController.calculatePotentialCosts(tp = usedTP)
        marginalCosts = self.viewController.calculateMarginalCosts(costLinks = usedTP.getCostsLinks(), potentialsLinks = potentialCosts)
        
        print(f"\n\n{BLUE}Potential Costs : \n{RESET}")
        self.displayCosts(potentialCosts)

        print(f"\n\n{BLUE}Marginal Costs : \n{RESET}")
        self.displayCosts(marginalCosts)


        '''
        checkMarginal = self.viewController.checkMarginalCosts(tp = usedTP, marginalCosts = marginalCosts)
        if checkMarginal != None:
            self.displayTransportationProblemMatrix(transportationProblem = checkMarginal)
        '''



        input("\nContinue ")
        self.isViewRunning = False