from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
import csv

app = Flask(__name__)
api = Api(app)


def check():
    data = pd.read_csv('monitors.csv')


    data['rate'] = data['rate'].astype(str)


    data.to_csv('monitors.csv', index=False)



check()


print()


class monitors(Resource):
    def get(self):
        parser = reqparse.RequestParser()  # initialize parser
        parser.add_argument('guid', required=False, type=int)  # add args
        parser.add_argument('brand', required=False)
        parser.add_argument('name', required=False)
        parser.add_argument('resolution', required=False)
        parser.add_argument('dimensions', required=False)
        parser.add_argument('rate', required=False, type=str)

#      guid,brand,name,resolution,dimensions,rate
        args = parser.parse_args()  # parse arguments to dictionary 
        
        # read our CSV
        data = pd.read_csv('monitors.csv')

        # filter the data based on the query parameters
        for key, value in args.items():
            if value is not None:
                data = data[data[key] == value]

        return {'data': data.to_dict()}, 200  # return data dict and 200 OK
    


    def post(self):
        parser = reqparse.RequestParser()  # initialize parser
        parser.add_argument('guid', required=True, type=int)  # add args
        parser.add_argument('brand', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('resolution', required=True)
        parser.add_argument('dimensions', required=True)
        parser.add_argument('rate', required=False, type=str)

#      guid,brand,name,resolution,dimensions,rate
        args = parser.parse_args()  # parse arguments to dictionary
        
        # read our CSV
        data = pd.read_csv('monitors.csv')
    

        max_guid = data['guid'].max()

        args['guid'] = int(max_guid)+1

        if args['name'] not in list(data['name']):
            new_data = pd.DataFrame({
                'guid': [args['guid']],
                'brand': [args['brand']],
                'name': [args['name']],
                'resolution': [args['resolution']],
                'dimensions': [args['dimensions']],
                'rate': [args['rate']]
            })

            
        else:
            # otherwise we return 404 not found
            return {
                'message': f"'{args['name']}' already exists"
            }, 0

        data = data.append(new_data, ignore_index=True)
        data.to_csv('monitors.csv', index=False)

        return {'data': data.to_dict()}, 200


    def patch(self):
        parser = reqparse.RequestParser()  # initialize parser
        parser.add_argument('guid', required=True, type=int)  # add args
        parser.add_argument('brand', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('resolution', required=True)
        parser.add_argument('dimensions', required=True)
        parser.add_argument('rate', required=False, type=str)

        args = parser.parse_args()  # parse arguments to dictionary
        
        # read our CSV
        data = pd.read_csv('monitors.csv')
        
        # check that the location exists
        if args['guid'] in list(data['guid']):
            # if it exists, we can update it, first we get user row
            user_data = data[data['guid'] == args['guid']]
            
            # if name has been provided, we update name
            if 'brand' in args:
                user_data['brand'] = args['brand']

            if 'name' in args:
                user_data['name'] = args['name']

            if 'resolution' in args:
                user_data['resolution'] = args['resolution']

            if 'dimensions' in args:
                user_data['dimensions'] = args['dimensions']

            if 'rate' in args:
                user_data['rate'] = args['rate']


            # update data
            data[data['guid'] == args['guid']] = user_data
            # now save updated data
            data.to_csv('monitors.csv', index=False)
            # return data and 200 OK
            return {'data': data.to_dict()}, 200

            # otherwise we return 404 not found

        
        else:
            # otherwise we return 404 not found
            return {
                'message': f"'{args['guid']}' location does not exist."
            }, 404
    
    def delete(self):
        parser = reqparse.RequestParser()  # initialize parser
        parser.add_argument('guid', required=True, type=int)  # add locationId arg
        args = parser.parse_args()  # parse arguments to dictionary

        # read our CSV
        data = pd.read_csv('monitors.csv')
        
        # check that the locationId exists
        # if args['name'] in list(data['name']):
        #     # if it exists, we delete it
        #     data = data[data['name'] != args['name']]
        #     # save the data
        #     data.to_csv('monitors.csv', index=False)
        #     # return data and 200 OK
        #     return {'data': data.to_dict()}, 200
        
        # else:
        #     # otherwise we return 404 not found
        #     return {
        #         'message': f"'{args['guid']}' location does not exist."
        #     }


api.add_resource(monitors, '/monitors') # adds endpoint

if __name__ == '__main__':
    app.run()  # run our Flask app

#http://127.0.0.1:5000/monitors?guid=int&brand=str&name=str&resolution=str&dimensions=str&rate=str