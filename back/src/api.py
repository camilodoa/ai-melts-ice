from flask import Flask, jsonify
from datetime import datetime
import pandas as pd
import pickle
import json


# REST API
api = Flask(__name__)


class InvalidUsage(Exception):
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

@api.errorhandler(InvalidUsage)
def invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@api.route('/dates', methods=['GET'])
def dates():
    'Returns list of predicted dates'

    predictions = pd.read_csv('predictions.csv', encoding = 'utf8')

    response = jsonify(predictions['Date'].values.tolist())
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


@api.route('/predict/<int:month>/<int:year>', methods=['GET'])
def predict(month, year):
    'Returns prediction for month year'

    target = datetime(year, month, 1)
    target_str = target.strftime("%-m/%-d/%Y")

    predictions = pd.read_csv('predictions.csv', infer_datetime_format = True,
        parse_dates = ['Date'], encoding = 'utf8')

    dates = predictions['Date']

    start, end = dates.iloc[0], dates.iloc[-1]

    if target < start or target > end:
        raise InvalidUsage('This date is outside our dataset', status_code = 410)

    data = predictions[predictions['Date'] == target_str].drop(['Date'], axis=1).to_dict(orient = 'records')[0]

    data = toGJSON(data)

    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


def toGJSON(data):
    'Turns {city : arrests} dictionary into geoJSON for mapbox'

    geoJSON = {
        'type' : 'FeatureCollection',
        'features' : []
    }

    mapping = pickle.load( open( 'county_to_coord.p', 'rb' ) )

    for county, arrests in data.items():
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

        geoJSON['features'].append(element)

    return geoJSON

@api.route('/counties', methods=['GET'])
def counties():
    'Returns list of counties'

    data = pd.read_csv('data.csv', encoding = 'utf8').drop(['Date'], axis=1)

    response = jsonify({'counties' : data.columns.values.tolist()})
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

@api.route('/countydata/<string:county>', methods=['GET'])
def countydata(county):
    'Returns data associated with speficied county'

    predictions = pd.read_csv('predictions.csv', encoding = 'utf8')

    response = {
        'county' : county,
        'data' : []
    }

    for prediction in predictions[[county, 'Date']].values.tolist():
        response['data'].append({
            'date' : prediction[1],
            'arrests' : prediction[0]
        })

    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')

    print(response)
    return response


if __name__ == '__main__':
    api.run(host='0.0.0.0',port=8080)
