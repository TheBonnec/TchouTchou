class Customer:
    def __init__(self, name: str, order: int):
        self.name = name
        self.order = order
        self.penalty = -1

    def print(self):
        print("Customer "+self.name+" with order "+str(self.order))