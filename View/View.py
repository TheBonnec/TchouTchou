import os
from colorama import Fore, Style

class View:
    def __init__(self, displayViewAtInit: bool = True):
        if displayViewAtInit:
            self.displayView()

    
    
    def afficher_proposition_transport(self, transportationProblem, transportProposition):
        COLOR_HEADER = Fore.BLACK
        COLOR_PROVISIONS = Fore.RED
        COLOR_COUTS = Fore.GREEN
        LENGTH = 15

        nb_lignes = len(transportationProblem.suppliers)
        nb_colonnes = len(transportationProblem.customers)

        provisions =[]
        commandes = []
        for i in range(nb_lignes):
            provisions.append(transportationProblem.suppliers[i].provision)
        for j in range(nb_colonnes):
            commandes.append(transportationProblem.customers[j].order)


        prix_transport = [[transportationProblem.links[i * nb_colonnes + j].units for j in range(nb_colonnes)] for i in range(nb_lignes)]


        proposition_transport = [[0 for _ in range(nb_colonnes)] for _ in range(nb_lignes)]
        for i in range(nb_lignes):
            for j in range(nb_colonnes):
                proposition_transport[i][j] = transportProposition.links[i * nb_colonnes + j].units

        




        print("\nProposition de transport:")
        print(" " * LENGTH, end="")
        for colonne in range(nb_colonnes):
            print(COLOR_HEADER + f"C{colonne + 1}" + " " * (LENGTH - len(str(colonne + 1)) - 2), end="")
        print(COLOR_HEADER + f"Provision Pi" + " " * (LENGTH - len("Provision Pi") - 1), end="")
        print(Style.RESET_ALL)
        for ligne in range(nb_lignes):
            print(COLOR_HEADER + f"P{ligne + 1}" + " " * (LENGTH - len(str(ligne + 1)) - 1), end="")
            for colonne in range(nb_colonnes):
                print(COLOR_PROVISIONS + f"{proposition_transport[ligne][colonne]}", end=" ")
                print(COLOR_COUTS + "(" + str(prix_transport[ligne][colonne]) + ")"+ " " * (LENGTH - len(str(proposition_transport[ligne][colonne])) - len(str(prix_transport[ligne][colonne])) - 4), end="")
            print(COLOR_PROVISIONS + f"{provisions[ligne]}" + " " * (LENGTH - len(str(provisions[ligne])) - 1), end="")
            print(Style.RESET_ALL)
        print(COLOR_HEADER + "Commandes Cj" + " " * (LENGTH - len("Commandes Cj")), end="")
        for colonne in range(nb_colonnes):
            print(COLOR_PROVISIONS + f"{commandes[colonne]}" + " " * (LENGTH - len(str(commandes[colonne])) - 1),end="")
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