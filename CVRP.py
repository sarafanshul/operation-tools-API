from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from Data import Data
from Writer import Writer

class VRP :
    
    def __init__ ( self , _num_vehicles , _depot , _locations , _vehicle_cap , _demands ):
        self.parser = Data( _num_vehicles , _depot , _locations , _vehicle_cap , _demands )
        
    def parseSolution(self ,data, manager, routing, solution):
        """saves solution to dict"""
        res = {}
        max_route_distance = 0
        total_route_distance = 0
        _vehicle = {}
        _route_distance = {}
        for vehicle_id in range(data['num_vehicles']):
            _vehicle[ vehicle_id ] = []
            index = routing.Start(vehicle_id)
            route_distance = 0
            while not routing.IsEnd(index):
                _vehicle[ vehicle_id ].append( manager.IndexToNode(index) )
                previous_index = index
                index = solution.Value(routing.NextVar(index))
                route_distance += routing.GetArcCostForVehicle( previous_index, index, vehicle_id )

            _vehicle[ vehicle_id ].append( manager.IndexToNode(index) )
            _route_distance[vehicle_id] = route_distance
            max_route_distance = max(route_distance, max_route_distance)

        res['ObjectiveValue'] = solution.ObjectiveValue()
        res['VehicleRoute'] = _vehicle
        res['RouteDistance'] = _route_distance
        res['MaxDistance'] = max_route_distance
        return res 

    def vrpNoConstraints( self , TIME_LIMIT):
        data = self.parser.create_data_model()
        def distance_callback(from_index, to_index):
            """Returns the distance between the two nodes."""
            # Convert from routing variable Index to distance matrix NodeIndex.
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data['distance_matrix'][from_node][to_node]

        def demand_callback(from_index):
            """Returns the demand of the node."""
            # Convert from routing variable Index to demands NodeIndex.
            from_node = manager.IndexToNode(from_index)
            return data['demands'][from_node]

        manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']), data['num_vehicles'], data['depot'])
        routing = pywrapcp.RoutingModel(manager)
        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        # Define cost of each arc.
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        dimension_name = 'Distance'
        routing.AddDimension(
            transit_callback_index,
            0,  # no slack
            3000,  # vehicle maximum travel distance
            True,  # start cumul to zero
            dimension_name)
        distance_dimension = routing.GetDimensionOrDie(dimension_name)
        distance_dimension.SetGlobalSpanCostCoefficient(100)

        # Setting first solution heuristic.
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = ( routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC )

        search_parameters.local_search_metaheuristic = ( routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH )

        search_parameters.time_limit.FromSeconds( TIME_LIMIT )

        solution = routing.SolveWithParameters(search_parameters)

        if solution:
            # Writer().print_solution_VRP(data, manager, routing, solution)
            res = self.parseSolution(data, manager, routing, solution)
            return res 
        return {}

class CVRP :
    
    def __init__ ( self , _num_vehicles , _depot , _locations , _vehicle_cap , _demands ):
        self.parser = Data( _num_vehicles , _depot , _locations , _vehicle_cap , _demands )
        
    def parseSolution(self ,data, manager, routing, solution):
        """saves solution to dict"""
        res = {}
        max_route_distance = 0
        total_route_distance = 0
        _vehicle = {}
        _route_distance = {}
        for vehicle_id in range(data['num_vehicles']):
            _vehicle[ vehicle_id ] = []
            index = routing.Start(vehicle_id)
            route_distance = 0
            while not routing.IsEnd(index):
                _vehicle[ vehicle_id ].append( manager.IndexToNode(index) )
                previous_index = index
                index = solution.Value(routing.NextVar(index))
                route_distance += routing.GetArcCostForVehicle( previous_index, index, vehicle_id )

            _vehicle[ vehicle_id ].append( manager.IndexToNode(index) )
            _route_distance[vehicle_id] = route_distance
            max_route_distance = max(route_distance, max_route_distance)

        res['ObjectiveValue'] = solution.ObjectiveValue()
        res['VehicleRoute'] = _vehicle
        res['RouteDistance'] = _route_distance
        res['MaxDistance'] = max_route_distance
        return res 

    def cvrpConstrained( self , TIME_LIMIT):
        data = self.parser.create_data_model()
        def distance_callback(from_index, to_index):
            """Returns the distance between the two nodes."""
            # Convert from routing variable Index to distance matrix NodeIndex.
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data['distance_matrix'][from_node][to_node]

        def demand_callback(from_index):
            """Returns the demand of the node."""
            # Convert from routing variable Index to demands NodeIndex.
            from_node = manager.IndexToNode(from_index)
            return data['demands'][from_node]

        manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']), data['num_vehicles'], data['depot'])
        routing = pywrapcp.RoutingModel(manager)
        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        # Define cost of each arc.
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        demand_callback_index = routing.RegisterUnaryTransitCallback(
        demand_callback)
        routing.AddDimensionWithVehicleCapacity(
            demand_callback_index,
            0,  # null capacity slack
            data['vehicle_capacities'],  # vehicle maximum capacities
            True,  # start cumul to zero
            'Capacity')


        # Setting first solution heuristic.
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
        search_parameters.local_search_metaheuristic = (
            routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)

        search_parameters.time_limit.FromSeconds( TIME_LIMIT )

        solution = routing.SolveWithParameters(search_parameters)

        if solution:
            # Writer().print_solution_VRP(data, manager, routing, solution)
            res = self.parseSolution(data, manager, routing, solution)
            return res 
        return {}

def main():
    """Test data https://developers.google.com/optimization/routing/vrp"""
    _locations = [(228, 0),(912, 0),(0, 80),(114, 80),(570, 160),(798, 160),(342, 240),(684, 240),(570, 400),
        (912, 400),(114, 480),(228, 480),(342, 560),(684, 560),(0, 640),(798, 640)]
    _depot = [(456, 320)] # location 0 - the depot
    _demands = [0, 1, 1, 2, 4, 2, 4, 8, 8, 1, 2, 1, 2, 4, 4, 8, 8]
    _vehicle_cap = [15, 15, 15, 15]
    _num_vehicles = 4
    solver = CVRP( _num_vehicles , _depot , _locations , _vehicle_cap , _demands )
    print( solver.vrpNoConstraints( 2 ) )

if __name__ == '__main__':
    main()