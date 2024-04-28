from Model.TransportationProblem import TransportationProblem
import copy


class TransportationProblemViewController:
    def __init__(self):
        pass


    def NordWestAlgorithm(transportationProblem: TransportationProblem):
        tp_copy = copy.deepcopy(transportationProblem)
        i, j = 0, 0

        while i < len(tp_copy.suppliers) and j < len(tp_copy.customers):
            # Calculate the minimum amount to allocate
            amount = min(tp_copy.suppliers[i].provision, tp_copy.customers[j].order)
            
            # Find the corresponding Link object and update its quantity
            link = next((l for l in tp_copy.links if l.supplier == tp_copy.suppliers[i] and l.customer == tp_copy.customers[j]), None)
            if link:
                link.units += amount  # Increment the quantity

            # Update the remaining supply and demand
            tp_copy.suppliers[i].provision -= amount
            tp_copy.customers[j].order -= amount

            # Move to the next supplier or customer
            if tp_copy.suppliers[i].provision == 0 and i < len(tp_copy.suppliers) - 1:
                i += 1
            elif tp_copy.customers[j].order == 0 and j < len(tp_copy.customers) - 1:
                j += 1
            elif tp_copy.suppliers[i].provision == 0:
                break
            elif tp_copy.customers[j].order == 0:
                break

        return tp_copy