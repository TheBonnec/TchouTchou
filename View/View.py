import os
from colorama import Fore, Style

class View:
    def __init__(self, displayViewAtInit: bool = True):
        if displayViewAtInit:
            self.displayView()

    
    
    def displayTransportProposition(self, transportationProblem, transportProposition):
        COLOR_HEADER = Fore.BLACK
        COLOR_PROVISIONS = Fore.RED
        COLOR_COUTS = Fore.GREEN
        LENGTH = 15

        nbRows = len(transportationProblem.suppliers)
        nbColumns = len(transportationProblem.customers)

        provisions =[]
        orders = []
        for i in range(nbRows):
            provisions.append(transportationProblem.suppliers[i].provision)
        for j in range(nbColumns):
            orders.append(transportationProblem.customers[j].order)


        transportPrices = [[transportationProblem.links[i * nbColumns + j].cost for j in range(nbColumns)] for i in range(nbRows)]


        proposition_transport = [[0 for _ in range(nbColumns)] for _ in range(nbRows)]
        for i in range(nbRows):
            for j in range(nbColumns):
                proposition_transport[i][j] = transportProposition.links[i * nbColumns + j].units

        
        print("\nTransportation proposition :")
        print(" " * LENGTH, end="")
        for column in range(nbColumns):
            print(COLOR_HEADER + f"C{column + 1}" + " " * (LENGTH - len(str(column + 1)) - 2), end="")
        print(COLOR_HEADER + f"Provision Pi" + " " * (LENGTH - len("Provision Pi") - 1), end="")
        print(Style.RESET_ALL)
        for row in range(nbRows):
            print(COLOR_HEADER + f"P{row + 1}" + " " * (LENGTH - len(str(row + 1)) - 1), end="")
            for column in range(nbColumns):
                print(COLOR_PROVISIONS + f"{proposition_transport[row][column]}", end=" ")
                print(COLOR_COUTS + "(" + str(transportPrices[row][column]) + ")"+ " " * (LENGTH - len(str(proposition_transport[row][column])) - len(str(transportPrices[row][column])) - 4), end="")
            print(COLOR_PROVISIONS + f"{provisions[row]}" + " " * (LENGTH - len(str(provisions[row])) - 1), end="")
            print(Style.RESET_ALL)
        print(COLOR_HEADER + "orders Cj" + " " * (LENGTH - len("orders Cj")), end="")
        for column in range(nbColumns):
            print(COLOR_PROVISIONS + f"{orders[column]}" + " " * (LENGTH - len(str(orders[column])) - 1),end="")
        print(Style.RESET_ALL)




    def displayView(self):
        self._clearConsole()
        self._title()
        self.body()
    
    
    def body(self):
        print("This is a view !\n\n")


    def _clearConsole(self):
        os.system('cls' if os.name=='nt' else 'clear')


    def _title(self):
        content = r"""
    
TTTTT   CCCC  H   H   OOO   U   U  TTTTT   CCCC  H   H   OOO   U   U
  T    C      HHHHH  O   O  U   U    T    C      HHHHH  O   O  U   U
  T    C      H   H  O   O  U   U    T    C      H   H  O   O  U   U
  T     CCCC  H   H   OOO    UUU     T     CCCC  H   H   OOO    UUU 

Operations Research Project

    """
        print(content)