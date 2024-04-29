from Model.TransportationProblem import TransportationProblem
import copy


class TransportationProblemViewController:
    def __init__(self):
        pass


    '''def NordWestAlgorithm(transportationProblem: TransportationProblem):
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

        return tpCopy'''
            
    def calculate_penalties(self, links):
        row_penalties = {}
        col_penalties = {}

        # Calculate row penalties
        for supplier in set(link.supplier for link in links):
            supplier_links = [link for link in links if link.supplier == supplier and link.customer.order > 0]
            if supplier_links:
                row_costs = sorted(link.cost for link in supplier_links)
                row_penalties[supplier] = row_costs[1] - row_costs[0] if len(row_costs) > 1 else 0

        # Calculate column penalties
        for customer in set(link.customer for link in links):
            customer_links = [link for link in links if link.customer == customer and link.supplier.provision > 0]
            if customer_links:
                col_costs = sorted(link.cost for link in customer_links)
                col_penalties[customer] = col_costs[1] - col_costs[0] if len(col_costs) > 1 else 0
            
        return row_penalties, col_penalties


        
    def BalasHammerAlgo(self, transportationProblem):
        tpCopy = copy.deepcopy(transportationProblem)

        while any(supplier.provision > 0 for supplier in tpCopy.suppliers) and any(customer.order > 0 for customer in tpCopy.customers):
            row_penalties, col_penalties = self.calculate_penalties(tpCopy.links)

            max_row_penalty_supplier = max(row_penalties, key=row_penalties.get, default=None)
            max_col_penalty_customer = max(col_penalties, key=col_penalties.get, default=None)

            # Determine whether to allocate based on row or column by comparing penalties
            allocate_row = True
            if max_row_penalty_supplier is not None and max_col_penalty_customer is not None:
                allocate_row = row_penalties[max_row_penalty_supplier] >= col_penalties[max_col_penalty_customer]
            elif max_col_penalty_customer is not None:
                allocate_row = False

            if allocate_row:
                # Allocate to the link with the minimum cost in the row of the supplier with the max penalty
                min_cost_link = min(
                    (link for link in tpCopy.links if link.supplier == max_row_penalty_supplier and link.customer.order > 0),
                    key=lambda link: link.cost,
                    default=None  # Handle case with no links available for allocation
                )
            else:
                # Allocate to the link with the minimum cost in the column of the customer with the max penalty
                min_cost_link = min(
                    (link for link in tpCopy.links if link.customer == max_col_penalty_customer and link.supplier.provision > 0),
                    key=lambda link: link.cost,
                    default=None
                )

            # If there is no link available for allocation, break the loop
            if not min_cost_link:
                break

            # Perform the allocation
            allocation = min(min_cost_link.supplier.provision, min_cost_link.customer.order)
            if allocation > 0:
                min_cost_link.units += allocation
                min_cost_link.supplier.provision -= allocation
                min_cost_link.customer.order -= allocation
            else:
                # If no allocation can be made, break the loop to prevent infinite loop
                break

        return tpCopy
        
        
