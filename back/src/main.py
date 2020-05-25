from flask import Flask, jsonify
from datetime import datetime
import pandas as pd
import pickle

# REST API definition
app = Flask(__name__)
# Predictions dataset
predictions = pd.read_csv('predictions.csv', infer_datetime_format = True,
    parse_dates = ['Date'], encoding = 'utf8')
# Predictions dataset with dates that are not parsed
predictions_unparsed = pd.read_csv('predictions.csv', encoding = 'utf8')
# Original dataset
data = pd.read_csv('data.csv', infer_datetime_format = True, parse_dates = ['Date'], encoding = 'utf8')
# {county : coordinate} dictionary
mapping = pickle.load( open( 'coordinates.dict', 'rb' ) )

class InvalidUsage(Exception):
    '''
    API error message handler class
    '''
    status_code = 400
    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.errorhandler(InvalidUsage)
def invalid_usage(error):
    '''
    Send error message
    '''
    # Define the response
    response = jsonify(error.to_dict())
    # Add status code
    response.status_code = error.status_code
    return response


@app.route('/dates', methods=['GET'])
def dates():
    '''
    Return list of predicted dates
    '''
    # Define response with all of the dates in dataset
    response = jsonify(predictions_unparsed['Date'].values.tolist())
    # Cross origin
#     response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/predict/<int:month>/<int:year>', methods=['GET'])
def predict(month, year):
    'Returns prediction for month year'
    # Convert requested month and year to datetime object
    target = datetime(year, month, 1)
    # Convert datetime to string
    target_str = target.strftime("%-m/%-d/%Y")
    # Keep only the dates
    dates = predictions['Date']
    # Find where predictions start
    prediction_dates = data['Date']
    prediction_start = prediction_dates.iloc[-1]
    # Find start and end dates
    start, end = dates.iloc[0], dates.iloc[-1]
    # If requested date is outside of the dataset, send error
    if target < start or target > end: raise InvalidUsage('This date is outside our dataset', status_code = 400)
    # Lookup date with datetime string and convert it into a dictionary
    prediction = predictions[predictions['Date'] == target_str].drop(['Date'], axis=1).to_dict(orient = 'records')[0]
    response = {
        'prediction' :  True if target >= prediction_start else False,
        'data' : to_geojson(prediction),
        'predictionStart' : prediction_start
    }
    # Define the response
    response = jsonify(response)
    # Cross origin
#     response.headers.add('Access-Control-Allow-Origin', '*')
    return response


def to_geojson(dataset):
    'Turns {city : arrests} dictionary into geoJSON for mapbox'
    # Define base of the GeoJSON dictionary
    geojson = {
        'type' : 'FeatureCollection',
        'features' : []
    }
    # For each county arrest pair in dictionary, create a GeoJson location
    for county, arrests in dataset.items():
        element = {
            'type' : 'Feature',
            'properties' : {
                'county' : county,
                'arrests' : arrests
            },
            'geometry' : {
                'type' : 'Point',
                'coordinates' : mapping.get(county)
            }
        }
        # Add element to GeoJSON object
        geojson['features'].append(element)
    return geojson

@app.route('/counties', methods=['GET'])
def counties():
    'Returns list of counties'
    # Load dataset and drop dates
    counties = data.drop(['Date'], axis=1)
    # Define the response
    response = jsonify({'counties' : counties.columns.values.tolist()})
    # Cross origin
#     response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/countydata/<string:county>', methods=['GET'])
def countydata(county):
    'Returns data associated with speficied county'
    # Initialize response dictionary
    response = {
        'county' : county,
        'data' : []
    }
    # Add each prediction as a dictionary
    for prediction in predictions_unparsed[[county, 'Date']].values.tolist():
        response['data'].append({
            'date' : prediction[1],
            'arrests' : prediction[0]
        })
    # Define response
    response = jsonify(response)
    # Cross origin
#     response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    'Usage'
    app.run(host='0.0.0.0',port=8080)
