from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd


app = Flask(__name__)
api = Api(app)

def parse_and_get_data(guid=None, brand=None, name=None, resolution=None, dimensions=None, rate=None):
    parser = reqparse.RequestParser()
    parser.add_argument('guid', required=False, type=int) 
    parser.add_argument('brand', required=False)
    parser.add_argument('name', required=False)
    parser.add_argument('resolution', required=False)
    parser.add_argument('dimensions', required=False)
    parser.add_argument('rate', required=False, type=str)

    args = parser.parse_args()
    data = pd.read_csv('monitors.csv')

    return args, data

def check():
    data = pd.read_csv('monitors.csv')
    data['rate'] = data['rate'].astype(str)
    data.to_csv('monitors.csv', index=False)

class monitors(Resource):
    def get(self):
        args, data = parse_and_get_data()

        for key, value in args.items():
            if value is not None:
                data = data[data[key] == value]

        return {'data': data.to_dict()}, 200 
    

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('guid', required=True, type=int)
        parser.add_argument('brand', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('resolution', required=True)
        parser.add_argument('dimensions', required=True)
        parser.add_argument('rate', required=False, type=str)

        args = parser.parse_args()
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
            return {
                'message': f"'{args['name']}' already exists"
            }, 0

        data = data.append(new_data, ignore_index=True)
        data.to_csv('monitors.csv', index=False)

        return {'data': data.to_dict()}, 200


    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument('guid', required=True, type=int)
        parser.add_argument('brand', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('resolution', required=True)
        parser.add_argument('dimensions', required=True)
        parser.add_argument('rate', required=False, type=str)

        args = parser.parse_args()
        data = pd.read_csv('monitors.csv')
    
        
        if args['guid'] in list(data['guid']):
            user_data = data[data['guid'] == args['guid']]
            
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


            data[data['guid'] == args['guid']] = user_data

            data.to_csv('monitors.csv', index = False)

            return {'data': data.to_dict()}, 200


        
        else:
            return {
                'message': f"'{args['guid']}' location does not exist."
            }, 404
    

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('guid', required=True, type=int)
        args = parser.parse_args()
        data = pd.read_csv('monitors.csv')


api.add_resource(monitors, '/monitors')

check()
app.run()  
