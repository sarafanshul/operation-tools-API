import requests
from flask import jsonify


import json

BASE = "http://127.0.0.1:5000/"
LONG_TO_FLOAT_CONST = 1000000
import random

def main():
	random.seed(177013)
	latlng = []
	with open( "in.json" , "r" ) as F :
		data = json.load(F)
		for v in data :
			latlng.append( ( int((float(v['lat']) *LONG_TO_FLOAT_CONST)) , int((float(v['lng']) * LONG_TO_FLOAT_CONST)) ) )
			# latlng.append( (float(v['lat']) , float(v['lng'])) )

	_locations = latlng[1:20:]
	_depot = latlng[0:1]
	_demands = [ random.randint(1 , 10) for _ in range( len(_locations) ) ]

	_num_vehicles = 10
	_vehicle_cap = [ random.randint(10 , 20) for _ in range( _num_vehicles ) ]

	res = {"vCount" : _num_vehicles , "depot" : _depot , 
		"locations" : _locations , "vCap" : _vehicle_cap ,
		"demands" : _demands , "TIME_LIMIT" : 7}

	response = requests.post( BASE + "cvrp" , json = res )
	print( response.json() ) 

if __name__ == '__main__':
	main()
