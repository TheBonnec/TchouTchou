from Model.TransportationProblem import TransportationProblem
import copy


class TransportationProblemViewController:
    def __init__(self):
        pass


    def NordWestAlgorithm(transportationProblem: TransportationProblem):
        tpCopy = copy.deepcopy(transportationProblem)
        i, j = 0, 0

        while i < len(tpCopy.suppliers) and j < len(tpCopy.customers):
            # Calculate the minimum amount to allocate
            amount = min(tpCopy.suppliers[i].provision, tpCopy.customers[j].order)
            
            # Find the corresponding Link object and update its quantity
            link = next((l for l in tpCopy.links if l.supplier == tpCopy.suppliers[i] and l.customer == tpCopy.customers[j]), None)
            if link:
                link.units += amount  # Increment the quantity

            # Update the remaining supply and demand
            tpCopy.suppliers[i].provision -= amount
            tpCopy.customers[j].order -= amount

            # Move to the next supplier or customer
            if tpCopy.suppliers[i].provision == 0 and i < len(tpCopy.suppliers) - 1:
                i += 1
            elif tpCopy.customers[j].order == 0 and j < len(tpCopy.customers) - 1:
                j += 1
            elif tpCopy.suppliers[i].provision == 0:
                break
            elif tpCopy.customers[j].order == 0:
                break

        return tpCopy