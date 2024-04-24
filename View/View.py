import os

class View:
    def __init__(self, displayViewAtInit: bool = True):
        if displayViewAtInit:
            self.displayView()



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