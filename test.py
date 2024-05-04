from Controller.SteppingStoneViewController import SteppingStoneViewController
from Model.TransportationProblem import TransportationProblem


if __name__ == "__main__":
    tp = TransportationProblem("TextFiles/TransportationProblem5.json")
    controller = SteppingStoneViewController()
    
    # Calculate and print potential costs
    potentialCosts = controller.calculatePotentials(tp)
    for costLink in potentialCosts:
        print(f"Potential cost from {costLink.supplier.name} to {costLink.customer.name}: {costLink.cost}")

    # Define cycle nodes and remove the cycle
    cycleNodes = [("P1", "C1"), ("P2", "C2"), ("P3", "C1")]
    updatedTp, removedLinks = controller.removeCycle(tp, cycleNodes)
    
    # Print removed links with their costs
    print("\nRemoved Links:")
    for link in removedLinks:
        print(f"Removed link from {link.supplier.name} to {link.customer.name} with cost {link.cost}")