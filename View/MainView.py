from View.TransportationProblemView import TransportationProblemView
from Model.TransportationProblem import TransportationProblem
from Model.ProblemsList import getAllTransportationProblems
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from InquirerPy import inquirer
from View.View import View



class MainView(View):

    ''' ----- Attributes ----- '''

    def __init__(self):
        self.transportationProblems: list[TransportationProblem] = getAllTransportationProblems()

        self.optionExit = Choice("Exit")

        self.options = self.getAllChoices(tps = self.transportationProblems)
        self.options.append(Separator())
        self.options.append(self.optionExit)

        super().__init__()





    ''' ----- View ----- '''
    
    def body(self):
        menu = inquirer.select(
            message = "Select a transportation problem : ",
            choices = self.options,
            default = None
        ).execute()


        if menu == self.optionExit.value:
            self.isViewRunning = False
        elif menu:
            selectedTP = self.getTPFromName(name = menu)
            if selectedTP != None:
                TransportationProblemView(transportationProblem = selectedTP)


    


    ''' ----- Methods ----- '''

    def getAllChoices(self, tps: list[TransportationProblem]) -> list[str]:
        names: list[str] = []

        for tp in tps:
            names.append(Choice(tp.name))

        return names
    


    def getTPFromName(self, name: str) -> TransportationProblem:
        selectedTP = None

        for tp in self.transportationProblems:
            if tp.name == name:
                selectedTP = tp

        return selectedTP
