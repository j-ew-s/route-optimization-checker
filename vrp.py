from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

# Simulated time matrix in minutes between 6 locations (0: depot, 1-5: clients)
time_matrix = [
    [0, 10, 15, 20, 12, 60],  # depot (Porto center)
    [10, 0, 5, 10, 5, 55],
    [15, 5, 0, 5, 10, 50],
    [20, 10, 5, 0, 15, 45],
    [12, 5, 10, 15, 0, 58],
    [60, 55, 50, 45, 58, 0],  # client in Aveiro
]

time_windows = [
    [0, 0],      # sede (deve ser 0 pois é fixa)
    [60, 120],   # 09:00 - 10:00
    [120, 180],  # 10:00 - 11:00
    [180, 240],  # 11:00 - 12:00
    [240, 300],  # 12:00 - 13:00
    [300, 480],  # 13:00 - 16:00 (cliente em Aveiro)
]

def create_data_model():
    """Stores the data for the problem."""
    return {
        'time_matrix': time_matrix,
        'num_vehicles': 1,
        'time_windows': time_windows,
        'depot': 0,
    }

def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    print("Route:")
    index = routing.Start(0)
    route = []
    route_time = 0
    while not routing.IsEnd(index):
        node = manager.IndexToNode(index)
        route.append(node)
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_time += routing.GetArcCostForVehicle(previous_index, index, 0)
    route.append(manager.IndexToNode(index))
    print(" -> ".join(str(loc) for loc in route))
    print(f"Total travel time: {route_time} min")

def main():
    data = create_data_model()

    # Create the routing index manager
    manager = pywrapcp.RoutingIndexManager(len(data['time_matrix']), data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)

    # Define cost of each arc
    def time_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['time_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(time_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Set search parameters
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

    # Solve the problem
    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        print_solution(data, manager, routing, solution)
    else:
        print("No solution found.")

if __name__ == '__main__':
    main() 