import flask
from flask import Flask
from ai import Predictor
from keras.models import load_model

from keras import backend as K
K.clear_session()

# Our AI model
p = Predictor()

# REST API
api = Flask(__name__)

@api.route('/predict/<int:year>/<int:month>', methods=['GET'])
def predict(year, month):

    print('in predict')

    data = p.predict(year, month)

    for key, value in data.items():
        if value < 0: data[key] = 0

    print(data)

    return flask.jsonify(data)

if __name__ == '__main__':
    api.run(host='0.0.0.0',port=8080, debug=False)
