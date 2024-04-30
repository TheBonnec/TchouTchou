class Supplier:
    def __init__(self, name: str, provision: int):
        self.name = name
        self.provision = provision
        self.penalty = -1

    def print(self):
        print("Supplier "+self.name+" with provision "+str(self.provision))
        
    def __lt__(self, other):
        # Assume that comparison is based on the 'provision' attribute
        return self.provision < other.provision    