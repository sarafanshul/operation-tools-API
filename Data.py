import numpy as np

def get_distance(p1 , p2 ): # manhattan distance , modify as per use
        return abs( p1[0] - p2[0] ) + abs( p1[1] - p2[1] ) 

class DataCVRP :
    points = []
    depot = []
    num_vehicles = 0 
    vehicle_cap = []
    demands = []

    def __init__(self , _num_vehicles , _depot , locations , _vehicle_cap , _demands ):
        self.points = locations # [ [x , y] , [x , y] .. ]
        self.depot = _depot # [ [ x , y ] ]
        self.demands = _demands 
        self.vehicle_cap = _vehicle_cap
        self.num_vehicles = _num_vehicles

    def merge(self , a , b ):
        return a + b 

    def generate_distance_matrix(self , locations , F ):
        n = len(locations)
        res = np.zeros( shape = (n , n) )
        for i in range( n ):
            for j in range( n ):
                if( i != j ): res[i][j] = F( locations[i] , locations[j] )
        return res 

    def create_data_model(self , F = get_distance ):
        locations = self.merge( self.depot , self.points )
        distance_matrix = self.generate_distance_matrix( locations , F )
        
        data = {}
        data['distance_matrix'] = distance_matrix
        data['demands'] = self.merge( [0] , self.demands)
        data['vehicle_capacities'] = self.vehicle_cap
        data['num_vehicles'] = self.num_vehicles
        data['depot'] = 0 # at idx 0 in locations
        return data


class DataBinPacking :
    weights = []
    values = []
    bin_capacities = []

    def __init__( self , _weights , _values , _bin_capacities ):
        self.weights = _weights
        self.values = _values
        self.bin_capacities = _bin_capacities

    def create_data_model(self):
        data = {}
        data['num_items'] = len( self.weights )
        data['all_items'] = range( data['num_items'] )
        data['weights'] = self.weights
        data['values'] = self.values
        data['bin_capacities'] = self.bin_capacities
        data['num_bins'] = len( data['bin_capacities'] )
        data['all_bins'] = range( data['num_bins'] )
        return data