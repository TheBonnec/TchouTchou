from Model.TransportationProblem import TransportationProblem
from colorama import Fore, Style
from tabulate import tabulate
from Model.Link import Link
from Model.Supplier import Supplier
from Model.Customer import Customer
from Model.CostLink import CostLink
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
        RESET = Style.RESET_ALL

        headers: list[str] = [""]
        rows: list[list[str]] = []
        bottomRow: list[str] = ["Orders"]
        totalOrders: int = 0

        # Building the header with the list of customers, as well as the orders row
        for customer in transportationProblem.customers:
            headers.append(customer.name)
            bottomRow.append(f"{COLOR_BLACK}{customer.order}{RESET}")
            totalOrders += customer.order
        headers.append("Provision")
        bottomRow.append(f"{COLOR_TOTAL}{totalOrders}{RESET}")

        # Building the rows from the list of suppliers
        for supplier in transportationProblem.suppliers:
            suppliersLink: list[Link] = transportationProblem.getSupplierLinks(supplier = supplier)
            suppliersLink.sort(key = lambda x: x.customer.name, reverse = False)
            row: list[str] = [supplier.name]

            # Adding each cell to the row
            for link in suppliersLink:
                cell: str = f"{COLOR_PROVISIONS}{link.units} {COLOR_COSTS}({link.cost}){RESET}"
                row.append(cell)

            # Adding the provisions
            row.append(f"{COLOR_BLACK}{supplier.provision}{RESET}")

            rows.append(row)

        # Adding the last row (the orders placed by the customer)
        rows.append(bottomRow)

        # Displaying the matrix
        matrix = tabulate(rows, headers = headers, tablefmt = "mixed_grid")
        print(matrix)
        


    
    def displayTransportationProblemMatrixWithPenalties(self, transportationProblem: TransportationProblem):
        COLOR_BLACK = Fore.BLACK
        COLOR_PROVISIONS = Fore.RED
        COLOR_COSTS = Fore.GREEN
        COLOR_TOTAL = Fore.YELLOW
        COLOR_PEN = Fore.MAGENTA
        RESET = Style.RESET_ALL

        headers: list[str] = [""]
        rows: list[list[str]] = []
        bottomRow1: list[str] = ["Orders"]
        bottomRow2: list[str] = ["Penalties"]
        totalOrders: int = 0

        # Building the header with the list of customers, as well as the orders row
        for customer in transportationProblem.customers:
            headers.append(customer.name)
            bottomRow1.append(f"{COLOR_BLACK}{customer.order}{RESET}")
            bottomRow2.append(f"{COLOR_PEN}{customer.penalty}{RESET}")
            totalOrders += customer.order
        headers.append("Provision")
        headers.append("Penalties")
        bottomRow1.append(f"{COLOR_TOTAL}{totalOrders}{RESET}")

        # Building the rows from the list of suppliers
        for supplier in transportationProblem.suppliers:
            suppliersLink: list[Link] = transportationProblem.getSupplierLinks(supplier = supplier)
            suppliersLink.sort(key = lambda x: x.customer.name, reverse = False)
            row: list[str] = [supplier.name]

            # Adding each cell to the row
            for link in suppliersLink:
                cell: str = f"{COLOR_PROVISIONS}{link.units} {COLOR_COSTS}({link.cost}){RESET}"
                row.append(cell)

            # Adding the provisions
            row.append(f"{COLOR_BLACK}{supplier.provision}{RESET}")

            # Adding the penalties
            row.append(f"{COLOR_PEN}{supplier.penalty}{RESET}")

            rows.append(row)

        # Adding the last row (the orders placed by the customer)
        rows.append(bottomRow1)
        rows.append(bottomRow2)

        # Displaying the matrix
        matrix = tabulate(rows, headers = headers, tablefmt = "mixed_grid")
        print(matrix)

    

    def displayCosts(self, costs: list[CostLink]):
        BLUE = Fore.BLUE
        RESET = Style.RESET_ALL

        suppliers: list[Supplier] = []
        customers: list[Customer] = []

        headers: list[str] = [""]

        for link in costs:
            if link.supplier not in suppliers:
                suppliers.append(link.supplier)
            if link.customer not in customers:
                customers.append(link.customer)
                headers.append(link.customer.name)
        
        rows: list[list[str]] = []

        for supplier in suppliers:
            row: list[str] = [supplier.name]
            for customer in customers:
                for cost in costs:
                    if cost.supplier == supplier and cost.customer == customer:
                        row.append(f"{BLUE}{cost.cost}{RESET}")
            rows.append(row)
        
        matrix = tabulate(rows, headers = headers, tablefmt = "mixed_grid")
        print(matrix)
        
        

        