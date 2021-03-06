from flask import Flask , jsonify ,make_response , request
from flask_restful import Api , Resource , reqparse
from CVRP import VRP , CVRP
from BinPacking import BinPacking

class Models():
	vrpModel = {'vCount' : 'Int' , 'depot' : '[[]]' , 'locations' : '[[]]' ,'vCap' : '[]'}
	cvrpModel = {'vCount' : 'Int' , 'depot' : '[[]]' , 'locations' : '[[]]' ,'vCap' : '[]' , 'damands' : '[]' }
	binPackingModel = {'weights':'[]' , 'values' : '[]' , 'bin_capacities' : '[]'}

	def getEx(self):
		return {'vrpModel' : self.vrpModel , 
		'cvrpModel' : self.cvrpModel , 
		'binpackingModel' : self.binPackingModel }

app = Flask( __name__ )

@app.route("/" , methods = [ 'GET' , 'POST' , 'PUT'])
def home():
	return jsonify( Models().getEx() ) , 200


@app.route("/vrp" , methods = ['POST' , 'PUT'])
def vrp():
	try : values = request.json
	except : return jsonify( {} ) , 406

	try :
		solver = VRP( values['vCount'] , values['depot'] , 
			values['locations'] , values['vCap'] , [] )
		res = solver.vrpNoConstraints( 1 )

		response = make_response( jsonify( res ) , 302 )
		response.headers['Warning'] = "Deprecated API"
		return response
	except :
		return make_response( jsonify( { } ) , 412 )


@app.route("/cvrp" , methods = ['POST' , 'PUT'])
def cvrp():
	try : values = request.json
	except : return jsonify( {} ) , 406
	try :
		solver = CVRP( values['vCount'] , values['depot'] , 
			values['locations'] , values['vCap'] , values['demands'] )

		TIME_LIMIT = min( values.get("TIME_LIMIT" , 5) , 7 ) # max 7 sec per ops 
		res = solver.cvrpConstrained( TIME_LIMIT )
		response = make_response( jsonify( res ) , 200 )
		return response
	except : 
		return make_response( jsonify( { } ) , 412 )

@app.route("/binpacking" , methods = ['POST' , 'PUT'] )
def binP():
	try : values = request.json
	except : return jsonify( {} ) , 406
	try :
		solver = BinPacking( values['weights'] , values['values'] , 
			values['bin_capacities'] )
		res = solver.multipleKnapsack( 1 )
		return jsonify( res ) , 200
	except Exception : 
		print( Exception )
		return jsonify( {} ) , 412

def main():
	app.run( threaded=True )

if __name__ == '__main__':
	main()