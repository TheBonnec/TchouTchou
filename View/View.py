from Model.TransportationProblem import TransportationProblem
from colorama import Fore, Style
from tabulate import tabulate
from Model.Link import Link
import os



class View:
    def __init__(self, displayViewAtInit: bool = True):
        self.isViewRunning = True
        if displayViewAtInit:
            self.displayView()



    def displayView(self):
        while self.isViewRunning:
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


    

    ''' ----- Tools ----- '''

    def displayTransportationProblemMatrix(self, transportationProblem: TransportationProblem):
        COLOR_BLACK = Fore.BLACK
        COLOR_PROVISIONS = Fore.RED
        COLOR_COSTS = Fore.GREEN
        COLOR_TOTAL = Fore.YELLOW

        headers: list[str] = [""]
        rows: list[list[str]] = []
        bottomRow: list[str] = ["Orders"]
        totalOrders: int = 0

        # Building the header with the list of customers, as well as the orders row
        for customer in transportationProblem.customers:
            headers.append(customer.name)
            bottomRow.append(f"{COLOR_BLACK}{customer.order}{Style.RESET_ALL}")
            totalOrders += customer.order
        headers.append("Provision")
        bottomRow.append(f"{COLOR_TOTAL}{totalOrders}{Style.RESET_ALL}")

        # Building the rows from the list of suppliers
        for supplier in transportationProblem.suppliers:
            suppliersLink: list[Link] = transportationProblem.getSupplierLinks(supplier = supplier)
            suppliersLink.sort(key = lambda x: x.customer.name, reverse = False)
            row: list[str] = [supplier.name]

            # Adding each cell to the row
            for link in suppliersLink:
                cell: str = f"{COLOR_PROVISIONS}{link.units} {COLOR_COSTS}({link.cost}){Style.RESET_ALL}"
                row.append(cell)

            # Adding the provisions
            row.append(f"{COLOR_BLACK}{supplier.provision}{Style.RESET_ALL}")

            rows.append(row)

        # Adding the last row (the orders placed by the customer)
        rows.append(bottomRow)


        # Displaying the matrix
        matrix = tabulate(rows, headers = headers, tablefmt = "mixed_grid")
        print(matrix)