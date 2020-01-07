from flask import Flask, jsonify
from datetime import datetime
import pandas as pd

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


@api.route('/start', methods=['GET'])
def start():
    'Returns list of predicted dates'

    predictions = pd.read_csv('predictions.csv')

    response = jsonify(predictions['Date'].values.tolist())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@api.route('/predict/<int:month>/<int:year>', methods=['GET'])
def predict(month, year):
    'Returns prediction for month year'

    target = datetime(year, month, 1)
    target_str = target.strftime("%-m/%-d/%Y")

    predictions = pd.read_csv('predictions.csv', infer_datetime_format = True,
        parse_dates = ['Date'])

    dates = predictions['Date']

    start, end = dates.iloc[0], dates.iloc[-1]

    if target < start or target > end:
        raise InvalidUsage('This date is outside our dataset', status_code = 410)

    data = predictions[predictions['Date'] == target_str].to_dict(orient = 'records')[0]

    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == '__main__':

    api.run(host='0.0.0.0',port=8080)
