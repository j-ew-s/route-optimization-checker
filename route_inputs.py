import requests
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def get_coordinates_from_user():
    coords = []
    print("Insira 5 coordenadas (latitude, longitude):")
    for i in range(5):
        lat = input(f"Latitude do local {i}: ").strip()
        lon = input(f"Longitude do local {i}: ").strip()
        coords.append((lat, lon))
    return coords

def build_distance_matrix(locations):
    ors_locations = [[float(lon), float(lat)] for lat, lon in locations]
    url = 'https://api.openrouteservice.org/v2/matrix/driving-car'
    headers = {
        'Authorization': 'eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6ImFkZWM0M2E2ZjU3MjQ1YTA5NTA1MDkxYTg5ZWIyMGFhIiwiaCI6Im11cm11cjY0In0=',
        'Content-Type': 'application/json'
    }
    body = {
        "locations": ors_locations,
        "metrics": ["duration"],
        "units": "m"
    }
    response = requests.post(url, json=body, headers=headers)
    data = response.json()
    if 'durations' not in data:
        print("Error from OpenRouteService:", data)
        exit(1)
    matrix = [[int(x) for x in row] for row in data['durations']]
    return matrix

def solve_tsp(distance_matrix):
    n = len(distance_matrix)
    for row in distance_matrix:
        if len(row) != n:
            print("Distance matrix is not square!")
            exit(1)
        if not all(isinstance(x, int) and x >= 0 for x in row):
            print("Distance matrix contains invalid values!")
            exit(1)
    manager = pywrapcp.RoutingIndexManager(n, 1, 0)
    routing = pywrapcp.RoutingModel(manager)
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]
    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    search_params = pywrapcp.DefaultRoutingSearchParameters()
    search_params.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    solution = routing.SolveWithParameters(search_params)
    if solution:
        route = []
        index = routing.Start(0)
        while not routing.IsEnd(index):
            route.append(manager.IndexToNode(index))
            index = solution.Value(routing.NextVar(index))
        route.append(manager.IndexToNode(index))
        return route
    else:
        return None

def export_route_to_google_maps(locations, route):
    waypoints = [f"{locations[idx][0]},{locations[idx][1]}" for idx in route]
    url = "https://www.google.com/maps/dir/" + "/".join(waypoints)
    print("\nOpen this URL in your browser to view the route in Google Maps:")
    print(url)

def main():
    locations = get_coordinates_from_user()
    print("\nConsultando OpenRouteService Matrix...")
    distance_matrix = build_distance_matrix(locations)
    print("Distance matrix:", distance_matrix)
    print("Calculando rota otimizada...")
    route = solve_tsp(distance_matrix)
    if route:
        print("\nSequência ótima de visita:")
        for idx in route:
            lat, lon = locations[idx]
            print(f"→ Local {idx}: {lat}, {lon}")
        export_route_to_google_maps(locations, route)
    else:
        print("Não foi possível encontrar uma rota.")

if __name__ == '__main__':
    main()
